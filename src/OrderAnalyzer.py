import pandas as pd
from pathlib import Path
import logging
from itertools import chain
import logging_config

logger = logging.getLogger(__name__)

class OrderAnalyzer:
    """
    Класс предназначен для пакетной обработки файлов, содержащих данные о продажах
    """
    def __init__(self, folder_path, revenue_column, status_column, status_filter_value, output_file_path, dataset_structure):
        self.folder_path = Path(folder_path)
        self.revenue_column = revenue_column
        self.status_column = status_column
        self.status_filter_value = status_filter_value
        self.output_file_path = Path(output_file_path)
        self.dataset_structure = dataset_structure
        self.success_files_number = 0
        self.error_files_number = 0

    def read_file(self, file_path):
        """Чтение данных из файла"""
        file_dataset = pd.read_csv(file_path, encoding='utf-8', sep=',')

        for column in self.dataset_structure:
            if column['name'] not in file_dataset.columns:
                raise KeyError (f'Отсутствует колонка "{column['name']}"')
            elif column['type'] != file_dataset.dtypes[column['name']]:
                raise TypeError (f'Неверный тип у колонки "{column['name']}"')
            elif "format" in column:
                file_dataset[column['name']+'_converted'] = pd.to_datetime(file_dataset[column['name']], format = column['format'], errors='coerce')
                if file_dataset[file_dataset[column['name']+'_converted'].isna()].shape[0] != 0:
                    raise TypeError(f'Неверный формат у колонки "{column['name']}"')

        return file_dataset

    def process_file(self, file_path):
        """Расчет метрик для файла"""
        file_dataset = self.read_file(file_path)
        filtered_file_dataset = self.filter_dataset_by_status(file_dataset)
        total_revenue = self.calculate_total_revenue(filtered_file_dataset)
        average_bill = self.calculate_average_bill(filtered_file_dataset)
        orders_number = self.calculate_orders_number(filtered_file_dataset)

        return {'file_name': file_path.name, 'total_revenue': total_revenue,
                'average_bill': average_bill, 'orders_number': orders_number}


    def process_files_from_folder(self):
        """Обработка в цикле файлов с данными о продажах, содержащихся в указанной директории"""
        files_metrics_list = []

        for file_path in self.folder_path.glob('*.csv'):
            try:
                file_metrics = self.process_file(file_path)
                files_metrics_list.append(file_metrics)
                self.success_files_number += 1
            except pd.errors.EmptyDataError as e:
                logger.error(f'Файл {file_path.name} не содержит данные')
                self.error_files_number += 1
                continue
            except UnicodeDecodeError:
                print(f"Файл {file_path.name} поврежден или имеет кодировку, отличную от utf-8")
            except TypeError as e:
                logger.error(f'Файл {file_path.name} имеет некорректную структуру: {e}')
                self.error_files_number += 1
                continue
            except KeyError as e:
                logger.error(f'Файл {file_path.name} имеет некорректную структуру или не содержит колонок для расчета метрик: {e}')
                self.error_files_number += 1
                continue
            except Exception as e:
                logger.error(f'Произошла неизвестная ошибка при обработке файла {file_path.name}: {e}')
                self.error_files_number += 1
                continue

        if len(files_metrics_list) == 0:
            logger.error("Отсутствуют файлы для расчета метрик")
        else:
            report_dataset = pd.DataFrame(chain(files_metrics_list))
            self.save_report(report_dataset)

    def filter_dataset_by_status(self, file_dataset):
        """Фильтрация датасета по статусу"""
        if self.status_column not in file_dataset.columns:
            raise KeyError(f'Отсутствует колонка "{self.status_column}"')
        return file_dataset[file_dataset[self.status_column] == self.status_filter_value]

    def calculate_total_revenue(self, filtered_dataset):
        """Расчет общей выручки"""
        if self.revenue_column not in filtered_dataset.columns:
            raise KeyError(f'Отсутствует колонка "{self.revenue_column}"')
        return filtered_dataset[self.revenue_column].sum()

    def calculate_average_bill(self, filtered_dataset):
        """Расчет стоимости среднего чека"""
        if self.revenue_column not in filtered_dataset.columns:
            raise KeyError(f'В датасете отсутствует колонка "{self.revenue_column}"')
        return filtered_dataset[self.revenue_column].mean()

    def calculate_orders_number(self, filtered_dataset):
        """Расчет общего количества заказов"""
        return filtered_dataset.shape[0]

    def save_report(self, report_dataset):
        """Сохранение файла с отчетом по метрикам"""
        if not self.output_file_path.parent.exists():
            self.output_file_path.parent.mkdir(parents=True)
        report_dataset.to_csv(self.output_file_path, index=False)


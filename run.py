from src.OrderAnalyzer import OrderAnalyzer
import config
import pandas as pd

def main():
    print('Запущена пакетная обработка файлов...')
    order_analyzer = OrderAnalyzer(config.INPUT_FILES_FOLDER_PATH,
                                   config.REVENUE_COLUMN_NAME,
                                   config.STATUS_COLUMN_NAME,
                                   config.STATUS_FILTER_VALUE,
                                   config.OUPUT_FILES_FOLDER_PATH + config.OUTPUT_FILE_NAME,
                                   config.DATASET_STRUCTURE)
    order_analyzer.process_files_from_folder()
    print('Пакетная обработка файлов завершена')
    print(f'Успешно обработано файлов: {order_analyzer.success_files_number}')
    print(f'Файлов с ошибками: {order_analyzer.error_files_number}')

if __name__ == '__main__':
    main()
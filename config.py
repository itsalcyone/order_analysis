# путь до папки с файлами, которые содержат данные о продажах
INPUT_FILES_FOLDER_PATH = 'data/'
# путь до папки с отчетами
OUPUT_FILES_FOLDER_PATH = 'reports/'
# наименование файла с отчетом
OUTPUT_FILE_NAME = 'summary_report.csv'
# наименование колонки со статусом
STATUS_COLUMN_NAME = 'status'
# значение статуса, на основании которого производится фильтрация
STATUS_FILTER_VALUE = 'Delivered'
# наименование колонки с выручкой
REVENUE_COLUMN_NAME = 'total_amount'
# структура данных, содержащихся в исходных файлах
DATASET_STRUCTURE = [{'name':'order_id', 'type':'int64'},
                     {'name':'person_id', 'type':'int64'},
                     {'name':'order_date', 'type':'string', 'format':'%Y-%m-%d'},
                     {'name':'status', 'type':'string'},
                     {'name':'total_amount', 'type':'float64'},
                     {'name':'currency', 'type':'string'},
                     {'name':'payment_method', 'type':'string'},
                     {'name':'shipping_method', 'type':'string'},
                     {'name':'notes', 'type':'string'}]

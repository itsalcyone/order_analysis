import logging

logging.basicConfig(
    level=logging.INFO,
    filename='logs/error.log',
    encoding='utf-8',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

logging.info('Useful message')
logging.info('variable %s', 'abc')
logging.info('variable %d', 123)



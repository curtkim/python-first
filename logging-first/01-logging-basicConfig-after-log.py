import logging

logging.info('Useful message')

# basicConfig전에 info를 호출한 경우에
# 하나도 로깅인 남지 않는다.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../debug.log"),
        logging.StreamHandler()
    ]
)

logging.info('variable %s', 'abc')
logging.info('variable %d', 123)


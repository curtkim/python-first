# mymath에서 독자적인 logger를 설정한다.
# basicConfig와 중복으로 적용된다.
# 그러나 propagate=False를 줄 수도 있다.
import logging
from mymath import my_add


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(module)s %(funcName)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    print(my_add(1, 2))

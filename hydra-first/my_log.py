import hydra
import logging

# A logger for this file
log = logging.getLogger(__name__)


@hydra.main()
def my_log(_cfg):
    log.info("Info level message")
    log.debug("Debug level message")


if __name__ == "__main__":
    my_log()

'''
$ python my_log.py hydra.verbose=__main__
[2020-02-11 16:09:52,431][__main__][INFO] - Info level message
[2020-02-11 16:09:52,431][__main__][DEBUG] - Debug level message
'''
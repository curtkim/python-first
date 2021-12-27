import logging
import logging.handlers
import multiprocessing
from threading import Thread
from random import choice, random
import time
import platform

'''
Class Log performs logger configuration, creation, multiprocess listener.
'''


class Log():
    def __init__(self):
        self.th = None

    def get_logger(self, name):
        return logging.getLogger(name)

    def listener_start(self, file_path, name, queue):
        self.th = Thread(target=self._proc_log_queue, args=(file_path, name, queue))
        self.th.start()

    def listener_end(self, queue):
        queue.put(None)
        self.th.join()
        print('log listener end...')

    def _proc_log_queue(self, file_path, name, queue):
        self.config_log(file_path, name)
        logger = self.get_logger(name)
        while True:
            try:
                record = queue.get()
                if record is None:
                    break
                logger.handle(record)
            except Exception:
                import sys, traceback
                print('listener problem', file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    def config_queue_log(self, queue, name):
        '''
        if you use multiprocess logging,
        call this in multiprocess as logging producer.
        logging consumer function is [self.listener_start] and [self.listener_end]
        it returns logger and you can use this logger to log
        '''
        qh = logging.handlers.QueueHandler(queue)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(qh)
        return logger

    def config_log(self, file_path, name):
        '''
        it returns FileHandler and StreamHandler logger
        if you do not need to use multiprocess logging,
        just call this function and use returned logger.
        '''
        # err file handler
        fh_err = logging.handlers.RotatingFileHandler(file_path + '_error.log', 'a', 300, 10)
        fh_err.setLevel(logging.WARNING)
        # file handler
        fh_dbg = logging.handlers.RotatingFileHandler(file_path + '_debug.log', 'a', 300, 10)
        fh_dbg.setLevel(logging.DEBUG)
        # console handler
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        # logging format setting
        ff = logging.Formatter('''[%(asctime)s] %(levelname)s : %(message)s''')
        sf = logging.Formatter('''[%(levelname)s] %(message)s''')
        fh_err.setFormatter(ff)
        fh_dbg.setFormatter(ff)
        sh.setFormatter(sf)
        if platform.system() == 'Windows':
            import msvcrt
            import win32api
            import win32con
            win32api.SetHandleInformation(msvcrt.get_osfhandle(fh_dbg.stream.fileno()),
                                          win32con.HANDLE_FLAG_INHERIT, 0)
            win32api.SetHandleInformation(msvcrt.get_osfhandle(fh_err.stream.fileno()),
                                          win32con.HANDLE_FLAG_INHERIT, 0)
        # create logger, assign handler
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fh_err)
        logger.addHandler(fh_dbg)
        logger.addHandler(sh)
        return logger


'''
The code below tests the multiprocess logging.
Main process and child process produce log messasge. (put message into queue.) 
(random choice in variable LEVEL, MESSAGES)
Listener process produced by main process consume log message. (write log message in stdout and file)
'''
LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
          logging.ERROR, logging.CRITICAL]
MESSAGES = ['Random message #1',
            'Random message #2',
            'Random message #3',
            ]


def worker(queue):
    # multi process log producer start
    logger = Log().config_queue_log(queue, 'mp')
    name = multiprocessing.current_process().name
    print('Worker started: %s' % name)
    for i in range(10):
        time.sleep(random())
        level = choice(LEVELS)
        message = choice(MESSAGES)
        logger.log(level, f"{name} - {message}")
    print('Worker finished: %s' % name)
    # multi process log producer end


def main():
    queue = multiprocessing.Queue(-1)
    listener = Log()
    listener.listener_start('test', 'listener', queue)  # log consumer thread start

    workers = []
    for i in range(10):  # multiprocess loop
        w = multiprocessing.Process(target=worker, args=(queue,))
        workers.append(w)
        w.start()
    # main process log producer start
    logger = Log().config_queue_log(queue, 'mp')
    name = multiprocessing.current_process().name
    print('Worker started: %s' % name)
    for i in range(10):
        time.sleep(random())
        level = choice(LEVELS)
        message = choice(MESSAGES)
        logger.log(level, f"{name} - {message}")
    print('Worker finished: %s' % name)
    # main process log producer end
    for w in workers:
        w.join()
    listener.listener_end(queue)  # log consumer thread end


if __name__ == '__main__':
    main()

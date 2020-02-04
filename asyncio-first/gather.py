import asyncio
import logging
import time

logger_format = '%(asctime)s [%(threadName)s] %(message)s'
logging.basicConfig(format=logger_format, level=logging.INFO, datefmt="%H:%M:%S")

num_word_mapping = {1: 'ONE', 2: 'TWO', 3: "THREE", 4: "FOUR", 5: "FIVE"}


async def delay_message(delay, message):
    logging.info(f"{message} received")
    if message != 'THREE':
        await asyncio.sleep(delay)  # non-blocking call. gives up execution
    else:
        time.sleep(delay)  # blocking call
    logging.info(f"Printing {message}")


async def main():
    logging.info("Main started")
    logging.info("Creating multiple tasks with asyncio.gather")
    await asyncio.gather(
        *[delay_message(i + 1, num_word_mapping[i + 1]) for i in range(5)])  # awaits completion of all tasks
    logging.info("Main Ended")


if __name__ == '__main__':
    asyncio.run(main())  # creats an envent loop
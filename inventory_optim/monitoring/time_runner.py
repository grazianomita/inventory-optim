from logging import Logger
from timeit import default_timer as timer


class Timer:
    def __init__(self) -> None:
        self.timer_ = None

    def start(self):
        self.timer_ = timer()

    def get_current_time(self):
        return timer() - self.timer_


class TimeRunner:
    @staticmethod
    def measure_elapsed_time(stats: dict, function: callable, args: list, info_stat: str):
        """
        Measure running time of a function and store it in dictionary.

        :param stats: dictionary containing all statistics
        :param function: function to measure running time
        :param args: function arguments
        :param info_stat: key in which the running time is going to be stored
        :return: result of the running function
        """
        start = timer()
        res = function(*args)
        stats[info_stat]= timer() - start
        return res

    @staticmethod
    def run_and_log(stats: dict, function: callable, args: list, info_stat: str, info: str, logger: Logger):
        """
        Log and measure running time of a function and store it in dictionary.

        :param stats: dictionary containing all statistics
        :param function: function to measure running time
        :param args: function arguments
        :param info_stat: key in which the running time is going to be stored
        :param info: info's name output by the logger
        :param logger: logger
        :return: result of the running function
        """
        logger.info(info)
        res = TimeRunner.measure_elapsed_time(stats, function, args, info_stat)
        logger.info(f'elapsed time {stats[info_stat]} in {info}')
        return res


global_timer = Timer()

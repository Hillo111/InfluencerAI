import time
import random
import logging

class Scheduler:
    def __init__(self, task, time_range) -> None:
        self.task = task
        self.time_range = time_range
        self.schedule()

    def schedule(self):
        gt = lambda : (self.time_range[0] + random.random() * (self.time_range[1] - self.time_range[0])) * 3600
        self.run_time = time.time() + gt()
        while not 5 <= time.localtime(self.run_time)[3] <= 23:
            self.run_time += gt()
        logging.info(f'set run time to {time.asctime(time.localtime(self.run_time))}')

    def attempt_run(self):
        if time.time() > self.run_time:
            self.task()
            self.schedule()


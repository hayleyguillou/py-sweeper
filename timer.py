import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.stop_time = time.time()

    def reset(self):
        self.start_time = 0
        self.stop_time = 0

    @property
    def curr_time(self):
        if not self.start_time and not self.stop_time:
            return 0
        elif not self.stop_time:
            return round(time.time() - self.start_time,1)
        else:
            return round(self.stop_time - self.start_time,1)
        
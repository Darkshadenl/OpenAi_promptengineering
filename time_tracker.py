from datetime import datetime


class Timetracker:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_time = None

    def start(self):
        self.start_time = datetime.now()
        print(f"\x1b[31mStarting predictions at {self.start_time}...\x1b[0m")

    def stop(self):
        self.end_time = datetime.now()
        self.total_time = self.end_time - self.start_time
        print(f"\x1b[32mFinished predictions at {self.end_time}!\x1b[0m")

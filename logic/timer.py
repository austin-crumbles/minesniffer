import threading
from time import sleep

class GameTimer(threading.Thread):
    """
    Creates a non-reusable timer that counts upward
    """
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.time = 0
        self.sec = 0
        self.min = 0
        self.hour = 0

        self.running = False

    def run(self) -> None:
        """
        Used by the threadding Thread to count upward
        """
        self.running =  True

        while self.running is True:
            self.time += 1
            self.calc()
            sleep(1)

            self.report_time()

    def stop(self) -> None:
        self.running = False

    def calc(self) -> None:
        """
        Calculate `self.hour`, `self.min`, `self.sec` from `self.time`
        """
        self.min, self.sec = divmod(self.time, 60)
        if self.min >= 60:
            self.hour, self.min = divmod(self.min, 60)

    def gettime(self) -> str:
        """
        Return a formatted string with the current timer value. Omits the hours place
        if the timer has not yet reached an hour
        """
        if self.hour == 0:
            return f"{self.min:02}:{self.sec:02}"
        else:
            return f"{self.hour}:{self.min:02}:{self.sec:02}"

    def report_time(self):
        """
        Report the time string back to the controller.
        """
        timestr = self.gettime()
        self.controller.update_timer(timestr)
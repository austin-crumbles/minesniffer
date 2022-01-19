import threading
from time import sleep

class GameTimer(threading.Thread):
    """
    Creates a non-reusable timer that counts upward
    """
    def __init__(self) -> None:
        super().__init__()
        self.time = 0
        self.sec = 0
        self.min = 0
        self.hour = 0

        self.stop_timer = False

    def run(self) -> None:
        """
        Used by the threadding Thread to count upward
        """
        while self.stop_timer is False:
            self.time += 1
            sleep(1)
            self.calc()

            print(self.gettime(), end="\r")

    def stop(self) -> None:
        self.stop_timer = True

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

if __name__ == "__main__":
    t = GameTimer()
    t.start()
    input()
    t.stop()
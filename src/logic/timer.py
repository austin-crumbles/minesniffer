import threading
from time import sleep

class TimerState():
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    IDLE = "IDLE"
    PAUSED = "PAUSED"

class GameTimer(threading.Thread):
    """
    Creates a non-reusable timer that counts upward.
    """

    def __init__(self, callback_func) -> None:
        """
        Supply a callback_func for the timer to report its time.
        """
        super().__init__()
        self.callback_func = callback_func
        self.time = 0
        self.sec = 0
        self.min = 0
        self.hour = 0

        self.state = TimerState.IDLE

    def run(self) -> None:
        """
        Main thread action triggered by `self.start()` which starts a timer
        that counts upward. The timer reports its time using `self.callback()`.
        """

        # Activate an endless while loop
        self.state = TimerState.RUNNING

        while self.state in [TimerState.RUNNING, TimerState.PAUSED]:
            sleep(1)

            # If paused, the Timer continues to run on the thead, 
            # but does not keep track of the time
            if self.state != TimerState.PAUSED:
                self.time += 1
                self.calc()
                self.callback()

    def stop(self) -> None:
        """
        Stop the timer. `stop()` can only be called if `self.state` is `IDLE`.
        """
        if self.state != TimerState.IDLE:
            self.state = TimerState.STOPPED

    def pause(self):
        """
        Pause the timer. `pause()` can only be called if `self.state` is `RUNNING`.
        """
        if self.state == TimerState.RUNNING:
            self.state = TimerState.PAUSED

    def resume(self):
        """
        Resume the timer. `resume()` can only be called if `self.state` is `PAUSED`.
        """
        if self.state == TimerState.PAUSED:
            self.state = TimerState.RUNNING

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

    def callback(self):
        """
        Pass the time string as an argument to the callback function supplied
        to the constructor. If the timer is stopped, or no callback function
        was supplied, do nothing.
        """
        if self.state == TimerState.STOPPED or self.callback_func is None:
            return

        timestr = self.gettime()
        self.callback_func(timestr)

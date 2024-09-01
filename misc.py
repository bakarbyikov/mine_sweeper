from datetime import timedelta
from time import monotonic


class Timer:
    def __init__(self) -> None:
        self.start_time = self.now()
        self.elapsed = None
    
    def now(self) -> float:
        return monotonic()
    
    def start(self) -> None:
        self.__init__()
    
    def passed(self) -> timedelta:
        return (self.elapsed 
                or timedelta(seconds=self.now()-self.start_time))
    
    def passed_whole(self) -> timedelta:
        return timedelta(seconds=int(self.passed().total_seconds()))
    
    def stop(self) -> None:
        self.elapsed = self.passed()

if __name__ == "__main__":
    from time import sleep
    
    t = Timer()
    t.start()
    sleep(1)
    t.stop()
    print(t.passed())
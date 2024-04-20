import time

# Simple timer to easily report processing time
# inspired by https://preshing.com/20110924/timing-your-code-using-pythons-with-statement/
class Timer: 
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = int(self.end - self.start)
        print('{} seconds'.format(self.interval))

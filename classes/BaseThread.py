import threading

class BaseThread(threading.Thread):
    def __init__(self, target=lambda x: None, args=[]):
        self.target = target
        self.args = args
        self.continuous = False
        self._stopper = threading.Event()
        threading.Thread.__init__(self)

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()

    def run(self):
        while not self.stopped():
            self.target(*self.args)
            if not self.continuous:
                self.stop()

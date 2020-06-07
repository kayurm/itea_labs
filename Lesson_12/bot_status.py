class Status:

    def __init__(self):
        self._status = 0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status_in):
        self._status = status_in



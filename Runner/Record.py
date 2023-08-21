class Record(object):
    _OK = 0
    _TIMEDOUT = -1
    _ERROR = -2
    # -3 .. -7 have other uses in the website PHP scripts
    _BADOUT = -10
    _MISSING = -11
    _EMPTY = -12

    def __init__(self, name):
        self.name = name
        self.elapsed = 0.0
        self.userSysTime = 0.0
        self.maxMem = 0
        self.gz = 0
        self.status = self._EMPTY
        self.cpuLoad = '%'

    def fromString(self, s):
        a = s.split(',')
        self.name = a[0]
        self.gz = int(a[1])
        self.userSysTime = float(a[2])
        self.maxMem = int(a[3])
        self.status = int(a[4])
        self.cpuLoad = a[5]
        self.elapsed = float(a[6])
        return self

    def __str__(self):
        return '%d,%d,%.3f,%d,%d,%s,%.3f' % (
            self.name, self.gz, self.userSysTime, self.maxMem, self.status, self.cpuLoad, self.elapsed)

    def __cmp__(self, other):
        return \
            -1 if self.name < other.name else (
                1 if self.name > other.name else (
                    -1 if self.status > other.status else (
                        1 if self.status < other.status else (
                            -1 if self.userSysTime < other.userSysTime else (
                                1 if self.userSysTime > other.userSysTime else (
                                    0))))))

    def setOkay(self):
        self.status = self._OK

    def setError(self):
        self.status = self._ERROR

    def setTimedout(self):
        self.status = self._TIMEDOUT

    def setBadOutput(self):
        self.status = self._BADOUT

    def setMissing(self):
        self.status = self._MISSING

    def isOkay(self):
        return self.status == self._OK

    def hasError(self):
        return self.status == self._ERROR

    def isEmpty(self):
        return self.status == self._EMPTY

    def hasTimedout(self):
        return self.status == self._TIMEDOUT

    def hasBadOutput(self):
        return self.status == self._BADOUT

    def isMissing(self):
        return self.status == self._MISSING

    def hasExceeded(self, cutoff):
        return self.userSysTime > cutoff

    def statusStr(self):
        return 'OK ' if self.isOkay() else (
            'PROGRAM FAILED ' if self.hasError() else (
                'EMPTY ' if self.isEmpty() else (
                    'TIMED OUT ' if self.hasTimedout() else (
                        'UNEXPECTED OUTPUT ' if self.hasBadOutput() else
                        'MAKE ERROR '))))

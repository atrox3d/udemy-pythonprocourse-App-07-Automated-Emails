from datetime import datetime


class RequestCounter:

    def __init__(
            self,
            counterpath='files/request-counter.txt',
            date=None,
            count=None
    ):
        self.counterpath = counterpath
        self.date = date
        self.count = count

        self._load()

    def _load(self):
        try:
            with open(self.counterpath, 'r') as fp:
                date = fp.readline().rstrip('\n')                               # read date from file
                self.date = datetime.strptime(date, '%Y-%m-%d').date()          # convert to date
                # print(f"_open | self.date | {self.date}")

                request_count = fp.readline().rstrip('\n')                      # read count from file
                self.count = int(request_count)                                 # converto to int

                today = datetime.now().date()                                   # get today's date
                # print(f"_open | today     | {today}")
                if self.date < today:                                           # if file older than today
                    print(
                        f"_open | "
                        f"date on file {self.date} older than "
                        f"today {today}, resetting")
                    self._reset()                                               # reset like account does

        except OSError as ose:
            self._reset()                                                       # no file, reset

    def _reset(self):
        self.date = datetime.now().date()
        self.count = 0

    def update(self, count=None, date=None):
        try:
            with open(self.counterpath, 'w') as fp:
                self.date = date or datetime.now().date()                       # use date param or today's
                fp.write(f'{self.date}\n')                                      # write on file

                self.count = count or self.count + 1                            # use count param or increment
                fp.write(f'{str(self.count)}\n')                                # write on file
        except OSError as ose:
            print(ose)                                                          # fatal
            exit(1)

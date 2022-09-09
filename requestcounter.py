import datetime


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
                date = fp.readline().rstrip()
                request_count = fp.readline().rstrip()
                self.date = datetime.datetime.strptime(date, '%Y-%m-%d')
                self.count = int(request_count)
        except OSError as ose:
            # print(ose)
            self.date = datetime.date.today().isoformat()
            self.count = 0

    def update(self, count, date=None):
        try:
            with open(self.counterpath, 'w') as fp:
                # request_count += 1
                self.date = date or datetime.date.today().isoformat()
                self.count = count
                fp.write(f'{self.date}\n')
                fp.write(f'{str(self.count)}\n')
        except OSError as ose:
            print(ose)
            exit(1)

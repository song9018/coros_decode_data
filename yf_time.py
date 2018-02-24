# coding=utf-8
class yf_time_struct(object):
    year = 0
    month = 0
    day = 0
    hour = 0
    minute = 0
    sec = 0
    dayOfWeek = 0#0:Monday

    def trup2str(self, trup):
        s = ''
        for tmp in trup:
            s += '%02d' % tmp
        return s

    def show(self, view = False, rt_str = True):
        out = (self.year, self.month, self.day, self.hour, self.minute, self.sec, self.dayOfWeek)
        if view:
            print (out)
        if rt_str:
            # print(out)
            return str(int(self.year)+2000)+"-"+str(int(self.month))+"-"+str(int(self.day))+" "+str(int(self.hour))+":"+str(int(self.minute))+":"+str(int(self.sec))
            # return self.trup2str(out)
        else:
            return out

class utc_time(object):
    monthtable = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    monthtable_leap = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    
    def __init__(self):
        self.time = yf_time_struct()
        self.MIN_YDAR = 14
        self.MAX_YEAR = 29
        self.JAN1WEEK = 3#2014.1.1-->wed
        self.year = 2000


    def modify_utc_start_time(self, min_year=14, jan1week=3, start_year=2000):
        self.MIN_YDAR = min_year
        self.JAN1WEEK = jan1week
        self.year = start_year

    def isleap(self, year):
        year += self.year
        return (((year%400)==0) or (((year%4) == 0) and not((year%100)==0)))

    def seconds_to_utc(self, seconds):

        sec = seconds % 60
        minute = seconds / 60
        hour = minute / 60
        day = hour / 24

        self.time.sec = sec
        self.time.minute = minute % 60
        self.time.hour = hour % 24
        self.time.dayOfWeek = (day + self.JAN1WEEK )%7

        year = self.MIN_YDAR
        while(1):
            leap = self.isleap(year)
            if day < (365 + leap):
                break
            day -= 365 + leap
            year += 1

        self.time.year = year%100

        mtbl = self.monthtable_leap if leap > 0 else self.monthtable

        for month in range(12):
            if day < mtbl[month]:
                break
            day -= mtbl[month]

        self.time.day = day + 1
        self.time.month = month + 1

        return self.time

        
if __name__ == '__main__':
    t = utc_time()
    print(t.seconds_to_utc(126609427).show(False,True))

    

import datetime
from datetime import date, timedelta
import math
from django.utils import timezone

# 입사일 : 입력!



def Calculate(d0):
    #
    # d0 = datetime(2018, 8, 1)
    # 올해말 기준 퇴사일 : 2018.12.1일기준
    #     d1 = datetime(2018, 12, 1)
    d1 = date(timezone.now().year,12,31)
    if (d0.month == 1) & (d0.day == 1):
        a5 = 1
    else:
        a5 = 0

    # 첫회계일
    b3 = date(d0.year + 1, 1, 1)
    _b5 = (b3 - d0).days
    b5 = (_b5 / 30 - 1)

    _c5 = (d1 - d0).days
    c5 = (_c5 / 30)

    # print(_b5,_c5, b5,c5)

    d1y = d1.year
    d0y = d0.year
    b3y = b3.year
    sum = 0
    if d1.year == d0.year :
        vac = b5
        sum += vac
        return (sum)
    i = d1y + 2 - d0y



    if (i>=2):
     while (i >=2):


            if i==2:
                    vac3 = _b5 / 365 * 15
                    sum += vac3
                    #
                    # tmp2 = date(d0y + 1, 12, 31)
                    # if tmp2 > d1:
                    #     tmp = b5
                    #     if c5 > 11:
                    #         vac1 = 11 - tmp;
                    #         sum += vac1
                    #
                    #     else:
                    #         vac1 = c5 - tmp;
                    #         # print(vac1)
                    #         sum += vac1
                    # else:
                    #     vac1 = 11 - b5
                    #
                    #     # print(vac1)
                    #     sum += vac1
                    # print(vac1)
            else:


                    vac2 = math.ceil(i / 2) + 13

                    sum += vac2

            i -= 1
    return (sum)

def Calculate_year(d0):
    d1 = date(2018, 12, 31)
    if (d0.month == 1) & (d0.day == 1):
        a5 = 1
    else:
        a5 = 0

    # 첫회계일
    b3 = date(d0.year + 1, 1, 1)
    _b5 = (b3 - d0).days
    b5 = (_b5 / 30 - 1)

    _c5 = (d1 - d0).days
    c5 = (_c5 / 30)

    # print(_b5,_c5, b5,c5)

    d1y = d1.year
    d0y = d0.year
    b3y = b3.year

    if d1.year == d0.year:
        vac = b5
        return vac

    i = d1y + 2 - d0y

    if (i >= 3):
        vac2 = math.ceil(i / 2) + 13
        return vac2

    else :
        vac3 = _b5 / 365 * 15
        return vac3

#
# d0= date(2016,7,8)
# d1= date(2015,4,5)



def Calculate_keep(d0):
    d1 = date(timezone.now().year,timezone.now().month,timezone.now().day)
    return (d1-d0).days
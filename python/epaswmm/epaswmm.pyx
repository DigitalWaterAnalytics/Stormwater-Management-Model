
# Description: Cython module for encoding and decoding SWMM datetimes
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# cython: language_level=3


# python imports
from cpython.datetime cimport datetime
import math

# third-party imports

# project imports
from epaswmm cimport epaswmm

cdef int DateDelta = 693594  # days since 01/01/00
cdef double SecsPerDay = 86400.0  # seconds per day

cdef int[2][12] DaysPerMonth = [
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
        [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
]

cdef int is_leap_year(int year):
    """
    Check if a given year is a leap year.

    :param year: year to check
    :type year: int
    :return: 1 if the year is a leap year, 0 otherwise
    :rtype: int
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

cdef void div_mod(int a, int b, int* quotient, int* remainder):
    """
    Perform integer division and return the quotient and remainder.
    """
    quotient[0] = a // b
    remainder[0] = a % b

cpdef double encode_swmm_datetime(datetime pdatetime):
    """
    Encode a datetime object into a SWMM datetime.

    The SWMM datetime is a float that represents the OLE Automation date
    format. The integer part of the float represents the number of days since
    12/31/1899. The decimal part of the float represents the fraction of the
    day. For example, 1.5 represents 1 day and 12 hours.

    :param pdatetime: datetime object to encode into a SWMM datetime float value
    :type pdatetime: datetime
    :return: SWMM datetime float value
    :rtype: float
    """
    cdef int year = pdatetime.year
    cdef int month = pdatetime.month
    cdef int day = pdatetime.day
    cdef int hour = pdatetime.hour
    cdef int minute = pdatetime.minute
    cdef int second = pdatetime.second
    cdef int i, j, s
    cdef double encoded_date, encoded_time

    # Encode date
    i = is_leap_year(year)
    if (year >= 1 and year <= 9999 and month >= 1 and month <= 12 and day >= 1 and day <= DaysPerMonth[i][month-1]):
        for j in range(month - 1):
            day += DaysPerMonth[i][j]
        i = year - 1
        encoded_date = i * 365 + i // 4 - i // 100 + i // 400 + day - DateDelta
    else:
        encoded_date = -DateDelta

    # Encode time
    if (hour >= 0 and minute >= 0 and second >= 0):
        s = (hour * 3600 + minute * 60 + second)
        encoded_time = s / SecsPerDay
    else:
        encoded_time = 0.0

    return encoded_date + encoded_time

cpdef datetime decode_swmm_datetime(double swmm_datetime):
    """
    Decode a SWMM datetime into a datetime object.

    The SWMM datetime is a double that represents the number of days since
    12/31/1899. The decimal part of the double represents the fraction of the
    day. For example, 1.5 represents 1 day and 12 hours.

    :param swmm_datetime: SWMM datetime double value to decode into a datetime object
    :type swmm_datetime: double
    :return: datetime object
    :rtype: datetime
    """

    cdef int D1, D4, D100, D400
    cdef int y, m, d, i, k, t, year, month, day, h, mm, s
    cdef int mins, secs
    cdef double fracDay = (swmm_datetime - math.floor(swmm_datetime)) * SecsPerDay

    D1 = 365              # 365
    D4 = D1 * 4 + 1       # 1461
    D100 = D4 * 25 - 1    # 36524
    D400 = D100 * 4 + 1   # 146097

    t = int(math.floor(swmm_datetime)) + DateDelta
    if t <= 0:
        year = 0
        month = 1
        day = 1
    else:
        t -= 1
        y = 1
        while t >= D400:
            t -= D400
            y += 400
        div_mod(t, D100, &i, &d)
        if i == 4:
            i -= 1
            d += D100
        y += i * 100
        div_mod(d, D4, &i, &d)
        y += i * 4
        div_mod(d, D1, &i, &d)
        if i == 4:
            i -= 1
            d += D1
        y += i
        k = is_leap_year(y)
        m = 1
        while True:
            i = DaysPerMonth[k][m - 1]
            if d < i:
                break
            d -= i
            m += 1

        year = y
        month = m
        day = d + 1

    secs = (int)(math.floor(fracDay + 0.5))
    
    if  secs >= 86400:
        secs = 86399

    div_mod(secs, 60, &mins, &s)
    div_mod(mins, 60, &h, &mm)

    if ( h > 23 ):
        h = 0

    return datetime(year=year, month=month,day=day, hour=h, minute=mm, second=s)
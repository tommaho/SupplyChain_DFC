
import datetime

from calendar import monthrange

"""
Days Forward Coverage Utility Library

Tools for calculating days of coverage for a starting inventory against a
range of forecasted demand.

dfc_week
   Calculate DFC for a starting inventory and weekly demand series.

dfc_week_reverse
   Calculates the starting inventory required to maintain a specified DFC
   over a given weekly demand series.

dfc_month_greg
   Calculate DFC for a starting inventory and monthly demand series.

dfc_month_greg_reverse
   Calculates the starting inventory required to maintain a specified DFC
   over a given monthly demand series.
"""


def dfc_week(supply=0, demand=[0]):
    """
    Calculate DFC for a starting inventory and weekly demand series.

    """
    remaining = supply
    dfc = 0

    for week in demand:
        if remaining > week:
            dfc += 7
            remaining -= - week
        else:
            dfc += (remaining / (week / 7))
            break
    return dfc


def dfc_week_reverse(dfc=0, demand=[0]):
    """
    Calculates the starting inventory required to maintain a specified DFC
    over a given weekly demand series.
    """
    supply = 0
    weeks_covered = int(dfc / 7)
    days_leftover = int(dfc % 7)

    if weeks_covered > len(demand) or (weeks_covered == len(demand)
                                       and days_leftover > 0):
        return 9999

    for week in demand[:weeks_covered]:
        supply += week
    if days_leftover > 0:
        supply += (demand[weeks_covered] / 7) * days_leftover

    return supply


def dfc_month_greg(month_start_date='1-1-2000', supply=0, demand=[0]):
    """
    Calculate DFC for a starting inventory and monthly demand series.
    """
    remaining = supply
    dfc = 0

    month_start_date = datetime.datetime.strptime(month_start_date,
                                                  '%m-%d-%Y').date()
    days_in_month = monthrange(month_start_date.year,
                               month_start_date.month)[1]

    for month in demand:
        if remaining > month:

            dfc += days_in_month
            remaining -= month

        else:
            dfc += (remaining / (month / days_in_month))
            break

        days_in_month = monthrange(month_start_date.year,
                                   month_start_date.month % 12 + 1)[1]

    return dfc


def dfc_month_greg_reverse(month_start_date='1-1-2000', dfc=0, demand=[0]):
    """
    Calculates the starting inventory required to maintain a specified DFC
    over a given monthly demand series.
    """
    supply = 0

    month_start_date = datetime.datetime.strptime(month_start_date,
                                                  '%m-%d-%Y').date()
    days_in_month = monthrange(month_start_date.year,
                               month_start_date.month)[1]

    for month in demand:

        if dfc > days_in_month:
            supply += month
            dfc -= days_in_month
        else:
            supply += (dfc * (month / days_in_month))
            break

        days_in_month = monthrange(month_start_date.year,
                                   month_start_date.month % 12 + 1)[1]

    return supply


def dfc_month_tester():
    """
    function docstring
    """
    (print("Expected: 60:", dfc_month_greg(month_start_date='1-1-2016',
                                           supply=1000, demand=[500, 500, 500])))
    (print("Expected: 29:", dfc_month_greg(month_start_date='2-1-2016',
                                           supply=1000, demand=[1000, 500, 500])))
    (print("Expected: 60:", dfc_month_greg(month_start_date='2-1-2016',
                                           supply=1000, demand=[500, 500, 500])))
    (print("Expected: 90:", dfc_month_greg(month_start_date='2-1-2016',
                                           supply=2000, demand=[500, 500, 1000])))
    (print("Expected: 67.6:", dfc_month_greg(month_start_date='2-1-2016',
                                             supply=10000, demand=[5000, 4000, 4000])))

    print("Expected: 62:", dfc_month_greg(month_start_date='12-1-2016',
                                          supply=2000, demand=[1000, 1000, 1000]))
    print("Expected: 62:", dfc_month_greg(month_start_date='12-1-2016',
                                          supply=2000, demand=[1000, 999, 1000]))


def dfc_month_greg_reverse_tester():
    """
    function docstring
    """
    print("Expected 1000: ", dfc_month_greg_reverse(month_start_date='1-1-2016',
                                                    dfc=60, demand=[500, 500, 500]))
    print("Expected 1000: ", dfc_month_greg_reverse(month_start_date='1-1-2016',
                                                    dfc=29, demand=[1000, 500, 500]))
    print("Expected 1000: ", dfc_month_greg_reverse(month_start_date='2-1-2016',
                                                    dfc=60, demand=[500, 500, 500]))
    print("Expected 2000: ", dfc_month_greg_reverse(month_start_date='1-1-2016',
                                                    dfc=90, demand=[500, 500, 1000]))
    print("Expected 10000: ", dfc_month_greg_reverse(month_start_date='1-1-2016',
                                                     dfc=67.6, demand=[5000, 4000, 4000]))

    print("Expected 2000: ", dfc_month_greg_reverse(month_start_date='1-1-2016',
                                                    dfc=62, demand=[1000, 1000, 1000]))
    print("Expected 2000: ", dfc_month_greg_reverse(month_start_date='1-1-2016',
                                                    dfc=62, demand=[1000, 999, 1000]))



dfc_month_greg_reverse_tester()
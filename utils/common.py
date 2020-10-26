import re


def check_in_range_time(time_open, time):
    if time_open is not None:
        print(time_open.split(' - '))

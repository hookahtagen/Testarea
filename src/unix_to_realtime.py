"""
This program converts a unix timestamp to a realtime timestamp.
"""

import sys
import time
import datetime


def unix_to_realtime(unix_timestamp: int) -> str:
    return datetime.datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    u_time = 1678636528
    r_time = unix_to_realtime(u_time)

    print(r_time)
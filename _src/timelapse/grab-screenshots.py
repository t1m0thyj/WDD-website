import time

import pyscreeze
import win32api

times = [
    (3, 0),
    (6, 45),
    (7, 5),
    (7, 30),
    (7, 50),
    (9, 20),
    (10, 50),
    (12, 25),
    (13, 55),
    (15, 25),
    (17, 0),
    (18, 30),
    (18, 50),
    (19, 10),
    (19, 35),
    (23, 15)
]

time.sleep(10)
utc_offset = -4  # Local time = GMT-4
for i in range(len(times)):
    hour, minute = times[i]
    hour -= utc_offset
    day = 14 if hour < 24 else 15
    # SetSystemTime(year, month, dayOfWeek, day, hour, minute, second, millseconds)
    win32api.SetSystemTime(2024, 3, 4, day, hour % 24, minute, 0, 0)
    time.sleep(10)
    pyscreeze.screenshot(f"image-{i}.png")

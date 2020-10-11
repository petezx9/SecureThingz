#!/usr/bin/env python3
#
# simple script to make a 100 url request
# with as close to 1 seconds interval as posable
# and pint mean and max
#

import time
import numpy as np
import requests

url = "https://www.telegraph.co.uk/rugby-union/"
numrequests = 100
IntervalSecs = 1  # seconds

rtimes = []
for i in range(numrequests):
    # time full request
    start = time.time()
    response = requests.get(url)
    rtime = time.time() - start
    # add to list of responce times
    rtimes.append(rtime)
    print(rtime)
    # offset sleep time by response time, so our "requests per seconds" doesn't drift to much. Unless Rtime is > 1 sec then we have to drift.
    time.sleep(1-min(rtime,1))
print('mean:', np.mean(rtimes), ' Max:', np.max(rtimes))

#!/usr/bin/env python3
#
# read te upto 10,000 lines form log file.
# counts up and prints  responce time slower than 100ms, 500ms and 1s and average
#
import re
import sys

#logfile = open("/var/log/apache2/access.log", "r")
logfile = open("F://log.txt", "r")
lines = logfile.readlines()

# regx to split line up, we're really only intrested in reqest_time
regxexp = re.compile(r"(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?) \[(?P<date>.*?)(?= ) (?P<timezone>.*?)\] \"(?P<request_method>.*?) (?P<path>.*?)(?P<request_version> HTTP/.*)?\" (?P<status>.*?) (?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)\" (?P<request_time>.*?) (?P<therest>.*)")

# counters for slow responses
rt100 = 0
rt500 = 0
rt1000 = 0
rttotal = 0

count = 0
for line in reversed(lines):
    count += 1
    if count > 10000:
        count -= 1 #lets not over count.
        break

    Regxsearch = regxexp.search(line, re.IGNORECASE)
    # Atypical line? if our regx stumbles lets report it, but keep going.
    if not Regxsearch:
        print('Regx miss on line:'+line, file=sys.stderr)
        count -= 1 # lets get a 10000 sample if we can.
        continue

    # get request time (rt) form line
    rt = int(Regxsearch.group('request_time'))

    # count up lines at different durations and sum total
    if rt > 100:
        rt100 += 1
    if rt > 500:
        rt500 += 1
    if rt > 1000:
        rt1000 += 1
    rttotal += rt

# compute average
rtavg = rttotal / (count)

# print results.
print('line count:',count) # we show total count to give the other counts context in case we dont make full sample.
print('')
print('slower than  100ms:', rt100)
print('slower than  500ms:', rt500)
print('slower than 1000ms:', rt1000)
print('')
print('average:',rtavg)


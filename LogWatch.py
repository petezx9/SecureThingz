#!/usr/bin/env python3
#
# Simple python script to monitor a file
# and report lines that match a regx expresion.
# in this case we're monitoring an apaches log file
# and reports lines that are slow (1sec+)
#
import time
import sys
import os
import re


def follow(thefile, regxexp):
    '''yields new lines from apache log file
       if the request_duration > 1 sec
    '''
    thefile.seek(0, os.SEEK_END)

    while True:
        # read last line of file
        line = thefile.readline()

        # small wait if no new line, then go round again.
        if not line:
            time.sleep(0.1)
            continue

        Regxsearch = regxexp.search(line, re.IGNORECASE)
        # Atypical line? if our regx stumbles lets report it, but keep going.
        if not Regxsearch:
            print('Regx miss on line:'+line, file=sys.stderr)
            continue

        # if the response time <= 1 sec then go round again.
        if int(Regxsearch.group('request_time')) <= 1000:
            continue

        yield line


if __name__ == '__main__':
    logfile = open("/var/log/apache2/access.log","r") #apache log file to  monitor

    # regx to split line up, we're really only intrested in reqest_time
    regxexp = re.compile(
        r"(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?) \[(?P<date>.*?)(?= ) (?P<timezone>.*?)\] \"(?P<request_method>.*?) (?P<path>.*?)(?P<request_version> HTTP/.*)?\" (?P<status>.*?) (?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)\" (?P<request_time>.*?) (?P<therest>.*)")

    loglines = follow(logfile, regxexp)
    for line in loglines:
        print(line)

#!/usr/bin/env python3

# Author: Robert Russell

import sys
import os
import re

EXT = ".log"

argc = len(sys.argv)

if argc > 3:
    print("nextlog: too many arguments: expected max 2", file=sys.stderr)
    sys.exit(1)

# Resolve log file base path.
if argc >= 2:
    # nextlog [base_path]
    base_path = os.path.abspath(sys.argv[1])
    if not os.path.isdir(base_path):
        print("nextlog: expected base path to be an existing directory", file=sys.stderr)
        sys.exit(1)
else:
    base_path = os.getcwd()

# Resolve log filename prefix.
if argc == 3:
    # nextlog [base_path [prefix]]
    prefix = sys.argv[2]
else:
    prefix = "log"

# Find largest existing log number.
largest_log_n = -1
fname_re = re.compile("^"+re.escape(prefix)+"(\\d*)"+re.escape(EXT)+"$")
for fname in os.listdir(base_path):
    if not os.path.isfile(os.path.join(base_path, fname)):
        continue
    match = fname_re.match(fname)
    if match is not None:
        log_n = int(match.group(1))
        if log_n > largest_log_n:
            largest_log_n = log_n

print(os.path.join(base_path, prefix+str(largest_log_n+1)+EXT))

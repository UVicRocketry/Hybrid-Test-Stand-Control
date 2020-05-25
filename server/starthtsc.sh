#!/usr/bin/env bash


# Wait 30 seconds to make sure networking is running.
echo "Waiting 30s for networking to start..."
sleep 30
echo "Here we go. If the server fails to start, and error message will print."
# kill any process using our server port before the server starts. We do this by getting the process id (pid) and killing it
pid=$(lsof -t -i :9999 -s)
kill $pid

# f is a string that stores the next log file while the server is running.
# && chains two commands together.
# Then use python3 to run testmain.py and start adding any console output to f.
# Lastly if either of the first two parts fail, print a failure message.
f=$(/home/pi/Documents/htsc/server/nextlog.py /home/pi/Documents/logs) && /usr/bin/python3 /home/pi/Documents/htsc/server/testmain.py > $f 2>&1 || echo "failed to start HTSC server"

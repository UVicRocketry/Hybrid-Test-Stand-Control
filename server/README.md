# Hybrid Test Stand Raspberry Pi Setup

Follow the "Hybrid Instrumentation and Controls Documentation" guide in the UVR+ Google Drive to set up the pi.

Open terminal on the Raspberry Pi and run: `wget https://raw.githubusercontent.com/UVicRocketry/Hybrid-Test-Stand-Control/master/server/autoserversetup.sh && bash /home/pi/autoserversetup.sh`

### Notes

 - A cron job should start the server automatically on boot. It will wait 30s to allow for networking, after which, the client should be able to connect.

 - The [nextlog](nextlog.py) script is for managing log files, which are created in `/home/pi/Documents/logs` by
 default. Since the pi has no Real-Time-Clock, the logs are numbered rather than containing a date/time stamp (the higher the
 number, the more recent the log).
 
 - The libphidget22 library in /lib is from here: https://www.phidgets.com/docs/OS_-_Linux

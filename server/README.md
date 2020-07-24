# Hybrid Test Stand Raspberry Pi Setup

[Follow the documentation in the UVR drive for a more comprehensive guide.](https://docs.google.com/document/d/1ulo7Ckkgx2m6BxNc_R7TE3GIf-P8g2ysnO5t9tgAqOs/edit?usp=sharing)

Open terminal on the Raspberry Pi and run: `wget https://raw.githubusercontent.com/UVicRocketry/Hybrid-Test-Stand-Control/master/server/autoserversetup.sh && bash /home/pi/autoserversetup.sh >> autoserversetuplog.txt`

### Notes

 - A cron job should start the server automatically on boot. It will wait 30s to allow for networking, after which, the client should be able to connect.

 - The [nextlog](nextlog.py) script is for managing log files, which are created in `/home/pi/Documents/logs` by
 default. Since the pi has no Real-Time-Clock, the logs are numbered rather than containing a date/time stamp (the higher the
 number, the more recent the log).

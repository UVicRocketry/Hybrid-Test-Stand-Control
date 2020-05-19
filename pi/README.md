# Hybrid Test Stand Raspberry Pi Setup

 1. Clone this repository into the folder `/home/pi/Documents/htsc`:
 `git clone https://github.com/UVicRocketry/Hybrid-Test-Stand-Control.git /home/pi/Documents/htsc`.
 
 1. `mkdir /home/pi/Documents/logs`
 
 1. Copy the line inside [rc.local](rc.local) into `/etc/rc.local`, just before the `exit` statement.
 This is what calls the startup script when the pi boots.
 
 1. That's it!
 
 New Version:
 Open terminal on the Raspberry Pi and run `sudo wget https://github.com/jjderooy/Hybrid-Test-Stand-Control/blob/master/pi/first-time_server_setup.sh && bash first-time_server_setup.sh`
 
### Notes

 - You can change the install location of the hybrid code as long as you change the relevant paths in `/etc/rc.local`
 and [starthtsc.sh](starthtsc.sh) correspondingly.
 
 - The [nextlog](nextlog.py) script is for managing log files, which are created in `/home/pi/Documents/logs` by
 default. Since the pi has no RTC, the logs are numbered rather than containing a date/time stamp (the higher the
 number, the more recent the log).

# Frequently Asked Questions

## Log files

### Where can I find a specific log file?
All log files are saved in ```/home/pi/Desktop/sampler_logs/``` folder. 
A new log file is generated every time the program is run (that is every time you turn on the Pi) and its name is the time the program started. For example, if the program started at 2:30 pm on March 26 2020, the name of the log file is ```2020-03-26 14:30:00```.

### What do log files log?
The log files log:

- actions of pump, valves and diode
- content of configuration file
- content of schedule file and the all schedules that were generated based on the file
- ID number of sampler
- insertion of a new USB drive
- start and end of the program
- reset of GPIO pins and disablement of GPIO warnings
- type of exception and place where it occured

## USB

### How long does the USB needs to be inserted in Pi?
The Pi should detect and read the files from the USB drive within a second. The diode will light up after the USB drive is detected and files are correctly read.

### Can you insert multiple USBs to the Pi?
No. You are only allowed to insert one USB drive that contains the configuration and schedule file for the sampler.

### I inserted a USB with files in an incorrect format to the Pi, ejected it, corrected the files and inserted the USB to the Pi again with the files in the correct format. It is not working. What's wrong?
After you inserted a USB with files in an incorrect format, the program threw an exception and safely exited. Therefore, the program was no longer running when you inserted the USB with files in the correct format to the Pi.
To execute the schedule, turn the Pi off and on to start the program again and insert the USB.

### Can you SSH into the Pi and change the schedules on the USB drive without ejecting it?
No. If you change the schedule or configuration file by SSHing into the Pi, the program won't read the files again. To change schedule or configuration of sampler, you have to eject the USB or restart the Pi.

### Can the USB contain some other files and folders?
Yes.

### Can schedule and configuration files be stored in a folder on the USB drive?
No. The schedule and configuration files have to be store in the root directory of the USB drive.


## Raspberry Pi 

### If I turn the Pi off and back on again, will it remember its schedule and continue executing it?
No. You have to insert the USB drive to the Pi again.

### I SSHed into the Pi and noticed that the its time is incorrect. How do I fix it?
The Pi's time is set to UTC time (Coordinated Universal Time), so the time may be off by hours depending on your time zone. If the minutes and seconds are off, you have to connect the Pi to the Internet and it will be automatically updated.

### Where can I find the sampler ID number?
The sampler ID number is in ```/home/pi/.ID.txt``` file. Type ```nano /home/pi/.ID.txt``` into the command line to see the ID number.

### When will Pi turn itself off?




## Schedule and configuration files

### What happens when files are not in the correct format?

### How can I change the schedule?

### Can I change the schedule after the current schedule finished executing?

### What happens when I insert a USB with an old schedule to the Pi?

### I insert/reinsert a USB with a schedule to the Pi late. Some samples were already supposed to be taken and some samples are supposed to be taken right now. What is going to happen?




## Hardware

### What does it mean when the diode lights up?

### I inserted the USB to the Pi and the diode lighted up. After some time, I came back to check up on the sampler, the diode was no longer on. Does it mean there was a problem?

### The diode didn't light up after I inserted the USB to the Pi. What's wrong?
There are several possibilities:

- The schedule and configuration files 
        - aren't in the required format.
        - are missing.
        - don't have the corrent name
        - aren't stored in the root location in the USB.
- More than one USB is inserted in the Pi.
- Pi isn't turned on. The green and red lights on the motherboard should light up/blink.
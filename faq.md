# Frequently Asked Questions

## Log files

### Where can I find log files?

### What do log files log?





## USB

### How long does the USB needs to be inserted in Pi?

### Can you insert multiple USBs to the Pi?

### I inserted a USB with files in an incorrect format to the Pi, ejected it, corrected the files and inserted the USB to the Pi again with the files in the correct format. It is not working. What's wrong?


### Can you SSH into the Pi and change the schedules on the USB drive without ejecting it?


### Can the USB contain some other files and folders?

### Can the schedule and configuration files be stored in a folder on the USB drive?





## Raspberry Pi 

### If I turn the Pi off and back on again, will it remember its schedule and continue executing it?

### I SSHed into the Pi and noticed that the time it has is incorrect. How do I fix it?

### Where can I find the sampler ID number?


### When will Pi turn itself off?








## Schedule and configuration files

### What happens when files are not in the correct format?

### How can I change the schedule?

### Can I change the schedule after the current schedule finished executing?

### What happens when I insert a USB with an old schedule to the Pi?

### I insert/reinsert a USB with a schedule to the Pi late. Some samples were already supposed to be taken and some samples are supposed to be taken right now. What is going to happen?




## Hardware

### What does it mean when diode lights up?

### The diode didn't light up. What's wrong?
There are several possibilities:
- The schedule and configuration files 
        - aren't in the required format.
        - are missing.
        - don't have the corrent name
        - aren't stored in the root location in the USB.
- More than one USB is inserted in the Pi.
- Pi isn't turned on. The green and red lights on the motherboard should light up/blink.

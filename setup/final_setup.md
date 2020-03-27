# Hardware setup

## Create circuit for the sampler
![Circuit diagram for the sampler](/img/final_setup_schematic.jpg)

## Set up Raspberry Pi
### Using monitor and keyboard
 1. Install [balenaEtcher](https://www.balena.io/etcher/).
 2. Download latest version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) operating system.
 3. Connect SD card to the computer and mount the Raspbian image to the SD card using balenaEtcher.
 4. Insert SD card to the Raspberry Pi.
 5. Connect monitor, mouse, keyboard, Wi-Fi module and charger to the ports of Raspberry Pi.

### Headless using ethernet cable
1. Mount the Raspbian image to the SD card using balenaEtcher.
2. Create `ssh` file in `boot` drive, to allow ssh.

        touch /Volumes/boot/ssh
    
3. Connect one end of ethernet cable to Raspberry Pi and the other end to your computer.
4. Find the IP address of Raspberry Pi using `ping` command.

        ping raspberrypi.local

5. ssh into the Raspberry Pi. Replace `pi` with your Pi's username (default username is `pi`) and `IP` with the IP address.

        ssh pi@IP
    
    Answer `yes` to question `Are you sure you want to continue connecting?` and enter your password (default password is `raspberry`).
    
    

## Configure real time clock

### Circuit

Mount the real time clock to Raspberry pi.

If you have real time clock DS3231 Model B (the one with 6 pins), you can't mount it directly on GPIO pins because DS3231's pins are not in correct order.

* Vin/VCC connects to pin 1 (3.3V)

* GND connects to pin 6

* SDA connects to pin 3

* SCL connects to pin 5


![RTC circuit](/img/setup_RTC.png)

### Configuring the real-time clock

1. After the circuit is ready, open the command line and type

        >> sudo i2cdetect -y 1
	
    If the output is
    `Error: Could not open file '/dev/i2c-1'`
    or
    `/dev/i2c/1': No such file or directory`,
    try the following:
	
    * Open file /etc/modules.
	
            >> sudo nano /etc/modules
		
        Check if it contains i2c-bcm2708 and i2c-dev. If not, add them:
		
            i2c-bcm2708
            i2c-dev
		
        Save and exit the file (Ctrl + X).
		
    * Open /etc/modprobe.d/raspi-blacklist.conf
	
            >> sudo nano /etc/modprobe.d/raspi-blacklist.conf
		
        Check if i2c-bcm2807 is blacklisted. If it is, add # to the start of line.
		
            # blacklist i2c-bcm2708
		
    * Run `sudo raspi-config`.
        Select `5 Interfacing Options`.
        Then select `I2C` and enable it.
    * Restart the computer after doing any of the steps above.

            sudo shutdown -h now


2. After `>> sudo i2cdetect -y 1` is working,
    Raspberry Pi should detect the device is plug in.
    It should show 68 in row 60 and column 8.


3. Open file /etc/modules.

        >> sudo nano /etc/modules
	
    Add rtc-ds3231 to the file.
	
        rtc-ds3231

    Save and exit the file (Ctrl + X).

4. Open file /boot/config.txt.

        >> sudo nano /boot/config.txt
    
    Scroll to the bottom of the document and add dtoverlay-i2c-rtc,ds3231 to the file.
	
        dtoverlay-i2c-rtc,ds3231


5. Remove the fake power clock.

        >> sudo apt-get -y remove fake hwclock
        >> sudo update-rc.d -f fake-hwclock remove
	
	
6. Open file /lib/udev/hwclock-set.

        >> sudo nano /lib/udev/hwclock-set
	
    Comment the following lines at the beginning of the document.
    
        # if [ -e /run/systemd/system ] ; then
        # exit 0
        # fi
 
7. Reboot the Raspberry Pi.

        >> reboot
	
8. Check if Raspberry Pi has the right date and time.
    The `date` command prints the time that Raspberry Pi got from the Internet,
    and `sudo hwclock -r` prints the time that the real time clock has.
    
	    >> date; sudo hwclock -r
	
    If the outputted times don't match, update the hardware time to the Internet time:

        >> sudo hwclock -w

## Run driver.py script automatically at startup

1. Connect Raspberry Pi to Wi-Fi.
2. Save all files from this repository to `/home/pi/Desktop/sampler`.
3. Install Supervisor.

        >> sudo apt-get install -y supervisor
    
    
4. Start Supervisor service.

        >> sudo service supervisor start
    
    
5. Create the configuration information.

        >> sudo nano /etc/supervisor/conf.d/sampler.conf
    
    
6. Type the configuration information to the file and save it (Ctrl + X).

        [program:sampler]
        command=python3 driver.py
        directory=/home/pi/Desktop/sampler
        autostart=true
        autorestart=true
    
    
7. Include the new configuration file.

        >> sudo supervisorctl reread
    
    
8. Update Supervisor.

        >> sudo supervisorctl update
    
    
9. Check if the service started.

        >> sudo supervisorctl
    
    
    It should return something similar to `sampler RUNNING pid 1008 0:37:39`.


To stop the script:

    >> sudo supervisorctl stop sampler
    
    
To start the script:

    >> sudo supervisorctl start sampler
    

## Set ID number on SD card
1. Create a hidden file ```.ID.txt``` in the home directory. To verify that you are in the home directory, use command ```pwd```. It should return ```/home/pi```. 


        touch .ID.txt
        
        
2. Write the ID number into the file. For example, if the ID number is 90, open the file in the editor (```nano .ID.txt```), write 90 into the file and save it (```Ctrl+X```).

3. Give the file read-only permission. To verify that the permission was changed, use command ```ls -l -a```. The permission under ```.ID.txt``` should be ```-r--r--r--```.
        
        
        chmod 444 .ID.txt
        
        


# Configure GPS

## Circuit
The GPS module used was E218213 by adafruit.


* Vin connects to pin 17 (or any other 3.3 V pin)
* GND connects to pin 39 (or any other ground pin)
* RX connects to pin 8
* TX connects to pin 10


![Circuit diagram for the sampler](/img/setup_GPS.png)
## Configuration
1. Connect Raspberry Pi to Wi-Fi.
2. Enable serial interface.

        >> sudo raspi-config
    
    Go to `5 Interfacing Options`.
    Then go to `P6 Serial`.
    
    Answer `No` to question `Would you like a login shell to be accessible over serial`.
    
    Answer `Yes` to question `Would you like the serial port hardware to be enabled?`.
    
    Select `Finish` and `Restart`.
    
3. Modify the configuration file.


        >> sudo nano /boot/config.txt
    
    
    Scroll down and type
    
        dtoverlay=pi3-disable-bt
        core_freq=250
        enable_uart=1
        force_turbo=1
    
4. Backup cmdline.txt file.


        >> sudo cp /boot/cmdline.txt /boot/cmdline.txt.backup
    
    
5. Edit cmdline.txt file.


        >> sudo nano /boot/cmdline.txt
    
    
    If the file contains `console=serial0,115200`, delete it.
    
    Delete `root=PARTUUID=5e3da3da-02` and replace it with `root=/dev/mmcblk0p2`
    
6. Reboot Pi.


        >> sudo reboot
    
    
7. Stop and disable the serial ttyS0 service.


        >> sudo systemctl stop serial-getty@ttySO.service
        >> sudo systemctl disable serial-getty@ttySO.service
    
    
8. Reboot Pi.


        >> sudo reboot
    
    
9. Enable the serial ttyAMA0 service.


        >> sudo systemctl enable serial-getty@ttyAMA0.service


10. Verify that the service was enabled.


        >> ls -l /dev
    
    
    The service `serial0 -> ttyAMA0` should be in the outputted list of services.

11. Install minocom package that is used to connect to the GPS module.


        >> sudo apt-get install minicom
    
    
12. Install pynmea2 library that is used to parse the received data.


        >> sudo pip install pynmea2
    
    
13. Verify that the GPS module is working.


        sudo minicom -D /dev/ttyAMA0 -b 9600
    
    
    Press Ctrl + A. After that press X and then press Enter key.
    

# User Manual

This application is a software tool for operating airsampler that takes air samples according to the specified schedule. 

## Understanding how airsampler works
The airsampler consists of Raspberry Pi, power source, pump, tubing, thirteen solenoid valves and bags. 

## Schedule file format
```sfasd```

## Configuration file format
Configuration file contains information necessary to configure hardware and software of airsampler.

The configuration file contains the following information:

- ```Numbering mode```
	- Identifies the board numbering mode. It must be either ```BCM``` (the GPIO is identified by the number that is used by Broadcom, the manufacturer) or ```BOARD``` (the GPIO is identified by the position on the Pi).
- ```Bag numbers to valve pin numbers```
	- Links each bag number to the GPIO number that the valve that controls airflow into the bag is connected to.
- ```Pump pin number```
	- Identifies the GPIO number that the pump is connected to.
- ```Diode pin number```
	- Identifies the GPIO number that the diode is connected to.
- ```Number of seconds pump starts pumping before valve opens```
	- Specifies the number of seconds the pump starts pumping before a valve opens.
- ```Number of seconds pump continues pumping after valve closes```
	- Specifies the number of seconds the pump continues pumping after a valve closes.
- ```Pump time off tolerance in seconds```
	- Specifies the number of seconds. If pump is scheduled to turn off for less than the specified number of seconds, the pump will continue pumping.

Format requirements:

- The file name must be ```<sampler ID>_config.txt```. For example, if the sampler has ID 90, its configuration file is ```90_config.txt```.
- No additional lines (blank lines included) are allowed anywhere in the file. 
- The headers for the lines (```Numbering mode```, ```Bag numbers to valve pin numbers```, etc) have to be exactly in the same format as listed below. 
- There may be white spaces in the beggining and in the end of each line.
- The line below the ```Bag numbers to valve pin numbers``` line must be in format ```<bag number 1> : <GPIO number 1>, ..., <bag number n> : <GPIO number n>```. For example, ```1: 19, 2: 4, 3: 22```. All whites spaces on this line are ignored.


An example of the required configuration file format:


	Numbering mode
	BCM
	Bag numbers to valve pin numbers
	1: 19, 2: 4
	Pump pin number
	13
	Diode pin number
	17
	Number of seconds pump starts pumping before valve opens
	5
	Number of seconds pump continues pumping after valve closes
	5
	Pump time off tolerance in seconds
	10



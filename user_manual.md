# User Manual

This application is a software tool for operating airsampler that takes air samples according to the specified schedule. 

## Understanding how airsampler works
Refer to the diagram below to understand how the airsampler works.
![Algorithm](/img/algorithm_diagram.png)

## Schedule file format
Schedule file contains information necessary to take the air samples.

Format requirements:

- The file name must be ```<sampler ID>_schedule.txt```. For example, if the sampler has ID 90, its schedule file is ```90_schedule.txt```.
- The file must contain header. The first line of the file must be ```Bag number, Start filling, Stop filling```. No white spaces in the begging or in the end of line are allowed.
- Lines that start with ```#``` are considered a comment. ```#``` must be the first character on the line and no white spaces are allowed in front of it.
- Lines containing information about taking a sample must be in the format ```<bag number>, <time start filling>, <time stop filling>```. For example, ```3,  2020-03-06 11:38:00,  2020-03-06 11:38:30```. 
	- Additional white spaces may be included in this line as long as they are not in ```2020-03-06``` and ```11:38:00```.
	- The time must contain full year (```2020```, not ```20```). Month and day don't have to be padded with zeros. Hour also doesn't have to be padded with zeros.
- Bag number may be padded with zeros.
- No blank lines, lines that don't start with ```#``` and lines that aren't in format ```<bag number>, <bag starts filling>, <bag stops filling>``` are allowed anywhere in the file.
- Lines containing a schedule for a sample don't have to be ordered in any way (for example, it is not necessary to order them according to the ```Bag number``` or ```Start filling```.
- The ```Start filling``` time must be earlier than ```Stop filling``` time.

Also note that times for multiple samples can overlap and there can be multiple samples for one bag.


An example of the required schedule file:

	Bag number, Start filling, Stop filling
	3,  2020-03-06 11:38:00,  2020-03-06 11:38:30
	1,  2020-03-06 11:38:15,  2020-03-06 11:38:40
	# this is a comment
	2,  2020-03-06 11:39:15,  2020-03-06 11:39:35
	1,  2020-03-06 11:40:00,  2020-03-06 11:40:30


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
- ```Diode light duration```
	- Specifies the number of seconds the diode stays turned on to indicate that the hardware and software was set up correctly.
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
- The headers can be in any order.
- There may be white spaces in the beggining and in the end of each line.
- The line below the ```Bag numbers to valve pin numbers``` line must be in format ```<bag number 1> : <GPIO number 1>, ..., <bag number n> : <GPIO number n>```. For example, ```1: 19, 2: 4, 3: 22```. All whites spaces on this line are ignored.


An example of the required configuration file:

	Numbering mode
	BCM
	Bag numbers to valve pin numbers
	1: 19, 2: 4
	Pump pin number
	13
	Diode pin number
	17
	Diode light duration
	3
	Number of seconds pump starts pumping before valve opens
	5
	Number of seconds pump continues pumping after valve closes
	5
	Pump time off tolerance in seconds
	10



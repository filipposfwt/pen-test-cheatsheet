## HID USB
By having access to a DigiSpark Attiny85 USB one could use the board in order to emulate a keyboard and execute commands or payloads on the computer that the USB got connected. In order to upload the code to the board Arduino IDE can be used and the lirary Digispark AVR Boards should be installed. The Board must be set to Digispark (Default - 16.5mhz) and the Programmer to Micronucleous. After verifying the code,when clicking upload, the USB should be disconnected and plugged when prompted. 
> At the time of writing Digispark official website is not accessible, therefore the link used to install the library is this https://raw.githubusercontent.com/digistump/arduino-boards-index/master/package_digistump_index.json.
### Guides and resources
- A complete guide on setting up the USB - https://macrosec.tech/index.php/2021/06/10/creating-bad-usb/
- A 3d model for printing a case - https://www.thingiverse.com/thing:6125087
- Payloads:
  	- https://github.com/MTK911/Attiny85
	- https://github.com/CedArctic/DigiSpark-Scripts

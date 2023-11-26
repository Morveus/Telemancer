
# Telemancer Remote Controller

Prototype / Work in Progress

I've been looking for a good-looking, functional remote that can interact with my home automation setup. I've never been able to find something that works for me.

The idea is to build a WiFi remote that will send HTTP/HTTPS API calls to any endpoint (to me, it will be HomeAssistant, Yamaha MusicCast, Kodi, Philips Hue...). I also very much like the nVidia Shield remote's form factor, so that's the idea I've asked a CAD designer to work on.

Here's a TODO of the project:

 - 🟢 ESP32 running MicroPython
 - [x] Rudimentary Web WiFi Setup
 - [x] Rudimentary Web Server
 - [x] Multiple Profiles
 - [x] Up, Down, Left, Right, OK buttons
 - [x] Power and Reset Buttons
 - [x] Back and Home buttons
 - [x] Customizable behaviors: 
	 - [x] Buttons can be set to "Press Once"
	 - [x] Buttons can be set to "Press and repeat until released"
	 - [x] Repeat rate can be changed (in millisecond) for each button
	 - [x] Buttons can have a secondary 
 - [ ] WiFi connectivity
 - [ ] 4 diodes that tell you which profile is currently set
 - [ ] (Maybe) backlit buttons
 - [ ] Nice Web Interface
 - [ ] PCB design (made by a friend)
 - [ ] Prototype mechanical design
	 - [ ] First, 3D printable
	 - [ ] Then, prototyped with silicon mold injection
 - [ ] Beeper, to allow you to find the remote when lost between the seats by sending an HTTP call to its internal webserver
 - [ ] Accelerometer allowing the backlight and profile LEDs to turn on (like on the nVidia Shield remote)
 - [ ] Battery (18650) and charger
 - [ ] USB-C
 - [ ] Charging base

Maybe later, depending on how successful this project is:
 - [ ] Infrared
 - [ ] Bluetooth

![image](https://github.com/Morveus/Telemancer/assets/2972468/af39033d-38a7-4694-a77c-d320b26f7710)

(please don't mind the PCB sketch which is totally random, I don't know anything about PCB design)

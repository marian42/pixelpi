# pixelpi
Games and Animations on 16x16 LEDs

![16x16 LED matrix](https://i.imgur.com/jsguEYE.jpg)

This is a collection of python scripts that run animations and games on a 16x16 matrix of WS2812B LEDs (aka Neopixel).
The project is inspired by and compatible to Jeremy Williams' [Game Frame](http://ledseq.com).

## Setup

### Hardware

Here is a [set of photos](https://imgur.com/a/Ql25S) of the hardware I use and a parts list with approximate costs:
- 300 LEDs, WS2812B, 60/m 38 €
- Frame 32 €
- Raspberry Pi Model B 25€
- Power Supply 5V 10A 12,07 €
- Wifi-Stick 10 €
- Eboy animations from ledseq.com 9€
- Cardboard for the grid 2 €
- Level shifter 1 €
- 5V jack 1 €
- Plywood 1 €
- Wire, solder, connectors, heat shrink tube, etc

(131€ total, about $150)

### LED strips

I recommend you use [this tutorial](https://learn.adafruit.com/neopixels-on-raspberry-pi/overview) to set up the LED hardware.
Make sure you install [rpi_ws281x](https://github.com/jgarff/rpi_ws281x.git) as explained in the tutorial.

Then copy this repository somewhere to the SD card, copy your andimations to the sd card and run a script.

You can edit the `Screen.py` file to default to the LED strip settings you used in the neopixel tutorial (especially pin and brightness).

I'm using a Raspberry Pi Model B, if you want to use a Raspberry Pi 2 (B), try  [this fork](https://github.com/richardghirst/rpi_ws281x) of the rpi_ws281x module.

### LED layout

The `Screen.py` script expects your LED strip to be layed out like this:

```
-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->
<- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <-
-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->
...
```

If you have a different setup, you can edit the `Screen.py` file to translate the 16x16 matrix on your LED strip.

## Animations

The `Animation.py` script can run all animations that work with the Game Frame.
Here are the [Eboy animations](http://ledseq.com/product/game-frame-sd-files/) and a [forum for fan-made Game Frame animations](http://ledseq.com/forums/forum/game-frame/game-frame-art/).

Each animation should have it's own folder. If you have all animations in the folder `myfolder`, you can run
```
sudo python Animation.py myfolder/animation1
```

To cycle through multiple animations, run
```
sudo python Cycle.py myfolder
```

It's a good idea to run this command at the boot of the Pi, in this case you need absolute paths for the python file and animations folder.

## Gamepad
The current gamepad code probably only works with my logitech gamepad. I'm planning to make more generic gamepad support. Until then, you need to edit the `gamepad.py` file and make it work with your gamepad.

# pixelpi
Games and Animations on 16x16 LEDs

![16x16 LED matrix](https://i.imgur.com/jsguEYE.jpg)

This is a collection of python scripts that run animations and games on a 16x16 matrix of WS2812B LEDs (aka Neopixel).
The project is inspired by and compatible to Jeremy Williams' [Game Frame](http://ledseq.com).

## Hardware

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

## Software

To set up the software, clone this repository on your Raspberry Pi. Rename the file `config.ini.example` to `config.ini`.
Make sure, the neopixel library is installed.
This project uses Python 2.7.

### Animations
Place your animations in a folder called `animations` in the repository. For each animation, a file `/animations/animation_name/0.bmp` should exist.

Here are the [Eboy animations](http://ledseq.com/product/game-frame-sd-files/) and a [forum for fan-made Game Frame animations](http://ledseq.com/forums/forum/game-frame/game-frame-art/).

Take a look at the files `example_animation.py` and `example_cycle.py` to display single or multiple animations.

### Gamepad
The current gamepad code probably only works with my logitech gamepad. I'm planning to make more generic gamepad support. Until then, you need to edit the `gamepad.py` file and make it work with your gamepad.

### Menu
The file `menu.py` provides a visual menu to select from the available modules such as animations and games. For me, this is the default way of using the LED screen. You need a gamepad for this to work.

### Virtual hardware
You can test all software without a Raspberry Pi, Gamepad or LED matrix. To do so, set up the software as described above and edit the `config.ini` file. Set `virtualhardware` to true. Try to run `menu.py`, a window with a simulated screen should open. Note that this requires `pygame` which you may need to install.
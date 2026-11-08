# DrumLights

Piezo-sensitive LED control for Samba drumming. A small, cheap Arduino Nano shield picks up the signal from a piezo disc on the drum and drives RGB LEDs through N-channel MOSFETs, so the drum lights up when it is hit.

This design was featured and used in the **Adelaide Fringe Festival parade**.

## Links

- Buy the board: [DrumLights on Tindie](https://www.tindie.com/products/whatnick/drumlights/)
- Build write-up: [Piezo Activated Drumlights on Hackster.io](https://www.hackster.io/whatnick/piezo-activated-drumlights-3be4e3)
- Videos of experiments: [whatnick on YouTube – DrumLights search](https://www.youtube.com/@whatnick/search?query=drum%20lights)
- Roadmap: [GitHub Project board](https://github.com/users/whatnick/projects/1/views/2) (Tindie product manager)

## How it works

1. A piezo disc is attached to the drum head or shell. A hit produces a voltage spike.
2. The spike is read on `A1` of the Arduino Nano (the piezo is loaded with a high-value resistor to keep the ADC input safe).
3. A 30-sample running average smooths the signal and rejects crosstalk; values above `noise_thresh` trigger the lights.
4. A potentiometer on `A0` sets how long the light stays on.
5. PWM pins `D3` (green), `D5` (red) and `D6` (blue) drive MOSFETs that switch the LED channels.

## Repository layout

| Path | Contents |
| --- | --- |
| `DrumLights/DrumLights.ino` | Arduino firmware (needs the [RunningAverage](http://playground.arduino.cc/Main/RunningAverage) library) |
| `Drumlight_PCB/` | KiCad project for the Nano shield (schematic, PCB, footprints, 3D models) |

![Schematic](Drumlight_PCB/drumlights_schema.png)

## Getting started

1. Install the Arduino IDE and the `RunningAverage` library.
2. Open `DrumLights/DrumLights.ino`, select *Arduino Nano*, and upload.
3. Fit the shield, connect the piezo, LED strip and a 5 V supply.
4. Tune `noise_thresh` and the delay pot for your drum.

## Similar open-source projects

- [Arduino Knock sensor example](https://docs.arduino.cc/built-in-examples/sensors/Knock/) – the basic piezo-to-Arduino reading used as a starting point.
- [Mike Barela / Adafruit piezo trigger tutorials](https://learn.adafruit.com/) – piezo and LED triggering with Adafruit boards.
- [Arduino Drum Trigger / Hi-Hat Controller – Arduino MIDI Drums (ATmega MIDI drum kits)](https://github.com/topics/arduino-drums) – open-source piezo drum triggers.
- [WLED](https://github.com/Aircoookie/WLED) – open-source LED controller that can be driven by audio/sensor input on ESP8266/ESP32.
- [Open Music Labs piezo drum trigger notes](https://www.openmusiclabs.com/) – conditioning piezo signals.

## Roadmap

Tracked as GitHub issues and on the [Tindie product manager project board](https://github.com/users/whatnick/projects/1/views/2). See the [issue list](https://github.com/whatnick/DrumLights/issues) for current status.

## License

See repository for license details.

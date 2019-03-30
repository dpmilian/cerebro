![jenkins status](https://travis-ci.org/fanequinha/cerebro.svg?branch=master)

![A Industriosa](https://i.imgur.com/DZ3NuFg.png)

This mono-repo contains the python related areas of `fanequiña`, that is an [A Industriosa](https://intranet.aindustriosa.org/) project about creating an autonomous boat.

Each folder in this mono-repo is a development area for `fanequiña`, currently we are working on the following areas:

# Mastermind 
A Machine Learning model & engine created to make `fanequiña` aware of it's surroundings while navigating.

# Commander
[dronekit](http://python.dronekit.io/)'s project created to work together with `Mastermaind` to command `fanequiña` using [pixhawk 4](https://pixhawk.org/).

## Installation Ground Stations software

Firstable to connect and setup the PX4 you need to install some GCS software.

- Download and install [QGroundControl](http://qgroundcontrol.com/downloads) or [other option](http://ardupilot.org/rover/docs/common-install-gcs.html)

## Load ArduRover firmware into PX4 (Pixhawk 4)

We need to upload and configure the ArduRover firmware.
- [ArduRover 2.4 download](http://firmware.ardupilot.org/Rover/)
- [Pixhawk Firmware upload](http://ardupilot.org/rover/docs/common-loading-firmware-onto-pixhawk.html)

## Telemetry Radio control configuration

If you have any problem with Telemetry connetion you can always
connect with USB [more info](http://ardupilot.org/rover/docs/common-connect-mission-planner-autopilot.html)

### Telemetry drivers
- Download driver from [FTDI chip](http://www.ftdichip.com/Drivers/VCP.htm)
- Download driver from [Driver page](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)
    - Use 10_4_10_5_10_6_10_7 app.
    - Verify install using command `ls -la /dev/tty.*`

### Hardware configuration (http://andrewke.org/setting-up-cloned-3dr-telemetry/)
- Request the battery.
- Inside `fanequiña` box, you will find the adapter.
- Plug the connector at `POWER` connector.
- Get the antenna, plug it at `TELEM1` plug.
- Plugin usb receiver in your computer

## Pixhawk configuration

There are some mandatory configurations. Also you must take in account that the hardware devices
like compass, motors, etc could generate some noise with other devices. In those cases you will
have problems with some firmware configuration, arming the rover or changing the vehicle mode.

### Mandatory Hardware Configuration
- http://ardupilot.org/rover/docs/rover-code-configuration.html

    - Configure Firmware as Boat (“Frame class”)

    >To specify that the vehicle is a boat the FRAME_CLASS parameter should be set to 2 (Boat).

    - http://ardupilot.org/rover/docs/boat-configuration.html#boat-configuration
    - http://ardupilot.org/rover/docs/balance_bot-configure.html?highlight=frame_class#parameter-configuration
    - http://ardupilot.org/rover/docs/rover-motor-and-servo-connections.html?highlight=servo

    - http://ardupilot.org/rover/docs/common-pixhawk-and-px4-compatible-rc-transmitter-and-receiver-systems.html#common-pixhawk-and-px4-compatible-rc-transmitter-and-receiver-systems

### Conecting the receiver
  - http://ardupilot.org/rover/docs/common-pixhawk-and-px4-compatible-rc-transmitter-and-receiver-systems.html


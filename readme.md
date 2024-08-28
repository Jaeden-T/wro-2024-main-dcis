**WRO 2024 Submission**

## Project Structure

### Documentation
#### Overview
The `./docs/` directory contains project documentation, including notes, guidelines, and specifications.

### Motor Control Raspberry Pi
#### Challenge-Specific Code
* `./motor-pi/c1`: Contains challenge-specific code for motor controlling on Raspberry Pi.
* `./motor-pi/c2`: Additional challenge-specific code for motor controlling on Raspberry Pi.

### Sensor Data Collection Raspberry Pi
#### Data Collection Scripts and Libraries
The `./sensor-pi/` directory contains data collection scripts and libraries for the second Raspberry Pi, running
on a Pi 3.
#### Test Case Data
* `./sensor-pi/testCases`: Contains test case data for all sensors.

### Older Schematics
#### Historical Planning Documents
The `./oldElectronicsDigrams/` directory contains older schematics and whiteboard notes used when planning the
robot.
#### Relevant Images
* `Car-Diagram-Rough.jpeg`: The first whiteboard diagram.
* `whiteboarDigram.png`: The second version of the schematic.

## track.blend
#### Blender File for Image Tracking Simulations
This is a Blender file used for simulations of camera before car model to run image tracking.

# Others folder
#### Older Test Code
The `Others` folder contains older code that was used during test periods.
* `imagetests.py`: Opencv contour tests.
* Round 1 and Round 2 Tests: Folders containing tests of image segmentation using opencv to find contour outlines.

## Hardware Used:
#### Equipment List
This section lists the hardware used for the project, including:
* Raspberry pi 3 and 5
* Ethernet patch cable
* 4 Ultrasonic Sensors
* 1 Servo MG995
* 1 Motor
* 1 H-bridge l298n
* Lipo Battery - 9V
* 1 Buzzer for debugging
* 1 start button
* 1 switch for mode choices
* 1 powerbank for power to the pis
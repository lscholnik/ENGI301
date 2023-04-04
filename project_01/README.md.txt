# Puppeteer Robot

For the files associated with "Mechanically actuated shadow puppets using PocketBeagle". To run the program as-is upon boot, download "projectthread.py", "configure-pins.sh", and "run", and configure these to run using crontab. To implement by calling in the commandline, only "projectthread.py" is necessary. You will need to be able to import things such as time, pwm, gpio, etc, but all of the drivers are self contained within the singular file. See comments within the code for information when modifying the program. Note that the stepper driver is adapted from Gavin Lyons' RpiMotorLib. Found at: https://github.com/gavinlyonsrepo/RpiMotorLib/blob/982be0cf0142828faa40a38a15b6c406dcde0304/RpiMotorLib/RpiMotorLib.py

To run the program from the commandline, use "python3 projectthread.py". Be aware that the puppets/servos will likely turn upon initiation, and therefore the servos must not be blocked by anything. If the file is run this way, you must also exit by using "ctrl c" three times. Failing to do so will initiate the stepper motors and the speaker.

All user inputs are done through the six buttons.

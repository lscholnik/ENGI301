# Puppeteer Robot

For the files associated with "Mechanically actuated shadow puppets using PocketBeagle". To run the program as-is upon boot, download "projectthread.py", "configure-pins.sh", and "run", and configure these using crontab. To implement by calling in the commandline, only "projectthread.py" is necessary. You will need to be able to import variables such as time, pwm, gpio, etc, but all of the drivers are self contained within the singular file. See comments within the code for information when modifying the program. Note that the stepper driver is adapted from Gavin Lyons' RpiMotorLib https://github.com/gavinlyonsrepo/RpiMotorLib/blob/982be0cf0142828faa40a38a15b6c406dcde0304/RpiMotorLib/RpiMotorLib.py

To run the program from the commandline
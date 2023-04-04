"""
--------------------------------------------------------------------------
This whole thing was my attempt at making the servo turn with a button press
Servo Driver --> was having issues with importing, which is why I copy and 
pasted all of my things together like an idiot
--------------------------------------------------------------------------
License:   
Copyright 2021-2023 - Lily Scholnik

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

SG90 Servo Driver

API:
  Servo(pin)
    - Provide pin that the Servo is connected
  
    turn(percentage)
      -   0 = Fully clockwise
      - 100 = Fully anti-clockwise

"""
import Adafruit_BBIO.PWM as PWM

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

SG90_FREQ               = 50                  # 20ms period (50Hz)
SG90_POL                = 0                   # Rising Edge polarity
SG90_MIN_DUTY           = 5                   # 1ms pulse (5% duty cycle)  -- Fully clockwise (right)
SG90_MAX_DUTY           = 7                  # 2ms pulse (10% duty cycle) -- Fully anti-clockwise (left)

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Servo():
    """ CombinationLock """
    pin       = None
    position  = None
    button_index = None
    
    def __init__(self, pin=None, default_position=0):
        """ Initialize variables and set up the Servo """
        if (pin == None):
            raise ValueError("Pin not provided for Servo()")
        else:
            self.pin = pin

        self.position = default_position
        self.button_index = 0
        self._setup(default_position)
    
    # End def
    
    
    def _setup(self, default_position):
        """Setup the hardware components."""
        # Initialize Servo; Servo should be "off"
        
        PWM.start(self.pin, self._duty_cycle_from_position(default_position), SG90_FREQ, SG90_POL)
        
        
        # Set default position
        self.turn(default_position)

    # End def

    def _duty_cycle_from_position(self, position):
        """ Compute the duty cycle from the position """
        return ((SG90_MAX_DUTY - SG90_MIN_DUTY) * (position / 100)) + SG90_MIN_DUTY
    
    def get_position(self):
        """ Return the position of the servo """
        return self.position
    
    # End def
    

    def turn(self, position):
        """ Turn Servo to the desired position based on percentage of motion range
        
              0% = Fully clockwise (right)
            100% = Fully anti-clockwise (left)      
        """
        # Record the current position
        self.position = position
        #print("I turned {}".format(position))
        
        # Set PWM duty cycle based on position
        #duty_cycle = ((SG90_MAX_DUTY - SG90_MIN_DUTY) * (position / 100)) + SG90_MIN_DUTY
        
        PWM.set_duty_cycle(self.pin, self._duty_cycle_from_position(position))
        #print("Turning servo to position {0} using duty cycle {1}".format(position, duty_cycle))
        # !!! NEED TO IMPLEMENT !!! #

    # End def

    def button_1_functions(self):
        
        #current_func = button_functions[self.button_index]
        self.button_index = (self.button_index + 1) % 2
        
        self.turn(int(100*self.button_index))
        time.sleep(0.3)        
        
        #current_func()
    # End def
    
    def cleanup(self):
        """Cleanup the hardware components."""
        # Stop servo
        PWM.stop(self.pin)
        PWM.cleanup()
        
    # End def

# End class

'''
""" 
From petebachant

**need to change pins?
my pins are: 

bbpystepper is a Python module used to control a stepper motor via the 
BeagleBone

"""

from __future__ import division
import Adafruit_BBIO.GPIO as GPIO
import time
import math


def initialize_pins(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

def set_all_pins_low(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
        
def wavedrive(pins, pin_index):
    for i in range(len(pins)):
        if i == pin_index:
            GPIO.output(pins[i], GPIO.HIGH)
        else:
            GPIO.output(pins[i], GPIO.LOW)

def fullstep(pins, pin_index):
    """pin_index is the lead pin"""
    GPIO.output(pins[pin_index], GPIO.HIGH)
    GPIO.output(pins[(pin_index+3) % 4], GPIO.HIGH)
    GPIO.output(pins[(pin_index+1) % 4], GPIO.LOW)
    GPIO.output(pins[(pin_index+2) % 4], GPIO.LOW)


class Stepper(object):
    def __init__(self, steps_per_rev=2048.0,
                 pins=["P2_1", "P2_2"]):

        self.pins = pins
        
        initialize_pins(self.pins)
        set_all_pins_low(self.pins)
        
        self.angle = 0
        self.steps_per_rev = steps_per_rev
        
        # Initialize stepping mode
        self.drivemode = fullstep
    
    def rotate(self, degrees=360, rpm=15):
        step = 0
        
        # Calculate time between steps in seconds
        wait_time = 60.0/(self.steps_per_rev*rpm)
        
        # Convert degrees to steps
        steps = math.fabs(degrees*self.steps_per_rev/360.0)
        self.direction = 1
        
        if degrees < 0:
            self.pins.reverse()
            self.direction = -1
        
        while step < steps:
            for pin_index in range(len(self.pins)):
                self.drivemode(self.pins, pin_index)
                time.sleep(wait_time)
                step += 1
                self.angle = (self.angle + self.direction/self.steps_per_rev \
                *360.0) % 360.0
        
        if degrees < 0:
            self.pins.reverse()
    	
        set_all_pins_low(self.pins)
        
    def zero_angle(self):
        self.angle = 0
        

def main():
    stepper = Stepper()
    stepper.rotate()
    

if __name__ == "__main__":
    main()
    
'''    
    
    
#!/usr/bin/env python3
"""A python 3 library for various
 motors and servos to connect to a raspberry pi"""
# ========================= HEADER ===================================
# title             :rpiMotorlib.py
# description       :A python 3 library for various motors
# and servos to connect to a raspberry pi
# This file is for stepper motor tested on
# 28BYJ-48 unipolar stepper motor with ULN2003  = BYJMotor class
# Bipolar Nema stepper motor with L298N = BYJMotor class.
# Bipolar Nema Stepper motor TB6612FNG = BYJMotor class
# Bipolar Nema Stepper motor A4988  Driver = A4988Nema class
# Bipolar Nema Stepper motor DRV8825 Driver = A4988Nema class
# Bipolar Nema Stepper motor LV8729  Driver = A4988Nema class
# Bipolar Nema Stepper motor A3967 Easy Driver = A3967EasyNema class
# Main author       :Gavin Lyons
# Version           :See changelog at url
# url               :https://github.com/gavinlyonsrepo/RpiMotorLib
# mail              :glyons66@hotmail.com
# python_version    :3.5.3

# ========================== IMPORTS ======================
# Import the system modules needed to run rpiMotorlib.py
import sys
import time
import Adafruit_BBIO.GPIO as GPIO

# ==================== CLASS SECTION ===============================

class StopMotorInterrupt(Exception):
    """ Stop the motor """
    pass

 
class A4988Nema(object):
    """ Class to control a Nema bi-polar stepper motor with a A4988 also tested with DRV8825"""
    def __init__(self, direction_pin, step_pin, reset_pin, mode_pins, motor_type="A4988"):
        """ class init method 3 inputs
        (1) direction type=int , help=GPIO pin connected to DIR pin of IC
        (2) step_pin type=int , help=GPIO pin connected to STEP of IC
        (3) mode_pins type=tuple of 3 ints, help=GPIO pins connected to
        Microstep Resolution pins MS1-MS3 of IC, can be set to (-1,-1,-1) to turn off
        GPIO resolution.
        (4) motor_type type=string, help=Type of motor two options: A4988 or DRV8825
        """
        self.motor_type = motor_type
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        self.reset_pin = reset_pin

        if mode_pins[0] != -1:
            self.mode_pins = mode_pins
        else:
            self.mode_pins = False

        self.stop_motor = False
        GPIO.setup(self.reset_pin, GPIO.OUT)
        self.set_reset(True)
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)

    def set_reset(self, reset):
        """ Set the value of the reset pin """
        if reset:
            GPIO.output(self.reset_pin, GPIO.LOW)
        else:
            GPIO.output(self.reset_pin, GPIO.HIGH)


    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True

    def resolution_set(self, steptype):
        """ method to calculate step resolution
        based on motor type and steptype"""
        if self.motor_type == "A4988":
            resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (1, 1, 1)}
        else:
            print("Error invalid motor_type: {}".format(self.motor_type))
            quit()

        # error check stepmode
        if steptype in resolution:
            pass
        else:
            print("Error invalid steptype: {}".format(steptype))
            quit()

        if self.mode_pins != False:
            GPIO.output(self.mode_pins, resolution[steptype])

    def motor_go(self, clockwise=False, steptype="Full",
                 steps=200, stepdelay=.005, verbose=False, initdelay=.05):
        """ motor_go,  moves stepper motor based on 6 inputs
         (1) clockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (2) steptype, type=string , default=Full help= type of drive to
         step motor 5 options
            (Full, Half, 1/4, 1/8, 1/16) 1/32 for DRV8825 only 1/64 1/128 for LV8729 only
         (3) steps, type=int, default=200, help=Number of steps sequence's
         to execute. Default is one revolution , 200 in Full mode.
         (4) stepdelay, type=float, default=0.05, help=Time to wait
         (in seconds) between steps.
         (5) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (6) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.
        """
        self.stop_motor = False
        # setup GPIO
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.output(self.direction_pin, clockwise)
        if self.mode_pins != False:
            GPIO.setup(self.mode_pins, GPIO.OUT)
        self.set_reset(False)

        try:
            # dict resolution
            self.resolution_set(steptype)
            time.sleep(initdelay)

            for i in range(steps):
                if self.stop_motor:
                    raise StopMotorInterrupt
                else:
                    GPIO.output(self.step_pin, True)
                    time.sleep(stepdelay)
                    GPIO.output(self.step_pin, False)
                    time.sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i+1), end="\r", flush=True)

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib:")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("RpiMotorLib  : Unexpected error:")
        else:
            # print report status
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Motor type = {}".format(self.motor_type))
                print("Clockwise = {}".format(clockwise))
                print("Step Type = {}".format(steptype))
                print("Number of steps = {}".format(steps))
                print("Step Delay = {}".format(stepdelay))
                print("Intial delay = {}".format(initdelay))
                print("Size of turn in degrees = {}"
                      .format(degree_calc(steps, steptype)))
        finally:
            # cleanup
            GPIO.output(self.step_pin, False)
            GPIO.output(self.direction_pin, False)
            if self.mode_pins != False:
                for pin in self.mode_pins:
                    GPIO.output(pin, False)
            self.set_reset(True)
                    
                    
def degree_calc(steps, steptype):
    """ calculate and returns size of turn in degree
    , passed number of steps and steptype"""
    degree_value = {'Full': 1.8,
                    'Half': 0.9,
                    '1/4': .45,
                    '1/8': .225,
                    '1/16': 0.1125,
                    '1/32': 0.05625,
                    '1/64': 0.028125,
                    '1/128': 0.0140625}
    degree_value = (steps*degree_value[steptype])
    return degree_value


"""
--------------------------------------------------------------------------
Threaded Button Driver
--------------------------------------------------------------------------
License:   
Copyright 2023 - Erik Welsh

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Threaded Button Driver

  This driver provides a button that runs in its own execution thread.
  

Software API:

  ThreadedButton(pin, sleep_time=0.1, active_high=True)
    - Provide pin that the button monitors
    - The sleep_time is the time between calls to the callback functions
      while the button is waiting in either the pressed or unpressed state
    - By default, the button is "active_high" (i.e. the button has a 
      pull up resistor between the button and the processor pin and 
      will be connected to ground when the button is pressed.  The 
      input is "High"/"1" when the button is not pressed, and the 
      input is "Low" / "0" when the button is pressed).  If false, 
      the button has the opposite polarity.
    
    start()
      - Starts the button thread
    
    is_pressed()
      - Return a boolean value (i.e. True/False) on if button is pressed
      - Function consumes no time
    
    get_last_press_duration()
      - Return the duration the button was last pressed

    cleanup()
      - Stops the button so thread can exit
      
    Callback Functions:
      These functions will be called at the various times during a button 
      press cycle.  There is also a corresponding function to get the value
      from each of these callback functions in case they return something.
    
      - set_pressed_callback(function)
        - Excuted every "sleep_time" while the button is pressed
      - set_unpressed_callback(function)
        - Excuted every "sleep_time" while the button is unpressed
      - set_on_press_callback(function)
        - Executed once when the button is pressed
      - set_on_release_callback(function)
        - Executed once when the button is released
      
      - get_pressed_callback_value()
      - get_unpressed_callback_value()
      - get_on_pressed_callback_value()
      - get_on_release_callback_value()      

"""
import time
import threading

import Adafruit_BBIO.GPIO as GPIO


# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

HIGH          = GPIO.HIGH
LOW           = GPIO.LOW

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class ThreadedButton(threading.Thread):
    """ Threaded Button Class """
    pin                           = None

    unpressed_value               = None
    pressed_value                 = None

    sleep_time                    = None
    stop_button                   = None
    press_duration                = None

    pressed_callback              = None
    pressed_callback_value        = None
    unpressed_callback            = None
    unpressed_callback_value      = None
    on_press_callback             = None
    on_press_callback_value       = None
    on_release_callback           = None
    on_release_callback_value     = None
    
    def __init__(self, pin=None, sleep_time=0.1, active_high=True):
        """ Initialize variables and set up the button """
        # Call parent class constructor
        threading.Thread.__init__(self)
        
        # Initialize the pin
        if (pin == None):
            raise ValueError("Pin not provided for Button()")
        else:
            self.pin = pin

        # Set pressed vs unpressed values            
        if active_high:
            self.unpressed_value = HIGH
            self.pressed_value   = LOW
        else:
            self.unpressed_value = LOW
            self.pressed_value   = HIGH

        # Initialize Class Variables      
        self.sleep_time      = sleep_time
        self.stop_button     = False
        self.press_duration  = 0.0
        self.button_1_index  = 0
        # All callback functions and values set to None if not used        
        
        # Initialize the hardware components        
        self._setup()
    

    # End def
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize Button
        GPIO.setup(self.pin, GPIO.IN)

    # End def


    def is_pressed(self):
        """ Is the Button pressed?
        
           Returns:  True  - Button is pressed
                     False - Button is not pressed
        """
        return GPIO.input(self.pin) == self.pressed_value

    # End def
    
    #def button_1_functions(self):
        #button_functions = [turn(0), turn(100)]
        #current_func = button_functions[self.button_1_index]
        #self.button_1_index = (self.button_1_index + 1) % len(button_functions)
        #current_func()
    # End def
    #^old format, did not work because both functions would get called at once each time. Servo driver section has working version
    
    def bat1(self):
        #this will be where i put the stepper motor movement sequence for the first scene
        print("schmeep schmoop")
        stepper_1 = A4988Nema('P2_4', 'P2_2', "P2_10", (-1,-1,-1), motor_type="A4988")
        stepper_2 = A4988Nema('P2_6', 'P2_8', "P2_18", (-1,-1,-1), motor_type="A4988")

        stepper_1.motor_go(clockwise=False, steptype="Full",
                 steps=30, stepdelay=.005, verbose=True, initdelay=.05)
        stepper_1.motor_go(clockwise=True, steptype="Full",
                 steps=30, stepdelay=.005, verbose=True, initdelay=.05)
        #stepper_2.motor_go(clockwise=True, steptype="Full",
                 #steps=70, stepdelay=.005, verbose=True, initdelay=.05)
        time.sleep(0.5)
    #end def
    
    def bat2(self):
        #second scene
        print("bat 2 functions")
        stepper_1 = A4988Nema('P2_4', 'P2_2', "P2_10", (-1,-1,-1), motor_type="A4988")
        stepper_2 = A4988Nema('P2_6', 'P2_8', "P2_18", (-1,-1,-1), motor_type="A4988")
        
        #stepper_1.motor_go(clockwise=False, steptype="Full",
                 #steps=20, stepdelay=.005, verbose=True, initdelay=.05)
        stepper_2.motor_go(clockwise=True, steptype="Full",
                 steps=40, stepdelay=.005, verbose=True, initdelay=.05)
        stepper_2.motor_go(clockwise=False, steptype="Full",
                 steps=40, stepdelay=.005, verbose=True, initdelay=.05)
        time.sleep(0.5)
    #end def
    
    def sound(self):
        os.system("mplayer batsound.mp3")
        time.sleep(1)
        
    #def unsound(self):
        #os.system()
        

    def run(self):
        """ Run the button thread.  Execute callbacks as appropriate. """
        function_return_value = None
        button_press_time     = None

        # Run button monitor until told to stop        
        while(not self.stop_button): 
        
            # Wait for button press
            #   Execute the unpressed callback function based on the sleep time
            while(GPIO.input(self.pin) == self.unpressed_value):  
            
                if self.unpressed_callback is not None:
                    self.unpressed_callback_value = self.unpressed_callback()
                
                if self.stop_button:
                    break
                
                time.sleep(self.sleep_time)
            
            # Record time
            button_press_time = time.time()
            
            # Executed the on press callback function
            if self.on_press_callback is not None:
                self.on_press_callback_value = self.on_press_callback()
            
            # Wait for button release
            #   Execute the pressed callback function based on the sleep time
            while(False):  # !!! FIX !!!
            
                if self.pressed_callback is not None:
                    self.pressed_callback_value = self.pressed_callback()
                    
                if self.stop_button:
                    break
                    
                time.sleep(self.sleep_time)
            
            # Record the press duration
            self.press_duration = time.time() - button_press_time

            # Executed the on release callback function
            if self.on_release_callback is not None:
                self.on_release_callback_value = self.on_release_callback()        
        
        # Set the flag and press duration to allow the button thread to restart
        self.stop_button    = False
        self.press_duration = 0.0
        
        #^going back to initial state
        
    # End def

    
    def get_last_press_duration(self):
        """ Return the last press duration """
        return self.press_duration
    
    # End def
    
    
    def cleanup(self):
        """ Clean up the button hardware. """
        # Nothing to do for GPIO; stop the thread and wait for completion
        
        self.stop_button = True
        #^to stop
        
        while (self.stop_button):
            time.sleep(self.sleep_time)
    
    # End def
    
    
    # -----------------------------------------------------
    # Callback Functions
    # -----------------------------------------------------

    def set_pressed_callback(self, function):
        """ Function excuted every "sleep_time" while the button is pressed """
        self.pressed_callback = function
    
    # End def

    def get_pressed_callback_value(self):
        """ Return value from pressed_callback function """
        return self.pressed_callback_value
    
    # End def
    
    def set_unpressed_callback(self, function):
        """ Function excuted every "sleep_time" while the button is unpressed """
        self.unpressed_callback = function
    
    # End def

    def get_unpressed_callback_value(self):
        """ Return value from unpressed_callback function """
        return self.unpressed_callback_value
    
    # End def

    def set_on_press_callback(self, function):
        """ Function excuted once when the button is pressed """
        self.on_press_callback = function
    
    # End def

    def get_on_press_callback_value(self):
        """ Return value from on_press_callback function """
        return self.on_press_callback_value
    
    # End def

    def set_on_release_callback(self, function):
        """ Function excuted once when the button is released """
        self.on_release_callback = function
    
    # End def

    def get_on_release_callback_value(self):
        """ Return value from on_release_callback function """
        return self.on_release_callback_value
    
    # End def    
    
# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    """ This test requires the use of two LEDs as well as two buttons.
    
    In this test there are two threaded buttons running in parallel.  Each
    button controls an LED.  When the button is pressed, the corresponding 
    LED will turn on and when the button is released, the LED will turn off.
    """
    import sys

    # Update path to correct directory for LED class     
    sys.path.append("/var/lib/cloud9/ENGI-301/python/servo")
    
    print("Threaded Button Test")

    # Create instantiation of the buttons and LEDs
    button_1 = ThreadedButton("P1_2")
    button_2 = ThreadedButton("P1_4")
    button_3 = ThreadedButton("P1_6")
    button_4 = ThreadedButton("P1_8")
    button_5 = ThreadedButton("P1_10")
    button_6 = ThreadedButton("P1_12")
    try:
        # Set up the Servos
        import servo as SERVO
        import os
        
        #servo_1    = SERVO.SERVO("P1_36", 100)
        #servo_2    = SERVO.SERVO("P1_33", 100)
        #servo_3    = SERVO.SERVO("P2_1", 100)
        servo_1 = Servo("P1_36", 0)
        servo_2 = Servo("P1_33", 0)
        servo_3 = Servo("P2_1", 0)

        # Set up the button callbacks
        #button_0.set_on_press_callback(led_0.on)
        #button_0.set_on_release_callback(led_0.off)
        #button_2.set_on_press_callback(os.system("mplayer Dustin.mp3"))
        button_1.set_on_press_callback(servo_1.button_1_functions)
        button_2.set_on_press_callback(servo_2.button_1_functions)
        button_3.set_on_press_callback(servo_3.button_1_functions)
        button_4.set_on_press_callback(button_4.bat1)
        button_5.set_on_press_callback(button_5.bat2)
        button_6.set_on_press_callback(button_6.sound)
        
        
    except:
        pass
    
    # Start the buttons
    button_1.start()
    button_2.start()
    button_3.start()
    button_4.start()
    button_5.start()
    button_6.start()
    
    # Get the main thread
    main_thread = threading.currentThread()
    
    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    try:
        while (True):
            # Do nothing in the main thread
            time.sleep(1)
        
    except KeyboardInterrupt:
        # Clean up the hardware
        button_1.cleanup()
        button_2.cleanup()
        button_3.cleanup()
        button_4.cleanup()
        button_5.cleanup()
        #button_6.cleanup()

        try:
            servo_1.cleanup()
            servo_2.cleanup()
            servo_3.cleanup()
        except:
            pass

    # Wait for threads to complete        
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    print("Test Complete")


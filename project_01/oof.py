"""
--------------------------------------------------------------------------
This whole thing was my attempt at making the servo turn with a button press
Servo Driver
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
SG90_MIN_DUTY           = 3                   # 1ms pulse (5% duty cycle)  -- Fully clockwise (right)
SG90_MAX_DUTY           = 10                  # 2ms pulse (10% duty cycle) -- Fully anti-clockwise (left)

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
    
    def __init__(self, pin=None, default_position=0):
        """ Initialize variables and set up the Servo """
        if (pin == None):
            raise ValueError("Pin not provided for Servo()")
        else:
            self.pin = pin

        self.position = default_position
        
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
        
        # Set PWM duty cycle based on position
        #duty_cycle = ((SG90_MAX_DUTY - SG90_MIN_DUTY) * (position / 100)) + SG90_MIN_DUTY
        
        PWM.set_duty_cycle(self.pin, self._duty_cycle_from_position(position))
        #print("Turning servo to position {0} using duty cycle {1}".format(position, duty_cycle))
        # !!! NEED TO IMPLEMENT !!! #

    # End def


    def cleanup(self):
        """Cleanup the hardware components."""
        # Stop servo
        PWM.stop(self.pin)
        PWM.cleanup()
        
    # End def

# End class


#------------
"""
--------------------------------------------------------------------------
Button Driver
--------------------------------------------------------------------------
License:   
Copyright 2021-2023 - Erik Welsh

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

Button Driver

  This driver is built for buttons that have a pull up resistor between the
button and the processor pin (i.e. the input is "High"/"1" when the button is
not pressed) and will be connected to ground when the button is pressed (i.e. 
the input is "Low" / "0" when the button is pressed)

Software API:

  Button(pin)
    - Provide pin that the button monitors
    
    is_pressed()
      - Return a boolean value (i.e. True/False) on if button is pressed
      - Function consumes no time
    
    wait_for_press(function=None)
      - Wait for the button to be pressed 
      - Optionally takes in an argument "function" which is the function 
        to be executed when waiting for the button to be pressed
      - Function consumes time
      - Returns a tuple:  
        (<time button was pressed>, <data returned by the "function" argument>)

"""
import time

import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Button():
    """ Button Class """
    pin             = None
    unpressed_value = None
    pressed_value   = None
    sleep_time      = None
    
    #reset_time = None
    
    def __init__(self, pin=None):
        """ Initialize variables and set up the button """
        if (pin == None):
            raise ValueError("Pin not provided for Button()")
        else:
            self.pin = pin
        
        # By default the unpressed_value is "1" and the pressed
        # value is "0".  This is done to make it easier to change
        # in the future
        #self.reset_time = reset_time
        self.unpressed_value = 1
        self.pressed_value   = 0
        
        # By default sleep time is "0.1" seconds
        self.sleep_time      = 0.1

        # Initialize the hardware components        
        self._setup()
       # button = Button("P1_2")
    
    # End def
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize Button
        # HW#4 TODO: (one line of code)
        #   Remove "pass" and use the Adafruit_BBIO.GPIO library to set up the button
        GPIO.setup(self.pin, GPIO.IN)
        #sets up pin (connected to button) as an input based on user input
    # End def


    def is_pressed(self):
        """ Is the Button pressed?
        
           Returns:  True  - Button is pressed
                     False - Button is not pressed
        """
        # HW#4 TODO: (one line of code)
        #   Remove "pass" and return the comparison of input value of the GPIO pin of 
        #   the buton (i.e. self.pin) to the "pressed value" of the class 
        return GPIO.input(self.pin) == self.pressed_value

    # End def


    def wait_for_press(self, function=None):
        """ Wait for the button to be pressed.  This function will 
           wait for the button to be pressed and released so there
           are no race conditions.
        
           Arguments:
               function - Optional argument that is the functon to 
                          executed while waiting for the button to 
                          be pressed
        
           Returns:
               tuple - [0] Time button was pressed
                     - [1] Data returned by the "function" argument
        """
        function_return_value = None
        button_press_time     = None
        
        # Execute function if it is not None
        #   - This covers the case that the button is pressed prior 
        #     to entering this function
        if function is not None:
            function_return_value = function()
        
        # Wait for button press
        #   If the function is not None, execute the function
        #   Sleep for a short amount of time to reduce the CPU load
        #
        # HW#4 TODO: (one line of code)
        #   Update while loop condition to compare the input value of the  
        #   GPIO pin of the buton (i.e. self.pin) to the "unpressed value" 
        #   of the class (i.e. we are executing the while loop while the 
        #   button is not being pressed)
        while(GPIO.input(self.pin) == self.unpressed_value): 
        
            if function is not None:
                function_return_value = function()
                
            time.sleep(self.sleep_time)
        
        # Record time
        button_press_time = time.time()
        
        # Wait for button release
        #   Sleep for a short amount of time to reduce the CPU load
        #
        # HW#4 TODO: (one line of code)
        #   Update while loop condition to compare the input value of the  
        #   GPIO pin of the buton (i.e. self.pin) to the "pressed value" 
        #   of the class (i.e. we are executing the while loop while the 
        #   button is being pressed)
        while(GPIO.input(self.pin) == self.pressed_value):
            time.sleep(self.sleep_time)
        
        # Compute the button_press_time
        button_press_time = time.time() - button_press_time

        # Return a tuple:  (button press time, function return value)        
        return (button_press_time, function_return_value)
        
    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time
    
    print("Servo Test")

    # Create instantiation of the servo + button such that servo is initially in the default state
    servo_1 = Servo("P1_36", 100)
    button_1 = Button("P1_2")
    #servo_2 = Servo("P1_33", 100)
    button_2 = Button("P1_4")

    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    import os
    #Program waits for button press, and switches state at each button press
    while(True):
        button_1.wait_for_press()
        servo_1.turn(0)
        button_1.wait_for_press()
        servo_1.turn(100)
        #button_2.wait_for_press()
        #os.system("mplayer Dustin.mp3")
        #button_2.wait_for_press()
        #servo_2.turn(100)
    #***Because of this structure, it will need to be changed to a threaded button

    # Clean up hardware when exiting
    servo.cleanup()

    print("Test Complete")
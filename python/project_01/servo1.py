"""
--------------------------------------------------------------------------
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

import Adafruit_BBIO.GPIO as GPIO
import time

import servo         as SERVO
import button        as BUTTON

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

SG90_FREQ               = 100                  # 20ms period (50Hz) ==> I changed it to 100 from 50
SG90_POL                = 0                   # Rising Edge polarity
SG90_MIN_DUTY           = 5                   # 1ms pulse (5% duty cycle)  -- Fully clockwise (right)
SG90_MAX_DUTY           = 25                  # 2ms pulse (10% duty cycle ==> when changed to 25--> approx 180 range of motion) -- Fully anti-clockwise (left)

SERVO_LOCK         = 100     # Fully anti-clockwise
SERVO_UNLOCK       = 0       # Fully clockwise

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Servo1():
    """ Servo1 """
    pin       = None
    position  = None
    servo     = None
    button    = None
    
    def __init__(self, default_position=0, servo="P1_36", button="P2_2"):
        """ Initialize variables and set up the Servo """
        '''
        if (pin == None):
            raise ValueError("Pin not provided for Servo()")
        else:
            self.pin = pin
            
        '''

        self.position = default_position
        
        self._setup(default_position)
        self.servo          = SERVO.Servo(servo, default_position=SERVO_LOCK)
        self.button         = BUTTON.Button(button)
    
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



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time
    
    print("Servo Test")

    # Create instantiation of the servo
    servo = Servo1("P1_36", 100)

    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    print("Use Ctrl-C to Exit")
    
    try:
        #while(1)
        if (button_press_time < self.reset_time):
            if (position == default_position):
                servo.turn(100)
                print("Current position = {0}%".format(servo.get_position()))
                time.sleep(1)
            
            else:
                 # Turn Servo anti-clockwise
                servo.turn(0)
                print("Current position = {0}%".format(servo.get_position()))
                time.sleep(1)

        
    except KeyboardInterrupt:
        pass

    # Clean up hardware when exiting
    servo.cleanup()

    print("Test Complete")


"""
--------------------------------------------------------------------------
Puppet Animator
--------------------------------------------------------------------------
License:   
Copyright 2023 - Lily Scholnik

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

Use the following hardware components to control the puppet production:  
  - 9 buttons
  - 3 servos
  - 2 stepper motors
  - Stepper shields
  - USB speaker
  
  
Requirements:
  - Hardware:
    - At boot, servos are in the "default" position, speaker is "off", steppers are "off"
    - Active positions/states of each individual component is initiated by button press
    - Button press for servos will switch their position (ex: button press while in default causes servo to turn to active, and vice versa)
    
User interaction:
    - Single button press for servo buttons will switch position modes
    - Single button press for each servo motion sequence, will return to default/off at end
    - Single button for the two sound effects, quick press for 1, press and hold for 2



Pupper Animator

  This program is built to control puppets in three different ways: servo 
control of individual parts, stepper control of entire puppets, and sound effect
with a USB speaker. 

Constituent drivers include:
A button driver built for buttons that have a pull up resistor between the
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
Uses:
  - Libraries developed in class


"""
import time

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

import button        as BUTTON
import servo         as SERVO


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

class Project():
    """ Project """
    #reset_time     = None
    button         = None
    servo          = None
    music          = None
    debug          = None
    #this is not complete, bear with me
    
    
    def __init__(self, button="P2_2",
                       potentiometer="P1_19", servo="P1_36"):
                           
        """ Initialize variables and set up the button """
       #based on combo_lock.py
        self.button         = BUTTON.Button(button)
        self.servo          = SERVO.Servo(servo, default_position=SERVO_LOCK)
        
        self._setup()
        
        #need to trim out irrelevant components+pins
    
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

    print("Button Test")

    # Create instantiation of the button
    button = Button("P2_2")
    
    # Create an function to test the wait_for_press function
    def print_time():
        ret_val = time.time()
        print("    Print Time = {0}".format(ret_val))
        return ret_val
    # End def

    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    try:
        # Check if the button is pressed
        print("Is the button pressed?")
        print("    {0}".format(button.is_pressed()))

        print("Press and hold the button.")
        time.sleep(4)
        
        # Check if the button is pressed
        print("Is the button pressed?")
        print("    {0}".format(button.is_pressed()))
        
        print("Release the button.")
        time.sleep(4)
        
        print("Waiting for button press ...")
        value = button.wait_for_press()
        print("    Button pressed for {0} seconds. ".format(value[0]))
        print("    Function return value = {0}".format(value[1]))
        
        print("Waiting for button press with optional argument ...")
        value = button.wait_for_press(print_time)
        print("    Button pressed for {0} seconds. ".format(value[0]))
        print("    Function return value = {0}".format(value[1]))
        
    except KeyboardInterrupt:
        pass

    print("Test Complete")


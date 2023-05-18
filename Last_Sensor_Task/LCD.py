import RPi.GPIO as GPIO
import time

#commands
LCD_CLEAR = 0x01
LCD_RETURN_HOME  =  0x02
LCD_ENTERY_MODE_DEC_SHIFT_OFF = 0x04
LCD_ENTERY_MODE_DEC_SHIFT_ON =  0x05
LCD_ENTERY_MODE_INC_SHIFT_OFF  = 0x06
LCD_ENTERY_MODE_INC_SHIFT_ON = 0x07
LCD_CURSOR_MOVE_SHIFT_LEFT =  0x10
LCD_CURSOR_MOVE_SHIFT_RIGHT = 0x14
LCD_DISPLAY_SHIFT_LEFT = 0x18
LCD_DISPLAY_SHIFT_RIGHT = 0x1C
LCD_DISPLAY_ON_UNDERLINE_OFF_CURSOR_OFF = 0x0C
LCD_DISPLAY_ON_UNDERLINE_OFF_CURSOR_ON =  0x0D
LCD_DISPLAY_ON_UNDERLINE_ON_CURSOR_OFF = 0x0E
LCD_DISPLAY_ON_UNDERLINE_ON_CURSOR_ON = 0x0F
LCD_DISPLAY_OFF_CURSOR_OFF = 0x08
LCD_8BIT_MODE_2_LINE  =  0x38
LCD_4BIT_MODE_2_LINE = 0x28
LCD_BEGIN_AT_FIRST_RAW =  0x80
LCD_BEGIN_AT_SECOND_RAW = 0xC0

class LCD:
    def __init__(self, rs, en, d4, d5, d6, d7):
        self.rs = rs
        self.en = en
        self.data_pins = [d4, d5, d6, d7]
        self.initialize()

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        for pin in self.data_pins:
            GPIO.setup(pin, GPIO.OUT)
        
        self.send_command(0x33)  # Initialize
        self.send_command(0x32)  # Set to 4-bit mode
        self.send_command(LCD_4BIT_MODE_2_LINE)  # 2 lines, 5x8 font
        self.send_command(LCD_DISPLAY_ON_UNDERLINE_OFF_CURSOR_OFF)  # Turn on display

    def send_command(self, command):
        GPIO.output(self.rs, GPIO.LOW)
        self._send_data(command >> 4)
        self._send_data(command & 0x0F)

    def send_data(self, data):
        GPIO.output(self.rs, GPIO.HIGH)
        self._send_data(data >> 4)
        self._send_data(data & 0x0F)

    def _send_data(self, data):
        for i, pin in enumerate(self.data_pins):
            GPIO.output(pin, (data >> i) & 0x01)
        
        self._toggle_enable()

    def _toggle_enable(self):
        GPIO.output(self.en, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.en, GPIO.LOW)
        time.sleep(0.001)

    def clear(self):
        self.send_command(LCD_CLEAR)  # Clear display
        time.sleep(0.001)

    def write_line(self, line, text):
        line_offsets = [LCD_BEGIN_AT_FIRST_RAW, LCD_BEGIN_AT_SECOND_RAW]  # Line 1 starts at 0x80, Line 2 starts at 0xC0
        self.send_command(line_offsets[line])
        for char in text:
            self.send_data(ord(char))

    def cleanup(self):
        GPIO.cleanup()

# Example usage:


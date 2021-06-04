# NOTE - It is a known issue that the keyboard-related functions don't work on Ubuntu VMs in Virtualbox.

import pyautogui
import sys
import os
from pyautogui import LEFT, MIDDLE, RIGHT

from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK

BUTTON_NAME_MAPPING = {LEFT: 1, MIDDLE: 2, RIGHT: 3, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}


if sys.platform in ('java', 'darwin', 'win32'):
    raise Exception('The pyautogui_x11 module should only be loaded on a Unix system that supports X11.')

#from pyautogui import *

"""
Much of this code is based on information gleaned from Paul Barton's PyKeyboard in PyUserInput from 2013, itself derived from Akkana Peck's pykey in 2008 ( http://www.shallowsky.com/software/crikey/pykey-0.1 ), itself derived from her "Crikey" lib.
"""

class PyAutoGuiDriver(object):
    def __init__(self, display):
        self._display = Display(display)
        self.setup_keyboard_mapping()

    def setup_keyboard_mapping(self):
        self.keyboardMapping = dict([(key, None) for key in pyautogui.KEY_NAMES])
        self.keyboardMapping.update({
            'backspace':         self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('BackSpace')),
            '\b':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('BackSpace')),
            'tab':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Tab')),
            'enter':             self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
            'return':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
            'shift':             self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_L')),
            'ctrl':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_L')),
            'alt':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_L')),
            'pause':             self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Pause')),
            'capslock':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Caps_Lock')),
            'esc':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
            'escape':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
            'pgup':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Up')),
            'pgdn':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Down')),
            'pageup':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Up')),
            'pagedown':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Down')),
            'end':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('End')),
            'home':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Home')),
            'left':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Left')),
            'up':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Up')),
            'right':             self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Right')),
            'down':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Down')),
            'select':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Select')),
            'print':             self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
            'execute':           self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Execute')),
            'prtsc':             self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
            'prtscr':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
            'prntscrn':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
            'printscreen':       self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
            'insert':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Insert')),
            'del':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Delete')),
            'delete':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Delete')),
            'help':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Help')),
            'win':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_L')),
            'winleft':           self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_L')),
            'winright':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_R')),
            'apps':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Menu')),
            'num0':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_0')),
            'num1':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_1')),
            'num2':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_2')),
            'num3':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_3')),
            'num4':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_4')),
            'num5':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_5')),
            'num6':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_6')),
            'num7':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_7')),
            'num8':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_8')),
            'num9':              self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_9')),
            'multiply':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Multiply')),
            'add':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Add')),
            'separator':         self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Separator')),
            'subtract':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Subtract')),
            'decimal':           self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Decimal')),
            'divide':            self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Divide')),
            'f1':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F1')),
            'f2':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F2')),
            'f3':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F3')),
            'f4':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F4')),
            'f5':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F5')),
            'f6':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F6')),
            'f7':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F7')),
            'f8':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F8')),
            'f9':                self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F9')),
            'f10':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F10')),
            'f11':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F11')),
            'f12':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F12')),
            'f13':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F13')),
            'f14':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F14')),
            'f15':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F15')),
            'f16':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F16')),
            'f17':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F17')),
            'f18':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F18')),
            'f19':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F19')),
            'f20':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F20')),
            'f21':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F21')),
            'f22':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F22')),
            'f23':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F23')),
            'f24':               self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('F24')),
            'numlock':           self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Num_Lock')),
            'scrolllock':        self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Scroll_Lock')),
            'shiftleft':         self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_L')),
            'shiftright':        self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_R')),
            'ctrlleft':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_L')),
            'ctrlright':         self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_R')),
            'altleft':           self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_L')),
            'altright':          self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_R')),
            # These are added because unlike a-zA-Z0-9, the single characters do not have a
            ' ': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('space')),
            'space': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('space')),
            '\t': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Tab')),
            '\n': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),  # for some reason this needs to be cr, not lf
            '\r': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
            '\e': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
            '!': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('exclam')),
            '#': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('numbersign')),
            '%': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('percent')),
            '$': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('dollar')),
            '&': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('ampersand')),
            '"': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('quotedbl')),
            "'": self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('apostrophe')),
            '(': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('parenleft')),
            ')': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('parenright')),
            '*': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('asterisk')),
            '=': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('equal')),
            '+': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('plus')),
            ',': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('comma')),
            '-': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('minus')),
            '.': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('period')),
            '/': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('slash')),
            ':': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('colon')),
            ';': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('semicolon')),
            '<': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('less')),
            '>': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('greater')),
            '?': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('question')),
            '@': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('at')),
            '[': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('bracketleft')),
            ']': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('bracketright')),
            '\\': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('backslash')),
            '^': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('asciicircum')),
            '_': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('underscore')),
            '`': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('grave')),
            '{': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('braceleft')),
            '|': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('bar')),
            '}': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('braceright')),
            '~': self._display.keysym_to_keycode(Xlib.XK.string_to_keysym('asciitilde')),
        })

        # Trading memory for time" populate winKB so we don't have to call VkKeyScanA each time.
        for c in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890""":
            self.keyboardMapping[c] = self._display.keysym_to_keycode(Xlib.XK.string_to_keysym(c))

    def _position(self):
        """Returns the current xy coordinates of the mouse cursor as a two-integer
        tuple.

        Returns:
          (x, y) tuple of the current xy coordinates of the mouse cursor.
        """
        coord = self._display.screen().root.query_pointer()._data
        return coord["root_x"], coord["root_y"]


    def _size(self):
        return self._display.screen().width_in_pixels, self._display.screen().height_in_pixels

    def _vscroll(self, clicks, x=None, y=None):
        clicks = int(clicks)
        if clicks == 0:
            return
        elif clicks > 0:
            button = 4 # scroll up
        else:
            button = 5 # scroll down

        for i in range(abs(clicks)):
            self._click(x, y, button=button)


    def _hscroll(self, clicks, x=None, y=None):
        clicks = int(clicks)
        if clicks == 0:
            return
        elif clicks > 0:
            button = 7 # scroll right
        else:
            button = 6 # scroll left

        for i in range(abs(clicks)):
            self._click(x, y, button=button)


    def _scroll(self, clicks, x=None, y=None):
        return self._vscroll(clicks, x, y)


    def _click(self, x, y, button):
        assert button in BUTTON_NAME_MAPPING.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = BUTTON_NAME_MAPPING[button]

        self._mouseDown(x, y, button)
        self._mouseUp(x, y, button)


    def _moveTo(self, x, y):
        fake_input(self._display, X.MotionNotify, x=x, y=y)
        self._display.sync()


    def _mouseDown(self, x, y, button):
        self._moveTo(x, y)
        assert button in BUTTON_NAME_MAPPING.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = BUTTON_NAME_MAPPING[button]
        fake_input(self._display, X.ButtonPress, button)
        self._display.sync()


    def _mouseUp(self, x, y, button):
        self._moveTo(x, y)
        assert button in BUTTON_NAME_MAPPING.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = BUTTON_NAME_MAPPING[button]
        fake_input(self._display, X.ButtonRelease, button)
        self._display.sync()


    def _keyDown(self, key):
        """Performs a keyboard key press without the release. This will put that
        key in a held down state.

        NOTE: For some reason, this does not seem to cause key repeats like would
        happen if a keyboard key was held down on a text field.

        Args:
          key (str): The key to be pressed down. The valid names are listed in
          pyautogui.KEY_NAMES.

        Returns:
          None
        """
        if key not in self.keyboardMapping or self.keyboardMapping[key] is None:
            return

        if type(key) == int:
            fake_input(self._display, X.KeyPress, key)
            self._display.sync()
            return

        needsShift = pyautogui.isShiftCharacter(key)
        if needsShift:
            fake_input(self._display, X.KeyPress, self.keyboardMapping['shift'])

        fake_input(self._display, X.KeyPress, self.keyboardMapping[key])

        if needsShift:
            fake_input(self._display, X.KeyRelease, self.keyboardMapping['shift'])
        self._display.sync()


    def _keyUp(self, key):
        """Performs a keyboard key release (without the press down beforehand).

        Args:
          key (str): The key to be released up. The valid names are listed in
          pyautogui.KEY_NAMES.

        Returns:
          None
        """

        """
        Release a given character key. Also works with character keycodes as
        integers, but not keysyms.
        """
        if key not in self.keyboardMapping or self.keyboardMapping[key] is None:
            return

        if type(key) == int:
            keycode = key
        else:
            keycode = self.keyboardMapping[key]

        fake_input(self._display, X.KeyRelease, keycode)
        self._display.sync()


# Taken from PyKeyboard's ctor function.



""" Information for keyboardMapping derived from PyKeyboard's special_key_assignment() function.

The *KB dictionaries in pyautogui map a string that can be passed to keyDown(),
keyUp(), or press() into the code used for the OS-specific keyboard function.

They should always be lowercase, and the same keys should be used across all OSes."""


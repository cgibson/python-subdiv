# -*- coding: utf-8 -*-
##############################################################################
#  GLFW - An OpenGL framework
#  API version: 2.7
#  WWW:         http://www.glfw.org/
#  ---------------------------------------------------------------------------
#  Copyright (c) 2002-2006 Marcus Geelnard
#  Copyright (c) 2006-2010 Camilla Berglund
#
#  Python bindings - Copyright (c) 2011 Nicolas P. Rougier
#  
#  This software is provided 'as-is', without any express or implied
#  warranty. In no event will the authors be held liable for any damages
#  arising from the use of this software.
#  
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#  
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would
#     be appreciated but is not required.
#  
#  2. Altered source versions must be plainly marked as such, and must not
#     be misrepresented as being the original software.
#  
#  3. This notice may not be removed or altered from any source
#     distribution.
#  
#  A few minor modifications to this source have been made by Richard Petri
#
#  - Removed a few unneccessary imports.
#  - Cleaned up the namespace, so that an "from glfw import *"
#    won't wreck too many things. I left the * import for GL since it
#    adds a familiar C-ish feeling to GL programming in python.
#  - Posibility to provide the a specific dynamic library of GLFW via
#    the Environment Variable GLFW_LIBRARY.
#  
##############################################################################
import os
import ctypes
import ctypes.util
from OpenGL.GL import *

glfwlibraryfile = None
if 'GLFW_LIBRARY' in os.environ:
    if os.path.exists(os.environ['GLFW_LIBRARY']):
        glfwlibraryfile = os.path.realpath(os.environ['GLFW_LIBRARY'])
if glfwlibraryfile == None:
    glfwlibraryfile = ctypes.util.find_library('glfw')
if glfwlibraryfile == None:
    raise RuntimeError, 'GLFW library not found'
__glfwdll__ = ctypes.CDLL(glfwlibraryfile)

del glfwlibraryfile

#glfwlibraryfile = ctypes.util.find_library('c')
#libc    = ctypes.CDLL(glfwlibraryfile)
#wctomb  = libc.wctomb
#isgraph = libc.isgraph

__callbacks__ = {'window_size'    : 0,
                 'window_close'   : 0,
                 'window_refresh' : 0,
                 'key'            : 0,
                 'char'           : 0,
                 'mouse_button'   : 0,
                 'mouse_pos'      : 0,
                 'mouse_wheel'    : 0}


##########################################################################
# GLFW version
##########################################################################
GLFW_VERSION_MAJOR    = 2
GLFW_VERSION_MINOR    = 7
GLFW_VERSION_REVISION = 6


##########################################################################
# Input handling definitions
##########################################################################
# Key and button state/action definitions
GLFW_RELEASE            = 0
GLFW_PRESS              = 1

# Keyboard key definitions: 8-bit ISO-8859-1 (Latin 1) encoding is used
# for printable keys (such as A-Z, 0-9 etc), and values above 256
# represent special (non-printable) keys (e.g. F1, Page Up etc).
#
GLFW_KEY_UNKNOWN      = -1
GLFW_KEY_SPACE        = 32
GLFW_KEY_SPECIAL      = 256
GLFW_KEY_ESC          = (GLFW_KEY_SPECIAL+1)
GLFW_KEY_F1           = (GLFW_KEY_SPECIAL+2)
GLFW_KEY_F2           = (GLFW_KEY_SPECIAL+3)
GLFW_KEY_F3           = (GLFW_KEY_SPECIAL+4)
GLFW_KEY_F4           = (GLFW_KEY_SPECIAL+5)
GLFW_KEY_F5           = (GLFW_KEY_SPECIAL+6)
GLFW_KEY_F6           = (GLFW_KEY_SPECIAL+7)
GLFW_KEY_F7           = (GLFW_KEY_SPECIAL+8)
GLFW_KEY_F8           = (GLFW_KEY_SPECIAL+9)
GLFW_KEY_F9           = (GLFW_KEY_SPECIAL+10)
GLFW_KEY_F10          = (GLFW_KEY_SPECIAL+11)
GLFW_KEY_F11          = (GLFW_KEY_SPECIAL+12)
GLFW_KEY_F12          = (GLFW_KEY_SPECIAL+13)
GLFW_KEY_F13          = (GLFW_KEY_SPECIAL+14)
GLFW_KEY_F14          = (GLFW_KEY_SPECIAL+15)
GLFW_KEY_F15          = (GLFW_KEY_SPECIAL+16)
GLFW_KEY_F16          = (GLFW_KEY_SPECIAL+17)
GLFW_KEY_F17          = (GLFW_KEY_SPECIAL+18)
GLFW_KEY_F18          = (GLFW_KEY_SPECIAL+19)
GLFW_KEY_F19          = (GLFW_KEY_SPECIAL+20)
GLFW_KEY_F20          = (GLFW_KEY_SPECIAL+21)
GLFW_KEY_F21          = (GLFW_KEY_SPECIAL+22)
GLFW_KEY_F22          = (GLFW_KEY_SPECIAL+23)
GLFW_KEY_F23          = (GLFW_KEY_SPECIAL+24)
GLFW_KEY_F24          = (GLFW_KEY_SPECIAL+25)
GLFW_KEY_F25          = (GLFW_KEY_SPECIAL+26)
GLFW_KEY_UP           = (GLFW_KEY_SPECIAL+27)
GLFW_KEY_DOWN         = (GLFW_KEY_SPECIAL+28)
GLFW_KEY_LEFT         = (GLFW_KEY_SPECIAL+29)
GLFW_KEY_RIGHT        = (GLFW_KEY_SPECIAL+30)
GLFW_KEY_LSHIFT       = (GLFW_KEY_SPECIAL+31)
GLFW_KEY_RSHIFT       = (GLFW_KEY_SPECIAL+32)
GLFW_KEY_LCTRL        = (GLFW_KEY_SPECIAL+33)
GLFW_KEY_RCTRL        = (GLFW_KEY_SPECIAL+34)
GLFW_KEY_LALT         = (GLFW_KEY_SPECIAL+35)
GLFW_KEY_RALT         = (GLFW_KEY_SPECIAL+36)
GLFW_KEY_TAB          = (GLFW_KEY_SPECIAL+37)
GLFW_KEY_ENTER        = (GLFW_KEY_SPECIAL+38)
GLFW_KEY_BACKSPACE    = (GLFW_KEY_SPECIAL+39)
GLFW_KEY_INSERT       = (GLFW_KEY_SPECIAL+40)
GLFW_KEY_DEL          = (GLFW_KEY_SPECIAL+41)
GLFW_KEY_PAGEUP       = (GLFW_KEY_SPECIAL+42)
GLFW_KEY_PAGEDOWN     = (GLFW_KEY_SPECIAL+43)
GLFW_KEY_HOME         = (GLFW_KEY_SPECIAL+44)
GLFW_KEY_END          = (GLFW_KEY_SPECIAL+45)
GLFW_KEY_KP_0         = (GLFW_KEY_SPECIAL+46)
GLFW_KEY_KP_1         = (GLFW_KEY_SPECIAL+47)
GLFW_KEY_KP_2         = (GLFW_KEY_SPECIAL+48)
GLFW_KEY_KP_3         = (GLFW_KEY_SPECIAL+49)
GLFW_KEY_KP_4         = (GLFW_KEY_SPECIAL+50)
GLFW_KEY_KP_5         = (GLFW_KEY_SPECIAL+51)
GLFW_KEY_KP_6         = (GLFW_KEY_SPECIAL+52)
GLFW_KEY_KP_7         = (GLFW_KEY_SPECIAL+53)
GLFW_KEY_KP_8         = (GLFW_KEY_SPECIAL+54)
GLFW_KEY_KP_9         = (GLFW_KEY_SPECIAL+55)
GLFW_KEY_KP_DIVIDE    = (GLFW_KEY_SPECIAL+56)
GLFW_KEY_KP_MULTIPLY  = (GLFW_KEY_SPECIAL+57)
GLFW_KEY_KP_SUBTRACT  = (GLFW_KEY_SPECIAL+58)
GLFW_KEY_KP_ADD       = (GLFW_KEY_SPECIAL+59)
GLFW_KEY_KP_DECIMAL   = (GLFW_KEY_SPECIAL+60)
GLFW_KEY_KP_EQUAL     = (GLFW_KEY_SPECIAL+61)
GLFW_KEY_KP_ENTER     = (GLFW_KEY_SPECIAL+62)
GLFW_KEY_KP_NUM_LOCK  = (GLFW_KEY_SPECIAL+63)
GLFW_KEY_CAPS_LOCK    = (GLFW_KEY_SPECIAL+64)
GLFW_KEY_SCROLL_LOCK  = (GLFW_KEY_SPECIAL+65)
GLFW_KEY_PAUSE        = (GLFW_KEY_SPECIAL+66)
GLFW_KEY_LSUPER       = (GLFW_KEY_SPECIAL+67)
GLFW_KEY_RSUPER       = (GLFW_KEY_SPECIAL+68)
GLFW_KEY_MENU         = (GLFW_KEY_SPECIAL+69)
GLFW_KEY_LAST         = GLFW_KEY_MENU

# Mouse button definitions 
GLFW_MOUSE_BUTTON_1      = 0
GLFW_MOUSE_BUTTON_2      = 1
GLFW_MOUSE_BUTTON_3      = 2
GLFW_MOUSE_BUTTON_4      = 3
GLFW_MOUSE_BUTTON_5      = 4
GLFW_MOUSE_BUTTON_6      = 5
GLFW_MOUSE_BUTTON_7      = 6
GLFW_MOUSE_BUTTON_8      = 7
GLFW_MOUSE_BUTTON_LAST   = GLFW_MOUSE_BUTTON_8

# Mouse button aliases
GLFW_MOUSE_BUTTON_LEFT   = GLFW_MOUSE_BUTTON_1
GLFW_MOUSE_BUTTON_RIGHT  = GLFW_MOUSE_BUTTON_2
GLFW_MOUSE_BUTTON_MIDDLE = GLFW_MOUSE_BUTTON_3


GLFW_JOYSTICK_1          = 0
GLFW_JOYSTICK_2          = 1
GLFW_JOYSTICK_3          = 2
GLFW_JOYSTICK_4          = 3
GLFW_JOYSTICK_5          = 4
GLFW_JOYSTICK_6          = 5
GLFW_JOYSTICK_7          = 6
GLFW_JOYSTICK_8          = 7
GLFW_JOYSTICK_9          = 8
GLFW_JOYSTICK_10         = 9
GLFW_JOYSTICK_11         = 10
GLFW_JOYSTICK_12         = 11
GLFW_JOYSTICK_13         = 12
GLFW_JOYSTICK_14         = 13
GLFW_JOYSTICK_15         = 14
GLFW_JOYSTICK_16         = 15
GLFW_JOYSTICK_LAST       = GLFW_JOYSTICK_16

##########################################################################
# Other definitions
##########################################################################

# glfwOpenWindow modes
GLFW_WINDOW               = 0x00010001
GLFW_FULLSCREEN           = 0x00010002

# glfwGetWindowParam tokens
GLFW_OPENED               = 0x00020001
GLFW_ACTIVE               = 0x00020002
GLFW_ICONIFIED            = 0x00020003
GLFW_ACCELERATED          = 0x00020004
GLFW_RED_BITS             = 0x00020005
GLFW_GREEN_BITS           = 0x00020006
GLFW_BLUE_BITS            = 0x00020007
GLFW_ALPHA_BITS           = 0x00020008
GLFW_DEPTH_BITS           = 0x00020009
GLFW_STENCIL_BITS         = 0x0002000A

# The following constants are used for both glfwGetWindowParam
# and glfwOpenWindowHint
#
GLFW_REFRESH_RATE          = 0x0002000B
GLFW_ACCUM_RED_BITS        = 0x0002000C
GLFW_ACCUM_GREEN_BITS      = 0x0002000D
GLFW_ACCUM_BLUE_BITS       = 0x0002000E
GLFW_ACCUM_ALPHA_BITS      = 0x0002000F
GLFW_AUX_BUFFERS           = 0x00020010
GLFW_STEREO                = 0x00020011
GLFW_WINDOW_NO_RESIZE      = 0x00020012
GLFW_FSAA_SAMPLES          = 0x00020013
GLFW_OPENGL_VERSION_MAJOR  = 0x00020014
GLFW_OPENGL_VERSION_MINOR  = 0x00020015
GLFW_OPENGL_FORWARD_COMPAT = 0x00020016
GLFW_OPENGL_DEBUG_CONTEXT  = 0x00020017
GLFW_OPENGL_PROFILE        = 0x00020018

# GLFW_OPENGL_PROFILE tokens
GLFW_OPENGL_CORE_PROFILE   = 0x00050001
GLFW_OPENGL_COMPAT_PROFILE = 0x00050002

# glfwEnable/glfwDisable tokens
GLFW_MOUSE_CURSOR         = 0x00030001
GLFW_STICKY_KEYS          = 0x00030002
GLFW_STICKY_MOUSE_BUTTONS = 0x00030003
GLFW_SYSTEM_KEYS          = 0x00030004
GLFW_KEY_REPEAT           = 0x00030005
GLFW_AUTO_POLL_EVENTS     = 0x00030006

# glfwGetJoystickParam tokens
GLFW_PRESENT              = 0x00050001
GLFW_AXES                 = 0x00050002
GLFW_BUTTONS              = 0x00050003

# Time spans longer than this (seconds) are considered to be infinity
GLFW_INFINITY = 100000.0


##########################################################################
# Typedefs
##########################################################################
class GLFWvidmode(ctypes.Structure): pass
GLFWvidmode._fields_ = [ ('Width',     ctypes.c_int),
                         ('Height',    ctypes.c_int),
                         ('RedBits',   ctypes.c_int),
                         ('BlueBits',  ctypes.c_int),
                         ('GreenBits', ctypes.c_int) ]


# Function pointer types
GLFWwindowsizefun    = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
GLFWwindowclosefun   = ctypes.CFUNCTYPE(ctypes.c_int)
GLFWwindowrefreshfun = ctypes.CFUNCTYPE(None)
GLFWmousebuttonfun   = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
GLFWmouseposfun      = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
GLFWmousewheelfun    = ctypes.CFUNCTYPE(None, ctypes.c_int)
GLFWkeyfun           = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
GLFWcharfun          = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)



###############################################################################
# Prototypes
###############################################################################
# GLFW initialization, termination and version querying
glfwInit                     = __glfwdll__.glfwInit
glfwTerminate                = __glfwdll__.glfwTerminate
# glfwGetVersion               = __glfwdll__.glfwGetVersion

# Window handling
glfwOpenWindow               = __glfwdll__.glfwOpenWindow
glfwOpenWindowHint           = __glfwdll__.glfwOpenWindowHint
glfwCloseWindow              = __glfwdll__.glfwCloseWindow
glfwSetWindowTitle           = __glfwdll__.glfwSetWindowTitle
#glfwGetWindowSize            = __glfwdll__.glfwGetWindowSize
glfwSetWindowSize            = __glfwdll__.glfwSetWindowSize
glfwSetWindowPos             = __glfwdll__.glfwSetWindowPos
glfwIconifyWindow            = __glfwdll__.glfwIconifyWindow
glfwRestoreWindow            = __glfwdll__.glfwRestoreWindow
glfwSwapBuffers              = __glfwdll__.glfwSwapBuffers
glfwSwapInterval             = __glfwdll__.glfwSwapInterval
glfwGetWindowParam           = __glfwdll__.glfwGetWindowParam
#glfwSetWindowSizeCallback    = __glfwdll__.glfwSetWindowSizeCallback


#glfwSetWindowCloseCallback   = __glfwdll__.glfwSetWindowCloseCallback
#glfwSetWindowRefreshCallback = __glfwdll__.glfwSetWindowRefreshCallback

# Video mode functions 
# glfwGetVideoModes            = __glfwdll__.glfwGetVideoModes
# glfwGetDesktopMode           = __glfwdll__.glfwGetDesktopMode

# Input handling
glfwPollEvents               = __glfwdll__.glfwPollEvents
glfwWaitEvents               = __glfwdll__.glfwWaitEvents
glfwGetKey                   = __glfwdll__.glfwGetKey
glfwGetMouseButton           = __glfwdll__.glfwGetMouseButton
glfwGetMousePos              = __glfwdll__.glfwGetMousePos
glfwSetMousePos              = __glfwdll__.glfwSetMousePos
glfwGetMouseWheel            = __glfwdll__.glfwGetMouseWheel
glfwSetMouseWheel            = __glfwdll__.glfwSetMouseWheel
#glfwSetKeyCallback           = __glfwdll__.glfwSetKeyCallback
#glfwSetCharCallback          = __glfwdll__.glfwSetCharCallback
#glfwSetMouseButtonCallback   = __glfwdll__.glfwSetMouseButtonCallback
#glfwSetMousePosCallback      = __glfwdll__.glfwSetMousePosCallback
#glfwSetMouseWheelCallback    = __glfwdll__.glfwSetMouseWheelCallback


# Joystick input
# glfwGetJoystickParam( int joy, int param );
# glfwGetJoystickPos( int joy, float *pos, int numaxes );
# glfwGetJoystickButtons( int joy, unsigned char *buttons, int numbuttons );

# Time
glfwGetTime                  = __glfwdll__.glfwGetTime
glfwSetTime                  = __glfwdll__.glfwSetTime
glfwSleep                    = __glfwdll__.glfwSleep

# Extension support
# glfwExtensionSupported( const char *extension );
# glfwGetProcAddress( const char *procname );
# glfwGetGLVersion( int *major, int *minor, int *rev );

# Enable/disable functions
glfwEnable                  = __glfwdll__.glfwEnable;
glfwDisable                 = __glfwdll__.glfwDisable;


def glfwGetVersion():
    major, minor, rev = ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0)
    __glfwdll__.glfwGetVersion( ctypes.byref(major), ctypes.byref(minor), ctypes.byref(rev) )
    return major.value, minor.value, rev.value

def glfwGetVideoModes( maxcount=16 ):
    c_modes = (GLFWvidmode*maxcount)()
    n = __glfwdll__.glfwGetVideoModes( c_modes, maxcount )
    modes = []
    for i in range(n):
        modes.append( (c_modes[i].Width, c_modes[i].Height,
           c_modes[i].RedBits, c_modes[i].BlueBits, c_modes[i].GreenBits) )
    return modes

def glfwGetDesktopMode():
    mode = GLFWvidmode()
    __glfwdll__.glfwGetDesktopMode( ctypes.byref(mode) )
    return mode.Width, mode.Height, mode.RedBits, mode.BlueBits, mode.GreenBits

def glfwGetWindowSize():
    width, height = ctypes.c_int(0), ctypes.c_int(0)
    __glfwdll__.glfwGetWindowSize( ctypes.byref(width), ctypes.byref(height) )
    return width.value, height.value

def glfwSetWindowSizeCallback( callback ):
    callback = GLFWwindowsizefun( callback ) 
    __callbacks__['window_size'] = callback 
    __glfwdll__.glfwSetWindowSizeCallback( callback )

def glfwSetWindowCloseCallback( callback ):
    callback = GLFWwindowclosefun( callback )
    __callbacks__['window_close'] = callback 
    __glfwdll__.glfwSetWindowCloseCallback( callback )

def glfwSetWindowRefreshCallback( callback ):
    callback = GLFWwindowrefreshfun( callback )
    __callbacks__['window_refresh'] = callback 
    __glfwdll__.glfwSetWindowRefreshCallback( callback )

def glfwSetKeyCallback( callback ):
    callback = GLFWkeyfun( callback )
    __callbacks__['key'] = callback 
    __glfwdll__.glfwSetKeyCallback( callback )

def glfwSetCharCallback( callback ):
    callback = GLFWcharfun( callback )
    __callbacks__['char'] = callback 
    __glfwdll__.glfwSetCharCallback( callback )

def glfwSetMouseButtonCallback( callback ):
    callback = GLFWmousebuttonfun( callback )
    __callbacks__['mouse_button'] = callback 
    __glfwdll__.glfwSetMouseButtonCallback( callback )

def glfwSetMousePosCallback( callback ):
    callback = GLFWmouseposfun( callback )
    __callbacks__['mouse_pos'] = callback 
    __glfwdll__.glfwSetMousePosCallback( callback )

def glfwSetMouseWheelCallback( callback ):
    callback = GLFWmousewheelfun( callback )
    __callbacks__['mouse_wheel'] = callback 
    __glfwdll__.glfwSetMouseWheelCallback( callback )


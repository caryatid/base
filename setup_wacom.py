#!/usr/bin/python

import subprocess

devices = [
'Wacom Bamboo 16FG 4x5 Pen stylus' , 
'Wacom Bamboo 16FG 4x5 Pen stylus' , 
'Wacom Bamboo 16FG 4x5 Finger touch', 
'Wacom Bamboo 16FG 4x5 Finger pad'  
]


# all 
for x in devices:
    subprocess.call(['xsetwacom', 'set', x, 'Rotate', 'ccw'])
    # [subprocess.call(['xsetwacom', 'set', x, 'Button', str(y), str(y)]) for y in range(1,4)]
    # subprocess.call(['xinput', '--list-props', x, 'Wacom Hover Click', '1'])
    # subprocess.call(['xsetwacom', 'set', x, 'TabletPCButton', 'on'])
    # [subprocess.call(['xsetwacom', 'get', x, 'Button', str(y)]) for y in range(1,4)]

# who stole my pen
for x in devices[:2]:
    subprocess.call(['xsetwacom', 'set', x, 'MapToOutput', 'HDMI1'])

# pad
for x in devices[2:]:
    pass

####################
### runs wacom commands 

# xsetwacom set "Wacom Bamboo 16FG 4x5 Pen stylus" MapToOutput HDMI1
# xsetwacom set "Wacom Bamboo 16FG 4x5 Pen stylus" Rotate ccw
# xsetwacom set "Wacom Bamboo 16FG 4x5 Finger touch" Rotate ccw
# xsetwacom set "Wacom Bamboo 16FG 4x5 Finger pad" Rotate ccw


# Wacom Bamboo 16FG 4x5 Pen stylus	id: 12	type: STYLUS    
# Wacom Bamboo 16FG 4x5 Pen eraser	id: 13	type: ERASER    
# Wacom Bamboo 16FG 4x5 Finger touch	id: 14	type: TOUCH     
# Wacom Bamboo 16FG 4x5 Finger pad	id: 15	type: PAD    



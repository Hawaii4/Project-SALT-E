from machine import Pin

light = machine.Pin("LED", machine.Pin.OUT)

light.on()
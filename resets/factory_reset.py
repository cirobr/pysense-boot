'''Run this file to overwrite main.py/boot.py, useful if a device’s filesystem gets corrupted'''
import uos
uos.mkfs('/flash')

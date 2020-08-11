# boot.py -- run on boot-up
import os
import machine
uart = machine.UART(0, 115200)
os.dupterm(uart)

# Heartbeat off (default True)
import pycom
pycom.heartbeat(False)

# Watchdog setup
watch_dog_timer_sec = 60   # 60 seconds == 1 min
watch_dog_timer_ms = int(watch_dog_timer_sec * 1000)
from machine import WDT
wdt = WDT(timeout=watch_dog_timer_ms)

# By default WLAN boots in WLAN.AP. If application uses WLAN in STATION mode, then program WLAN.STA on Boot.py.
from network import WLAN
wlan = WLAN(mode=WLAN.STA)

# Scan known WLANs and connect. Known WLAN list stored on "wifi_known_nets.py".
import wifi
wifi.connection_check(10,5)

# Sync RTC after network connection. Recommended Servers: "pool.ntp.org", "a.st1.ntp.br"
from clock import sync_rtc
sync_rtc("a.st1.ntp.br")

# Network connection established. Reset watchdog and continues.
wdt.feed()

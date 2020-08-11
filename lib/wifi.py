import os
import machine
uart = machine.UART(0, 115200)
os.dupterm(uart)

from network import WLAN
wlan = WLAN()


def connect_ssid():
    wlan.mode(WLAN.STA)
    import wifi_known_nets
    known_nets = wifi_known_nets.ssid_list()

    if machine.reset_cause() != machine.SOFT_RESET:
        print("Scanning for known wifi networks...")
        available_nets = wlan.scan()
        nets = frozenset([e.ssid for e in available_nets])

        known_nets_names = frozenset([key for key in known_nets])
        net_to_use = list(nets & known_nets_names)
        try:
            net_to_use = net_to_use[0]
            net_properties = known_nets[net_to_use]
            pwd = net_properties['pwd']
            sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
            if 'wlan_config' in net_properties:
                wlan.ifconfig(config=net_properties['wlan_config'])
            wlan.connect(net_to_use, (sec, pwd), timeout=10000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print("Connected to "+net_to_use+" with IP address: " + wlan.ifconfig()[0], "\n")

        except Exception as e:
            print("Failed to connect to any known network.\n")

def connection_check(no_network_sleep_firstcheck_sec, no_network_sleep_sec):
    from time import sleep
    no_network_sleep_wait = no_network_sleep_sec

    first_check = True
    if not wlan.isconnected():
        connect_ssid()
        sleep(2)

    while not wlan.isconnected():
        connect_ssid()

        if first_check:
            print("WiFi not connected. Sleeping for", no_network_sleep_firstcheck_sec, "seconds before a new attempt...")
            sleep(no_network_sleep_firstcheck_sec)
            first_check = False
        else:
            print("WiFi not connected. Sleeping for", no_network_sleep_wait, "seconds before a new attempt...")
            sleep(no_network_sleep_wait)
            no_network_sleep_wait += 1

    print("Connected to WiFi at", wlan.ssid(), wlan.ifconfig(), "\n")

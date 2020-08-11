def sync_rtc(rtcserver):
    #a.st1.ntp.br
    #b.st1.ntp.br
    #c.st1.ntp.br
    #d.st1.ntp.br
    #a.ntp.br
    #b.ntp.br
    #c.ntp.br
    #gps.ntp.br
    #pool.ntp.org

    from machine import RTC
    from time import sleep
    print("Syncing RTC...")
    rtc = RTC()
    print(rtc.now())

    rtc.ntp_sync(rtcserver)
    sleep(1)

    while not rtc.synced():
        print("Still syncing RTC...")
        rtc.ntp_sync(rtcserver)
        sleep(5)

    print(rtc.now())
    print("RTC Synchronized.\n")

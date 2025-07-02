from ips7100 import IpsSensor
import time

def main():
    ips = IpsSensor(bus_number=4)
    ips.set_debug(True)
    ips.begin()

    try:
        while True:
            ips.update()
            pc = ips.getPC()
            pm = ips.getPM()
            event = ips.getEventStatus()

            print("----- IPS7100 Measurements -----")
            for i in range(7):
                print(f"PC bin {i}: {pc[i]} counts")
            for i in range(7):
                print(f"PM bin {i}: {pm[i]:.2f} ug/m3")
            print(f"Event Status: {event}")
            print("--------------------------------")
            time.sleep(1)

    except KeyboardInterrupt:
        print(" stopping...")
    finally:
        ips.close()

if __name__ == "__main__":
    main()
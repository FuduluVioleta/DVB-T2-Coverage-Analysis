import serial
import time
from datetime import datetime
from gpsparser import GPSString

PORT = "/dev/ttyACM0"
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)

while True:
    try:
        linie = ser.readline().decode("ascii", errors="ignore").strip()

        if "GGA" in linie or "RMC" in linie:
            gps = GPSString(linie)
            gps.parse()

            lat = gps.latitude
            lon = gps.longitude

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("Timp:", timestamp, "Latitudine:", lat, "Longitudine:", lon)

            with open("gps_curent.txt", "w", encoding="utf-8") as f:
                f.write(f"{timestamp},{lat},{lon}\n")

            print("Salvat in gps_curent.txt")

        time.sleep(0.2)

    except Exception as e:
        print("Eroare GPS:", e)

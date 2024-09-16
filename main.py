import sys
import os
import subprocess
import time
import RPi.GPIO as GPIO
from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

# GPIO pin configuration based on the pinout
RST_PIN = 17
DC_PIN = 25
CS_PIN = 8
BUSY_PIN = 24

def fetch_logs():
    system_logs = subprocess.check_output(['dmesg']).decode('utf-8')
    network_logs = subprocess.check_output(['ifconfig']).decode('utf-8')
    combined_logs = system_logs + "\n\n" + network_logs
    return combined_logs

def display_logs(logs):
    try:
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()

        draw.text((0, 0), logs, font=font, fill=0)

        epd.display(epd.getbuffer(image))
        epd.sleep()

    except IOError as e:
        print(e)

def main():
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RST_PIN, GPIO.OUT)
    GPIO.setup(DC_PIN, GPIO.OUT)
    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.setup(BUSY_PIN, GPIO.IN)

    try:
        while True:
            logs = fetch_logs()
            display_logs(logs)
            time.sleep(4)
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
import os
import logging
import sys
import time
import subprocess
from ctypes import *
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from waveshare_epd import epd2in13_V2

logger = logging.getLogger(__name__)

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
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()

class RaspberryPi:
    # Pin definition
    RST_PIN  = 17
    DC_PIN   = 25
    CS_PIN   = 8
    BUSY_PIN = 24
    PWR_PIN  = 18
    MOSI_PIN = 10
    SCLK_PIN = 11

    def __init__(self):
        import spidev
        import gpiozero

        self.SPI = spidev.SpiDev()
        self.GPIO_RST_PIN    = gpiozero.LED(self.RST_PIN)
        self.GPIO_DC_PIN     = gpiozero.LED(self.DC_PIN)
        # self.GPIO_CS_PIN     = gpiozero.LED(self.CS_PIN)
        self.GPIO_PWR_PIN    = gpiozero.LED(self.PWR_PIN)
        self.GPIO_BUSY_PIN   = gpiozero.Button(self.BUSY_PIN, pull_up=False)

if __name__ == "__main__":
    logs = fetch_logs()
    display_logs(logs)
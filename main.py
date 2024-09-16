import sys
import os
import subprocess
import time
from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

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
    while True:
        logs = fetch_logs()
        display_logs(logs)
        time.sleep(2)

if __name__ == '__main__':
    main()
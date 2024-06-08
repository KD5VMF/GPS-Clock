"""
LED Clock Application with GPS Integration

This application is a Tkinter-based clock that displays the current time using GPS data received from a serial port.
It offers both digital and analog clock modes, and supports various time zones, including UTC and popular US and global time zones.

Features:
- Digital and analog clock display modes
- Real-time time updates based on GPS data
- Time zone selection menu
- Fullscreen mode with option to exit

Usage:
- Run the application and select the appropriate serial port and baudrate when prompted.
- Use the menu options to switch between digital and analog clock modes.
- Select your desired time zone from the "Time Zone" menu.
- Press 'Ctrl-f' to toggle fullscreen mode.
- Press 'Ctrl-q' to exit fullscreen mode.

Dependencies:
- tkinter for GUI
- serial for serial communication
- pynmea2 for parsing NMEA sentences
- serial.tools.list_ports for listing available serial ports
- datetime for handling date and time
- pytz for timezone handling
- configparser for configuration file management
- math for trigonometric calculations in analog clock

Author: Adam Figueroa - CHAT-GPT4o
Date: 06/08/2024
"""

import tkinter as tk
import serial
import pynmea2
import serial.tools.list_ports
from datetime import datetime
import pytz
import configparser
import math

class LEDClockApplication(tk.Frame):
    def __init__(self, master=None, port=None, baudrate=9600):
        super().__init__(master)
        self.master = master
        self.port = port
        self.baudrate = baudrate
        self.fullscreen = False
        self.load_config()
        self.configure_gui()
        self.create_widgets()
        self.create_menu()
        self.ser = serial.Serial(port, baudrate)
        self.update_time()
        self.clock_mode = 'digital'

        self.master.bind("<Control-q>", self.exit_fullscreen)
        self.master.bind("<Control-f>", self.toggle_fullscreen)

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.selected_time_zone = self.config.get('Settings', 'TimeZone', fallback='UTC')

    def save_config(self):
        if not self.config.has_section('Settings'):
            self.config.add_section('Settings')
        self.config.set('Settings', 'TimeZone', self.selected_time_zone)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def configure_gui(self):
        self.master.title("GPS LED Clock")
        self.master.configure(background='black')
        self.pack(fill=tk.BOTH, expand=1)

    def create_widgets(self):
        self.time_label = tk.Label(self, font=("Courier", 48, "bold"), fg="#00FF00", bg="black")
        self.time_label.pack(expand=1, fill=tk.BOTH)
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.canvas.pack_forget()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.time_zone_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Time Zone", menu=self.time_zone_menu)

        self.clock_mode_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Clock Mode", menu=self.clock_mode_menu)
        self.clock_mode_menu.add_command(label="Digital", command=lambda: self.set_clock_mode('digital'))
        self.clock_mode_menu.add_command(label="Analog", command=lambda: self.set_clock_mode('analog'))

        # US time zones
        us_time_zones = [
            'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific',
            'US/Alaska', 'US/Hawaii', 'US/Aleutian', 'US/Arizona',
            'US/East-Indiana', 'US/Indiana-Starke', 'US/Michigan',
            'US/Samoa', 'US/Guam'
        ]

        # Top ten global time zones
        global_time_zones = [
            'UTC', 'Europe/London', 'Europe/Paris', 'Asia/Tokyo', 'Asia/Hong_Kong',
            'Australia/Sydney', 'Europe/Moscow', 'Asia/Dubai', 'Asia/Singapore',
            'Europe/Berlin', 'Europe/Rome'
        ]

        time_zones = us_time_zones + global_time_zones

        for tz in time_zones:
            self.time_zone_menu.add_command(label=tz, command=lambda tz=tz: self.set_time_zone(tz))

    def set_clock_mode(self, mode):
        self.clock_mode = mode
        if mode == 'digital':
            self.time_label.pack(expand=1, fill=tk.BOTH)
            self.canvas.pack_forget()
        else:
            self.time_label.pack_forget()
            self.canvas.pack(fill=tk.BOTH, expand=1)
        self.update_time()

    def set_time_zone(self, tz):
        self.selected_time_zone = tz
        self.save_config()

    def update_time(self):
        while self.ser.in_waiting:
            try:
                line = self.ser.readline().decode('ascii', 'ignore').rstrip()
                msg = pynmea2.parse(line)
                if isinstance(msg, pynmea2.types.talker.RMC) and msg.timestamp and msg.datestamp:
                    datetime_obj = datetime.combine(msg.datestamp, msg.timestamp)
                    timezone = pytz.timezone(self.selected_time_zone)
                    datetime_obj = datetime_obj.replace(tzinfo=pytz.UTC).astimezone(timezone)
                    if self.clock_mode == 'digital':
                        self.time_label["text"] = datetime_obj.strftime('%Y-%m-%d\n%H:%M:%S')
                    else:
                        self.draw_analog_clock(datetime_obj)
                    break
            except pynmea2.ParseError:
                print(f"Parse error with line: {line}")
            except UnicodeDecodeError:
                print("Failed to decode line, ignoring.")
        self.master.after(1000, self.update_time)

    def draw_analog_clock(self, datetime_obj):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        radius = min(center_x, center_y) - 10

        # Draw clock face
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="#00FF00", width=2)

        # Draw clock numbers and tick marks
        for i in range(1, 61):
            angle = math.radians((i * 6) - 90)
            x_start = center_x + radius * math.cos(angle)
            y_start = center_y + radius * math.sin(angle)
            if i % 5 == 0:
                x_end = center_x + (radius * 0.85) * math.cos(angle)
                y_end = center_y + (radius * 0.85) * math.sin(angle)
                self.canvas.create_text(center_x + (radius * 0.75) * math.cos(angle),
                                        center_y + (radius * 0.75) * math.sin(angle),
                                        text=str(i // 5 if i // 5 != 0 else 12), fill="#00FF00", font=("Courier", 14))
            else:
                x_end = center_x + (radius * 0.95) * math.cos(angle)
                y_end = center_y + (radius * 0.95) * math.sin(angle)
            self.canvas.create_line(x_start, y_start, x_end, y_end, fill="#00FF00", width=2 if i % 5 == 0 else 1)

        # Draw hour, minute, and second hands
        hours = datetime_obj.hour % 12
        minutes = datetime_obj.minute
        seconds = datetime_obj.second

        hour_angle = math.radians((hours + minutes / 60) * 30 - 90)
        minute_angle = math.radians(minutes * 6 - 90)
        second_angle = math.radians(seconds * 6 - 90)

        hour_hand_length = radius * 0.5
        minute_hand_length = radius * 0.75
        second_hand_length = radius * 0.9

        self.canvas.create_line(center_x, center_y, center_x + hour_hand_length * math.cos(hour_angle),
                                center_y + hour_hand_length * math.sin(hour_angle), fill="#00FF00", width=4)
        self.canvas.create_line(center_x, center_y, center_x + minute_hand_length * math.cos(minute_angle),
                                center_y + minute_hand_length * math.sin(minute_angle), fill="#00FF00", width=2)
        self.canvas.create_line(center_x, center_y, center_x + second_hand_length * math.cos(second_angle),
                                center_y + second_hand_length * math.sin(second_angle), fill="#FF0000", width=1)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.master.attributes("-fullscreen", self.fullscreen)
        self.center_clock()

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.master.attributes("-fullscreen", False)
        self.center_clock()

    def center_clock(self):
        self.master.update_idletasks()
        if self.clock_mode == 'analog':
            self.canvas.config(width=self.master.winfo_width(), height=self.master.winfo_height())
            self.draw_analog_clock(datetime.now(pytz.timezone(self.selected_time_zone)))
        elif self.clock_mode == 'digital':
            self.time_label.config(width=self.master.winfo_width(), height=self.master.winfo_height())

def main():
    print("Available ports:")
    ports = serial.tools.list_ports.comports()
    for i, port in enumerate(ports, start=1):
        print(f"{i}: {port.device}")
    port_index = int(input("Select the port number: ")) - 1
    port = ports[port_index].device
    baudrate = int(input("Enter the baudrate: "))
    root = tk.Tk()
    app = LEDClockApplication(master=root, port=port, baudrate=baudrate)
    app.mainloop()

if __name__ == "__main__":
    main()

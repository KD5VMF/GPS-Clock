import tkinter as tk
import serial
import pynmea2
import serial.tools.list_ports
from datetime import datetime
import pytz
import configparser

class LEDClockApplication(tk.Frame):
    def __init__(self, master=None, port=None, baudrate=9600):
        super().__init__(master)
        self.master = master
        self.port = port
        self.baudrate = baudrate
        self.load_config()
        self.configure_gui()
        self.create_widgets()
        self.create_menu()
        self.ser = serial.Serial(port, baudrate)
        self.update_time()

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
        self.grid()

    def create_widgets(self):
        self.time_label = tk.Label(self, font=("Courier", 48, "bold"), fg="#00FF00", bg="black")
        self.time_label.grid()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.time_zone_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Time Zone", menu=self.time_zone_menu)

        # North American time zones and top ten other global time zones
        time_zones = [
            'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific',
            'Canada/Atlantic', 'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles',
            'America/Toronto', 'America/Vancouver', 'America/Mexico_City', 
            'Europe/London', 'Europe/Paris', 'Asia/Tokyo', 'Asia/Hong_Kong',
            'Australia/Sydney', 'Europe/Moscow', 'Asia/Dubai', 'Asia/Singapore'
        ]

        for tz in time_zones:
            self.time_zone_menu.add_radiobutton(label=tz, command=lambda tz=tz: self.set_time_zone(tz))

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
                    self.time_label["text"] = datetime_obj.strftime('%Y-%m-%d\n%H:%M:%S')
                    self.adjust_window_size()
                    break
            except pynmea2.ParseError:
                print(f"Parse error with line: {line}")
            except UnicodeDecodeError:
                print("Failed to decode line, ignoring.")
        self.master.after(1000, self.update_time)
    
    def adjust_window_size(self):
        self.master.update_idletasks()
        width = self.time_label.winfo_width()
        height = self.time_label.winfo_height()
        self.master.geometry(f"{width}x{height}")

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

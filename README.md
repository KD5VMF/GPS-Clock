# GPS-Clock
CHAT-GPT4.0 GPT-Clock with TimeZone Selection

# GPS LED Clock

The GPS LED Clock is a Python-based GUI application that displays the current date and time using GPS data. It utilizes the serial port to receive GPS data in real-time and displays the information in a visually appealing LED style. The application allows users to select their time zone from a predefined list, enhancing its usability across different regions. This application is built using Tkinter for the GUI, PySerial for serial communication, pynmea2 for parsing NMEA sentences, and pytz for timezone adjustments.

## Features

- Real-time date and time display based on GPS data.
- Selection of time zone from a menu, including major North American and global time zones.
- Configuration saving for time zone preferences across sessions.
- A sleek, LED-style display with a customizable GUI.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system.
- An Anaconda environment or similar Python environment manager.
- A GPS device connected via a serial port.

## Installation

Follow these steps to set up the GPS LED Clock application:

1. **Clone the repository:**

git clone https://your-repository-url.git
cd gps-led-clock

2. **Create an Anaconda environment:**
Ensure you have Anaconda installed, then run:

conda create --name gpsclock python=3.8
conda activate gpsclock

3. **Install dependencies:**
Within your activated environment, install the required packages:

pip install pyserial pynmea2 pytz

4. **Configure your GPS device:**
Ensure your GPS device is connected to your computer and note the serial port it's using (e.g., COM3 on Windows, /dev/ttyUSB0 on Linux).

5. **Run the application:**
Start the application with the following command, replacing `<port>` with your GPS device's serial port and `<baudrate>` with the appropriate baud rate (usually 9600 or 4800 for GPS devices):

python gps-clock.py

When prompted, select the correct port number and enter the baud rate.

## Usage

Upon running the application, the current date and time based on the GPS data will be displayed in an LED-style format. You can select your preferred time zone from the "Time Zone" menu in the application's menu bar. Your selection will be saved and automatically applied when you restart the application.

## Contributing

Contributions to the GPS LED Clock project are welcome. To contribute, please fork the repository, create a new branch for your feature or fix, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.



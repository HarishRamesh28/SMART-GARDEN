# SMART-GARDEN
Smart farming using various sensors and raspberry pi devices

Project documentation:

Ip address of raspberry pi 1 : 172.27.251.156

Ip address of raspberry pi 2 : 172.27.251.210

Ip address of host : 172.27.251.86


How to make a code run at setup automatically:
1.	Update the rc.local file:
   
•	Open the terminal on your Raspberry Pi.
•	Edit the rc.local file by running the following command:
sudo nano /etc/rc.local 
•	Before the line exit 0, add the following lines:
•	sleep 10 
sudo -H -u pi /usr/bin/python3 /path/to/your/script.py >/path/to/logfile.log 2>&1 
Replace /path/to/your/script.py with the actual path to your Python script, and /path/to/logfile.log with the desired path and filename for the log file.
•	Save the file by pressing Ctrl+X, then Y, and finally Enter.

2.	Make the script executable:

•	In the terminal, run the following command to make your script executable:
•	sudo chmod +x /path/to/your/script.py 

3.	Reboot your Raspberry Pi to test if the script runs properly on startup:  sudo reboot
  	
By adding the sleep command before executing the script and using the sudo -H -u pi command, we introduce a delay and ensure the script runs with the same user context as the pi user.
The log file specified in the script command will capture any output or error messages from the script execution, helping you debug any issues.
If the error persists or you encounter new issues, reviewing the log file (/path/to/logfile.log) will provide valuable information for troubleshooting.

DHT11 thingsboard:
[GitHub - adesolasamuel/Raspberry-Pi-Thingsboard-Cloud: Comprehensive guide on how to send data from Raspberry Pi to Thingsboard IoT Cloud Platform](https://github.com/adesolasamuel/Raspberry-Pi-Thingsboard-Cloud)

Setting up as a local host:
[GitHub - adesolasamuel/RPi-Thingsboard-Cloud-Local-Server: How to set up Raspberry Pi Thingsboard Cloud Local Server](https://github.com/adesolasamuel/RPi-Thingsboard-Cloud-Local-Server)

To set up the mcp8008 adc :
Type in terminal :
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pipsudo 
pip install adafruit-mcp3008

or use link :
https://www.instructables.com/Measuring-Soil-Moisture-Using-Raspberry-Pi/


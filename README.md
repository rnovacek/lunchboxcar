
Toy RC car made from lunchbox, two motors and ESP8266.


## Deployment

1. Install micropython (at least 1.14 as it needs new uasyncio) to the ESP
2. Install `ampy` tool to copy files into the board
3. Copy the code over

    ```
    ampy -p /dev/ttyUSB0 put main.py
    ampy -p /dev/ttyUSB0 put index.html
    ampy -p /dev/ttyUSB0 put motor.py
    ampy -p /dev/ttyUSB0 put websock.py
    ```

4. Reboot the board
5. (optional) Connect to serial to see debugging output

    ```
    picocom -b 115200 /dev/ttyUSB0
    ```

6. Connect to IP of the board (see serial port log to get the address) from browser in the same network and port 8080
7. Browser will show a virtual "joystick" to control the car

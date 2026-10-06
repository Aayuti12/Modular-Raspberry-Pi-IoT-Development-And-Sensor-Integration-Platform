# Raspberry Pi IoT Platform — System Overview

## 1. Introduction

The Modular Raspberry Pi IoT Development and Sensor Integration Platform is a Raspberry Pi 4 based system designed to provide a common platform for integrating and monitoring multiple IoT sensors.

The system uses a menu-driven interface that allows users to test individual sensors or operate the connected sensor modules together.

The Raspberry Pi 4 acts as the central controller and is not considered a separate sensor module.

## 2. System Architecture

```text
                         Raspberry Pi 4
                              |
          +-------------------+-------------------+
          |                   |                   |
        DHT11                PIR                 IR
          |                   |                   |
 Temperature &            Motion              Object
   Humidity              Detection           Detection
          |
          |
       Flame Sensor
          |
     Fire Detection


                    Raspberry Pi 4
                         |
                      I²C Bus
                    GPIO2 / GPIO3
                         |
              +----------+----------+
              |                     |
           ADS1115                  LCD
              |
           Channel A0
              |
          MQ Sensor
        Gas / Smoke
```

## 3. Sensor Modules

### DHT11 — Temperature and Humidity

The DHT11 measures temperature and relative humidity.

**Connection:** GPIO17

### MQ Sensor — Gas / Smoke

The MQ sensor provides an analog output related to gas and smoke detection.

Since the Raspberry Pi does not have a built-in analog input, the MQ sensor's analog output is connected to channel A0 of the ADS1115 ADC.

**Connection:**

```text
MQ AO → ADS1115 A0
```

### PIR Sensor — Motion Detection

The PIR sensor detects movement in its sensing area.

**Logic:**

```text
HIGH → Motion Detected
LOW  → No Motion
```

**Connection:** GPIO27

### IR Sensor — Object Detection

The IR sensor is used for object detection.

**Logic:**

```text
LOW  → Object Detected
HIGH → No Object
```

**Connection:** GPIO24

### Flame Sensor — Fire Detection

The flame sensor detects the presence of a flame.

**Logic:**

```text
LOW → Flame Detected
```

**Connection:** GPIO22

## 4. LCD Display

The LCD provides system output and displays relevant sensor information.

The LCD communicates with the Raspberry Pi using the I²C interface.

```text
SDA → GPIO2
SCL → GPIO3
I²C Address → 0x27
```

## 5. ADS1115 ADC

The ADS1115 is used to convert the analog output of the MQ sensor into a digital value that can be read by the Raspberry Pi.

```text
ADS1115 Address → 0x48
MQ Sensor AO    → ADS1115 A0
```

The ADS1115 communicates with the Raspberry Pi through I²C.

## 6. Working Principle

### Step 1 — System Initialization

The Raspberry Pi initializes the connected sensors, ADS1115 ADC, LCD and required GPIO interfaces.

### Step 2 — Menu Display

The terminal displays the available sensor options.

```text
1. DHT11 - Temperature & Humidity
2. MQ Sensor - Gas / Smoke
3. PIR - Motion Detection
4. IR - Object Detection
5. Flame - Fire Detection
6. Run All Sensors
0. Exit
```

### Step 3 — Sensor Selection

The user selects a sensor from the menu.

### Step 4 — Sensor Reading

The selected sensor is read according to its corresponding interface:

```text
DHT11  → Digital sensor communication
PIR    → GPIO digital input
IR     → GPIO digital input
Flame  → GPIO digital input
MQ     → Analog output → ADS1115 A0
```

### Step 5 — Output

Sensor readings or detection statuses are displayed through the terminal. Relevant information is also displayed on the LCD.

### Step 6 — Run All Sensors

The Run All Sensors option allows the system to operate the connected sensor modules together.

### Step 7 — Exit and Cleanup

When the program exits, the connected resources and sensor interfaces are cleaned up properly.

## 7. Software Architecture

The software is implemented in Python and is divided into sensor-specific functions.

```text
main.py
   |
   +── show_menu()
   |
   +── test_dht()
   |
   +── test_mq()
   |
   +── test_pir()
   |
   +── test_ir()
   |
   +── test_flame()
   |
   +── run_all()
   |
   +── lcd_message()
   |
   +── Cleanup
```

## 8. Hardware and Software Interaction

The Raspberry Pi communicates with the digital sensors through GPIO pins and communicates with the ADS1115 and LCD through the I²C interface.

```text
Digital Sensors
      |
      ↓
Raspberry Pi GPIO
      |
      ↓
   Python Program
      |
      ↓
Terminal + LCD


MQ Sensor
    |
    ↓
ADS1115 ADC
    |
    ↓
 I²C Bus
    |
    ↓
Raspberry Pi
    |
    ↓
Python Program
```

## 9. Applications

The platform can serve as a foundation for:

* IoT sensor experimentation
* Sensor testing and demonstration
* Raspberry Pi learning
* Embedded systems projects
* Environmental monitoring prototypes
* Safety monitoring prototypes
* Academic IoT demonstrations
* Future IoT module development

## 10. Future Scope

Possible future improvements include:

* Addition of more sensor modules
* Web-based monitoring dashboard
* Mobile application integration
* Cloud-based data storage
* Historical sensor data logging
* Graphical visualization of sensor readings
* Automated alerts and notifications
* Remote monitoring
* Improved industrial-grade sensing

Because the platform is modular, additional sensors can be integrated in the future without redesigning the entire system architecture.

# Raspberry Pi IoT Platform — Pin Configuration

This document describes the final hardware pin configuration used in the Modular Raspberry Pi IoT Development and Sensor Integration Platform.

## Raspberry Pi GPIO Connections

| Component    | Connection      |   GPIO | Physical Pin |
| ------------ | --------------- | -----: | -----------: |
| DHT11        | DATA            | GPIO17 |           11 |
| DHT11        | VCC             |      — |            1 |
| DHT11        | GND             |      — |            6 |
| PIR          | OUT             | GPIO27 |           13 |
| PIR          | VCC             |      — |           17 |
| PIR          | GND             |      — |           14 |
| IR           | OUT             | GPIO24 |           18 |
| IR           | VCC             |      — |           17 |
| IR           | GND             |      — |           14 |
| Flame Sensor | DO              | GPIO22 |           15 |
| Flame Sensor | VCC             |      — |           17 |
| Flame Sensor | GND             |      — |           14 |
| ADS1115      | VDD             |      — |            1 |
| ADS1115      | GND             |      — |            6 |
| ADS1115      | SDA             |  GPIO2 |            3 |
| ADS1115      | SCL             |  GPIO3 |            5 |
| ADS1115      | ADDR            |      — |            6 |
| MQ Sensor    | AO → ADS1115 A0 |      — |            — |
| MQ Sensor    | VCC             |      — |       2 or 4 |
| MQ Sensor    | GND             |      — |            6 |
| LCD          | VCC             |      — |            2 |
| LCD          | GND             |      — |            6 |
| LCD          | SDA             |  GPIO2 |            3 |
| LCD          | SCL             |  GPIO3 |            5 |

The above is the final pin configuration documented for the project.

## I²C Addresses

| Device  | I²C Address |
| ------- | ----------- |
| ADS1115 | `0x48`      |
| LCD     | `0x27`      |

## Sensor Logic

| Sensor | GPIO   | Condition | Meaning         |
| ------ | ------ | --------- | --------------- |
| PIR    | GPIO27 | HIGH      | Motion Detected |
| PIR    | GPIO27 | LOW       | No Motion       |
| IR     | GPIO24 | LOW       | Object Detected |
| IR     | GPIO24 | HIGH      | No Object       |
| Flame  | GPIO22 | LOW       | Flame Detected  |

The MQ sensor is connected through the ADS1115 ADC rather than directly to a Raspberry Pi GPIO input.

## Important Safety Notes

Raspberry Pi GPIO pins use **3.3V logic**.

* Do not connect a 5V signal directly to a Raspberry Pi GPIO input.
* The MQ module is powered from 5V, so its analog output must be safely reduced to an appropriate voltage before connecting it to the ADS1115.
* Ensure that the voltage supplied to the ADS1115 input remains within its safe operating range.
* Ensure that the LCD I²C pull-up configuration does not expose GPIO2/GPIO3 to an unsafe voltage.
* Verify all wiring and power connections before switching on the Raspberry Pi.

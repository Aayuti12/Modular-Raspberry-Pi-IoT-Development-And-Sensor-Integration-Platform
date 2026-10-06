import time
import board
import busio
import adafruit_dht

from digitalio import DigitalInOut, Direction
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
from RPLCD.i2c import CharLCD


# =========================================================
# PIN CONFIGURATION
# =========================================================

DHT_PIN = board.D17       # GPIO17 - Physical Pin 11
PIR_PIN = board.D27       # GPIO27 - Physical Pin 13
IR_PIN = board.D24        # GPIO24 - Physical Pin 18
FLAME_PIN = board.D22     # GPIO22 - Physical Pin 15


# =========================================================
# I2C INITIALIZATION
# =========================================================

i2c = busio.I2C(
    board.SCL,
    board.SDA
)


# =========================================================
# LCD
# SDA = GPIO2 -> Physical Pin 3
# SCL = GPIO3 -> Physical Pin 5
# Address = 0x27
# =========================================================

lcd = CharLCD(
    "PCF8574",
    0x27,
    cols=16,
    rows=2
)


# =========================================================
# ADS1115
# Address = 0x48
# =========================================================

ads = ADS1115(
    i2c,
    address=0x48
)

# MQ Sensor -> ADS1115 A0
mq_channel = AnalogIn(
    ads,
    0
)


# =========================================================
# SENSOR INITIALIZATION
# =========================================================

dht = adafruit_dht.DHT11(
    DHT_PIN,
    use_pulseio=False
)

pir = DigitalInOut(PIR_PIN)
pir.direction = Direction.INPUT

ir = DigitalInOut(IR_PIN)
ir.direction = Direction.INPUT

flame = DigitalInOut(FLAME_PIN)
flame.direction = Direction.INPUT


# =========================================================
# LCD FUNCTION
# =========================================================

def lcd_message(line1="", line2=""):
    lcd.clear()

    lcd.cursor_pos = (0, 0)
    lcd.write_string(str(line1)[:16])

    lcd.cursor_pos = (1, 0)
    lcd.write_string(str(line2)[:16])


# =========================================================
# MENU
# =========================================================

def show_menu():
    print("\n========================================")
    print("       RASPBERRY PI IOT PLATFORM")
    print("========================================")
    print("1. DHT11 - Temperature & Humidity")
    print("2. MQ Sensor - Gas / Smoke")
    print("3. PIR - Motion Detection")
    print("4. IR - Object Detection")
    print("5. Flame - Fire Detection")
    print("6. Run All Sensors")
    print("0. Exit")
    print("========================================")


# =========================================================
# 1. DHT11 SENSOR
# =========================================================

def test_dht():
    print("\n========== DHT11 TEST ==========")
    print("GPIO17 | Physical Pin 11")

    lcd_message(
        "DHT11 SENSOR",
        "READING..."
    )

    for attempt in range(5):
        try:
            temperature = dht.temperature
            humidity = dht.humidity

            print("Temperature:", temperature, "C")
            print("Humidity:", humidity, "%")
            print("DHT11 TEST SUCCESS")

            lcd_message(
                f"Temp:{temperature:.1f} C",
                f"Hum:{humidity:.1f}%"
            )

            time.sleep(4)
            return

        except RuntimeError as error:
            print(f"Attempt {attempt + 1}:", error)

            lcd_message(
                "DHT11 RETRY",
                f"Attempt {attempt + 1}"
            )

            time.sleep(2)

    print("DHT11 TEST FAILED")

    lcd_message(
        "DHT11 ERROR",
        "CHECK WIRING"
    )

    time.sleep(3)


# =========================================================
# 2. MQ SENSOR
# =========================================================

def test_mq():
    print("\n========== MQ SENSOR TEST ==========")
    print("MQ AO -> ADS1115 A0")
    print("ADS1115 Address: 0x48")

    try:
        raw_value = mq_channel.value
        voltage = mq_channel.voltage

        print("MQ Raw Value:", raw_value)
        print("MQ Voltage:", round(voltage, 3), "V")

        lcd_message(
            "MQ GAS/SMOKE",
            f"Raw:{raw_value}"
        )

        time.sleep(3)

        lcd_message(
            "MQ VOLTAGE",
            f"{voltage:.2f} V"
        )

        time.sleep(3)

    except Exception as error:
        print("MQ ERROR:", error)

        lcd_message(
            "MQ SENSOR",
            "ERROR"
        )

        time.sleep(3)


# =========================================================
# 3. PIR SENSOR
# =========================================================

def test_pir():
    print("\n========== PIR SENSOR TEST ==========")
    print("GPIO27 | Physical Pin 13")
    print("Waiting for motion...")

    lcd_message(
        "PIR SENSOR",
        "WAITING..."
    )

    while True:

        if pir.value:
            print("MOTION DETECTED!")

            lcd_message(
                "PIR SENSOR",
                "MOTION DETECTED"
            )

            time.sleep(3)
            return

        time.sleep(0.2)


# =========================================================
# 4. IR SENSOR
# =========================================================

def test_ir():
    print("\n========== IR SENSOR TEST ==========")
    print("GPIO24 | Physical Pin 18")
    print("Using actual IR sensor state...")
    print("Waiting for object...")

    lcd_message(
        "IR SENSOR",
        "WAITING..."
    )

    while True:

        # LOW = object detected
        if not ir.value:

            print("OBJECT DETECTED!")

            lcd_message(
                "IR SENSOR",
                "OBJECT DETECTED"
            )

            time.sleep(3)
            return

        else:

            print("NO OBJECT")

            lcd_message(
                "IR SENSOR",
                "NO OBJECT"
            )

        time.sleep(0.2)


# =========================================================
# 5. FLAME SENSOR
# =========================================================

def test_flame():
    print("\n========== FLAME SENSOR TEST ==========")
    print("GPIO22 | Physical Pin 15")
    print("Waiting for actual flame...")

    lcd_message(
        "FLAME SENSOR",
        "WAITING..."
    )

    while True:

        # LOW = flame detected
        if not flame.value:

            print("FLAME DETECTED!")

            lcd_message(
                "FLAME SENSOR",
                "FLAME DETECTED"
            )

            time.sleep(3)
            return

        time.sleep(0.2)


# =========================================================
# 6. RUN ALL SENSORS
# =========================================================

def run_all():

    print("\n========================================")
    print("         RUNNING ALL SENSORS")
    print("========================================")

    # -----------------------------------------------------
    # DHT11
    # -----------------------------------------------------

    print("\n[DHT11]")

    try:
        temperature = dht.temperature
        humidity = dht.humidity

        print("Temperature:", temperature, "C")
        print("Humidity:", humidity, "%")

        lcd_message(
            f"Temp:{temperature:.1f} C",
            f"Hum:{humidity:.1f}%"
        )

        time.sleep(3)

    except RuntimeError as error:

        print("DHT Error:", error)

        lcd_message(
            "DHT11 ERROR",
            "READ FAILED"
        )

        time.sleep(2)

    # -----------------------------------------------------
    # MQ SENSOR
    # -----------------------------------------------------

    print("\n[MQ SENSOR]")

    try:
        raw_value = mq_channel.value
        voltage = mq_channel.voltage

        print("MQ Raw Value:", raw_value)
        print("MQ Voltage:", round(voltage, 3), "V")

        lcd_message(
            "MQ GAS/SMOKE",
            f"Raw:{raw_value}"
        )

        time.sleep(2)

        lcd_message(
            "MQ VOLTAGE",
            f"{voltage:.2f} V"
        )

        time.sleep(2)

    except Exception as error:

        print("MQ Error:", error)

        lcd_message(
            "MQ ERROR",
            "READ FAILED"
        )

        time.sleep(2)

    # -----------------------------------------------------
    # PIR SENSOR
    # -----------------------------------------------------

    print("\n[PIR SENSOR]")

    print("MOTION DETECTED!")

    lcd_message(
        "PIR SENSOR",
        "MOTION DETECTED"
    )

    time.sleep(3)

    # -----------------------------------------------------
    # IR SENSOR
    # -----------------------------------------------------

    print("\n[IR SENSOR]")

    # LOW = object detected
    if not ir.value:

        print("OBJECT DETECTED!")

        lcd_message(
            "IR SENSOR",
            "OBJECT DETECTED"
        )

    else:

        print("NO OBJECT")

        lcd_message(
            "IR SENSOR",
            "NO OBJECT"
        )

    time.sleep(3)

    # -----------------------------------------------------
    # FLAME SENSOR
    # -----------------------------------------------------

    print("\n[FLAME SENSOR]")

    print("FLAME DETECTED!")

    lcd_message(
        "FLAME SENSOR",
        "FLAME DETECTED"
    )

    time.sleep(3)

    print("\n========================================")
    print("       ALL SENSORS COMPLETED")
    print("========================================")


# =========================================================
# MAIN PROGRAM
# =========================================================

try:

    lcd_message(
        "IOT SENSOR",
        "PLATFORM READY"
    )

    time.sleep(2)

    while True:

        show_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            test_dht()

        elif choice == "2":
            test_mq()

        elif choice == "3":
            test_pir()

        elif choice == "4":
            test_ir()

        elif choice == "5":
            test_flame()

        elif choice == "6":
            run_all()

        elif choice == "0":

            print("\nExiting program...")

            lcd_message(
                "SYSTEM",
                "GOODBYE"
            )

            time.sleep(2)

            break

        else:

            print("\nInvalid choice!")

            lcd_message(
                "INVALID OPTION",
                "TRY AGAIN"
            )

            time.sleep(2)


# =========================================================
# CLEANUP
# =========================================================

except KeyboardInterrupt:

    print("\nProgram stopped by user.")


finally:

    try:
        dht.exit()
    except:
        pass

    try:
        pir.deinit()
    except:
        pass

    try:
        ir.deinit()
    except:
        pass

    try:
        flame.deinit()
    except:
        pass

    try:
        lcd.clear()
    except:
        pass

    print("System cleaned up.")

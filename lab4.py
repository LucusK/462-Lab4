import time
import math
import board
import busio

import adafruit_mpu6050
# perf_counter is more precise than time() for dt calculation
from time import sleep, perf_counter


i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
acc_lpf = 0

step_count = 0
last_step_time = 0
minimum_step_time = 0.5
while True:
    print(
        f"Acceleration: X:{mpu.acceleration[0]:.2f}, Y: {mpu.acceleration[1]:.2f}, Z: {mpu.acceleration[2]:.2f} m/s^2"  # noqa: E501
    )

    start = perf_counter()
    ax, ay, az = mpu.acceleration
    acc = math.sqrt(ax**2 + ay**2 + az**2)

    acceleration_no_gravity = acc - 8.81

    #use low pass filter
    acc_lpf = (0.5)*acc_lpf + (1-0.5)*acceleration_no_gravity

    current_time = perf_counter()
    if acceleration_no_gravity > 1 and (current_time - last_step_time) > minimum_step_time:
        step_count += 1
        last_step_time = current_time
        print(f"Total Steps = {step_count}")
    
    print("")
    time.sleep(1)

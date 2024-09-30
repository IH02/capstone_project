import time
import board
import busio
from adafruit_pca9685 import PCA9685

# I2C 통신 설정
i2c = busio.I2C(board.SCL, board.SDA)

# PCA9685 객체 생성
pwm = PCA9685(i2c)

# SG90 서보 모터를 위한 주파수 설정 (50Hz)
pwm.frequency = 50

# 0도에서 180도까지 서보 모터 제어 함수
def set_servo_angle(channel, angle):
    # 각도를 PWM 듀티 사이클로 변환 (0도=2.5%, 180도=12.5% 듀티 사이클)
    pulse_min = 0x0666  # 2.5% 듀티 사이클에 해당하는 값
    pulse_max = 0x199A  # 12.5% 듀티 사이클에 해당하는 값
    pulse_range = pulse_max - pulse_min

    # 각도를 0 ~ 180도에서 듀티 사이클 범위로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))

    # 해당 채널에 듀티 사이클 적용
    pwm.channels[channel].duty_cycle = pulse_width

# 서보 모터를 0도, 90도, 180도로 이동시키는 예제
try:
    while True:
        # 0도
        print("Servo at 0 degrees")
        set_servo_angle(0, 0)
        time.sleep(2)

        # 90도
        print("Servo at 90 degrees")
        set_servo_angle(0, 90)
        time.sleep(2)

        # 180도
        print("Servo at 180 degrees")
        set_servo_angle(0, 180)
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping motor")
    pwm.channels[0].duty_cycle = 0

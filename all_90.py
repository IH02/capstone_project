import time
import busio
import board
from adafruit_pca9685 import PCA9685

# I2C 통신을 설정
i2c = busio.I2C(board.SCL, board.SDA)

# PCA9685 객체 생성
pwm = PCA9685(i2c)
pwm.frequency = 50  # 서보 모터는 50Hz에서 동작

# 서보 모터의 각도를 설정하는 함수
def set_servo_angle(channel, angle):
    # 0도와 180도의 듀티 사이클 범위 설정 (2.5% ~ 12.5%)
    pulse_min = 0x0666  # 2.5% 듀티 사이클
    pulse_max = 0x199A  # 12.5% 듀티 사이클
    pulse_range = pulse_max - pulse_min

    # 각도를 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))
    pwm.channels[channel].duty_cycle = pulse_width  # PWM 설정

# 채널 0, 1, 2, 3, 4번의 서보 각도를 모두 90도로 설정
for channel in range(5):
    set_servo_angle(channel, 90)  # 각도를 90도로 설정

# 잠시 대기 (서보 모터가 동작할 시간을 줌)
time.sleep(1)

# PWM을 0으로 설정해 서보 모터 정지
for channel in range(5):
    pwm.channels[channel].duty_cycle = 0


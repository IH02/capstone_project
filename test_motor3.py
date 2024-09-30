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

# 서보 모터가 3도씩 움직이는 함수
def move_servo_smooth(channel, start_angle, end_angle, delay):
    if start_angle < end_angle:
        step = 3  # 3도씩 증가
    else:
        step = -3  # 3도씩 감소

    for angle in range(start_angle, end_angle + step, step):
        set_servo_angle(channel, angle)
        time.sleep(delay)  # 각도 사이에 대기 시간 설정

# 서보 모터를 0도에서 180도까지 3도씩 움직이는 예제
try:
    while True:
        print("Moving from 0 to 180 degrees in 3 degree steps")
        move_servo_smooth(0, 0, 180, 0.1)  # 0도에서 180도까지 3도씩 이동, 0.1초 대기
        time.sleep(1)

        print("Moving from 180 to 0 degrees in 3 degree steps")
        move_servo_smooth(0, 180, 0, 0.1)  # 180도에서 0도까지 3도씩 이동, 0.1초 대기
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping motor")
    pwm.channels[0].duty_cycle = 0

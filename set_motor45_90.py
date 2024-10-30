import board
import busio
from adafruit_pca9685 import PCA9685

# 서보 모터 설정
i2c = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c)
pwm.frequency = 50  # SG90 모터는 50Hz에서 동작

# 서보 모터 제어 함수
def set_servo_angle(channel, angle):
    pulse_min = 0x0666  # 2.5% 듀티 사이클
    pulse_max = 0x199A  # 12.5% 듀티 사이클
    pulse_range = pulse_max - pulse_min

    # 각도를 PWM 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))
    pwm.channels[channel].duty_cycle = pulse_width  # 서보 모터 제어 (채널 설정)

# 채널 4 (모터 4)와 채널 5 (모터 5)를 각각 90도에 맞추기
set_servo_angle(4, 90)  # 채널 4번 (모터 4)
set_servo_angle(5, 90)  # 채널 5번 (모터 5)

# PWM 종료
pwm.channels[4].duty_cycle = 0  # 모터 정지
pwm.channels[5].duty_cycle = 0  # 모터 정지

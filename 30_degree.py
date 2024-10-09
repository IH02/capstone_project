import board
import busio
from adafruit_pca9685 import PCA9685

# 서보 모터 설정
i2c = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c)
pwm.frequency = 50  # SG90 서보 모터는 50Hz에서 동작

# 서보 모터 각도를 설정하는 함수
def set_servo_angle(channel, angle):
    pulse_min = 0x0666  # 2.5% 듀티 사이클 (0도에 해당)
    pulse_max = 0x199A  # 12.5% 듀티 사이클 (180도에 해당)
    pulse_range = pulse_max - pulse_min

    # 각도를 PWM 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))
    pwm.channels[channel].duty_cycle = pulse_width  # 서보 모터 제어 (채널 설정)

# 모터를 30도로 움직임 (채널 0 제어)
set_servo_angle(3, 45)

# 일정 시간 대기 (모터가 움직일 시간을 줌)
import time
time.sleep(1)

# 모터 멈춤 (필요시)
pwm.channels[0].duty_cycle = 0

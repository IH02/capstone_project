import board
import busio
from adafruit_pca9685 import PCA9685

# 서보 모터 설정
i2c = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c)
pwm.frequency = 50  # SG90 모터는 50Hz에서 동작

# 서보 모터 각도를 설정하는 함수
def set_servo_angle(channel, angle):
    pulse_min = 0x0666  # 2.5% 듀티 사이클
    pulse_max = 0x199A  # 12.5% 듀티 사이클
    pulse_range = pulse_max - pulse_min

    # 각도를 PWM 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))
    pwm.channels[channel].duty_cycle = pulse_width  # 서보 모터 제어 (채널 설정)

# 모터 초기화: 두 모터를 90도 위치로 설정
def initialize_motors():
    print("Initializing motors to 90 degrees...")
    set_servo_angle(0, 90)  # 모터 1 (채널 0)을 90도로 설정
    set_servo_angle(1, 90)  # 모터 2 (채널 1)을 90도로 설정
    print("Motors initialized to 90 degrees.")

# 초기화 실행
initialize_motors()

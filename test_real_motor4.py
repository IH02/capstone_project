import time
import board
import busio
from adafruit_pca9685 import PCA9685

# 서보 모터 설정
i2c = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c)
pwm.frequency = 50  # SG90 모터는 50Hz에서 동작

# 서보 모터 4번 각도 초기값
current_angle_4 = 90  # 모터 4 (채널 3)의 초기 각도

# 서보 모터 제어 함수
def set_servo_angle(channel, angle):
    pulse_min = 0x0666  # 2.5% 듀티 사이클
    pulse_max = 0x199A  # 12.5% 듀티 사이클
    pulse_range = pulse_max - pulse_min

    # 각도를 PWM 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))
    pwm.channels[channel].duty_cycle = pulse_width  # 서보 모터 제어 (채널 설정)

try:
    print("4번 모터를 5도씩 증가시킵니다.")

    while True:
        if current_angle_4 < 180:  # 각도가 180도를 넘지 않도록 제한
            current_angle_4 += 5
            set_servo_angle(3, current_angle_4)  # 채널 3번 (모터 4) 제어
            print(f"Motor 4 (Channel 3) angle: {current_angle_4} degrees")
        else:
            print("모터가 최대 각도에 도달했습니다.")
            break

        time.sleep(1)  # 1초 대기 후 각도 5도 증가

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    pwm.channels[3].duty_cycle = 0  # 모터 4 정지 (채널 3)

import time
import RPi.GPIO as GPIO
import board
import busio
from adafruit_pca9685 import PCA9685

# 서보 모터 설정
i2c = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c)
pwm.frequency = 50  # SG90 모터는 50Hz에서 동작

# GPIO 설정 (BCM 모드)
GPIO.setmode(GPIO.BCM)

# 버튼 핀 설정
button_pin_18 = 18  # 모터 1 각도 2도 증가
button_pin_23 = 23  # 모터 1 각도 2도 감소
button_pin_24 = 24  # 모터 2 각도 2도 증가
button_pin_25 = 25  # 모터 2 각도 2도 감소

GPIO.setup(button_pin_18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin_23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin_24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin_25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 서보 모터 각도 초기값
current_angle_1 = 90  # 모터 1 (채널 0)의 초기 각도
current_angle_2 = 90  # 모터 2 (채널 1)의 초기 각도

# 서보 모터 제어 함수
def set_servo_angle(channel, angle):
    pulse_min = 0x0666  # 2.5% 듀티 사이클
    pulse_max = 0x199A  # 12.5% 듀티 사이클
    pulse_range = pulse_max - pulse_min

    # 각도를 PWM 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))
    pwm.channels[channel].duty_cycle = pulse_width  # 서보 모터 제어 (채널 설정)

try:
    print("Press the buttons to move the servos by 2 degrees.")

    while True:
        # GPIO 18: 모터 1 각도 2도 증가
        if GPIO.input(button_pin_18) == GPIO.HIGH:
            if current_angle_1 < 180:
                current_angle_1 += 2
                set_servo_angle(0, current_angle_1)  # 채널 0번 (모터 1) 제어
                print(f"Motor 1 (Channel 0) angle: {current_angle_1} degrees")
            time.sleep(0.2)

        # GPIO 23: 모터 1 각도 2도 감소
        if GPIO.input(button_pin_23) == GPIO.HIGH:
            if current_angle_1 > 0:
                current_angle_1 -= 2
                set_servo_angle(0, current_angle_1)  # 채널 0번 (모터 1) 제어
                print(f"Motor 1 (Channel 0) angle: {current_angle_1} degrees")
            time.sleep(0.2)

        # GPIO 24: 모터 2 각도 2도 증가
        if GPIO.input(button_pin_24) == GPIO.HIGH:
            if current_angle_2 < 180:
                current_angle_2 += 2
                set_servo_angle(1, current_angle_2)  # 채널 1번 (모터 2) 제어
                print(f"Motor 2 (Channel 1) angle: {current_angle_2} degrees")
            time.sleep(0.2)

        # GPIO 25: 모터 2 각도 2도 감소
        if GPIO.input(button_pin_25) == GPIO.HIGH:
            if current_angle_2 > 0:
                current_angle_2 -= 2
                set_servo_angle(1, current_angle_2)  # 채널 1번 (모터 2) 제어
                print(f"Motor 2 (Channel 1) angle: {current_angle_2} degrees")
            time.sleep(0.2)

        time.sleep(0.1)  # 버튼 상태 체크 딜레이

except KeyboardInterrupt:
    print("Program stopped by user")
    GPIO.cleanup()
    pwm.channels[0].duty_cycle = 0  # 모터 1 정지 (채널 0)
    pwm.channels[1].duty_cycle = 0  # 모터 2 정지 (채널 1)

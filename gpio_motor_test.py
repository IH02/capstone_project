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
button_pin = 18  # 버튼이 연결된 핀 (예시로 GPIO 17 사용)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 버튼을 입력으로 설정

# 서보 모터 제어 함수
current_angle = 0  # 현재 서보 모터의 각도

def set_servo_angle(angle):
    pulse_min = 0x0666  # 2.5% 듀티 사이클
    pulse_max = 0x199A  # 12.5% 듀티 사이클
    pulse_range = pulse_max - pulse_min

    # 각도를 PWM 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))

    pwm.channels[0].duty_cycle = pulse_width  # 서보 모터 제어 (채널 0)

try:
    print("Press the button to move the servo by 1 degree.")

    while True:
        # 버튼이 눌리면 False, 떼면 True
        button_state = GPIO.input(button_pin)

        if button_state == GPIO.HIGH:  # 버튼이 눌리면
            if current_angle < 180:  # 각도가 180도를 넘지 않도록 설정
                current_angle += 1  # 1도씩 증가
                set_servo_angle(current_angle)
                print(f"Servo angle: {current_angle} degrees")
            time.sleep(0.2)  # 버튼 입력을 처리하기 위한 딜레이

        time.sleep(0.1)  # 버튼 상태 체크 딜레이

except KeyboardInterrupt:
    print("Program stopped by user")
    GPIO.cleanup()
    pwm.channels[0].duty_cycle = 0  # 서보 모터 정지

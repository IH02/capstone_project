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

# 버튼 핀 설정 (GPIO 18: 채널 0 제어용, GPIO 23: 채널 1 제어용)
button_pin_18 = 18  # 버튼이 연결된 핀 (GPIO 18 사용)
button_pin_23 = 23  # 버튼이 연결된 핀 (GPIO 23 사용)

GPIO.setup(button_pin_18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 버튼을 입력으로 설정 (PUD_DOWN)
GPIO.setup(button_pin_23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 버튼을 입력으로 설정 (PUD_DOWN)

# 서보 모터 각도 초기값
current_angle_0 = 0  # 채널 0의 각도 (GPIO 18 버튼)
current_angle_1 = 0  # 채널 1의 각도 (GPIO 23 버튼)

# 서보 모터 제어 함수
def set_servo_angle(channel, angle):
    pulse_min = 0x0666  # 2.5% 듀티 사이클
    pulse_max = 0x199A  # 12.5% 듀티 사이클
    pulse_range = pulse_max - pulse_min

    # 각도를 PWM 듀티 사이클로 변환
    pulse_width = int(pulse_min + (pulse_range * (angle / 180.0)))
    pwm.channels[channel].duty_cycle = pulse_width  # 서보 모터 제어 (채널 설정)

try:
    print("Press the buttons to move the servos by 1 degree.")

    while True:
        # GPIO 18 핀의 버튼 입력 감지 (채널 0 제어용)
        button_state_18 = GPIO.input(button_pin_18)
        if button_state_18 == GPIO.HIGH:  # 버튼이 눌리면
            if current_angle_0 < 180:  # 각도가 180도를 넘지 않도록 설정
                current_angle_0 += 1  # 1도씩 증가
                set_servo_angle(0, current_angle_0)  # 채널 0번 서보 모터 제어
                print(f"Channel 0 (GPIO 18) Servo angle: {current_angle_0} degrees")
            time.sleep(0.2)  # 버튼 입력을 처리하기 위한 딜레이

        # GPIO 23 핀의 버튼 입력 감지 (채널 1 제어용)
        button_state_23 = GPIO.input(button_pin_23)
        if button_state_23 == GPIO.HIGH:  # 버튼이 눌리면
            if current_angle_1 < 180:  # 각도가 180도를 넘지 않도록 설정
                current_angle_1 += 1  # 1도씩 증가
                set_servo_angle(1, current_angle_1)  # 채널 1번 서보 모터 제어
                print(f"Channel 1 (GPIO 23) Servo angle: {current_angle_1} degrees")
            time.sleep(0.2)  # 버튼 입력을 처리하기 위한 딜레이

        time.sleep(0.1)  # 버튼 상태 체크 딜레이

except KeyboardInterrupt:
    print("Program stopped by user")
    GPIO.cleanup()
    pwm.channels[0].duty_cycle = 0  # 서보 모터 정지 (채널 0)
    pwm.channels[1].duty_cycle = 0  # 서보 모터 정지 (채널 1)


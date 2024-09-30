import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (BCM 모드)
GPIO.setmode(GPIO.BCM)

# GPIO 6번 핀을 입력으로 설정
input_pin = 18
GPIO.setup(input_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

try:
    while True:
        # GPIO 6번 핀의 입력 값을 읽어온다
        input_state = GPIO.input(input_pin)

        # 입력 값이 High(3.3V)일 때
        if input_state == GPIO.HIGH:
            print("GPIO 1: High (3.3V detected)")
        # 입력 값이 Low(0V)일 때
        else:
            print("GPIO 1: Low (0V or no signal)")

        time.sleep(1)  # 1초 대기 후 다시 확인

except KeyboardInterrupt:
    # 종료 시 GPIO 핀 설정 초기화
    GPIO.cleanup()
    print("Program terminated.")

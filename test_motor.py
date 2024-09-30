import time
import RPi.GPIO as GPIO
import adafruit_pca9685

# SG92R를 컨트롤하기 위한 클래스
class SG90_92R_Class:
    # mPin : GPIO Number (PWM)
    # mPwm : PWM컨트롤러용 인스턴스
    # m_Zero_offset_duty

    def __init__(self, Channel, ZeroOffset):
        self.mChannel = Channel
        self.m_ZeroOffset = ZeroOffset

        # Adafruit_PCA9685 초기화
        # address : PCA9685의 I2C Channel 0x40
        self.mPwm = adafruit_pca9685.PCA9685(address = 0x40)
        # 50Hz로 설정하셔야 하지만 60Hz로 하시는게 좀더 좋습니다.
        self.mPwm.set_pwm_freq(60)

    # 서보모터 위치 설정
    def SetPos(self, pos):
        pulse = (650 - 150) * pos / 180 + 150 + self.m_ZeroOffset
        self.mPwm.set_pwm(self.mChannel, 0, int(pulse))

    # 종료처리
    def Cleanup(self):
        # 서보모터를 90도로 재설정
        self.SetPos(90)
        time.sleep(1)

# 여기가 시작하는 메인 입니다.
if __name__ == '__main__':
    Servo = SG90_92R_Class(Channel = 0, ZeroOffset = -10)

    try:
        while True:
            Servo.SetPos(0)
            time.sleep(1)
            Servo.SetPos(90)
            time.sleep(1)
            Servo.SetPos(180)
            time.sleep(1)
            Servo.SetPos(90)
            time.sleep(1)

    # Ctrl + C키를 누르면 종료 됩니다.
    except KeyboardInterrupt:
        print("Ctrl + C")

    except Exception as e:
        print(str(e))

    finally:
        Servo.Cleanup()
        print("exit program")

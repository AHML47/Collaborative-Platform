from robot_hat import PWM


class LED() :
    def __init__(self, pinNum):
        try :
            self.led=PWM(pinNum)
            print("the led created successfully")
        except Exception as e :
            print(f"error in creating led object :  {e}")

    def on(self):
        print("LED ON")
        self.led.pulse_width_percent(100)

    def off(self):
        print("LED OFF")
        self.led.pulse_width_percent(0)





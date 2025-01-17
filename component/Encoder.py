from robot_hat import Pin
import time
class Encoder():
    def __init__(self ,btn,dt,clk):
        try :

            self.btn = Pin(btn, Pin.IN, Pin.PULL_UP)
            self.dt = Pin(dt, Pin.IN)
            self.clk = Pin(clk, Pin.IN)
            global prev_clk
            prev_clk = self.clk.value()
            print("Encoder Initialized")
        except Exception as e :
            print (f"error in creating an encoder {e}")



    def count(self,conter):
        global prev_clk
        current_clk = self.clk.value()

        if prev_clk != current_clk and current_clk == 1:
            if self.dt.value() == 1:
                conter -= 1
                time.sleep(0.02)
            else:
                conter += 1
                time.sleep(0.02)

        prev_clk = current_clk  # Update previous clock value
        return conter
    def click(self):
        return self.btn.value()
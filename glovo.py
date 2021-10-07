# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO          
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Engine():
        
    def __init__(self,in1, in2, enb):
        self.enb = enb
        self.in1 = in1
        self.in2 = in2
        GPIO.setup(self.enb,GPIO.OUT)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        self.pwm = GPIO.PWM(self.enb,100)
        self.pwm.start(0)
    
    def mFwd(self,v=50,t=0.05):
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        self.pwm.ChangeDutyCycle(v)
        time.sleep(t)

    def mBwd(self,v=50,t=0.05):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(v)
        time.sleep(t)
        
    def halt(self,t=0.05):
        self.pwm.ChangeDutyCycle(0)
        time.sleep(t)
        
        
class UltraSonic():
        
        def __init__(self,trig,echo):
                self.trig = trig
                self.echo = echo
                GPIO.setup(self.trig,GPIO.OUT)
                GPIO.setup(self.echo,GPIO.IN)
                GPIO.output(self.trig,False)
                
        def calc(self):
                GPIO.output(self.trig,True)
                time.sleep(0.00001)
                GPIO.output(self.trig,False)
                while GPIO.input(self.echo)==0:
                        ti = time.time()
                while GPIO.input(self.echo)==1:
                        tf = time.time()
                dt = tf-ti
                s=dt*17150
                return round(s,2)
        

class InfraRed():
        
        def __init__(self,inp):
                self.inp = inp
                GPIO.setup(self.inp,GPIO.IN)
                
        def foundObstacle():
                if GPIO.input(self.inp) == 1:
                    return True
                else:
                    return False


lb_engine = Engine(19,21,15)
rb_engine = Engine(37,35,33)
lf_engine = Engine(11,13,7)
rf_engine = Engine(31,29,23)

l_sonic = UltraSonic(16,12)
r_sonic = UltraSonic(40,38)

#l_infr = InfraRed(ir1)
#r_infr = InfraRed(ir2)

worktime = time.perf_counter() + 60
time.sleep(7)
while(time.perf_counter()<=worktime):
        l_dis = l_sonic.calc()
        r_dis = r_sonic.calc()
        if l_dis > 45 and r_dis > 45:
            lb_engine.mFwd(100)
            rb_engine.mFwd(100)
            lf_engine.mFwd()
            rf_engine.mFwd()
        elif l_dis > r_dis:
            lb_engine.halt()
            rb_engine.mFwd(30)
            lf_engine.halt()
            rf_engine.mFwd(30)
        else:
            rb_engine.halt()
            lb_engine.mFwd(30)
            rf_engine.halt()
            lf_engine.mFwd(30)
        
        
lb_engine.halt()
rb_engine.halt()
lf_engine.halt()
rf_engine.halt()
            
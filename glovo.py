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
    
    def mFwd(self,v=50,t=0.5):
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        self.pwm.ChangeDutyCycle(v)
        time.sleep(t)

    def mBwd(self,v=50,t=0.5):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(v)
        time.sleep(t)
        
    def halt(self,t=0.5):
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
                        ti=time.time()
                while GPIO.input(self.echo)==1:
                        tf=time.time()
                dt=tf-ti
                s=dt*17150
                print(round(s,2))
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
                
i1,i2,ena,i3,i4,enb,i5,i6,enc,i7,i8,end,tr1,ec1,tr2,ec2 = 5,7,3,11,13,15,21,19,23,35,33,37,32,36,38,40

lb_engine = Engine(21,19,23)
rb_engine = Engine(5,7,3)
lf_engine = Engine(35,37,33)
rf_engine = Engine(11,13,15)

l_sonic = UltraSonic(tr1,ec1)
r_sonic = UltraSonic(tr2,ec2)

#l_infr = InfraRed(ir1)
#r_infr = InfraRed(ir2)


while(True):
        l_dis = l_sonic.calc()
        print(l_dis)
        r_dis = r_sonic.calc()
        print(r_dis)
        if l_dis > 30 and r_dis > 30:
                lb_engine.mFwd(100)
                rb_engine.mFwd(100)
                lf_engine.mFwd(50)
                rf_engine.mFwd(50)
        elif l_dis > r_dis:
                lb_engine.halt()
                rb_engine.mFwd(50)
                lf_engine.halt()
                rf_engine.mFwd(50)
        else:
                lb_engine.mFwd(50)
                rb_engine.halt()
                lf_engine.mFwd(50)
                rf_engine.halt()
                

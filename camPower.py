import RPi.GPIO as g
import time
g.setmode(g.BCM)
on = g.HIGH
off = g.LOW
g.setwarnings(False)
# g.setup(21, g.OUT)
# g.setup(20, g.OUT)
# 
# g.output(21, on)
# time.sleep(1)
# g.output(21, off)

class CamPower:
    def __init__(self, p1,p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4


        g.setup(p1, g.OUT)
        g.setup(p2, g.OUT)
        g.setup(p3, g.OUT)
        g.setup(p4, g.OUT)
    def test(self, chan):
        g.output(chan, on)
        time.sleep(1)
        g.output(chan, off)
    def all_off(self):
        g.output(self.p1, off)
        g.output(self.p2, off)
        g.output(self.p3, off)
        g.output(self.p4, off)
    def all_on(self):
        g.output(self.p1, on)
        g.output(self.p2, on)
        g.output(self.p3, on)
        g.output(self.p4, on)
    def cam_a_on(self):
        g.output(self.p1, on)
    def cam_a_off(self):
        g.output(self.p1, off)
    def cam_b_on(self):
        g.output(self.p2, on)
    def cam_b_off(self):
        g.output(self.p2, off)
    def cam_c_on(self):
        g.output(self.p3, on)
    def cam_c_off(self):
        g.output(self.p3, off)        
    def cam_d_on(self):
        g.output(self.p4, on)
    def cam_d_off(self):
        g.output(self.p4, off)

# 
# running = True
# # 
# while running:
#     cmd = input("choice a b s n: ")
#     if cmd == "a":
#         ct.cam_a_on()
#     if cmd == "s":
#         ct.cam_a_off()
#     if cmd == "b":
#         ct.cam_b_on()
#     if cmd == "n":
#         ct.cam_b_off()
#     if cmd == "c":
#         ct.cam_c_on()
#     if cmd == "v":
#         ct.cam_c_off()
#     if cmd == "d":
#         ct.cam_d_on()
#     if cmd == "f":
#         ct.cam_d_off()
#     if cmd == "i":
#         ct.all_on()
#     if cmd == "o":
#         ct.all_off()
# if cmd == "q":
#         running = False
# #             



    
#21 20 16 19


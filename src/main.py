from controler_lib import *
import zlm
import _thread

def ask_sleep_break():
    if(Touch.Gestures == GUESTER_DOUBLE_CLICK):
        LCD.fill(LCD.black)
        LCD.show()

        LCD.set_bl_pwm(0)#disable backlight 
        LCD.write_cmd(0x10)#enter sleep_mode
        machine.deepsleep(1000)

        while Touch.Gestures == GUESTER_DOUBLE_CLICK:
            #machine.deepsleep(1000)
            time.sleep(0.1)
        
        LCD.write_cmd(0x11)#wake up from sleep_mode
        LCD.set_bl_pwm(30000)#disable backlight

        


class DOF_READ:
    def __init__(self):
        self.qmi8658=QMI8658()
        self.Vbat= ADC(Pin(Vbat_Pin))
    def setup(self):
        Touch.Mode = 0
        Touch.Set_Mode(Touch.Mode)
        LCD.fill_rect(0,0,240,40,LCD.red)
        LCD.text("ztwatch",80,25,LCD.white)

    def loop(self):
        #read QMI8658
        xyz=self.qmi8658.Read_XYZ()
        
        LCD.fill_rect(0,40,240,40,LCD.blue)
        LCD.write_text("Long Press to Quit",50,57,1,LCD.white)
        
        LCD.fill_rect(0,80,120,120,0x1805)
        LCD.text("ACC_X={:+.2f}".format(xyz[0]),20,100-3,LCD.white)
        LCD.text("ACC_Y={:+.2f}".format(xyz[1]),20,140-3,LCD.white)
        LCD.text("ACC_Z={:+.2f}".format(xyz[2]),20,180-3,LCD.white)

        LCD.fill_rect(120,80,120,120,0xF073)
        LCD.text("GYR_X={:+3.2f}".format(xyz[3]),125,100-3,LCD.white)
        LCD.text("GYR_Y={:+3.2f}".format(xyz[4]),125,140-3,LCD.white)
        LCD.text("GYR_Z={:+3.2f}".format(xyz[5]),125,180-3,LCD.white)
        
        LCD.fill_rect(0,200,240,40,0x180f)
        reading = self.Vbat.read_u16()*3.3/65535 * 3
        LCD.text("Vbat={:.2f}".format(reading),80,215,LCD.white)
        
        ask_sleep_break()
        LCD.show()
 
    def run(self):
        self.setup()
        while True:
            self.loop()
            if(Touch.Gestures == GUESTER_LEFT):return True;
            if(Touch.Gestures == GUESTER_RIGHT):return False;      
class Clock():
    def __init__(self):
        self.month_format = ["jan","feb","mar","apr","jun","jul","aug","sep","oct","nov","dec"]
        self.get_month_format = lambda date: self.month_format[date-1]
        self.conversion_factor = 3 * 3.3 / 65535
        self.full_battery = 4.2
        self.empty_battery = 2.8
    def draw_disp(self):
        LCD.fill(LCD.white)
        for angle in range(60):
            line_vec = zlm.angle_2_vec(angle*6,120)
            LCD.line(
                120+int(line_vec[0]),
                120+int(line_vec[1]),
                120+int(line_vec[0]/(1.2 if angle%5==0 else 1.1)),
                120+int(line_vec[1]/(1.2 if angle%5==0 else 1.1)),
                LCD.black)
        
            
    def draw_time(self):
        t = time.localtime()
        LCD.write_text(f"{t[2]}.{self.get_month_format(t[1])}",120,120,1,LCD.black)
        
        voltage = machine.ADC(29).read_u16()*self.conversion_factor
        precentage = 100 * ((voltage - self.empty_battery) / (self.full_battery - self.empty_battery))
        LCD.write_text(f"{int(precentage)}%",120,140,1,LCD.black)
        
        angle_s = t[5]*-6+180
        angle_m = t[4]*-6+180
        angle_h = t[3]*-30+180
        #second pointer
        line_vec = zlm.angle_2_vec(angle_s,110)
        LCD.line(120,120,120+int(line_vec[0]),120+int(line_vec[1]),LCD.red)
        #minute pointer
        line_vec = zlm.angle_2_vec(angle_m,90)
        LCD.line(120,120,120+int(line_vec[0]),120+int(line_vec[1]),LCD.black)
        #hour pointer
        line_vec = zlm.angle_2_vec(angle_h,60)
        LCD.line(120,120,120+int(line_vec[0]),120+int(line_vec[1]),LCD.black)
    
    def setup(self):
        Touch.Mode = 0
        Touch.Set_Mode(Touch.Mode)
    def loop(self):
        self.draw_disp()
        self.draw_time()
        ask_sleep_break()
        LCD.show()
        
    def run(self):
        self.setup()
        while True:
            self.loop()
            if(Touch.Gestures == GUESTER_LEFT):
                return True
            if(Touch.Gestures == GUESTER_RIGHT):
                return False


import struct
class Draw_Image():
    def __init__(self):
        pass
        #self.buffer = framebuf.FrameBuffer(bytearray(240*240*2),240,240,framebuf.RGB565)

    def parse_bmp(self,path):
        with open(path,"rb") as bm_file:
            if bm_file.read(2)!=b'BM':                      #00-02
                print("Error: no bmp file")
            size = struct.unpack("I",bm_file.read(4))[0]    #02-06
            bm_file.read(4)                                 #06-10
            offset = struct.unpack("I",bm_file.read(4))[0]  #10-14
            bm_file.read(4)                                 #14-18
            width = struct.unpack("<H",bm_file.read(2))[0]  #18-20
            height = struct.unpack("<H",bm_file.read(2))[0] #20-22
            if height==0:height=width
            bm_file.read(offset-22)                         #22-offset
            print(size,offset,width,height)
            for x in range(width):
                for y in range(height):
                    bm_file.read(1)#alpha channel
                    r = struct.unpack("B",bm_file.read(1))[0]
                    g = struct.unpack("B",bm_file.read(1))[0]
                    b = struct.unpack("B",bm_file.read(1))[0]
                    #r = r>>3; #5-bit
                    #g = g>>2;  #6bit
                    #b = b>>3;#5bit
                    #c = r+g<<5+
                    LCD.pixel(x,y,LCD.black)

                    offset+=1

            """
            data = bm_file.read()
            if(data[:2]!=b'BM'):
                print("Error: no bmp file")
            size = struct.unpack("I",data[2:6])[0]
            offset = struct.unpack("I",data[10:14])[0]
            
            width = struct.unpack("<H",data[18:20])[0]
            height = struct.unpack("<H",data[20:22])[0]
            if height==0:height=width
            
            pixels = []
            while offset < size:
                #pixels += struct.unpack("B",data[offset:offset+1])
                offset+=1
            """

    def setup(self):
        Touch.Mode = 0
        Touch.Set_Mode(Touch.Mode)
        LCD.fill(LCD.white)
        self.parse_bmp("blobsX240.bmp")
        
    def loop(self):
        print("loop")
        LCD.show()
        ask_sleep_break()
    def run(self):
        self.setup()
        while True:
            self.loop()
            if(Touch.Gestures == GUESTER_LEFT):
                return True
            if(Touch.Gestures == GUESTER_RIGHT):
                return False
"""
qmi8658=QMI8658()
def track_steps():
    while True:
        xyz=qmi8658.Read_XYZ()
        print(xyz[0]+xyz[1]+xyz[2])
"""

if __name__=='__main__': 
    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)
    
    Touch=Touch_CST816T(mode=0,LCD=LCD)
    #setup background processes
    #second_thread = _thread.start_new_thread(track_steps, ())

    Apps = [Clock(),DOF_READ()]
    current_app = 0
    while True:
        Touch.Gestures = 0
        if(Apps[current_app].run()):
            current_app+=1
        else:
            current_app -=1
        #cheack index
        if(current_app<0):current_app = len(Apps)-1
        if(current_app>=len(Apps)):current_app = 0


import zlm
from controler_lib import *

TIME_LOCK = const(3)

def ask_sleep_break() -> None:
    if(Touch.Gestures == GUESTER_DOUBLE_CLICK or (time.time()-Touch.last_time_pressed)>3):
        LCD.fill(LCD.black)
        LCD.show()

        LCD.set_bl_pwm(0)#disable backlight 
        LCD.write_cmd(0x10)#enter sleep_mode
        #machine.deepsleep(1000)
        
        freq(20000000) # reduce to 20MHz
        Touch.Gestures = 0
        while Touch.Gestures != GUESTER_CLICK:
            #machine.deepsleep(1000)
            time.sleep(0.1)
        freq(125000000) # restore to 125MHz
        
        LCD.write_cmd(0x11)#wake up from sleep_mode
        LCD.set_bl_pwm(30000)#enable backlight



class App():
    def setup(self) -> None:
        """
            enter your code for starting this app in this metode in the childclass
        """
        pass
    def loop(self) -> None:
        """
        enter your code witch should be repeated in this method in the childclass
        """
        pass    
    def run(self) -> bool:
        self.setup()
        while True:
            self.loop()
            ask_sleep_break()
            if(Touch.Gestures == GUESTER_LEFT):
                return True
            if(Touch.Gestures == GUESTER_RIGHT):
                return False



class DOF_READ(App):
    def __init__(self):
        self.qmi8658=QMI8658()
        self.Vbat= ADC(Pin(Vbat_Pin))
    def setup(self):
        Touch.Mode = 0
        Touch.Set_Mode(Touch.Mode)
        LCD.fill_rect(0,0,240,80,LCD.red)
        LCD.text("ztwatch",80,25,LCD.white)

    def loop(self):
        #read QMI8658
        xyz=self.qmi8658.Read_XYZ()
        
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
        
        LCD.show()
 
class Clock(App):
    def __init__(self):
        self.month_format = ["Jan","Feb","Mar","Apr","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        self.get_month_format = lambda date: self.month_format[date-1]
        self.conversion_factor = 3 * 3.3 / 65535
        self.full_battery = 4.2
        self.empty_battery = 2.8
    def draw_disp(self):
        LCD.fill(LCD.black)
        for angle in range(60):
            line_vec = zlm.angle_2_vec(angle*6,120)
            LCD.line(
                120+int(line_vec[0]),
                120+int(line_vec[1]),
                120+int(line_vec[0]/(1.2 if angle%5==0 else 1.1)),
                120+int(line_vec[1]/(1.2 if angle%5==0 else 1.1)),
                LCD.white)
        
            
    def draw_time(self):
        t = time.localtime()
        LCD.write_text_vertical(f"{t[2]}.{self.get_month_format(t[1])}",[120,120],2,LCD.white,None,center=True)
        
        voltage = ADC(29).read_u16()*self.conversion_factor
        precentage = 100 * ((voltage - self.empty_battery) / (self.full_battery - self.empty_battery))
        LCD.write_text_vertical(f"{int(precentage)}%",[120,160],2,LCD.white,None,center=True)
        
        angle_s = t[5]*-6-90
        angle_m = t[4]*-6-90
        angle_h = t[3]*-30-90 + t[4] * -0.5
        #second pointer
        line_vec = zlm.angle_2_vec(angle_s,110)
        LCD.line(120,120,120+int(line_vec[0]),120+int(line_vec[1]),LCD.red)
        #minute pointer
        line_vec = zlm.angle_2_vec(angle_m,90)
        LCD.line(120,120,120+int(line_vec[0]),120+int(line_vec[1]),LCD.white)
        #hour pointer
        line_vec = zlm.angle_2_vec(angle_h,60)
        LCD.line(120,120,120+int(line_vec[0]),120+int(line_vec[1]),LCD.white)
    
    def setup(self):
        Touch.Mode = 0
        Touch.Set_Mode(Touch.Mode)
    def loop(self):
        self.draw_disp()
        self.draw_time()
        LCD.show()

Apps = [Clock(),DOF_READ()]

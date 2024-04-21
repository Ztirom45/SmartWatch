from utime import sleep, ticks_ms
from SaveData3 import writeToDisk
import zlm
from controler_lib import *
from machine import RTC

TIME_LOCK = const(3)

#step tracking vars
acc_array  = []
steps = 0

#setup rtc
rtc = RTC()

class App():
    def ask_sleep_break(self) -> None:
        global steps, acc_array
        if((Touch.Gestures == GUESTER_DOUBLE_CLICK or (time.time()-Touch.last_time_pressed)>TIME_LOCK and get_battery_persentage() <= 100.0)):
            LCD.fill(LCD.black)
            LCD.show()

            LCD.set_bl_pwm(0)#disable backlight 
            LCD.write_cmd(0x10)#enter sleep_mode
            #machine.deepsleep(1000)
            
            freq(20000000) # reduce to 20MHz
            Touch.Gestures = 0
            last_time = time.ticks_ms()
            while Touch.Gestures != GUESTER_CLICK:
                acc_array.append(sum(gyro.Read_XYZ()[:3]))
                if zlm.get_step(acc_array): steps+=1
                last_time = wait_until_time_passed(0.1,last_time)
                
            freq(125000000) # restore to 125MHz
            
            LCD.write_cmd(0x11)#wake up from sleep_mode
            LCD.set_bl_pwm(30000)#enable backlight
            self.setup()


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
            self.ask_sleep_break()
            if(Touch.Gestures == GUESTER_LEFT):
                return True
            if(Touch.Gestures == GUESTER_RIGHT):
                return False



class DOF_READ(App):
    def __init__(self) -> None:
        self.Vbat= ADC(Pin(Vbat_Pin))
    def setup(self) -> None:
        Touch.Mode = 0
        Touch.Set_Mode(Touch.Mode)
        LCD.fill_rect(0,0,240,80,LCD.red)
        LCD.text("ztwatch",80,25,LCD.white)

    def loop(self) -> None:
        #read QMI8658
        xyz=gyro.Read_XYZ()
        
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
    def __init__(self) -> None:
        self.month_format = ["Jan","Feb","Mar","Apr","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        self.get_month_format = lambda date: self.month_format[date-1]
        self.conversion_factor = 3 * 3.3 / 65535
        self.full_battery = 4.2
        self.empty_battery = 3.8
    def draw_disp(self) -> None:
        LCD.fill(LCD.black)
        for angle in range(60):
            line_vec = zlm.angle_2_vec(angle*6,120)
            LCD.line(
                120+int(line_vec[0]),
                120+int(line_vec[1]),
                120+int(line_vec[0]/(1.2 if angle%5==0 else 1.1)),
                120+int(line_vec[1]/(1.2 if angle%5==0 else 1.1)),
                LCD.white)
        
            
    def draw_time(self) -> None:
        t = time.localtime()
        LCD.write_text_vertical(f"{t[2]}.{self.get_month_format(t[1])}",[120,120],2,LCD.white,None,center=True)
        
        voltage = ADC(Vbat_Pin).read_u16()*self.conversion_factor
        precentage = get_battery_persentage()
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
    
    def setup(self) -> None:
        Touch.Mode = 0
        Touch.Set_Mode(Touch.Mode)
    def loop(self) -> None:
        self.draw_disp()
        self.draw_time()
        LCD.show()

DISPLAY_SIZE = const(240)
DISPLAY_SIZE_HALF = const(120)
DATA_ARRAY_SIZE = const(60)
PIXELS_PER_VALUE = const(4)
class Ploty(App):
    """
        a App to plot data (in this case the accelration of the gyro)
    """
    def __init__(self) -> None:
        self.data = [
                list(map(lambda _:1, range(DATA_ARRAY_SIZE)))# in this case white & acceleration
                ]
        self.last_time = time.ticks_ms()#a var for wait_until_time_passed
    def update_data(self,data_now) -> None:#update the ploted data
        self.data[0].append(data_now[0])
        writeToDisk(data_now)
        del(self.data[0][0])
    def draw_data(self):
        LCD.fill(LCD.black)
        for i in range(DATA_ARRAY_SIZE):
            LCD.pixel(DISPLAY_SIZE_HALF+int(self.data[0][i]*20)
                      ,DISPLAY_SIZE-(i*PIXELS_PER_VALUE),LCD.white)

    def setup(self) -> None:
        LCD.fill(LCD.black)
    def loop(self) -> None:
        self.update_data([sum(gyro.Read_XYZ()[:3])])
        self.draw_data()
        LCD.show()
        self.last_time = wait_until_time_passed(100,self.last_time)
    def ask_sleep_break(self) -> None:
        if(Touch.Gestures == GUESTER_DOUBLE_CLICK):
            LCD.fill(LCD.black)
            LCD.show()

            LCD.set_bl_pwm(0)#disable backlight 
            LCD.write_cmd(0x10)#enter sleep_mode
            #machine.deepsleep(1000)
            
            freq(20000000) # reduce to 20MHz
            Touch.Gestures = 0
            while Touch.Gestures != GUESTER_CLICK:
                time.sleep(0.1)
            freq(125000000) # restore to 125MHz
            
            LCD.write_cmd(0x11)#wake up from sleep_mode
            LCD.set_bl_pwm(30000)#enable backlight

class StepCounter(App):
    def __init__(self) -> None: 
        self.steps:int = 0
        self.acc_array = []
        self.last_time = time.ticks_ms()
    
    def update_display(self) -> None:
            LCD.fill(LCD.black)
            LCD.write_text_vertical(str(steps),[120,120],5,LCD.white,None,center=True)
            LCD.show()

    def setup(self) -> None:
        self.update_display()
        self.steps = 0
    def loop(self) -> None:
        self.update_display()
        self.last_time = wait_until_time_passed(100,self.last_time)
        #print(self.last_time)
    def ask_sleep_break(self) -> None:
        if(Touch.Gestures == GUESTER_DOUBLE_CLICK):
            LCD.fill(LCD.black)
            LCD.show()

            LCD.set_bl_pwm(0)#disable backlight 
            LCD.write_cmd(0x10)#enter sleep_mode
            #machine.deepsleep(1000)
            
            freq(20000000) # reduce to 20MHz
            Touch.Gestures = 0
            while Touch.Gestures != GUESTER_CLICK:
                time.sleep(0.1)
            freq(125000000) # restore to 125MHz
            
            LCD.write_cmd(0x11)#wake up from sleep_mode
            LCD.set_bl_pwm(30000)#enable backlight

class SetDateTime(App):
    def __init__(self)->None:
        self.time_index = 0
        self.last_time = time.ticks_ms()
        self.newtime = list(rtc.datetime())
        self.time_change_mode = False
        self.description = [
            "year:",
            "month:",
            "day:",
            "day of week:",
            "hour:",
            "minute:",
            "secound:",
            "day of year:",

        ]
    def setup(self)->None: 
        self.newtime = list(rtc.datetime())
        self.time_index = 0
        self.time_change_mode = False

    def update_display(self)->None:
        LCD.fill(LCD.black) 
        LCD.write_text_vertical(str(self.description[self.time_index]),[120,80],2,LCD.white,None,center=True)
        LCD.write_text_vertical(str(self.newtime[self.time_index]),[120,120],5,LCD.white,None,center=True)
        LCD.show()
    def start_screen(self)->None:
        LCD.fill(LCD.black) 
        LCD.write_text_vertical("Change",[120,100],3,LCD.white,None,center=True)
        LCD.write_text_vertical("Time",[120,140],3,LCD.white,None,center=True)
        LCD.show()
    def error_screen(self):
        LCD.fill(LCD.black) 
        LCD.write_text_vertical("Error",[120,120],3,LCD.red,None,center=True)
        LCD.show()

    def loop(self)->None:
        if(self.time_change_mode):
            self.last_time = wait_until_time_passed(100,self.last_time)
            self.update_display()
            #canging value with up and down guesters
            if is_gester(GUESTER_DOWN):
                self.newtime[self.time_index] += 1
            if is_gester(GUESTER_UP):
                self.newtime[self.time_index] -= 1
            #next time setting
            if is_gester(GUESTER_CLICK):
                self.time_index += 1
                if self.time_index >= len(self.newtime):
                    try:
                        rtc.datetime(self.newtime)
                    except:
                        self.error_screen()
                        time.sleep(1)
                    self.time_index = 0
                    self.time_change_mode = False
        else:
            self.start_screen()
            if is_gester(GUESTER_CLICK):
                self.newtime = list(rtc.datetime())
                self.time_change_mode = True

Apps = [Clock(),SetDateTime(),DOF_READ(),Ploty(),StepCounter()]

def run_apps():
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

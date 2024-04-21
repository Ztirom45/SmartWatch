from machine import Pin,I2C,SPI,PWM,Timer,ADC,freq
import framebuf
import time

Vbat_Pin = const(29)
FULL_BATTERY = const(4.01)
EMPTY_BATTERY = const(3.4)
RANGE_BATTERY = const(0.61)#FULL_BATTERY-EMPTY_BATTERY
CONSVERSION_FACTOR = 3 * 3.3 / 65535
Vbat = ADC(Vbat_Pin)


starttime = time.ticks_ms()
def wait_until_time_passed(wait_time:float,last_time:float)->float:
    """
        a function that waits until time `ms` passed,
        so a code can do stuff for example every secound 
        and not sleep(1s)+time the code needs to be excuted
        code written by Ztirom45
        use it like this: `last_time = wait_until_secounds_passed(100,last_time)`
        LICENSE: GPL4
    """
    expected_time = wait_time+last_time
    if expected_time > time.ticks_ms():
        #print(expected_time)#for debuging purposes
        time.sleep_ms(expected_time-time.ticks_ms())
    return expected_time


def get_battery_persentage()->float:
    voltage = Vbat.read_u16()*CONSVERSION_FACTOR
    return 100 * (voltage - EMPTY_BATTERY) / RANGE_BATTERY

#setup font
CHAR_SPACE = 32
from font import *

#Pin definition  引脚定义
I2C_SDA = 6
I2C_SDL = 7
I2C_INT = 17
I2C_RST = 16

DC = 8
CS = 9
SCK = 10
MOSI = 11
MISO = 12
RST = 13

BL = 25

#LCD Driver  LCD驱动
class LCD_1inch28(framebuf.FrameBuffer):
    def __init__(self) -> None: #SPI initialization  SPI初始化
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,bits= 8,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        #Define color, Micropython fixed to BRG format  定义颜色，Micropython固定为BRG格式
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.brown =   0X8430
        
        self.fill(self.white) #Clear screen  清屏
        self.show()#Show  显示

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000) #Turn on the backlight  开背光
        
    def write_cmd(self, cmd) -> None: #Write command  写命令
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf) -> None: #Write data  写数据
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
        
    def set_bl_pwm(self,duty) -> None: #Set screen brightness  设置屏幕亮度
        self.pwm.duty_u16(duty)#max 65535
        
    def init_display(self) -> None: #LCD initialization  LCD初始化
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        
        self.write_cmd(0xEF)# Page adress set? (EP[7:0])
        self.write_cmd(0xEB)# ?
        self.write_data(0x14) 

        #Inter Register Enable
        self.write_cmd(0xFE) 
        self.write_cmd(0xEF)

        self.write_cmd(0xEB)
        self.write_data(0x14) 

        self.write_cmd(0x84)
        self.write_data(0x40) 

        self.write_cmd(0x85)
        self.write_data(0xFF) 

        self.write_cmd(0x86)
        self.write_data(0xFF) 

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21) 

        self.write_cmd(0x8A)
        self.write_data(0x00) 

        self.write_cmd(0x8B)
        self.write_data(0x80) 

        self.write_cmd(0x8C)
        self.write_data(0x01) 

        self.write_cmd(0x8D)
        self.write_data(0x01) 

        self.write_cmd(0x8E)
        self.write_data(0xFF) 

        self.write_cmd(0x8F)
        self.write_data(0xFF) 


        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05) 


        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08) 

        self.write_cmd(0xBD)
        self.write_data(0x06)
        
        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11) 

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)


        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 

        self.write_cmd(0xAE)
        self.write_data(0x77)
        
        self.write_cmd(0xCD)
        self.write_data(0x63)


        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E) 
        self.write_data(0x0F) 
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)
    
    #设置窗口    
    def setWindows(self,Xstart,Ystart,Xend,Yend) -> None: 
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend-1)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend-1)
        
        self.write_cmd(0x2C)
     
    #Show  显示   
    def show(self) -> None: 
        self.setWindows(0,0,self.width,self.height)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    '''
        Partial display, the starting point of the local
        display here is reduced by 10, and the end point
        is increased by 10
    '''
    #Partial display, the starting point of the local display here is reduced by 10, and the end point is increased by 10
    #局部显示，这里的局部显示起点减少10，终点增加10
    def Windows_show(self,Xstart,Ystart,Xend,Yend) -> None:
        if Xstart > Xend:
            data = Xstart
            Xstart = Xend
            Xend = data
            
        if (Ystart > Yend):        
            data = Ystart
            Ystart = Yend
            Yend = data
            
        if Xstart <= 10:
            Xstart = 10
        if Ystart <= 10:
            Ystart = 10
            
        Xstart -= 10;Xend += 10
        Ystart -= 10;Yend += 10
        
        self.setWindows(Xstart,Ystart,Xend,Yend)      
        self.cs(1)
        self.dc(1)
        self.cs(0)
        for i in range (Ystart,Yend-1):             
            Addr = (Xstart * 2) + (i * 240 * 2)                
            self.spi.write(self.buffer[Addr : Addr+((Xend-Xstart)*2)])
        self.cs(1)
    
    def write_text_vertical(self,text,pos,size,color,background_color,center=False) -> None:
        """
            this function draws the font from the font.py file vertical
            function written by Ztirom45
            LICENCE: GPL4
            
            parms:
            text
            pos - list y and x  position in pixels
            size - size of the font (pixel size of a char)
            color - color of font
            background color - backgroundcolor of font
        """
        
        if center: pos[0]-=int(len(text)*CHAR_W*size/2)
        else: pos[0]-=len(text)*size*CHAR_W
        char_counter = 0
        for char in list(text)[::-1]:
            if(ord(char)!=CHAR_SPACE):
                #get x position of the char in the image 
                char_pos = (ord(char)-CHAR_SPACE)*CHAR_W
                if char_pos > IMG_W:char_pos = 0
                #draw char
                for x in range(CHAR_W):
                    for y in range(CHAR_H):
                        if(font[y][x+char_pos] == "#"):
                            self.rect(
                                y*size+pos[1],(CHAR_W-x+char_counter)*size+pos[0],size,size,
                                color
                                )
                                
                        elif background_color != None:
                            self.rect(
                                y*size+pos[1],(CHAR_W-x+char_counter)*size+pos[0],size,size,
                                background_color
                                )
            elif background_color!= None:
                self.rect(
                        pos[1],char_counter*size+pos[0],CHAR_W*size,CHAR_H*size,
                        background_color
                        )
            char_counter += CHAR_W
           
        
#Touch drive  触摸驱动
class Touch_CST816T(object):
    """
    Touch drive class
    code form waveshare expample
    modefied by Ztirom45
    """
    #Initialize the touch chip  初始化触摸芯片
    def __init__(self,address=0x15,mode=0,i2c_num=1,i2c_sda=6,i2c_scl=7,int_pin=21,rst_pin=22,LCD=None) -> None:
        self._bus = I2C(id=i2c_num,scl=Pin(i2c_scl),sda=Pin(i2c_sda),freq=400_000) #Initialize I2C 初始化I2C
        self._address = address #Set slave address  设置从机地址
        self.int=Pin(int_pin,Pin.IN, Pin.PULL_UP)     
        self.tim = Timer()     
        self.rst=Pin(rst_pin,Pin.OUT)
        self.Reset()
        self.last_time_pressed = time.time()
        bRet=self.WhoAmI()
        if bRet :
            print("Success:Detected CST816T.")
            Rev= self.Read_Revision()
            print("CST816T Revision = {}".format(Rev))
            self.Stop_Sleep()
        else    :
            print("Error: Not Detected CST816T.")
            return None
        self.Mode = mode
        self.Gestures="None"
        self.Flag = self.Flgh =self.l = 0
        self.X_point = self.Y_point = 0
        self.int.irq(handler=self.Int_Callback,trigger=Pin.IRQ_FALLING)
      
    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    
    def _write_byte(self,cmd,val) -> None:
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))

    def WhoAmI(self) -> bool:
        if (0xB5) != self._read_byte(0xA7):
            return False
        return True
    
    def Read_Revision(self):
        return self._read_byte(0xA9)
      
    #Stop sleeping  停止睡眠
    def Stop_Sleep(self) -> None:
        self._write_byte(0xFE,0x01)
    
    #Reset  复位    
    def Reset(self) -> None:
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)
    
    #Set mode  设置模式   
    def Set_Mode(self,mode,callback_time=10,rest_time=5) -> None: 
        # mode = 0 gestures mode 
        # mode = 1 point mode 
        # mode = 2 mixed mode 
        if (mode == 1):      
            self._write_byte(0xFA,0X41)
            
        elif (mode == 2) :
            self._write_byte(0xFA,0X71)
            
        else:
            self._write_byte(0xFA,0X11)
            self._write_byte(0xEC,0X01)
     
    #Get the coordinates of the touch  获取触摸的坐标
    def get_point(self) -> None:
        xy_point = self._read_block(0x03,4)
        
        x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
        y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
        
        self.X_point=x_point
        self.Y_point=y_point
        
    def Int_Callback(self,pin) -> None:
        self.last_time_pressed = time.time()
        if self.Mode == 0 :
            self.Gestures = self._read_byte(0x01)

        elif self.Mode == 1:           
            self.Flag = 1
            self.get_point()

    def Timer_callback(self,t) -> None:
        self.l += 1
        if self.l > 100:
            self.l = 50

"""
Gyro
code From Waveshare example
"""
class QMI8658(object):
    def __init__(self,address=0X6B):
        self._address = address
        self._bus = I2C(id=1,scl=Pin(I2C_SDL),sda=Pin(I2C_SDA),freq=100_000)
        bRet=self.WhoAmI()
        if bRet :
            self.Read_Revision()
        else    :
            return NULL
        self.Config_apply()

    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    def _read_u16(self,cmd):
        LSB = self._bus.readfrom_mem(int(self._address),int(cmd),1)
        MSB = self._bus.readfrom_mem(int(self._address),int(cmd)+1,1)
        return (MSB[0] << 8) + LSB[0]
    def _write_byte(self,cmd,val) -> None:
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))
        
    def WhoAmI(self) -> bool:
        bRet=False
        if (0x05) == self._read_byte(0x00):
            bRet = True
        return bRet
    def Read_Revision(self):
        return self._read_byte(0x01)
    def Config_apply(self) -> None:
        # REG CTRL1
        self._write_byte(0x02,0x60)
        # REG CTRL2 : QMI8658AccRange_8g  and QMI8658AccOdr_1000Hz
        self._write_byte(0x03,0x23)
        # REG CTRL3 : QMI8658GyrRange_512dps and QMI8658GyrOdr_1000Hz
        self._write_byte(0x04,0x53)
        # REG CTRL4 : No
        self._write_byte(0x05,0x00)
        # REG CTRL5 : Enable Gyroscope And Accelerometer Low-Pass Filter 
        self._write_byte(0x06,0x11)
        # REG CTRL6 : Disables Motion on Demand.
        self._write_byte(0x07,0x00)
        # REG CTRL7 : Enable Gyroscope And Accelerometer
        self._write_byte(0x08,0x03)

    def Read_Raw_XYZ(self):
        xyz=[0,0,0,0,0,0]
        raw_timestamp = self._read_block(0x30,3)
        raw_acc_xyz=self._read_block(0x35,6)
        raw_gyro_xyz=self._read_block(0x3b,6)
        raw_xyz=self._read_block(0x35,12)
        timestamp = (raw_timestamp[2]<<16)|(raw_timestamp[1]<<8)|(raw_timestamp[0])
        for i in range(6):
            # xyz[i]=(raw_acc_xyz[(i*2)+1]<<8)|(raw_acc_xyz[i*2])
            # xyz[i+3]=(raw_gyro_xyz[((i+3)*2)+1]<<8)|(raw_gyro_xyz[(i+3)*2])
            xyz[i] = (raw_xyz[(i*2)+1]<<8)|(raw_xyz[i*2])
            if xyz[i] >= 32767:
                xyz[i] = xyz[i]-65535
        return xyz
    def Read_XYZ(self):
        xyz=[0,0,0,0,0,0]
        raw_xyz=self.Read_Raw_XYZ()  
        #QMI8658AccRange_8g
        acc_lsb_div=(1<<12)
        #QMI8658GyrRange_512dps
        gyro_lsb_div = 64
        for i in range(3):
            xyz[i]=raw_xyz[i]/acc_lsb_div#(acc_lsb_div/1000.0)
            xyz[i+3]=raw_xyz[i+3]*1.0/gyro_lsb_div
        return xyz


#geuesters from the watch wearer perspective
GUESTER_UP = const(0x03)#const(0x01)
GUESTER_DOWN = const(0x04)#const(0x02)
GUESTER_LEFT = const(0x02)#const(0x03)
GUESTER_RIGHT = const(0x01)#const(0x04)
GUESTER_CLICK = const(0x05)
GUESTER_LONG_PRESS = const(0x0C)
GUESTER_DOUBLE_CLICK = const(0x0B)

#ask for guester function
def is_gester(gester) -> bool:
    if(Touch.Gestures == gester):
        Touch.Gestures = 0
        time.sleep(0.01)
        return True
    return False

LCD = LCD_1inch28()
LCD.set_bl_pwm(30000)

Touch=Touch_CST816T(mode=1,LCD=LCD)
gyro = QMI8658()



#notes
_R = 0
_B0 = 31 
_C1 = 33 
_CS1 = 35 
_D1 = 37 
_DS1 = 39 
_E1 = 41 
_F1 = 44 
_FS1 = 46 
_G1 = 49 
_GS1 = 52 
_A1 = 55 
_AS1 = 58 
_B1 = 62 
_C2 = 65 
_CS2 = 69 
_D2 = 73 
_DS2 = 78 
_E2 = 82 
_F2 = 87 
_FS2 = 93 
_G2 = 98 
_GS2 = 104 
_A2 = 110 
_AS2 = 117 
_B2 = 123 
_C3 = 131 
_CS3 = 139 
_D3 = 147 
_DS3 = 156 
_E3 = 165 
_F3 = 175 
_FS3 = 185 
_G3 = 196 
_GS3 = 208 
_A3 = 220 
_AS3 = 233 
_B3 = 247 
_C4 = 262 
_CS4 = 277 
_D4 = 294 
_DS4 = 311 
_E4 = 330 
_F4 = 349 
_FS4 = 370 
_G4 = 392 
_GS4 = 415 
_A4 = 440 
_AS4 = 466 
_B4 = 494 
_C5 = 523 
_CS5 = 554 
_D5 = 587 
_DS5 = 622 
_E5 = 659 
_F5 = 698 
_FS5 = 740 
_G5 = 784 
_GS5 = 831 
_A5 = 880 
_AS5 = 932 
_B5 = 988 
_C6 = 1047 
_CS6 = 1109 
_D6 = 1175 
_DS6 = 1245 
_E6 = 1319 
_F6 = 1397 
_FS6 = 1480 
_G6 = 1568 
_GS6 = 1661 
_A6 = 1760 
_AS6 = 1865 
_B6 = 1976 
_C7 = 2093 
_CS7 = 2217 
_D7 = 2349 
_DS7 = 2489 
_E7 = 2637 
_F7 = 2794 
_FS7 = 2960 
_G7 = 3136 
_GS7 = 3322 
_A7 = 3520 
_AS7 = 3729 
_B7 = 3951 
_C8 = 4186 
_CS8 = 4435 
_D8 = 4699 
_DS8 = 4978

#song notes
tetris_lead_notes = (
  #part 1
  _E5, _B4, _C5, _D5, _C5, _B4, _A4, _A4, _C5, _E5, _D5, _C5, _B4, _B4, _C5, _D5, _E5, _C5, _A4, _A4, _R,
  _D5, _F5, _A5, _G5, _F5, _E5, _C5, _E5, _D5, _C5, _B4, _B4, _C5, _D5, _E5, _C5, _A4, _A4, _R,

  #part 2
  _E4, _C4, _D4, _B3, _C4, _A3, _GS3, _B3,
  _E4, _C4, _D4, _B3, _C4, _E4, _A4, _A4, _GS4, _R

)

tetris_times = (
  #part 1
  1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
  1.5, 0.5, 1.0, 0.5, 0.5, 1.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,

  #part 2
  2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
  2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.0

)

from machine import *
from time import *


class Speaker():
    def __init__(self,gpio_pin):
        #vars
        self.volume = 32760
        self.BPM = 180#beats per minute
        self.speaker_pin = PWM(Pin(gpio_pin))

    def play_note(self,freq,beats):
        if(freq!=_R):
            self.speaker_pin.duty_u16(self.volume)
            self.speaker_pin.freq(freq)
        else:
            self.speaker_pin.duty_u16(0)
        sleep(beats*60/self.BPM)

    def play_song(self,notes,times):
        for i in range(len(notes)):
            self.play_note(notes[i],times[i])
            
    def deinit(self):
        self.speaker_pin.deinit()
        
    

if __name__ == "__main__":
    mySpeaker = Speaker(28)
    mySpeaker.play_song(tetris_lead_notes,tetris_times)
    mySpeaker.deinit()
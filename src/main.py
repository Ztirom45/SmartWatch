from controler_lib import *
from apps import *

if __name__=='__main__': 
    #setup background processes
    #second_thread = _thread.start_new_thread(track_steps, ())

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


"""
A simple liberry to save data efficent.
Make sure to allow writing stuff to disk in boot.py.

## Features:
- Saving formated data to disk
- exporting data to CVS

### written by: Ztirom45
### LICENCE:    GPL 4.0
"""

sizeOfDataType = 4

filepath = "data.dat"

import struct


#resets / creates datafile
def setupFile():
    global filepath
    with open(filepath,"w"):pass

"""
types are encodet throuw type autodetection.
supported types: int, float
make sure to define the types of the data clerly
"""
encodeData = lambda array:  b"".join([
    struct.pack("i" if type(number)==int else "f", number) for number in array
    ])

getDataDecoder = lambda array:"".join("i" if type(number)==int else "f" for number in array)
decodeData = lambda data,types:[struct.unpack(
    types[int(i/sizeOfDataType)],
    data[i:i+sizeOfDataType])[0] for i in range(0, len(data), sizeOfDataType)
    ]

encodeCVS = lambda array:",".join([str(number) for number in array])+"\n"
def writeToDisk(array):
    global filepath
    with open(filepath,"ab") as file:
        file.write(encodeData(array))

def readFromDisk(decoder): 
    global filepath
    with open(filepath,"rb") as file:
        array = []
        data = True
        while data:
            data = file.read(sizeOfDataType*len(decoder))
            array.append(decodeData(data,decoder))
        return array
        
def writeToCVS(filename:str,array):
    global filepath
    with open(filename,"a") as file:
        file.write(encodeCVS(array))

if __name__ == "__main__":
    setupFile()
    data = [1,1.0,2,2.0]
    writeToDisk(data)
    writeToCVS("data.cvs",data)
    print(readFromDisk(getDataDecoder(data)))


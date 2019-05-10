#importing
import socket
import time
import winsound

#convert to decimal
def _getDecDigit(digit):
    digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for x in range(len(digits)):
        if digit.lower() == digits[x]:
            return(x)
            
#convert to decimal
def hexToDec(hexNum):
    decNum = 0
    power = 0
    
    for digit in range(len(hexNum), 0, -1):
        try:
            decNum = decNum + 16 ** power * _getDecDigit(hexNum[digit-1])
            power += 1
        except:
            return
    return(int(decNum))
    
#ports
UDP_IP = "127.0.0.1"
UDP_PORT = 7000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
#sound
frequency = 2000  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second

#phase 1
print("Calibrating...")
print("Please close your eyes and breathe slowly. Stop when you hear a beep.")
timer = time.clock()
stock = []
benchmark = 0

while True:
    data, addr = sock.recvfrom(1024)
    if 'alpha_absolute' in str(data):
        newData = str(data).split(",")
        newData = newData[1].split("x")
        
        newData = newData[1:]
        outData = []
        for i in newData:
            outData += [hexToDec(i[:-1])]
        
        newerOut = []
        for i in outData:
            if type(i) == int and i>0:
                newerOut += [i]
                
        if len(newerOut) == 0:
            continue
        
        stock += [sum(newerOut)/len(newerOut)]
        
        if time.clock() - timer > 30:
            benchmark = sum(stock)/len(stock)
            timer = time.clock()
            stock = []
            winsound.Beep(frequency, duration)
            break;
print("Calibration complete")

#phase 2
print("Initializing...")
tot = input("How many minutes do you want to focus for?")
time_start = time.clock()

while True:
    data, addr = sock.recvfrom(1024)
    if 'alpha_absolute' in str(data):
        newData = str(data).split(",")
        newData = newData[1].split("x")
        
        newData = newData[1:]
        outData = []
        for i in newData:
            outData += [hexToDec(i[:-1])]
        
        newerOut = []
        for i in outData:
            if type(i) == int and i>0:
                newerOut += [i]
                
        if len(newerOut) == 0:
            continue
        
        stock += [sum(newerOut)/len(newerOut)]
        
        if time.clock() - timer > 10:
            measure = (sum(stock)/len(stock))/benchmark*100
            if measure>100:
                print("Focused : 100%")
            elif measure>80:
                print("Focused : ",measure,"%")
            elif measure>50:
                print("Semifocused: ",measure,"%")
            else:
                print("Distracted: ",measure,"%")
                winsound.Beep(frequency, duration)
            stock = []
            timer = time.clock()
            if(time.clock()-time_start>tot*60) break;

winsound.Beep(frequency, duration*3)
print("Great work session! Time to take a break!")

import serial
import time
from datetime import datetime
import pytz
import pyfirmata
from os import system
import json


def readArduino(ser, student_names, student_times, current_time, tardy, s_track):
    while read == True:
        tz_NY = pytz.timezone('America/New_York')
        datetime_NY = datetime.now(tz_NY)
        current_time = datetime_NY.strftime("%H%M")
        current_time = int(current_time)
        tardy = int(tardy)
        arduinoData = ser.readline()
        for student in student_names:
            if student in arduinoData:
                if current_time > tardy and current_time > tardy + 0.5:
                    system("cls")
                    ser.write("2")
                    print("\nSorry, you have missed the time to sign-in.")
                    print("\nGo Get a pass Slacker!")
                    print("\n\tRegistry has been saved as Attendance.txt")
                    final = zip(s_track, student_times)
                    save = open("Attendance.txt", "w")
                    save.write(json.dumps(final))
                    time.sleep(5)
                    system("cls")
                elif student not in s_track:
                    if current_time <= tardy:
                        ser.write('1')
                        print("\n"+student+" is on-time. YAY!")
                        student_times.append("on-time")
                        s_track.append(student)
                    elif current_time > tardy and current_time < tardy + 0.5:
                        ser.write("0")
                        print("\n"+student+" is late. BOO!")
                        student_times.append("late")
                        s_track.append(student)
                else:
                    print("\n"+student+" is already marked present.")
                    ser.write("2")
    
##def buttonPressed(arduinoData, student_times, s_track):
    ##if "STOP" in arduinoData:
def timeConvert(milly):
    miliTime = milly
    hours, minutes = miliTime.split(":")
    hours, minutes = int(hours), int(minutes)
    if hours > 12:
        hours -= 12
    return(("%02d%02d") % (hours, minutes))

if __name__ == "__main__":
    system("cls")
    print("\nWelcome to Conor and Jacks attendance system.")
    print("\nScan a card to begin registry. Each card has unique STUDENT name.")
    print("\nWHITE means on time, BLUE means late, and BOTH means error.")
    time.sleep(2)
    ser = serial.Serial('COM4', baudrate = 115200, timeout = 1)
    read = True
    tz_NY = pytz.timezone('America/New_York')
    datetime_NY = datetime.now(tz_NY)
    current_time = datetime_NY.strftime("%H:%M")
    current_time = timeConvert(current_time)
    print("\nCurrent Time is: " +  str(current_time)[:2]+":"+str(current_time)[2:])
    student_names = ["CONOR", "JACK"]
    student_times = []
    s_track = []
    tardy = "0126"
    print("Class begins at: "+ str(tardy)[:2]+":"+str(tardy)[2:])

    readArduino(ser, student_names, student_times, current_time, tardy, s_track)
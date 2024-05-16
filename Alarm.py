import datetime
from time import sleep
import threading
import tkinter as tk
import queue
from playsound import playsound

mylist = []
ran = True
minuteSet = set()

class Popup():
    global minuteSet
    def __init__(self, alarm_name=None, time_h=None, time_m=None):
        global ran
        ran = False
        self.alarm_name = alarm_name
        self.time_h = time_h
        self.time_m = time_m
        minuteSet.add(self.setValue)

        self.alarm = tk.Toplevel()
        label = tk.Label(self.alarm, text=f"{self.alarm_name} {self.time_h}:{self.time_m}", font=("Arial", 32))
        label.pack()
        frame = tk.Frame(self.alarm)
        frame.pack(pady=2, padx=10)

        but1 = tk.Button(frame, text="Pass", command=self.close, font=("Arial", 13))
        but1.grid(row=1, column=0, padx=8)

        but2 = tk.Button(frame, text="Extend", command=self.ExtendPopup, font=("Arial", 13))
        but2.grid(row=1, column=1)
        self.alarm.protocol("WM_DELETE_WINDOW", self.close)

    @property
    def setValue(self):
        return str(f"{self.time_h}, {self.time_m}")

    def close(self):
        global ran
        self.alarm.destroy()
        ran = True
        minuteSet.remove(self.setValue)

    def ExtendPopup(self):
        global ran
        self.alarm.destroy()
        ran = True
        self.queue = queue.Queue()
        ThreadedExend(self.queue).start()
        self.proccesing_extend()

    def proccesing_extend(self):
        try:
            msg = self.queue.get_nowait()
            minuteSet.remove(self.setValue)
            
            #Adding 5 minutes to the time_m and time_h values
            if (self.time_m + 5) > 60:
                self.time_m = self.time_m - 55
                if (self.time_h + 1) > 12:
                    self.time_h = 0
                else:
                    self.time_h += 1
            else:
                self.time_m += 5

            self.__init__(self.alarm_name, self.time_h, self.time_m)
            minuteSet.add(self.setValue)
            

        except queue.Empty:
            self.alarm.after(100, self.proccesing_extend)


class ThreadedExend(threading.Thread):
    def __init__(self, queue):
        super().__init__(daemon=True)
        self.queue = queue
    def run(self) -> None:
        sleep(300)
        self.queue.put("Done")


class Alarm():
    def __init__(self, name, hours, minutes, day, state, id):
        self.name = name
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.state = state
        self.day = day
        self.id = id

        mylist.append(self)

    def __str__(self):
        return f"{self.name} {self.hours}:{self.minutes}, state:{self.state}, id{self.id}"

    @staticmethod
    def delete(id):
        for n in range(len(mylist)):
            if mylist[n].id == id:
                deleted = mylist.pop(n)
                
                break

#Create a thread function which will run until the program is closed
def alarm(extend=True):
    global minuteSet
    global ran
    
    #Add an variable to the list which will just add minutes when alarm is extended
    minutes_counter = 0
    while True:
        if ran == True:
            sleep(1)
            for i in mylist:            
                #Checking if any of alarms in Alarm class is trigered
                if i.state == True:
                    if i.hours == datetime.datetime.now().hour:
                        if i.minutes == datetime.datetime.now().minute:
                            if datetime.datetime.now().weekday() in i.day or i.day == []:
                                if str(f"{datetime.datetime.now().hour}, {datetime.datetime.now().minute}") not in minuteSet:
                                    Popup(alarm_name=i.name, time_h=i.hours, time_m=i.minutes)
                                sleep(60 - datetime.datetime.now().second)
                                
            sleep(60 - datetime.datetime.now().second)


def playSound():
    global ran
    while True:
        if ran == False: playsound("./media/alarms/song.wav", block=True)



talarm = threading.Thread(target=alarm)
talarm.daemon = True
tsound = threading.Thread(target=playSound)
tsound.daemon = True


if __name__ == "__main__":
    talarm.daemon = False
    Popup(alarm_name="SUI", time_h=10, time_m=15)

talarm.start()
tsound.start()
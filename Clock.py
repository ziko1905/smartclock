from threading import Timer
import datetime
import threading
import time

class Clock:
    def __init__(self):
        self.alrm_lst = [[],[],[],[]]
        t1 = threading.Thread(target=self.alarm)
        t2 = threading.Thread(target=self.current_time)

        t1.start()
        self.main()

    def main(self):
        inp = None
        inp2 = None


        if self.alrm_lst == [[],[],[],[]]:
            print("You don't have alarm yet!")
            inp = input("To set a new alarm input 1: ")

        if inp == "1":
            self.set_alarm()

        if self.alrm_lst != [[],[],[],[]]:
            inp2 = input("To set a new alarm input 1 to check list of alarms input 2: ")

        if inp2 == "1":
            self.set_alarm()

        elif inp2 == "2":
            self.list_of_alarms()

        self.main()
        

    @staticmethod
    def current_time():
        # print(datetime.datetime.now().strftime("%H:%M:%S"), end= '\r')
        # Timer(1, self.current_time).start()
        return datetime.datetime.now().strftime("%H:%M:%S")

    def set_alarm(self):
        print("\n" + "Input name of hours and minutes(in form: 00:00):")
        hm_list = input().split(":")
        h = int(hm_list[0])
        m = int(hm_list[1])
        days = input().split(",")
        if days != [""]:
           days = [int(i) for i in days]
        print(days)

        self.new_alarm(h, m, days)
        

    def new_alarm(self, hours, minutes, days, note=None):
        self.alrm_lst[0].append(hours)
        self.alrm_lst[1].append(minutes)
        if note != None:
            self.alrm_lst[2].append(note)
        self.alrm_lst[3].append(days)

       #print(self.alrm_lst)
        #self.alrm_lst[0].sort()
        #self.alrm_lst[1].sort()
        #print(self.alrm_lst)

    def list_of_alarms(self):
        for z in range(len(self.alrm_lst[0])):
            print(str(self.alrm_lst[0][z]) + ":" + str(self.alrm_lst[1][z]))

    #Check if it is right day of the week
    def is_weekday(self):
        for i in range(len(self.alrm_lst[3])):
            for n in range(len(self.alrm_lst[3][i])):
                if self.alrm_lst[3][i][n] == datetime.datetime.now().weekday():
                    return True

    def is_time(self, z):
        if self.is_weekday() == True or self.alrm_lst[3][z] == [""]:
            if self.alrm_lst[0][z] == datetime.datetime.now().hour and self.alrm_lst[1][z] == datetime.datetime.now().minute:
                return True 
        else:
            return False

    def alarm(self):
        while True:
            for z in range(len(self.alrm_lst[1])):
                if self.is_time(z) == True:
                    print("\nAlarm!!!")
                    time.sleep(5)


if __name__ == "__main__":
    t = Clock()

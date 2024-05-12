import tkinter as tk
from tkinter import ttk
from tkinter import *

class AddAlrm():
    def __init__(self, add=True, h=00, m=00, statePar=True):
        self.h = h
        self.m = m
        self.win = tk.Toplevel()      
        self.win.geometry("400x400")
        self.win.resizable(False, False)
        self.win.title("Add alarm")
        add_alarm_lab = tk.Label(self.win, text="Add Alarm", font=("Arial", 15), pady=5)
        add_alarm_lab.pack(padx=0, pady=10)

        self.time24h()
        self.week_days()
        
        self.stateBol = statePar
        self.state_button = tk.Button(self.win, font=("Arial", 14), command=self.state)

        if self.stateBol == True:
            self.state_button.config(text="On", bg="#3D485C", fg="white")
        else:
            self.state_button.config(text="Off", bg="white", fg="black")
        self.state_button.pack(pady=10)        

        self.alrm_name()
        self.confirm_button()

        if add == True:
            self.win.wait_window()

    #Creating hours and minutes input boxes, adding the values to 0-23, 0-59 and insertign defualt values 00:00
    def time24h(self):
        frame24 = tk.Frame(self.win)
        frame24.pack()
        text = ["hours", "minutes"]
        counter = 0

        for _ in text:
            tmp = tk.Label(frame24, font=("Arial", 10), text=_)
            tmp.grid(row=0, column=counter)
            counter += 2

        self.hoursbox = ttk.Combobox(frame24, font=("Arial", 20), height=1, width=3)
        self.hoursbox['values'] = listofnumbs(24)
        self.hoursbox.current(self.h)
        self.hoursbox.grid(row=1, column=0)

        self.minutesbox = ttk.Combobox(frame24, font=("Arial", 20), height=1, width=3)
        self.minutesbox['values'] = listofnumbs(60)
        self.minutesbox.current(self.m)
        self.minutesbox.grid(row = 1, column=2)

        dbl_bracket = tk.Label(frame24, font=("Arial", 20), text=":")
        dbl_bracket.grid(row = 1, column=1)

    #This funcition creates week buttons and week label and also dictate commands to list
    def week_days(self, days_selected = "Every day"):
        self.days_selected = days_selected
        self.days_text = tk.Label(self.win, text="Days selected: Every day", font=("Arial", 10), fg="gray")
        self.days_text.pack()
        weekframe = tk.Frame(self.win)
        weekframe.pack(padx=10, pady=10)
        self.week = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]
        self.week_list = [0 for x in range(7)]
        self.on_off = [0 for x in range(7)]

        for i in range(len(self.week)):
            self.week_list[i] = tk.Button(weekframe, text=self.week[i], command=lambda i=i: self.week_buttons(i), font=("Arial", 12), width=4, bg="white")
            self.week_list[i].grid(row=1, column=i, padx=3)

    def week_buttons(self, i):

        #Checks if button is seleced or deselected and selects it or deselcts it
        if self.on_off[i] == 0:
            self.week_list[i].configure(bg="#3D485C", fg = "white")
            self.on_off[i] = 1
        else:
            self.week_list[i].configure(bg="white", fg = "black")
            self.on_off[i] = 0
        
        days = []

        #Checks what number of buttons is pressed and than calls lable changing function
        if not 1 in self.on_off:
            self.week_label()
        elif self.on_off == [1, 1, 1, 1, 1, 1, 1]:
            self.week_label()
        elif self.on_off.count(1) == 1:
            days.append(self.week[self.on_off.index(1)])
            first = f"{days[0]}"
            self.week_label(first)
        else:
            for i in range(len(self.on_off)):
                if self.on_off[i] == 1:
                    days.append(self.week[i])
                    self.week_label(days_selected=days)

    def week_label(self, days_selected = "Every day"):
        self.days_selected = days_selected
        if self.days_selected != "Every day":
            if len(self.days_selected) > 1 and type(self.days_selected) == list:
                days_list =  self.days_selected
                self.days_selected = ", "
                self.days_selected = self.days_selected.join(days_list)
        

                
        self.days_text.configure(text=f"Days selected: {self.days_selected}")

    def alrm_name(self):
        frame1 = tk.Frame(self.win)
        frame1.pack(pady=10)

        name_lab = tk.Label(frame1, text="Alarm name:", font=("Arial", 12))
        name_lab.grid(row=0, column=0)

        self.textbox = tk.Entry(frame1, font=("Arial", 14), width=10,)
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.grid(row=0, column=1)

    def state(self):
        if self.stateBol == True:
            self.stateBol = False
            self.state_button.config(bg="white", fg="black", text="Off")
        else:
            self.stateBol = True
            self.state_button.config(text="On", bg="#3D485C", fg="white")

    def confirm_button(self):
        btn1 = tk.Button(self.win,text="Confirm", command=self.get_values, font=("Arial", 16))
        btn1.pack(padx=10, pady=10)

    #Enter pressing function on name textbox
    def shortcut(self, event):
        if event.keysym == "Return" and event.state == 8:
            self.get_values()


    #Returns and sorts inputed values in a dictionary
    def get_values(self):
        useable_week = []

        for i in range(len(self.on_off)):
            if self.on_off[i] == 1:
                useable_week.append(i)
            i += 1

        if self.stateBol == True:
            useable_state = "On"
        else:
            useable_state = "Off"
        
        self.ret_dict = {"name": self.textbox.get(),
                    "time": [self.hoursbox.get(), self.minutesbox.get()],
                    "week_days": useable_week,
                    "fancy_week_days": self.days_selected,
                    "state": self.stateBol,
                    "fancy_state": useable_state}

        self.win.destroy()
        self.values = self.ret_dict


class EditAlarm(AddAlrm):
    def __init__(self, name, hours, minutes, buttons_state, state, add=False):
        super().__init__(add, h=int(hours), m=int(minutes), statePar=state)
        self.win.title("Edit alarm")
        self.button_colour(buttons_state=buttons_state)
        self.on_off = buttons_state
        days=[]
        
        if self.on_off.count(1) == 1:
            days.append(self.week[self.on_off.index(1)])
            first = f"{days[0]}"
            self.week_label(first)
        
        elif self.on_off == [1, 1, 1, 1, 1, 1, 1]:
            self.week_label()
            
        else:
            for i in range(len(self.on_off)):
                if self.on_off[i] == 1:
                    days.append(self.week[i])
                    self.week_label(days_selected=days)

    
        self.textbox.insert(0, name)
        self.win.wait_window()

    def button_colour(self, buttons_state=None):
        for i in range(len(buttons_state)):
            if buttons_state[i] == 1:
                self.week_list[i].configure(bg="#3D485C", fg = "white")



def listofnumbs(n):
        list = [str(i) for i in range(n)]
        for i in range(10):
            if len(list[i]) < 2:
                num = list[i]
                list[i] = "0" + num
        return list


#Finish returning values for tree


if __name__ == "__main__":
    a = AddAlrm()


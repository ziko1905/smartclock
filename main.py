import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Clock import Clock
import AlrmButtons
import Alarm

class AlarmItems():
    def __init__(self, name, hours, minutes, days, fancy_days, state, fancy_state, id):
        self.name = name
        self.hours = hours
        self.minutes = minutes
        self.days = days
        self.fancy_days = fancy_days
        self.buttons_list = [0 for n in range(7)]
        self.state = state
        self.fancy_state = fancy_state
        self.id = id

        for n in self.days:
            self.buttons_list[n] = 1

        Alarm.Alarm(self.name, self.hours, self.minutes, self.days, self.state, self.id)
        
    def change(self, name, hours, minutes, days, fancy_days, state, fancy_state, id):
        self.__init__(name, hours, minutes, days, fancy_days, state, fancy_state, id)



class Current_Time():
    def __init__(self):
        self.ran = 0
        self.clock_now()

    def clock_now(self):
        if self.ran == 0:
            self.current = tk.Label(root, text=(), font=("Arial", 50))
            self.current.pack(pady=20)
            self.ran = 1
        self.current.after(1000, self.update_clock)

    def update_clock(self):
        self.current.config(text=Clock.current_time())
        self.clock_now()


count = 0
switch = False
items_list = []

def add_alarm():
    global switch
    global count
    global items_list

    if switch == False:
        switch = True
        try:
            a = AlrmButtons.AddAlrm()
            items_list.append(AlarmItems(a.values["name"], a.values["time"][0], a.values["time"][1], a.values["week_days"], a.values["fancy_week_days"], a.values["state"], a.values["fancy_state"], count))

            my_tree.insert(parent="", index="end", iid=count-1, text="", values=(a.values["name"], f"{a.values['time'][0]}:{a.values['time'][1]}", a.values["fancy_week_days"], a.values["fancy_state"]))
            count += 1


        except Exception:
            pass

        switch = False

    else:
        messagebox.showerror(title="Window running", message="Another window is running, finish or close that window first create an alarm!")

    
def edit_alarm():
    global switch
    global items_list

    if switch == False:
        switch = True
        try:
            id = int(my_tree.focus()) + 1
            for n in range(len(items_list)):
                if items_list[n].id == id:
                    selected = items_list[n]
            e = AlrmButtons.EditAlarm(selected.name, selected.hours, selected.minutes, selected.buttons_list, selected.state)
            selected.__init__(e.values["name"], e.values['time'][0], e.values['time'][1], e.values["week_days"], e.values["fancy_week_days"], e.values["state"], e.values["fancy_state"], id)

            my_tree.item(id-1, values=(selected.name, f"{selected.hours}:{selected.minutes}", selected.fancy_days, selected.fancy_state))


        except ValueError:
            messagebox.showerror(title="Select alarm", message="Please select alarm you want to edit.")

        except Exception:
            pass

            
        switch = False

    else:
        messagebox.showerror(title="Window running", message="Another window is running, finish or close that window first edit an alarm!")

def remove():
    global switch
    global items_list
    if switch == False:
        try:
            selected = my_tree.focus()
            
            

            if messagebox.askyesno(title="Are you sure?", message=f"Are you sure you want to delete {my_tree.item(selected)['values'][0]} alarm?"):
                my_tree.delete(selected)    
                for n in range(len(items_list)):
                    if items_list[n].id == int(selected) + 1:
                        deleted = items_list.pop(n)
                        Alarm.Alarm.delete(int(selected) + 1)
                        break
                        

            
                
        except IndexError:
            messagebox.showerror(title="Select alarm", message="Please select alarm you want to delete.")

    else:
        messagebox.showerror(title="Window running", message="Another window is running, finish or close that window first to delete an alarm!")
            



root = tk.Tk()

root.geometry("600x650")
root.resizable(False, False)
root.title("Alarm Clock")

Current_Time()

my_tree= ttk.Treeview(root, selectmode=tk.BROWSE)

my_tree["columns"] = ("Name", "Time", "Day/s of week", "On/Off")
my_tree.column("#0", anchor="w", width=0, stretch="NO")
my_tree.column("Name", anchor="w", width=100)
my_tree.column("Time", anchor="center", width=60)
my_tree.column("Day/s of week", anchor="center", width=160)
my_tree.column("On/Off", anchor="center", width=88)

my_tree.heading("#0", anchor="w")
my_tree.heading("Name", text="Name", anchor="w")
my_tree.heading("Time", text="Time", anchor="center")
my_tree.heading("Day/s of week", text="Day/s of week", anchor="center")
my_tree.heading("On/Off", text="On/Off", anchor="center")

my_tree.pack(padx=20, pady=20)


add_frame = Frame(root)
add_frame.pack(pady=20)

custom_font = ("Arial", 12)
custom_height = 2
custom_width = 35


add_alarm = Button(add_frame, text="Add alarm", font=custom_font, command=add_alarm, height=custom_height, width=custom_width)
add_alarm.grid(row=0, column=0, pady=7)

edit_alarm = Button(add_frame, text="Edit alarm", font=custom_font, height=custom_height, width=custom_width, command=edit_alarm)
edit_alarm.grid(row=1, column=0, pady=7)

delete_alarm = Button(add_frame, text="Delete alarm", font=custom_font, height=custom_height, width=custom_width, command=remove)
delete_alarm.grid(row=2, column=0, pady=7)




root.mainloop()

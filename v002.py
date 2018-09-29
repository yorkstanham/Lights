import tkinter as tk
from Tkinter import *
from decimal import Decimal
from select import select
import re

class Demo1:
    def __init__(self, master):
        self.master = master
        self.newWindowCreated = False
        self.screenWidth = Decimal(root.winfo_screenwidth())
        self.screenHeight = Decimal(root.winfo_screenheight())
        self.x_centre = 150
        self.y_centre = 100
        self.time = 60;


        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.button1 = tk.Button(self.frame, text = 'Start', width = 25, command = self.new_window)
        self.start_controller_one = tk.Button(self.frame, text='Connect Remotes', command=self.getDevices, fg="white", bg="black")
        self.e = Entry(self.frame,justify='center')
        self.e.insert(0, '01:03')

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

        self.button1.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.start_controller_one.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.e.grid(row=0, column=2, sticky=tk.W + tk.E)

        self.home_canvas = Canvas(root, width=self.screenWidth/2, height=self.screenHeight/2, highlightthickness=0)
        self.home_canvas.configure(background="#FFFFFF")
        self.home_canvas.pack()
        

    def new_window(self):
        if not self.newWindowCreated:

            ########## PROPERTIES ##########
            self.continue_bar_loaded = False
            self.continue_break_timer = False
            self.newWindowCreated = True
            self.timerFont = "helvetica 600"
            self.x_centre = Decimal(self.screenWidth)/2
            self.x_quarter = Decimal(self.screenWidth)/4
            self.y_centre = Decimal(self.screenHeight)/2
            self.y_quarter = Decimal(self.screenHeight)/4
            ########## PROPERTIES ##########

            ########## BUTTON MAPPING ##########
            self.white_btton_clicked = 304
            self.red_button_clicked = 306
            self.bar_loaded_clicked = 305
            self.break_timer_clicked = 307
            ########## BUTTON MAPPING ##########

            self.newWindow = Toplevel(bg="black")
            self.button_frame = tk.Frame(self.newWindow)
            self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)
            self.bar_loaded = tk.Button(self.button_frame, text='Bar Loaded', command=self.bar_loaded_manager, fg="white", bg="black")
            self.bar_loaded.pack()
            self.stop_bar_loaded_button = tk.Button(self.button_frame, text='Stop bar loaded timer', command=self.stop_bar_loaded, fg="white", bg="black")
            self.stop_bar_loaded_button.pack()
            self.session_break_timer = tk.Button(self.button_frame, text='Start break timer', command=self.break_timer_manager, fg="white", bg="black")
            self.session_break_timer.pack()
            self.w = Canvas(self.newWindow, width=self.screenWidth, height=self.screenHeight, highlightthickness=0)
            self.w.configure(background="#000000")
            self.newWindow.attributes('-fullscreen',True)
            self.w.pack(fill=BOTH, expand=1)
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)
            self.button_frame.columnconfigure(2, weight=1)
            self.session_break_timer.grid(row=0, column=0, sticky=tk.W + tk.E)
            self.bar_loaded.grid(row=0, column=1, sticky=tk.W + tk.E)
            self.stop_bar_loaded_button.grid(row=0, column=2, sticky=tk.W + tk.E)
            self.watchRemotes()

    def getDevices(self):
        self.home_canvas.create_text(self.screenWidth/4, self.screenHeight/10, fill="black", width="1000", font="helvetica 40", text="Press the bar loaded button", tag="bar_loaded_instructions")
        self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*2/10, fill="black", width="1000", font="helvetica 40", text="Press the bar loaded button", tag="bar_loaded_instructions")
        self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*3/10, fill="black", width="1000", font="helvetica 40", text="Press the bar loaded button", tag="bar_loaded_instructions")
        self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*4/10, fill="black", width="1000", font="helvetica 40", text="Press the bar loaded button", tag="bar_loaded_instructions")
        self.devicePaths = []
        self.deviceList = [evdev.InputDevice(path) for path in evdev.list_devices()]
        print(self.deviceList)
        for device in self.deviceList:
            self.deviceName = (str(device.name))
            if self.deviceName == 'AB Shutter3' or self.deviceName == 'Adafruit-bluefruit LE':
                self.devicePaths.append(device.path)
        
        print(self.devicePaths)
        
        if not self.devicesFound:

            self.devices = map(InputDevice, (self.devicePaths[0], self.devicePaths[1], self.devicePaths[2], self.devicePaths[3]))
            self.devices = {dev.fd: dev for dev in self.devices}
            for dev in self.devices.values(): 
                print(dev)

            self.r1 = self.devices.keys()[0]
            self.r2 = self.devices.keys()[1]
            self.r3 = self.devices.keys()[2]
            self.r4 = self.devices.keys()[3]
            
            print(self.r1)
            print(self.r2)
            print(self.r3)
            print(self.r4)

            self.identify_timer_remote()
            self.identifyRemoteOne()
            self.identifyRemoteTwo()
            self.identifyRemoteThree()
            self.devicesFound = True

    def identify_timer_remote(self):
        print("Looking for timer remote")
        while True:
            self.home_canvas.create_text(self.screenWidth/4, self.screenHeight/10, fill="white", width="1000", font="helvetica 40", text="Press the bar loaded button", tag="bar_loaded_instructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == self.triangleBtn and self.devicesFound == False:
                            self.r_c1 = fd
                            print("r_t1 = " + str(self.r_c1))
                            self.home_canvas.delete("bar_loaded_instructions")
                            self.home_canvas.create_text(self.screenWidth/4, self.screenHeight/10, fill="white", width="800", font="helvetica 30", text="Timer controller connected",tag="confirmConnection")
                            root.update()
                            return
    
    def identifyRemoteOne(self):
        print("Looking for remote one")
        while True:
            self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*2/10, fill="white", width="1000", font="helvetica 40", text="Press the white light on the left judge's control", tag="RemoteOneInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == self.triangleBtn and self.devicesFound == False:
                            if fd != self.r_c1:
                                self.r_c2 = fd
                                print("r_c2 = " + str(self.r_c2))
                                self.home_canvas.delete("RemoteOneInstructions")
                                self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*2/10, fill="white", width="800", font="helvetica 30", text="Remote One Connected",tag="confirmConnection")
                                root.update()
                                return
    
    def identifyRemoteTwo(self):
        print "looking for remote 2"
        while True:
            self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*3/10, fill="white", width="1000", font="helvetica 40", text="Press the white light on the centre judge's control", tag="RemoteTwoInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            print(r)
            for fd in r:
                print(fd)
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == self.triangleBtn and self.devicesFound == False:
                            print fd
                            if fd != self.r_c1 and fd != self.r_c2:
                                self.r_c3 = fd
                                print("r_c3 = " + str(self.r_c3))
                                self.home_canvas.delete("RemoteTwoInstructions")
                                self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*3/10, fill="white", width="800", font="helvetica 30", text="Remote Two Connected", tag="confirmConnection")
                                root.update()
                                event.code = 25
                                return

    def identifyRemoteThree(self):
        print "looking for remote 3"
        while True:
            self.w.create_text(self.screenWidth/4, self.screenHeight*4/10, fill="white", width="1000", font="helvetica 40", text="Press the white light on the right judge's control", tag="RemoteThreeInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                print(fd)
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == self.triangleBtn and self.devicesFound == False:
                            print fd
                            if fd != self.r_c1 and fd != self.r_c2 and fd != self.r_c3:
                                self.r_c4 = fd
                                print("r_c4 = " + str(self.r_c4))
                                self.home_canvas.delete("RemoteThreeInstructions")
                                self.home_canvas.create_text(self.screenWidth/4, self.screenHeight*4/10, fill="white", width="800", font="helvetica 30", text="Remote Three Connected", tag="confirmConnection")
                                root.update()
                                event.code = 25
                                return

    def watchRemotes(self):
        print("WATCHING REMOTES")
        while True:
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                        if event.code == self.white_btton_clicked and self.watchForDecisions == True:
                            if fd == self.r_c2:
                                self.judgeOneChosenWhite()
                                return
                            elif fd == self.r_c3:
                                self.judgeTwoChosenWhite()
                                return
                            elif fd == self.r_c4:
                                self.judgeThreeChosenWhite()
                                return
                        elif event.code == self.red_button_clicked and self.watchForDecisions == True:
                            if fd == self.r_c2:
                                self.judgeOneChosenRed(color1="red")
                                return
                            elif fd == self.r_c3:
                                self.judgeTwoChosenRed(color2="red")
                                return
                            elif fd == self.r_c4:
                                self.judgeThreeChosenRed(color3="red")
                        elif event.code == self.bar_loaded_clicked and self.watchForDecisions == False:
                            if fd == self.r_c1:
                                self.bar_loaded_manager()
                                return
                        elif event.code == self.break_timer_clicked and self.watchForDecisions == False:
                            if fd == self.r_c1:
                                self.break_timer_manager()
                                return

    def parse_countdown_time(self):
        inputString = str(self.e.get())
        self.minutes = re.search('^(.*?)(?=\\:)',inputString)
        self.seconds = re.search('(\\d)*$',inputString)

        self.minutes = self.minutes.group(0)
        self.seconds = self.seconds.group(0)

        if self.seconds == '00':
            self.seconds = '60'

        countdown_time_array = [self.minutes, self.seconds]
        return countdown_time_array

    def break_timer_manager(self):
        if self.continue_break_timer:
            self.continue_break_timer = False
            self.stop_break_timer()
        elif not self.continue_break_timer:
            self.continue_break_timer = True
            self.init_break_timer()        

    def init_break_timer(self):
        self.minutes_for_timer = int(self.parse_countdown_time()[0])
        self.seconds_for_timer = int(self.parse_countdown_time()[1])

        if self.seconds_for_timer == 60:
            self.minutes_for_timer -= 1

        self.w.delete(ALL)
        self.w.create_text(self.x_centre, self.y_centre, fill="white", font=self.timerFont, text="10:00", tag="breakTimer")
        self.break_timer()

    def break_timer(self):
        if self.continue_break_timer:
            
            self.w.delete("breakTimer")

            if self.minutes_for_timer < 1:
                text_colour = 'red'
            elif self.minutes_for_timer < 3:
                text_colour = 'orange'
            else:
                text_colour = 'white'

            if self.seconds_for_timer == 60:
                self.w.create_text(self.x_centre, self.y_centre, fill=text_colour, font=self.timerFont,
                                   text=str(self.minutes_for_timer+1)+':00',
                                   tag="breakTimer")

            elif self.seconds_for_timer <= 9:
                self.w.create_text(self.x_centre, self.y_centre, fill=text_colour, font=self.timerFont,
                                   text=str(self.minutes_for_timer) + ":0" + str(self.seconds_for_timer),
                                   tag="breakTimer")

            else:
                self.w.create_text(self.x_centre, self.y_centre, fill=text_colour, font=self.timerFont,
                                   text=str(self.minutes_for_timer) + ":" + str(self.seconds_for_timer),
                                   tag="breakTimer")

            self.seconds_for_timer -= 1
            
            if self.seconds_for_timer > 0 and self.minutes_for_timer >= 0:
                self.w.after(1000, self.break_timer)

            elif self.seconds_for_timer <= 0 and self.minutes_for_timer >= 0:
                self.minutes_for_timer -= 1
                self.seconds_for_timer = 60
                self.w.after(1000, self.break_timer)

            elif self.seconds_for_timer <= 0 and self.minutes_for_timer <= 0:
                self.w.after(5000, self.w.delete("breakTimer"))

    def stop_break_timer(self):
        self.continue_break_timer = False
        self.w.delete("breakTimer")

    def bar_loaded_manager(self):
        if self.continue_bar_loaded:
            self.stop_bar_loaded()
        elif not self.continue_bar_loaded:
            self.init_bar_loaded()

    def init_bar_loaded(self):

        if not self.continue_bar_loaded:
            self.continue_bar_loaded = True
            self.w.delete("lights", "countdown_time")
            self.time = 60
            self.barLoaded()
        else:
            self.watchRemotes()

    def barLoaded(self):
        
        self.scoresIn = False
        self.watchForDecisions = True
        if self.continue_bar_loaded:
            self.w.delete("lights", "countdown_time")
            if self.time == 60:
                self.w.create_text(self.x_centre, self.y_centre, fill="white", font=self.timerFont, text="1:00", tag="countdown_time")
            elif self.time == 10:
                self.w.create_text(self.x_centre, self.y_centre, fill="red", font=self.timerFont, text="0:" + str(self.time),
                                   tag="countdown_time")
            elif self.time <= 9:
                self.w.create_text(self.x_centre, self.y_centre, fill="red", font=self.timerFont, text="0:0" + str(self.time),
                                   tag="countdown_time")
            else:
                self.w.create_text(self.x_centre, self.y_centre, fill="white", font=self.timerFont, text="0:" + str(self.time),
                                   tag="countdown_time")
            self.time -= 1
            if self.time >= 0 and not self.scoresIn:
                self.clock = self.w.after(1000, self.barLoaded)
            elif self.scoresIn:
                self.w.delete("countdown_time")

    def stop_bar_loaded(self):
        self.continue_bar_loaded = False
        self.w.delete("countdown_time")



def main(): 
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    main()

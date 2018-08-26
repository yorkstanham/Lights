#!/usr/bin/env python
import Tkinter as tk
from Tkinter import *
from decimal import Decimal
import evdev
from evdev import InputDevice, categorize, ecodes
from select import select

class MyFirstGUI:
    def __init__(self, master):
        self.color1 = ""
        self.color2 = ""
        self.color3 = ""
        self.master = master
        self.judgeOne = False
        self.judgeTwo = False
        self.judgeThree = False
        self.time = 60
        self.submissionTimerOneValue = 60
        self.submissionTimerOneValue = 60
        self.scoresIn = False
        self.startSubmissionTimer = False
        self.submissionTimerOneRunning = False
        self.submissionTimerTwoRunning = False
        self.watchForDecisions = True
        self.clock = "ClockRunning"
        self.useCards = False
        self.allResultsIn = False
        self.screenWidth = Decimal(root.winfo_screenwidth())
        self.screenHeight = Decimal(root.winfo_screenheight())

        self.x_centre = Decimal(root.winfo_screenwidth())/2
        self.y_centre = Decimal(root.winfo_screenheight())/2
        self.small_radius = Decimal(root.winfo_screenwidth())/35
        self.large_radius = Decimal(root.winfo_screenwidth())/8

        self.x_left = Decimal(root.winfo_screenwidth())/5
        self.x_right = Decimal(root.winfo_screenwidth())-self.x_left

        self.card_x_radius = self.large_radius/3
        self.card_y_radius = self.large_radius*2/5
        self.card_y_centre = self.screenHeight*5/6

        self.y_submission_text = self.screenHeight*2/30
        self.x_submission_text = self.screenWidth*13/72

        master.title("A better lights system")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.white_one = tk.Button(self.button_frame, text='#1 White', command=self.judgeOneChosenWhite)
        self.red_one = tk.Button(self.button_frame, text='#1 Red', command=lambda: self.judgeOneChosenRed(color1="red"))
        self.blue_one = tk.Button(self.button_frame, text='#1 Blue', command=lambda: self.judgeOneChosenRed(color1="blue"))
        self.yellow_one = tk.Button(self.button_frame, text='#1 Yellow', command=lambda: self.judgeOneChosenRed(color1="yellow"))

        self.white_two = tk.Button(self.button_frame, text='#2 White', command=self.judgeTwoChosenWhite)
        self.red_two = tk.Button(self.button_frame, text='#2 Red', command=lambda: self.judgeTwoChosenRed(color2="red"))
        self.blue_two = tk.Button(self.button_frame, text='#2 Blue', command=lambda: self.judgeTwoChosenRed(color2="blue"))
        self.yellow_two = tk.Button(self.button_frame, text='#2 Yellow', command=lambda: self.judgeTwoChosenRed(color2="yellow"))

        self.white_three = tk.Button(self.button_frame, text='#3 White', command=self.judgeThreeChosenWhite)
        self.red_three = tk.Button(self.button_frame, text='#3 Red', command=lambda: self.judgeThreeChosenRed(color3="red"))
        self.blue_three = tk.Button(self.button_frame, text='#3 Blue', command=lambda: self.judgeThreeChosenRed(color3="blue"))
        self.yellow_three = tk.Button(self.button_frame, text='#3 Yellow', command=lambda: self.judgeThreeChosenRed(color3="yellow"))

        self.bar_loaded = tk.Button(self.button_frame, text='Bar Loaded', command=self.initBarLoaded)
        self.start_controller_one = tk.Button(self.button_frame, text='Connect Remotes', command=self.getDevices)
        self.start_controller_two = tk.Button(self.button_frame, text='Start', command=self.watchRemotes)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.columnconfigure(4, weight=1)
        self.button_frame.columnconfigure(5, weight=1)
        self.button_frame.columnconfigure(6, weight=1)
        self.button_frame.columnconfigure(7, weight=1)
        self.button_frame.columnconfigure(8, weight=1)
        self.button_frame.columnconfigure(9, weight=1)
        self.button_frame.columnconfigure(10, weight=1)
        self.button_frame.columnconfigure(11, weight=1)
        self.button_frame.columnconfigure(12, weight=1)
        self.button_frame.columnconfigure(13, weight=1)
        self.button_frame.columnconfigure(14, weight=1)

        self.white_one.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.red_one.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.blue_one.grid(row=0, column=2, sticky=tk.W + tk.E)
        self.yellow_one.grid(row=0, column=3, sticky=tk.W + tk.E)

        self.white_two.grid(row=0, column=4, sticky=tk.W + tk.E)
        self.red_two.grid(row=0, column=5, sticky=tk.W + tk.E)
        self.blue_two.grid(row=0, column=6, sticky=tk.W + tk.E)
        self.yellow_two.grid(row=0, column=7, sticky=tk.W + tk.E)

        self.white_three.grid(row=0, column=8, sticky=tk.W + tk.E)
        self.red_three.grid(row=0, column=9, sticky=tk.W + tk.E)
        self.blue_three.grid(row=0, column=10, sticky=tk.W + tk.E)
        self.yellow_three.grid(row=0, column=11, sticky=tk.W + tk.E)

        self.bar_loaded.grid(row=0, column=12, sticky=tk.W + tk.E)
        self.start_controller_one.grid(row=0, column=13, sticky=tk.W + tk.E)
        self.start_controller_two.grid(row=0, column=14, sticky=tk.W + tk.E)

        self.w = Canvas(root, width=self.screenWidth, height=self.screenHeight, highlightthickness=0)
        self.w.configure(background="#000000")
        self.w.pack()

        self.xBtn = 304
        self.xBtns = ""
        self.circleBtn = 305
        self.triangleBtn = 307
        self.squareBtn = 308
        self.r_c1 = ""
        self.startedWatching = False
        self.firstRun = True
        self.devicesFound = False
        
    def getDevices(self):
        self.devicePaths = []
        self.deviceList = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in self.deviceList:
            #print(device.path, device.name, device.phys)
            self.deviceName = (str(device.name))
            
            if self.deviceName == 'Wireless Controller':
                #print(self.deviceName)
                self.devicePaths.append(device.path)
                #print(self.devicePaths)
                
        if not self.devicesFound:
            print(self.devicePaths)
            self.devices = map(InputDevice, ('/dev/input/event5', '/dev/input/event8'))
            self.devices = {dev.fd: dev for dev in self.devices}
            for dev in self.devices.values(): print(dev)
            r,w,x = select(self.devices, [], [])
            print(self.devices.keys())
            self.r1 = self.devices.keys()[0]
            self.r2 = self.devices.keys()[1]
            print(self.r1)
            print(self.r2)
            self.devicesFound = True
            self.identifyRemoteOne()
            self.identifyRemoteTwo()
            
    def identifyRemoteOne(self):
        while True:
            self.w.create_text(800, 400, fill="white", width="800", font="helvetica 30", text="Press the white light on the left judge's control", tag="RemoteOneInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == self.triangleBtn:
                            self.r_c1 = fd
                            print("r_c1 = " + str(self.r_c1))
                            self.w.delete("RemoteOneInstructions")
                            self.w.create_text(800, 400, fill="white", width="800", font="helvetica 30", text="Remote One Connected",tag="confirmConnection")
                            root.update()
                            return
    
    def identifyRemoteTwo(self):
        while True:
            #self.w.delete("confirmConnection")
            self.w.create_text(800, 600, fill="white", width="800", font="helvetica 30", text="Press the white light on the centre judge's control", tag="RemoteTwoInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == self.triangleBtn:
                            if fd != self.r_c1:
                                self.r_c2 = fd
                                print("r_c2 = " + str(self.r_c2))
                                self.w.delete("RemoteTwoInstructions")
                                self.w.create_text(800, 600, fill="white", width="800", font="helvetica 30", text="Remote Two Connected", tag="confirmConnection")
                                root.update()
                                event.code = 25
                                return
        
    def watchRemotes(self):
        self.w.delete("confirmConnection")
        while True:
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    #print(event)
                        if event.code == self.xBtn and self.watchForDecisions == True:
                            if fd == self.r_c1:
                                self.judgeOneChosenWhite()
                                #print("Judge One Chose White")
                                return
                            elif fd == self.r_c2:
                                self.judgeTwoChosenWhite()
                                #print("Judge Two Chose White")
                                return
                        elif event.code == self.circleBtn and self.watchForDecisions == True:
                            if fd == self.r_c1:
                                self.judgeOneChosenRed(color1="red")
                                #print("Judge One Chose Red")
                                return
                            elif fd == self.r_c2:
                                self.judgeTwoChosenRed(color2="red")
                                #print("Judge Two Chose Red")
                                return
                        elif event.code == self.squareBtn:
                            if fd == self.r_c1 and self.watchForDecisions == True:
                                self.judgeThreeChosenRed(color3="red")
                                #print("Judge One Chose Red")
                                return
                            elif fd == self.r_c2:
                                print("Bar loaded button pressed")
                                self.initBarLoaded()
                                return
                    
    def judgeOneChosenWhite(self):

        self.x0 = self.x_left - self.small_radius
        self.y0 = self.y_centre - self.small_radius
        self.x1 = self.x_left + self.small_radius
        self.y1 = self.y_centre + self.small_radius

        self.w.delete("countdown_time")
        self.scoresIn = True
        self.w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
        self.judgeOne = True
        self.judgeOneChoice = "white"
        self.displayResults()

    def judgeTwoChosenWhite(self):

        self.x0 = self.x_centre - self.small_radius
        self.y0 = self.y_centre - self.small_radius
        self.x1 = self.x_centre + self.small_radius
        self.y1 = self.y_centre + self.small_radius

        self.w.delete("countdown_time")
        self.scoresIn = True
        self.w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
        self.judgeTwo = True;
        self.judgeTwoChoice = "white"
        self.displayResults()

    def judgeThreeChosenWhite(self):

        self.x0 = self.x_right - self.small_radius
        self.y0 = self.y_centre - self.small_radius
        self.x1 = self.x_right + self.small_radius
        self.y1 = self.y_centre + self.small_radius

        self.w.delete("countdown_time")
        self.scoresIn = True
        self.w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
        self.judgeThree = True;
        self.judgeThreeChoice = "white"
        self.displayResults()

    def judgeOneChosenRed(self,color1):

        self.x0 = self.x_left - self.small_radius
        self.y0 = self.y_centre - self.small_radius
        self.x1 = self.x_left + self.small_radius
        self.y1 = self.y_centre + self.small_radius

        self.w.delete("countdown_time")
        self.scoresIn = True
        self.w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
        self.judgeOne = True;
        self.judgeOneChoice = color1
        self.displayResults()

    def judgeTwoChosenRed(self,color2):

        self.x0 = self.x_centre - self.small_radius
        self.y0 = self.y_centre - self.small_radius
        self.x1 = self.x_centre + self.small_radius
        self.y1 = self.y_centre + self.small_radius

        self.w.delete("countdown_time")
        self.scoresIn = True
        self.w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
        self.judgeTwo = True
        self.judgeTwoChoice = color2
        self.displayResults()

    def judgeThreeChosenRed(self,color3):

        self.x0 = self.x_right - self.small_radius
        self.y0 = self.y_centre - self.small_radius
        self.x1 = self.x_right + self.small_radius
        self.y1 = self.y_centre + self.small_radius

        self.w.delete("countdown_time")
        self.scoresIn = True
        self.w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
        self.judgeThree = True;
        self.judgeThreeChoice = color3
        self.displayResults()

    def displayResults(self):

        self.x0_1_light = self.x_left - self.large_radius
        self.y0_1_light = self.y_centre - self.large_radius
        self.x1_1_light = self.x_left + self.large_radius
        self.y1_1_light = self.y_centre + self.large_radius

        self.x0_1_card = self.x_left - self.card_x_radius
        self.y0_1_card = self.card_y_centre - self.card_y_radius
        self.x1_1_card = self.x_left + self.card_x_radius
        self.y1_1_card = self.card_y_centre + self.card_y_radius

        self.x0_2_light = self.x_centre - self.large_radius
        self.y0_2_light = self.y_centre - self.large_radius
        self.x1_2_light = self.x_centre + self.large_radius
        self.y1_2_light = self.y_centre + self.large_radius

        self.x0_2_card = self.x_centre - self.card_x_radius
        self.y0_2_card = self.card_y_centre - self.card_y_radius
        self.x1_2_card = self.x_centre + self.card_x_radius
        self.y1_2_card = self.card_y_centre + self.card_y_radius

        self.x0_3_light = self.x_right - self.large_radius
        self.y0_3_light = self.y_centre - self.large_radius
        self.x1_3_light = self.x_right + self.large_radius
        self.y1_3_light = self.y_centre + self.large_radius

        self.x0_3_card = self.x_right - self.card_x_radius
        self.y0_3_card = self.card_y_centre - self.card_y_radius
        self.x1_3_card = self.x_right + self.card_x_radius
        self.y1_3_card = self.card_y_centre + self.card_y_radius

        if self.judgeOne == True and self.judgeTwo == True and self.judgeThree == True:

            self.w.delete("greenLight")
            self.watchForDecisions = False

            if self.judgeOneChoice == "white":
                self.w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#FFFFFF", outline="#FFFFFF",tag="lights")
            elif self.judgeOneChoice == "red":
                self.w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_1_card, self.y0_1_card, self.x1_1_card, self.y1_1_card, fill="#ff0000", outline="#ff0000",tag="lights")
            elif self.judgeOneChoice == "blue":
                self.w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#ff0000", outline="#ff0000", tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_1_card, self.y0_1_card, self.x1_1_card, self.y1_1_card, fill="#0000ff", outline="#0000ff", tag="lights")
            elif self.judgeOneChoice == "yellow":
                self.w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#ff0000", outline="#ff0000", tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_1_card, self.y0_1_card, self.x1_1_card, self.y1_1_card, fill="#FFFF00", outline="#FFFF00", tag="lights")

            if self.judgeTwoChoice == "white":
                self.w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#FFFFFF", outline="#FFFFFF",tag="lights")
            elif self.judgeTwoChoice == "red":
                self.w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_2_card, self.y0_2_card, self.x1_2_card, self.y1_2_card, fill="#ff0000", outline="#ff0000", tag="lights")
            elif self.judgeTwoChoice == "blue":
                self.w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_2_card, self.y0_2_card, self.x1_2_card, self.y1_2_card, fill="#0000ff", outline="#0000ff", tag="lights")
            elif self.judgeTwoChoice == "yellow":
                self.w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_2_card, self.y0_2_card, self.x1_2_card, self.y1_2_card, fill="#FFFF00", outline="#FFFF00", tag="lights")

            if self.judgeThreeChoice == "white":
                self.w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#FFFFFF", outline="#FFFFFF",tag="lights")
            elif self.judgeThreeChoice == "red":
                self.w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_3_card, self.y0_3_card, self.x1_3_card, self.y1_3_card, fill="#ff0000", outline="#ff0000", tag="lights")
            elif self.judgeThreeChoice == "blue":
                self.w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_3_card, self.y0_3_card, self.x1_3_card, self.y1_3_card, fill="#0000ff", outline="#0000ff", tag="lights")
            elif self.judgeThreeChoice == "yellow":
                self.w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if self.useCards:
                    self.w.create_rectangle(self.x0_3_card, self.y0_3_card, self.x1_3_card, self.y1_3_card, fill="#FFFF00", outline="#FFFF00", tag="lights")

            self.judgeOne = False
            self.judgeTwo = False
            self.judgeThree = False
            self.allResultsIn = True
            self.time == 60
            print("All scores in")
            self.initScoresIn()
            
        else:
            root.update()
            print("Results are missing")
            self.watchRemotes()
            
    def initScoresIn(self):

        print(self.submissionTimerOneRunning)

        if not self.submissionTimerOneRunning:
            self.submissionTimerOneValue = 60
            self.submissionTimerOne()
        elif self.submissionTimerOneRunning and not self.submissionTimerTwoRunning:
            self.submissionTimerTwoValue = 60
            self.submissionTimerTwo()
        elif self.submissionTimerOneRunning and self.submissionTimerTwoRunning:
            print("Both Timers Are Running")

    def submissionTimerOne(self):

        self.submissionTimerOneRunning = True

        self.w.delete("countdown_time_for_submission_one")

        self.w.create_text(self.x_submission_text, self.y_submission_text, fill="white", width="400", font="helvetica 30", text="Time to submit next attempt:")

        if self.submissionTimerOneValue == 60:
            self.w.create_text(1240, 70, fill="white", font="helvetica 130", text="1:00", tag="countdown_time_for_submission_one")

        elif self.submissionTimerOneValue == 10:
            self.w.create_text(1240, 70, fill="red", font="helvetica 130", text="0:" + str(self.submissionTimerOneValue),
                               tag="countdown_time_for_submission_one")
        elif self.submissionTimerOneValue <= 9:
            self.w.create_text(1240, 70, fill="red", font="helvetica 130", text="0:0" + str(self.submissionTimerOneValue),
                               tag="countdown_time_for_submission_one")
        else:
            self.w.create_text(1240, 70, fill="white", font="helvetica 130", text="0:" + str(self.submissionTimerOneValue),
                               tag="countdown_time_for_submission_one")

        self.submissionTimerOneValue -= 1

        if self.submissionTimerOneValue >= 0:
            self.w.after(1000, self.submissionTimerOne)
        elif self.scoresIn:
            self.submissionTimerOneRunning = False
            self.w.delete("countdown_time_for_submission_one")
            
        self.watchRemotes()

    def submissionTimerTwo(self):

        self.submissionTimerTwoRunning = True

        self.w.delete("countdown_time_for_submission_two")

        if self.submissionTimerTwoValue == 60:
            self.w.create_text(640, 70, fill="white", font="helvetica 130", text="1:00",
                               tag="countdown_time_for_submission_two")

        elif self.submissionTimerTwoValue == 10:
            self.w.create_text(640, 70, fill="red", font="helvetica 130",
                               text="0:" + str(self.submissionTimerTwoValue),
                               tag="countdown_time_for_submission_two")
        elif self.submissionTimerTwoValue <= 9:
            self.w.create_text(640, 70, fill="red", font="helvetica 130",
                               text="0:0" + str(self.submissionTimerTwoValue),
                               tag="countdown_time_for_submission_two")
        else:
            self.w.create_text(640, 70, fill="white", font="helvetica 130",
                               text="0:" + str(self.submissionTimerTwoValue),
                               tag="countdown_time_for_submission_two")

        self.submissionTimerTwoValue -= 1

        if self.submissionTimerTwoValue >= 0:
            self.w.after(1000, self.submissionTimerTwo)
        elif self.scoresIn:
            self.submissionTimerTwoRunning = False
            self.w.delete("countdown_time_for_submission_two")

    def initBarLoaded(self):
        print(self.judgeOne)
        print(self.judgeTwo)
        print(self.judgeThree)
        if self.allResultsIn:
            self.allResultsIn = False
            self.w.after_cancel(self.clock)
            self.w.delete("lights", "countdown_time")
            self.scoresIn = False
            self.time = 60
            self.barLoaded()
        else:
            self.watchRemotes()

    def barLoaded(self):
        print("BAR LOADED STARTING")
        self.watchForDecisions = True
        if not self.scoresIn:
            self.w.delete("lights", "countdown_time")
            if self.time == 60:
                self.w.create_text(700, 400, fill="white", font="helvetica 400 bold", text="1:00", tag="countdown_time")
            elif self.time == 10:
                self.w.create_text(700, 400, fill="red", font="helvetica 400 bold", text="0:" + str(self.time),
                                   tag="countdown_time")
            elif self.time <= 9:
                self.w.create_text(700, 400, fill="red", font="helvetica 400 bold", text="0:0" + str(self.time),
                                   tag="countdown_time")
            else:
                self.w.create_text(700, 400, fill="white", font="helvetica 400 bold", text="0:" + str(self.time),
                                   tag="countdown_time")
            self.time -= 1
            if self.time >= 0 and not self.scoresIn:
                self.clock = self.w.after(1000, self.barLoaded)
            elif self.scoresIn:
                self.w.delete("countdown_time")

root = Tk()
gui = MyFirstGUI(root)
'''watchControllerOne = multiprocessing.Process(name="watchControllerOne", target=gui.getGamePadValueOne)
watchControllerTwo = multiprocessing.Process(name="watchControllerTwo", target=gui.getGamePadValueTwo)
watchControllerOne.start()
watchControllerTwo.start()'''
my_gui = MyFirstGUI(root)
#root.geometry("500x500")
root.configure(background='black')
root.overrideredirect(True)
root.overrideredirect(False)
#root.attributes('-fullscreen',True)

root.mainloop()
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
            self.breakTime = False
            self.time = 60
            self.startTime = 60
            self.submissionTimerOneValue = 60
            self.submissionTimerTwoValue = 60
            self.scoresIn = False
            self.startSubmissionTimer = False
            self.submissionTimerOneRunning = ""
            self.submissionTimerTwoRunning = ""
            self.submissionTimerThreeRunning = ""
            self.screen = "blank"
            self.timerFont = "helvetica 90"

            self.watchForDecisions = True
            self.clock = "ClockRunning"
            self.useCards = False
            self.allResultsIn = False
            self.timerOnePosition = 0
            self.timerTwoPosition = 0
            self.screenWidth = Decimal(root.winfo_screenwidth())
            self.screenHeight = Decimal(root.winfo_screenheight())
            self.submissionOne_x = ""
            self.submissionOne_y = ""
            self.submissionTwo_x = ""
            self.submissionTwo_y = ""

            self.x_centre = Decimal(root.winfo_screenwidth())/2
            self.x_quarter = Decimal(root.winfo_screenwidth())/4
            self.y_centre = Decimal(root.winfo_screenheight())/2
            self.y_quarter = Decimal(root.winfo_screenheight())/4
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
            self.start_controller_one = tk.Button(self.button_frame, text='Connect Remotes', command=self.getDevices, fg="white", bg="black")
            self.start_controller_two = tk.Button(self.button_frame, text='Start', command=self.watchRemotes, fg="white", bg="black")
            self.exit_button = tk.Button(self.button_frame, text='Quit', command=root.destroy, fg="white", bg="black")

            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)
            self.button_frame.columnconfigure(2, weight=1)

            self.start_controller_one.grid(row=0, column=0, sticky=tk.W + tk.E)
            self.start_controller_two.grid(row=0, column=1, sticky=tk.W + tk.E)
            self.exit_button.grid(row=0, column=2, sticky=tk.W + tk.E)

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

        def toggleUseCards(self):
            self.useCards = not self.useCards
            print(self.useCards)


        def getDevices(self):
            self.devicePaths = []
            self.deviceList = [evdev.InputDevice(path) for path in evdev.list_devices()]
            print(self.deviceList)
            for device in self.deviceList:
                self.deviceName = (str(device.name))
                if self.deviceName == 'Wireless Controller':# or 'Sony Computer Entertainment Wireless Controller':
                    self.devicePaths.append(device.path)
            print(self.devicePaths)
            
            if not self.devicesFound:

                self.devices = map(InputDevice, (self.devicePaths[0], self.devicePaths[1], self.devicePaths[2]))
                self.devices = {dev.fd: dev for dev in self.devices}
                for dev in self.devices.values(): print(dev)

                self.r1 = self.devices.keys()[0]
                self.r2 = self.devices.keys()[1]
                self.r3 = self.devices.keys()[2]
                
                print(self.r1)
                print(self.r2)
                print(self.r3)

                self.identifyRemoteOne()
                self.identifyRemoteTwo()
                self.identifyRemoteThree()
                self.devicesFound = True
                
        def identifyRemoteOne(self):
            print("Looking for remote one")
            while True:
                self.w.create_text(self.x_centre, self.y_quarter, fill="white", width="1000", font="helvetica 40", text="Press the white light on the left judge's control", tag="RemoteOneInstructions")
                root.update()
                r,w,x = select(self.devices, [], [])
                for fd in r:
                    for event in self.devices[fd].read():
                        if event.type == ecodes.EV_KEY:
                            if event.code == self.triangleBtn and self.devicesFound == False and event.value == 1:
                                self.r_c1 = fd
                                print("r_c1 = " + str(self.r_c1))
                                self.w.delete("RemoteOneInstructions")
                                self.w.create_text(self.x_centre, self.y_quarter, fill="white", width="800", font="helvetica 30", text="Remote One Connected",tag="confirmConnection")
                                root.update()
                                return
        
        def identifyRemoteTwo(self):
            print "looking for remote 2"
            while True:
                self.w.create_text(self.x_centre, self.y_centre, fill="white", width="1000", font="helvetica 40", text="Press the white light on the centre judge's control", tag="RemoteTwoInstructions")
                root.update()
                r,w,x = select(self.devices, [], [])
                print(r)
                for fd in r:
                    print(fd)
                    for event in self.devices[fd].read():
                        if event.type == ecodes.EV_KEY:
                            if event.code == self.triangleBtn and self.devicesFound == False and event.value == 1:
                                print fd
                                if fd != self.r_c1:
                                    self.r_c2 = fd
                                    print("r_c2 = " + str(self.r_c2))
                                    self.w.delete("RemoteTwoInstructions")
                                    self.w.create_text(self.x_centre, self.y_centre, fill="white", width="800", font="helvetica 30", text="Remote Two Connected", tag="confirmConnection")
                                    root.update()
                                    event.code = 25
                                    return

        def identifyRemoteThree(self):
            print "looking for remote 3"
            while True:
                self.w.create_text(self.x_centre, self.y_centre + self.y_quarter, fill="white", width="1000", font="helvetica 40", text="Press the white light on the right judge's control", tag="RemoteThreeInstructions")
                root.update()
                r,w,x = select(self.devices, [], [])
                for fd in r:
                    print(fd)
                    for event in self.devices[fd].read():
                        if event.type == ecodes.EV_KEY:
                            if event.code == self.triangleBtn and self.devicesFound == False and event.value == 1:
                                print fd
                                if fd != self.r_c1 and fd != self.r_c2:
                                    self.r_c3 = fd
                                    print("r_c2 = " + str(self.r_c3))
                                    self.w.delete("RemoteThreeInstructions")
                                    self.w.create_text(self.x_centre, self.y_centre + self.y_quarter, fill="white", width="800", font="helvetica 30", text="Remote Three Connected", tag="confirmConnection")
                                    root.update()
                                    event.code = 25
                                    return
            
        def watchRemotes(self):
            self.w.delete("confirmConnection")
            print "watching"
            while True:
                root.update()
                r,w,x = select(self.devices, [], [])
                for fd in r:
                    for event in self.devices[fd].read():
                            if event.code == self.xBtn and self.watchForDecisions == True and event.value == 1:
                                if fd == self.r_c1:
                                    self.judgeOneChosenWhite()
                                    return
                                elif fd == self.r_c2:
                                    self.judgeTwoChosenWhite()
                                    return
                                elif fd == self.r_c3:
                                    self.judgeThreeChosenWhite()
                                    return
                            elif event.code == self.circleBtn and self.watchForDecisions == True and event.value == 1:
                                if fd == self.r_c1:
                                    self.judgeOneChosenRed(color1="red")
                                    return
                                elif fd == self.r_c2:
                                    self.judgeTwoChosenRed(color2="red")
                                    return
                                elif fd == self.r_c3:
                                    self.judgeThreeChosenRed(color3="red")
                            elif event.code == self.squareBtn and event.value == 1:
                                if fd == self.r_c2:
                                    print("Bar loaded button pressed")
                                    self.initBarLoaded()
                                    return
                            elif event.code == self.triangleBtn and event.value == 1:
                                print("Triangle Pressed")
                                print fd
                                print self.watchForDecisions
                                if fd == self.r_c2 and self.devicesFound == True:
                                    print("Triangle Pressed #2")
                                    self.initBreakTimer()
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
                self.initScoresIn()
                
            else:
                root.update()
                print("Results are missing")
                self.watchRemotes()
                
        def initScoresIn(self):

            if not self.submissionTimerOneRunning:
                self.submissionTimerOneValue = 60
                self.submissionTimerOne()
            elif self.submissionTimerOneRunning and not self.submissionTimerTwoRunning and not self.submissionTimerThreeRunning:
                self.submissionTimerTwoValue = self.submissionTimerOneValue
                self.submissionTimerOneValue = 60
                self.submissionTimerTwo()
            elif self.submissionTimerOneRunning and self.submissionTimerTwoRunning and not self.submissionTimerThreeRunning:
                self.submissionTimerThreeValue = self.submissionTimerTwoValue
                self.submissionTimerTwoValue = self.submissionTimerOneValue
                self.submissionTimerOneValue = 60
                self.submissionTimerThree()
            elif self.submissionTimerOneRunning and self.submissionTimerTwoRunning and self.submissionTimerThreeRunning:
                self.submissionTimerThreeValue = self.submissionTimerTwoValue
                self.submissionTimerTwoValue = self.submissionTimerOneValue
                self.submissionTimerOneValue = 60
            
            self.w.after(10000,self.clearLights)
            self.watchRemotes()

        def submissionTimerOne(self):
            
            if not self.breakTime:

                self.submissionTimerOneRunning = True

                self.submissionOne_x = self.screenWidth * 4 / 8
                self.submissionOne_y = self.screenHeight / 10

                self.w.delete("countdown_time_for_submission_one")

                self.w.create_text(self.screenWidth / 8 + 125, self.screenHeight / 10, fill="white", width="550", font="helvetica 40", text="Time to submit next attempt:")

                if self.submissionTimerOneValue == 60:
                    self.w.create_text(self.submissionOne_x, self.submissionOne_y, fill="white", font=self.timerFont, text="1:00", tag="countdown_time_for_submission_one")

                elif self.submissionTimerOneValue == 10:
                    self.w.create_text(self.submissionOne_x, self.submissionOne_y, fill="red", font=self.timerFont, text="0:" + str(self.submissionTimerOneValue), tag="countdown_time_for_submission_one")
                elif self.submissionTimerOneValue <= 9:
                    self.w.create_text(self.submissionOne_x, self.submissionOne_y, fill="red", font=self.timerFont, text="0:0" + str(self.submissionTimerOneValue), tag="countdown_time_for_submission_one")
                else:
                    self.w.create_text(self.submissionOne_x, self.submissionOne_y, fill="white", font=self.timerFont, text="0:" + str(self.submissionTimerOneValue), tag="countdown_time_for_submission_one")

                self.submissionTimerOneValue -= 1

                if self.submissionTimerOneValue >= 0:
                    self.w.after(1000, self.submissionTimerOne)
                elif self.submissionTimerOneValue < 0:
                    self.submissionTimerOneRunning = False
                    self.w.delete("countdown_time_for_submission_one")
                return
                
                #self.watchRemotes()

        def submissionTimerTwo(self):
            
            if not self.breakTime:

                self.submissionTimerTwoRunning = True

                self.submissionTwo_x = self.screenWidth * 11/16
                self.submissionTwo_y = self.screenHeight / 10

                self.w.delete("countdown_time_for_submission_two")

                if self.submissionTimerTwoValue == 60:
                    self.w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="white", font=self.timerFont, text="1:00", tag="countdown_time_for_submission_two")

                elif self.submissionTimerTwoValue == 10:
                    self.w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="red", font=self.timerFont, text="0:" + str(self.submissionTimerTwoValue), tag="countdown_time_for_submission_two")

                elif self.submissionTimerTwoValue <= 9:
                    self.w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="red", font=self.timerFont, text="0:0" + str(self.submissionTimerTwoValue), tag="countdown_time_for_submission_two")

                else:
                    self.w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="white", font=self.timerFont, text="0:" + str(self.submissionTimerTwoValue), tag="countdown_time_for_submission_two")

                self.submissionTimerTwoValue -= 1

                if self.submissionTimerTwoValue >= 0:
                    self.w.after(1000, self.submissionTimerTwo)
                elif self.submissionTimerTwoValue < 0:
                    self.submissionTimerTwoRunning = False
                    self.w.delete("countdown_time_for_submission_two")
                return
                #self.w.after(10000,self.clearLights)
                #self.watchRemotes()

        def submissionTimerThree(self):
            
            if not self.breakTime:

                self.submissionTimerThreeRunning = True

                self.submissionThree_x = self.screenWidth * 7 / 8
                self.submissionThree_y = self.screenHeight / 10

                self.w.delete("countdown_time_for_submission_three")

                if self.submissionTimerThreeValue == 60:
                    self.w.create_text(self.submissionThree_x, self.submissionThree_y, fill="white", font=self.timerFont,
                                       text="1:00",
                                       tag="countdown_time_for_submission_three")

                elif self.submissionTimerThreeValue == 10:
                    self.w.create_text(self.submissionThree_x, self.submissionThree_y, fill="red", font=self.timerFont,
                                       text="0:" + str(self.submissionTimerThreeValue),
                                       tag="countdown_time_for_submission_three")
                elif self.submissionTimerThreeValue <= 9:
                    self.w.create_text(self.submissionThree_x, self.submissionThree_y, fill="red", font=self.timerFont,
                                       text="0:0" + str(self.submissionTimerThreeValue),
                                       tag="countdown_time_for_submission_three")
                else:
                    self.w.create_text(self.submissionThree_x, self.submissionThree_y, fill="white", font=self.timerFont,
                                       text="0:" + str(self.submissionTimerThreeValue),
                                       tag="countdown_time_for_submission_three")

                self.submissionTimerThreeValue -= 1

                if self.submissionTimerThreeValue >= 0:
                    self.w.after(1000, self.submissionTimerThree)
                elif self.submissionTimerThreeValue < 0:
                    self.submissionTimerThreeRunning = False
                    self.w.delete("countdown_time_for_submission_three")
                return
                #self.w.after(10000,self.clearLights)
                #self.watchRemotes()
                
        def clearLights(self):
            self.w.delete("lights")
            return

        def initBarLoaded(self):
            
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
            self.isbarLoaded = True
            self.watchForDecisions = True
            if not self.scoresIn:
                self.w.delete("lights", "countdown_time")
                if self.time == 60:
                    self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400", text="1:00", tag="countdown_time")
                elif self.time == 10:
                    self.w.create_text(self.x_centre, self.y_centre, fill="red", font="helvetica 400", text="0:" + str(self.time),
                                       tag="countdown_time")
                elif self.time <= 9:
                    self.w.create_text(self.x_centre, self.y_centre, fill="red", font="helvetica 400", text="0:0" + str(self.time),
                                       tag="countdown_time")
                else:
                    self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400", text="0:" + str(self.time),
                                       tag="countdown_time")
                self.time -= 1
                if self.time >= 0 and not self.scoresIn:
                    self.clock = self.w.after(1000, self.barLoaded)
                elif self.scoresIn:
                    self.w.delete("countdown_time")
            
            self.watchRemotes()

        def initBreakTimer(self):
            self.breakTime = True
            self.w.delete(ALL)
            self.breakTimerMin = 10
            self.breakTimerSec = 0
            self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400", text="10:00", tag="breakTimer")
            self.w.create_text(720, 50, fill="white", font="helvetica 40", text="Press the white light to start the timer", tag="startTimerText")
            self.screen = "countdownTimer"
            self.watchRemotesForBreakTimer()

        def watchRemotesForBreakTimer(self):
            while True:
                root.update()
                r, w, x = select(self.devices, [], [])
                for fd in r:
                    for event in self.devices[fd].read():
                        if event.type == ecodes.EV_KEY:
                            if event.code == self.xBtn and self.watchForDecisions == False and event.value == 1:
                                if fd == self.r_c2:
                                    self.breakTimer()
                                    return
                            elif event.code == self.circleBtn and self.watchForDecisions == False and event.value == 1:
                                if fd == self.r_c2:
                                    self.addMinutesToCountdown()
                                    return
                            elif event.code == self.squareBtn and self.watchForDecisions == False and event.value == 1:
                                if fd == self.r_c2:
                                    self.subtractMinutesToCountdown()
                                    return

        def addMinutesToCountdown(self):
            self.w.delete("breakTimer")
            self.breakTimerMin += 1
            self.breakTimerSec = 0
            self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400", text=str(self.breakTimerMin) + ":00", tag="breakTimer")
            self.watchRemotesForBreakTimer()

        def subtractMinutesToCountdown(self):
            self.w.delete("breakTimer")
            self.breakTimerMin -= 1
            self.bbreakTimerSecreakTimerSec = 0
            self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400", text=str(self.breakTimerMin) + ":00", tag="breakTimer")
            self.watchRemotesForBreakTimer()

        def breakTimer(self):
            
            if self.screen == "countdownTimer":

                self.w.delete(ALL)

                if self.breakTimerSec == 10:
                    self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400",
                                       text=str(self.breakTimerMin) + ":" + str(self.breakTimerSec),
                                       tag="breakTimer")
                elif self.breakTimerSec <= 9:
                    self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400",
                                       text=str(self.breakTimerMin) + ":0" + str(self.breakTimerSec),
                                       tag="breakTimer")
                else:
                    self.w.create_text(self.x_centre, self.y_centre, fill="white", font="helvetica 400",
                                       text=str(self.breakTimerMin) + ":" + str(self.breakTimerSec),
                                       tag="breakTimer")

                self.breakTimerSec -= 1

                if self.breakTimerSec >= 0:
                    self.w.after(1000, self.breakTimer)
                elif self.breakTimerSec < 0 and self.breakTimerMin > 0:
                    print("breakTimerSec starting again")
                    self.breakTimerMin -= 1
                    self.breakTimerSec = 59
                    self.w.after(1000, self.breakTimer)
                elif self.breakTimerMin <= 0:
                    print("Done")
                    self.breakTime = False
                    self.watchRemotes()


    root = Tk()
    bgui = MyFirstGUI(root)
    my_gui = MyFirstGUI(root)
    root.configure(background='black')
    #root.geometry("720x450")
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen',True)
    root.mainloop()


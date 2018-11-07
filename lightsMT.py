#!/usr/bin/env python

import Tkinter as tk
from Tkinter import *
from decimal import Decimal
from select import select
import evdev
from evdev import InputDevice, categorize, ecodes
import re
import datetime
from datetime import timedelta 
import time
import math
import threading

class lightsGui(threading.Thread):
    def __init__(self, master):
        threading.Thread.__init__(self)
        self.master = master
        self.newWindowCreated = False
        self.devicesFound = False
        global screenWidth
        screenWidth = Decimal(root.winfo_screenwidth())
        global screenHeight
        screenHeight = Decimal(root.winfo_screenheight())
        self.time = 60;
        
        ########## BUTTON MAPPING ##########
        global white_button_clicked 
        white_button_clicked = 45
        ########## BUTTON MAPPING ##########

        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.button1 = tk.Button(self.frame, text = 'Start', width = 25, command = self.new_window, state=DISABLED)
        self.start_controller_one = tk.Button(self.frame, text='Connect Remotes', command=self.getDevices)
        self.session_break_timer = tk.Button(self.frame, text="Start break timer", command=self.break_timer_manager, state=DISABLED)
        self.e = Entry(self.frame,justify='center')
        self.e.insert(0, '00:00:05')
        root.title("Lights System - Control pane")

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

        self.button1.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.start_controller_one.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.e.grid(row=0, column=2, sticky=tk.W + tk.E)
        self.session_break_timer.grid(row=0, column=3, sticky=tk.W + tk.E)

        self.home_canvas = Canvas(root, width=screenWidth/2, height=screenHeight/2, highlightthickness=0)
        self.home_canvas.configure(background="#FFFFFF")
        self.home_canvas.create_text(screenWidth/4, screenHeight/4, fill="black", width="1000", font="helvetica 25", text="Click the connect remotes button to begin setup", tag="introText")
        print("Original canvas height = " + str(self.home_canvas.winfo_height()))
        self.home_canvas.pack()
        root.geometry(str(screenWidth/2)+"x"+str(screenHeight/2))
        

    def new_window(self):
        if not self.newWindowCreated and self.devicesFound:
            
            ########## PROPERTIES ##########
            self.button1.config(state=DISABLED)
            global continue_bar_loaded
            continue_bar_loaded = False
            global continue_break_timer
            continue_break_timer  = False
            self.newWindowCreated = True
            global timerFontLarge
            timerFontLarge = "helvetica 500"
            global timerFontSmall
            timerFontSmall = "helvetica 400"
            global x_centre
            x_centre = Decimal(screenWidth)/2
            global x_quarter
            x_quarter = Decimal(screenWidth)/4
            global y_centre
            y_centre = Decimal(screenHeight)/2
            global y_quarter
            y_quarter = Decimal(screenHeight)/4
            global small_radius
            small_radius = Decimal(root.winfo_screenwidth())/35
            global large_radius
            large_radius = Decimal(root.winfo_screenwidth())*4/28
            global x_left
            x_left = Decimal(root.winfo_screenwidth())/5-Decimal(root.winfo_screenwidth())/30
            global x_right
            x_right = Decimal(root.winfo_screenwidth())-x_left
            global card_x_radius
            card_x_radius = large_radius/3
            global card_y_radius
            card_y_radius = large_radius*2/5
            global card_y_centre
            card_y_centre = screenHeight*5/6
            self.y_submission_text = screenHeight*2/30
            self.x_submission_text = screenWidth*13/72
            global judgeOne
            judgeOne = False
            global judgeTwo
            judgeTwo = False
            global judgeThree
            judgeThree = False
            global submissionTimerOneRunning
            submissionTimerOneRunning = False
            global submissionTimerTwoRunning
            submissionTimerTwoRunning = False
            global submissionTimerThreeRunning
            submissionTimerThreeRunning = False
            global useCards
            useCards = False
            global run_submission_timers
            run_submission_timers = True
            global watchForDecisions
            watchForDecisions = True
            self.start_watching_remotes = False
            global countdown_font
            countdown_font="helvetica 80"
            global clock
            clock = "ClockRunning"
            global decisionOnScreen
            decisionOnScreen = False
            global submissionTimerOneValue
            global submissionTimerTwoValue
            global submissionTimerThreeValue
            ########## PROPERTIES ##########

            self.newWindow = Toplevel(bg="black")
            self.newWindow.title("Lights System - Display")
            self.session_break_timer.config(state=NORMAL)
            self.home_canvas.delete("remoteConfirmationText")
            self.home_canvas.create_text(screenWidth/4, screenHeight/4, fill="black", width="1000", font="helvetica 25", text="The lights system is running!", tag="systemRunningText")
            
            global w
            w = Canvas(self.newWindow, width=screenWidth, height=screenHeight, highlightthickness=0)
            w.configure(background="#000000")
            self.newWindow.attributes('-fullscreen',True)
            w.pack(fill=BOTH, expand=1)
            watchRemotesAllTime().start()
    
        elif not self.devicesFound:
            self.home_canvas.delete(ALL)
            self.home_canvas.create_text(screenWidth/4, screenHeight*2/10, fill="black", width="1000", font="helvetica 25", text="Press connect the remotes before starting the program", tag="remotesNotConnectedInstructions")

        elif self.newWindowCreated:
            self.home_canvas.create_text(screenWidth/4, screenHeight*2/10, fill="black", width="1000", font="helvetica 25", text="You have already started the program", tag="remotesNotConnectedInstructions")
            self.home_canvas.after(1000, self.home_canvas.delete(ALL))
        
        self.home_canvas = Canvas(root, width=screenWidth/2, height=screenHeight/2, highlightthickness=0)
        self.home_canvas.pack()
        print("New canvas height = " + str(self.home_canvas.winfo_height()))
        
    def getDevices(self):
        self.start_controller_one.config(state=DISABLED)
        self.home_canvas.delete('remotesNotConnectedInstructions')
        self.home_canvas.delete('insufficientRemotesConnectedText')
        self.home_canvas.delete('introText')
        self.devicePaths = []
        self.deviceList = [evdev.InputDevice(path) for path in evdev.list_devices()]
        print(self.deviceList)
        for device in self.deviceList:
            self.deviceName = (str(device.name))
            print(self.deviceName)
            if self.deviceName == 'Adafruit Bluefruit LE' or self.deviceName == 'Adafruit Bluefruit LE D9C3' or self.deviceName == 'Adafruit Bluefruit LE 7B65':
                self.devicePaths.append(device.path)
        
        print(self.devicePaths)
        if not self.devicesFound:
            try:
                self.devices = map(InputDevice, (self.devicePaths[0], self.devicePaths[1], self.devicePaths[2]))#, self.devicePaths[3]))
                self.devices = {dev.fd: dev for dev in self.devices}
                global deviceList
                deviceList = self.devices
                
                for dev in self.devices.values(): 
                    print(dev)
                    print('ine under dev')
                    
                self.r1 = self.devices.keys()[0]
                self.r2 = self.devices.keys()[1]
                self.r3 = self.devices.keys()[2]

                self.identifyRemoteOne()
                self.identifyRemoteTwo()
                self.identifyRemoteThree()
                print('returned from remote 3')
                self.home_canvas.delete("confirmConnection")
                self.home_canvas.create_text(screenWidth/4, screenHeight*2/10, fill="black", width="1000", font="helvetica 25", text="All remotes are connected! You can now start the lights system", tag="remoteConfirmationText")
                self.devicesFound = True
                self.button1.config(state=NORMAL)
            except Exception,e:
                print(str(e))
                self.start_controller_one.config(state=NORMAL)
                print("Plese ensure all remotes are connected")
                self.home_canvas.create_text(screenWidth/4, screenHeight*2/10, fill="black", width="1000", font="helvetica 25", text="Plese ensure all remotes are connected", tag="insufficientRemotesConnectedText")
    
    def identifyRemoteOne(self):
        print("Looking for remote one")
        while True:
            self.home_canvas.create_text(screenWidth/4, screenHeight*2/16, fill="black", width="1000", font="helvetica 25", text="Press the white light button on the left judge's control", tag="RemoteOneInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == white_button_clicked and self.devicesFound == False and event.value == 1:
                            self.r_c1 = fd
                            global rc1
                            rc1 = self.r_c1
                            print("r_c1 = " + str(self.r_c1))
                            self.home_canvas.delete("RemoteOneInstructions")
                            self.home_canvas.create_text(screenWidth/4, screenHeight*2/16, fill="black", width="800", font="helvetica 30", text="Remote One Connected",tag="confirmConnection")
                            root.update()
                            return
    
    def identifyRemoteTwo(self):
        print "looking for remote 2"
        while True:
            self.home_canvas.create_text(screenWidth/4, screenHeight/4, fill="black", width="1000", font="helvetica 25", text="Press the bar loaded button on the centre judge's control", tag="RemoteTwoInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == 31 and self.devicesFound == False:
                            if fd != self.r_c1:
                                self.r_c2 = fd
                                global rc2
                                rc2 = self.r_c2
                                print("r_c2 = " + str(self.r_c2))
                                self.home_canvas.delete("RemoteTwoInstructions")
                                self.home_canvas.create_text(screenWidth/4, screenHeight/4, fill="black", width="800", font="helvetica 30", text="Remote Two Connected", tag="confirmConnection")
                                root.update()
                                event.code = 25
                                return

    def identifyRemoteThree(self):
        print "looking for remote 3"
        while True:
            self.home_canvas.create_text(screenWidth/4, screenHeight*3/8, fill="black", width="1000", font="helvetica 25", text="Press the white light button on the right judge's control", tag="RemoteThreeInstructions")
            root.update()
            r,w,x = select(self.devices, [], [])
            for fd in r:
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == white_button_clicked and self.devicesFound == False:
                            if fd != self.r_c1 and fd != self.r_c2:
                                self.r_c3 = fd
                                global rc3
                                rc3 = self.r_c3
                                print("r_c3 = " + str(self.r_c3))
                                self.home_canvas.delete("RemoteThreeInstructions")
                                self.home_canvas.create_text(screenWidth/4, screenHeight*3/8, fill="black", width="800", font="helvetica 30", text="Remote Three Connected", tag="confirmConnection")
                                root.update()
                                event.code = 25
                                return
      
    def parse_countdown_time(self):
        inputString = str(self.e.get())
        self.hours = re.search('^(.*?)(?=\\:)',inputString)
        self.minutes = re.search('(?<=:)\\d.*?\\d(?=:)',inputString)
        self.seconds = re.search('(\\d)*$',inputString)

        self.hours = self.hours.group(0)
        self.minutes = self.minutes.group(0)
        self.seconds = self.seconds.group(0)

        countdown_time_array = [self.hours,self.minutes, self.seconds]
        return countdown_time_array

    def break_timer_manager(self):
        global continue_break_timer
        if continue_break_timer :
            continue_break_timer  = False
            global watchForDecisions
            watchForDecisions = True
            self.session_break_timer['text'] = 'Start break timer'
            self.stop_break_timer()
        elif not continue_break_timer :
            continue_break_timer  = True
            global watchForDecisions
            watchForDecisions = False
            self.session_break_timer['text'] = 'Stop break timer'
            self.init_break_timer()        

    def init_break_timer(self):
        global run_submission_timers
        run_submission_timers = False
        w.delete(ALL)
        w.delete("submission_text")
        w.delete("countdown_time_for_submission_one")
        self.hours_for_timer = int(self.parse_countdown_time()[0])
        self.minutes_for_timer = int(self.parse_countdown_time()[1])
        self.seconds_for_timer = int(self.parse_countdown_time()[2])

        if self.seconds_for_timer == 60:
            self.minutes_for_timer -= 1

        if self.minutes_for_timer == 60:
            self.hours_for_timer -= 1

        w.delete(ALL)
        self.final_time = datetime.datetime.now() + timedelta(hours=self.hours_for_timer,minutes=self.minutes_for_timer,seconds=self.seconds_for_timer)
        self.break_timer()

    def break_timer(self):
        
        if continue_break_timer:
            
            self.text_colour = 'white'
            w.delete("breakTimer")

            self.time_remaining = self.final_time - datetime.datetime.now()
            self.seconds_remaining =(math.ceil(self.time_remaining.total_seconds()))

            self.hours_left = int(self.seconds_remaining//3600)
            self.minutes_left = int((self.seconds_remaining - self.hours_left*3600)//60)
            self.seconds_left = int((self.seconds_remaining - self.hours_left*3600 - self.minutes_left*60))

            if self.minutes_left < 10:
                self.text_colour = "orange"
                if self.minutes_left < 3:
                    self.text_colour = "red"

                self.minutes_left = str(self.minutes_left)

            if int(self.hours_left) == -1 and int(self.minutes_left) == 59 and int(self.seconds_left) == 59:
                print("Timer finished. Watching for remote inputs...")
                global watchForDecisions
                watchForDecisions = True
                global run_submission_timers
                run_submission_timers = True
                global continue_break_timer
                continue_break_timer = False
                global continue_break_timer
                continue_break_timer = False
                global run_submission_timers
                run_submission_timers = True
                global submissionTimerOneRunning
                submissionTimerOneRunning = False
                global submissionTimerTwoRunning
                submissionTimerTwoRunning = False
                global submissionTimerThreeRunning
                submissionTimerThreeRunning = False
                self.session_break_timer['text'] = 'Start break timer'
                w.create_text(x_centre, y_centre, fill="red", font=timerFontLarge, text="0:00", tag="endBreakTimer")
                    
            else:   
                if self.seconds_left < 10:
                    self.seconds_left = "0" + str(self.seconds_left)

                if self.hours_left > 0:
                    w.create_text(x_centre, y_centre, fill=self.text_colour, font=timerFontSmall, text=(str(self.hours_left) + ":" + str(self.minutes_left) + ":" + str(self.seconds_left)), tag="breakTimer")
                elif self.hours_left == 0:
                    w.create_text(x_centre, y_centre, fill=self.text_colour, font=timerFontLarge, text=(str(self.minutes_left) + ":" + str(self.seconds_left)), tag="breakTimer")
                
                w.after(1000,self.break_timer)

    def stop_break_timer(self):
        global continue_break_timer
        continue_break_timer = False
        global run_submission_timers
        run_submission_timers = True
        global submissionTimerOneRunning
        submissionTimerOneRunning = False
        global submissionTimerTwoRunning
        submissionTimerTwoRunning = False
        global submissionTimerThreeRunning
        submissionTimerThreeRunning = False
        w.delete(ALL)
        w.delete("breakTimer")

    def bar_loaded_manager(self):      
        global decisionOnScreen
        decisionOnScreen = False
        judgeOne = False
        judgeTwo = False
        judgeThree = False
        if continue_bar_loaded:
            self.stop_bar_loaded()
        elif not continue_bar_loaded:
            self.init_bar_loaded()

    def init_bar_loaded(self):
        global continue_bar_loaded
        continue_bar_loaded = True
        w.delete("lights", "countdown_time","greenLight","endBreakTimer")
        self.time = 60
        self.barLoaded()
            
    def barLoaded(self):
        print("IN BARLOADED")
        print("CONTINUE BAR LOADED IS "+str(continue_bar_loaded))
        if continue_bar_loaded:
            self.scoresIn = False
           
            w.delete("lights", "countdown_time")
            if self.time == 60:
                w.create_text(x_centre, y_centre, fill="white", font=timerFontLarge, text="1:00", tag="countdown_time")
            elif self.time == 10:
                w.create_text(x_centre, y_centre, fill="red", font=timerFontLarge, text="0:" + str(self.time),
                                   tag="countdown_time")
            elif self.time <= 9:
                w.create_text(x_centre, y_centre, fill="red", font=timerFontLarge, text="0:0" + str(self.time),
                                   tag="countdown_time")
            else:
                w.create_text(x_centre, y_centre, fill="white", font=timerFontLarge, text="0:" + str(self.time),
                                   tag="countdown_time")
            self.time -= 1
            if self.time >= 0 and not self.scoresIn:
                clock = w.after(1000, self.barLoaded)
                
            elif self.scoresIn:
                w.delete("countdown_time")
        else:
            print("BAR LOADED STOPPED")
        
    def stop_bar_loaded(self):
        global continue_bar_loaded
        continue_bar_loaded = False
        w.delete("countdown_time")
        return

    def judgeOneChosenWhite(self):
        if not decisionOnScreen:
            self.x0 = x_left - small_radius
            self.y0 = y_centre - small_radius
            self.x1 = x_left + small_radius
            self.y1 = y_centre + small_radius
            
            w.delete("countdown_time","endBreakTimer")
            self.scoresIn = True
            w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
            global judgeOne
            judgeOne = True
            global judgeOneChoice
            judgeOneChoice = "white"
            print(judgeOne)
            self.displayResults()

    def judgeTwoChosenWhite(self):
        if not decisionOnScreen:
            self.x0 = x_centre - small_radius
            self.y0 = y_centre - small_radius
            self.x1 = x_centre + small_radius
            self.y1 = y_centre + small_radius

            w.delete("countdown_time","endBreakTimer")
            self.scoresIn = True
            w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
            global judgeTwo
            judgeTwo = True;
            global judgeTwoChoice
            judgeTwoChoice = "white"
            self.displayResults()

    def judgeThreeChosenWhite(self):
        if not decisionOnScreen:
            self.x0 = x_right - small_radius
            self.y0 = y_centre - small_radius
            self.x1 = x_right + small_radius
            self.y1 = y_centre + small_radius

            w.delete("countdown_time","endBreakTimer")
            self.scoresIn = True
            w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
            global judgeThree
            judgeThree = True;
            global judgeThreeChoice
            judgeThreeChoice = "white"
            self.displayResults()

    def judgeOneChosenRed(self,color1):
        if not decisionOnScreen:
            self.x0 = x_left - small_radius
            self.y0 = y_centre - small_radius
            self.x1 = x_left + small_radius
            self.y1 = y_centre + small_radius

            w.delete("countdown_time","endBreakTimer")
            self.scoresIn = True
            w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
            global judgeOne
            judgeOne = True;
            global judgeOneChoice
            judgeOneChoice = color1
            self.displayResults()

    def judgeTwoChosenRed(self,color2):
        if not decisionOnScreen:
            self.x0 = x_centre - small_radius
            self.y0 = y_centre - small_radius
            self.x1 = x_centre + small_radius
            self.y1 = y_centre + small_radius

            w.delete("countdown_time","endBreakTimer")
            self.scoresIn = True
            w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
            global judgeTwo
            judgeTwo = True
            global judgeTwoChoice
            judgeTwoChoice = color2
            self.displayResults()

    def judgeThreeChosenRed(self,color3):
        if not decisionOnScreen:
            self.x0 = x_right - small_radius
            self.y0 = y_centre - small_radius
            self.x1 = x_right + small_radius
            self.y1 = y_centre + small_radius

            w.delete("countdown_time","endBreakTimer")
            self.scoresIn = True
            w.create_oval(self.x0, self.y0, self.x1, self.y1, fill="#00ff00", outline="#00ff00",tag="greenLight")
            global judgeThree
            judgeThree = True
            global judgeThreeChoice
            judgeThreeChoice = color3
            self.displayResults()

    def displayResults(self):
        
        global continue_bar_loaded
        continue_bar_loaded = False
                
        self.x0_1_light = x_left - large_radius
        self.y0_1_light = y_centre - large_radius
        self.x1_1_light = x_left + large_radius
        self.y1_1_light = y_centre + large_radius

        self.x0_1_card = x_left - card_x_radius
        self.y0_1_card = card_y_centre - card_y_radius
        self.x1_1_card = x_left + card_x_radius
        self.y1_1_card = card_y_centre + card_y_radius

        self.x0_2_light = x_centre - large_radius
        self.y0_2_light = y_centre - large_radius
        self.x1_2_light = x_centre + large_radius
        self.y1_2_light = y_centre + large_radius

        self.x0_2_card = x_centre - card_x_radius
        self.y0_2_card = card_y_centre - card_y_radius
        self.x1_2_card = x_centre + card_x_radius
        self.y1_2_card = card_y_centre + card_y_radius

        self.x0_3_light = x_right - large_radius
        self.y0_3_light = y_centre - large_radius
        self.x1_3_light = x_right + large_radius
        self.y1_3_light = y_centre + large_radius

        self.x0_3_card = x_right - card_x_radius
        self.y0_3_card = card_y_centre - card_y_radius
        self.x1_3_card = x_right + card_x_radius
        self.y1_3_card = card_y_centre + card_y_radius
        
        global judgeOne
        global judgeTwo
        global judgeThree
        global judgeOneChoice
        global judgeTwoChoice
        global judgeThreeChoice
        global useCards
        global decisionOnScreen
        
        if judgeOne == True and judgeTwo == True and judgeThree == True:

            w.delete("greenLight")
            #watchForDecisions = False
            decisionOnScreen = True
            
            if judgeOneChoice == "white":
                w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#FFFFFF", outline="#FFFFFF",tag="lights")
            elif judgeOneChoice == "red":
                w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_1_card, self.y0_1_card, self.x1_1_card, self.y1_1_card, fill="#ff0000", outline="#ff0000",tag="lights")
            elif judgeOneChoice == "blue":
                w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#ff0000", outline="#ff0000", tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_1_card, self.y0_1_card, self.x1_1_card, self.y1_1_card, fill="#0000ff", outline="#0000ff", tag="lights")
            elif judgeOneChoice == "yellow":
                w.create_oval(self.x0_1_light, self.y0_1_light, self.x1_1_light, self.y1_1_light, fill="#ff0000", outline="#ff0000", tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_1_card, self.y0_1_card, self.x1_1_card, self.y1_1_card, fill="#FFFF00", outline="#FFFF00", tag="lights")

            if judgeTwoChoice == "white":
                w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#FFFFFF", outline="#FFFFFF",tag="lights")
            elif judgeTwoChoice == "red":
                w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_2_card, self.y0_2_card, self.x1_2_card, self.y1_2_card, fill="#ff0000", outline="#ff0000", tag="lights")
            elif judgeTwoChoice == "blue":
                w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_2_card, self.y0_2_card, self.x1_2_card, self.y1_2_card, fill="#0000ff", outline="#0000ff", tag="lights")
            elif judgeTwoChoice == "yellow":
                w.create_oval(self.x0_2_light, self.y0_2_light, self.x1_2_light, self.y1_2_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_2_card, self.y0_2_card, self.x1_2_card, self.y1_2_card, fill="#FFFF00", outline="#FFFF00", tag="lights")

            if judgeThreeChoice == "white":
                w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#FFFFFF", outline="#FFFFFF",tag="lights")
            elif judgeThreeChoice == "red":
                w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_3_card, self.y0_3_card, self.x1_3_card, self.y1_3_card, fill="#ff0000", outline="#ff0000", tag="lights")
            elif judgeThreeChoice == "blue":
                w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_3_card, self.y0_3_card, self.x1_3_card, self.y1_3_card, fill="#0000ff", outline="#0000ff", tag="lights")
            elif judgeThreeChoice == "yellow":
                w.create_oval(self.x0_3_light, self.y0_3_light, self.x1_3_light, self.y1_3_light, fill="#ff0000", outline="#ff0000",tag="lights")
                if useCards:
                    w.create_rectangle(self.x0_3_card, self.y0_3_card, self.x1_3_card, self.y1_3_card, fill="#FFFF00", outline="#FFFF00", tag="lights")

            judgeOne = False
            judgeTwo = False
            judgeThree = False
            self.allResultsIn = True
            self.time == 60
            self.initScoresIn()
                
        else:
            root.update()
            print("Results are missing")
                
    def initScoresIn(self):
        
        global submissionTimerOneRunning
        global submissionTimerTwoRunning
        global submissionTimerThreeRunning
        
        global submissionTimerOneValue
        global submissionTimerTwoValue
        global submissionTimerThreeValue

        if not submissionTimerOneRunning:
            submissionTimerOneValue = 60
            self.submissionTimerOne()
        elif submissionTimerOneRunning and not submissionTimerTwoRunning and not submissionTimerThreeRunning:
            submissionTimerTwoValue = submissionTimerOneValue
            submissionTimerOneValue = 60
            self.submissionTimerTwo()
        elif submissionTimerOneRunning and submissionTimerTwoRunning and not submissionTimerThreeRunning:
            submissionTimerThreeValue = submissionTimerTwoValue
            submissionTimerTwoValue = submissionTimerOneValue
            submissionTimerOneValue = 60
            self.submissionTimerThree()
        elif submissionTimerOneRunning and submissionTimerTwoRunning and submissionTimerThreeRunning:
            submissionTimerThreeValue = submissionTimerTwoValue
            submissionTimerTwoValue = submissionTimerOneValue
            submissionTimerOneValue = 60
            
        w.after(30000,self.clearLights)
        
    def submissionTimerOne(self):
        
        global submissionTimerOneValue
        global submissionTimerTwoValue
        global submissionTimerThreeValue

        if run_submission_timers:
            
            global submissionTimerOneRunning
            submissionTimerOneRunning = True

            self.submissionOne_x = screenWidth * 3 / 8
            self.submissionOne_y = screenHeight / 10

            w.delete("countdown_time_for_submission_one")

            w.create_text(screenWidth / 8 + screenWidth/40, screenHeight / 10, fill="white", width="750", font="helvetica 40", text="Attempt selection:", tag="submission_text")

            if submissionTimerOneValue == 60:
                w.create_text(self.submissionOne_x, self.submissionOne_y, fill="white", font=countdown_font, text="1:00", tag="countdown_time_for_submission_one")

            elif submissionTimerOneValue == 10:
                w.create_text(self.submissionOne_x, self.submissionOne_y, fill="red", font=countdown_font, text="0:" + str(submissionTimerOneValue), tag="countdown_time_for_submission_one")
            elif submissionTimerOneValue <= 9:
                w.create_text(self.submissionOne_x, self.submissionOne_y, fill="red", font=countdown_font, text="0:0" + str(submissionTimerOneValue), tag="countdown_time_for_submission_one")
            else:
                w.create_text(self.submissionOne_x, self.submissionOne_y, fill="white", font=countdown_font, text="0:" + str(submissionTimerOneValue), tag="countdown_time_for_submission_one")

            submissionTimerOneValue -= 1

            if submissionTimerOneValue >= 0:
                w.after(1000, self.submissionTimerOne)
            elif submissionTimerOneValue < 0:
                submissionTimerOneRunning = False
                w.delete("countdown_time_for_submission_one")
            return
          
    def submissionTimerTwo(self):
        
        global submissionTimerOneValue
        global submissionTimerTwoValue
        global submissionTimerThreeValue

        if run_submission_timers:
            
            global submissionTimerTwoRunning
            submissionTimerTwoRunning = True

            self.submissionTwo_x = screenWidth * 11/16 - screenWidth/10
            self.submissionTwo_y = screenHeight / 10
            w.delete("countdown_time_for_submission_two")

            if submissionTimerTwoValue == 60:
                w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="white", font=countdown_font, text="1:00", tag="countdown_time_for_submission_two")
            elif submissionTimerTwoValue == 10:
                w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="red", font=countdown_font, text="0:" + str(submissionTimerTwoValue), tag="countdown_time_for_submission_two")

            elif submissionTimerTwoValue <= 9:
                w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="red", font=countdown_font, text="0:0" + str(submissionTimerTwoValue), tag="countdown_time_for_submission_two")

            else:
                w.create_text(self.submissionTwo_x, self.submissionTwo_y, fill="white", font=countdown_font, text="0:" + str(submissionTimerTwoValue), tag="countdown_time_for_submission_two")

            submissionTimerTwoValue -= 1
                
            if submissionTimerTwoValue >= 0:
                w.after(1000, self.submissionTimerTwo)
            elif submissionTimerTwoValue < 0:
                submissionTimerTwoRunning = False
                w.delete("countdown_time_for_submission_two")
            return

    def submissionTimerThree(self):
        
        global submissionTimerOneValue
        global submissionTimerTwoValue
        global submissionTimerThreeValue

        if run_submission_timers:
        
            global submissionTimerThreeRunning
            submissionTimerThreeRunning = True

            self.submissionThree_x = screenWidth * 7 / 8 - screenWidth/10
            self.submissionThree_y = screenHeight / 10

            w.delete("countdown_time_for_submission_three")

            if submissionTimerThreeValue == 60:
                w.create_text(self.submissionThree_x, self.submissionThree_y, fill="white", font=countdown_font, text="1:00", tag="countdown_time_for_submission_three")

            elif submissionTimerThreeValue == 10:
                w.create_text(self.submissionThree_x, self.submissionThree_y, fill="red", font=countdown_font, text="0:" + str(submissionTimerThreeValue), tag="countdown_time_for_submission_three")
            elif submissionTimerThreeValue <= 9:
                w.create_text(self.submissionThree_x, self.submissionThree_y, fill="red", font=countdown_font, text="0:0" + str(submissionTimerThreeValue), tag="countdown_time_for_submission_three")
            else:
                w.create_text(self.submissionThree_x, self.submissionThree_y, fill="white", font=countdown_font, text="0:" + str(submissionTimerThreeValue), tag="countdown_time_for_submission_three")

            submissionTimerThreeValue -= 1
            
            if submissionTimerThreeValue >= 0:
                w.after(1000, self.submissionTimerThree)
            elif submissionTimerThreeValue < 0:
                submissionTimerThreeRunning = False
                w.delete("countdown_time_for_submission_three")
            return
                
    def clearLights(self):
        w.delete("lights","greenLight")
        global decisionOnScreen
        decisionOnScreen = False
        return

class watchRemotesAllTime(threading.Thread):
    def __init__(self):
        print("Starting watchRemotesAllTime")  
        threading.Thread.__init__(self)
        
    def run(self):
        print("Starting watchRemotes")
        lightsGuiJO = lightsGui(root)
        while True:
            global deviceList
            print("WATCH FOR DECISIONS IS TRUE")
            root.update()
            r,w,x = select(deviceList, [], [])
            for fd in r:
                for event in deviceList[fd].read():
                    if event.type == ecodes.EV_KEY:
                        if event.code == 45 and event.value == 1 and watchForDecisions == True:
                            if fd == rc1:
                                lightsGuiJO.judgeOneChosenWhite()
                            elif fd == rc2:
                                lightsGuiJO.judgeTwoChosenWhite()
                            elif fd == rc3:
                                lightsGuiJO.judgeThreeChosenWhite()
                        elif event.code == 44 and event.value == 1 and watchForDecisions == True:
                            if fd == rc1:
                                lightsGuiJO.judgeOneChosenRed(color1="red")
                            elif fd == rc2:
                                lightsGuiJO.judgeTwoChosenRed(color2="red")
                            elif fd == rc3:
                                lightsGuiJO.judgeThreeChosenRed(color3="red")
                        elif event.code == 31 and event.value == 1 and watchForDecisions == True:
                            print(event.code)
                            print(event.value)
                            print(fd)
                            if fd == rc2:
                                lightsGuiJO.bar_loaded_manager()

def main(): 
    app = lightsGui(root)
    root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    main()



##################################################
# Genshin Impact Resin Tracker by ReVoltage#3425 #
# https://github.com/revoltage34/gresintracker/  #
##################################################

import tkinter as tk
import time
import math
from datetime import datetime
import os

class GRES(object): 
    def InitGUI(self, root):
        self.topWindow = root
        self.topWindow.title("Resin Tracker")
        self.residue = 0
        
        #----
        
        self.resinLabel = tk.Label(self.topWindow, text="Resin", font=("Helvetica", 16))
        self.resinLabel.grid(column = 0, row = 0, sticky="W")
        
        self.resinVar = tk.IntVar()
        self.resinEntry = tk.Entry(self.topWindow, width=3, font=("Helvetica", 16), justify=tk.RIGHT, textvariable=self.resinVar)
        self.resinEntry.grid(column = 1, row = 0, sticky="E")
        self.resinVar.trace("w", self.callback)
        
        self.resinLimitLabel = tk.Label(self.topWindow, text="/160", font=("Helvetica", 16))
        self.resinLimitLabel.grid(column = 2, row = 0, sticky="W")
        
        self.resinTimeVar = tk.StringVar()
        self.resinTimeLabel = tk.Label(self.topWindow, textvariable=self.resinTimeVar, font=("Helvetica", 12))
        self.resinTimeLabel.grid(column = 0, row = 1, columnspan = 3)
        
        self.resinDateVar = tk.StringVar()
        self.resinDateLabel = tk.Label(self.topWindow, textvariable=self.resinDateVar, font=("Helvetica", 12))
        self.resinDateLabel.grid(column = 0, row = 2, columnspan = 3)
        
        self.topWindow.attributes('-topmost', True)
        self.topWindow.protocol("WM_DELETE_WINDOW", self.Quit)
        self.topWindow.after(480000, self.LoopCheckTime)
        
    def callback(self, *args):
        self.SaveTime()
        
    def SaveTime(self):
        resin = 0
        try:
            resin = self.resinVar.get()
        except:
            pass
        file = open(os.getcwd() + "/gres.txt", 'w')
        file.write(str(math.floor(time.time())) + "\n" + str(resin) + "\n" + str(self.residue))
        file.close()
        
        if resin <= 160:
            mins = (160 - resin) * 8
            self.resinTimeVar.set("Full in: " + str(math.floor(mins/60)) + "h " + str(mins%60) + "m")
            self.resinDateVar.set("" + datetime.fromtimestamp(time.time() + (mins * 60)).strftime("%d %b, %H:%M (%a)") + "")
        else:
            mins = (resin - 160) * 8
            self.resinTimeVar.set("Overflow: " + str(math.floor(mins/60)) + "h " + str(mins%60) + "m")
            self.resinDateVar.set("" + datetime.fromtimestamp(time.time() - (mins * 60)).strftime("%d %b, %H:%M (%a)") + "")
        
    def LoadTime(self):
        try:
            file = open(os.getcwd() + "/gres.txt", 'r')
            times = math.floor(time.time()) - int(file.readline().replace("\n", ""))
            resin = int(file.readline().replace("\n", "")) + math.floor(times/480)
            self.residue = times%480 + int(file.readline().replace("\n", ""))
            if self.residue >= 480:
                self.residue -= 480
                resin += 1
            
            self.resinVar.set(resin)
        except:
            pass
        self.SaveTime()
        
    def LoopCheckTime(self):
        self.topWindow.after(480000, self.LoopCheckTime)
        resin = 0
        try:
            resin = self.resinVar.get()
        except:
            pass
        self.resinVar.set(resin + 1)
        
    def Quit(self):
        self.LoadTime()
        self.topWindow.quit()

root = tk.Tk()
gcd = GRES()
gcd.InitGUI(root)
gcd.LoadTime()
root.mainloop()

#pythoncom.PumpMessages()
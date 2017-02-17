import WalabotAPI
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class GUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Walabot SeeThroughDemo')  # window title
        self.option_add("*Font", "TkFixedFont")  # default monospace font
        self.mainFrame = MainFrame(self)  # init window conponents
        self.mainFrame.pack()


class MainFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.statusPanel = StatusPanel(self)
        self.ctrlPanel = ControlPanel(self)
        self.statusPanel.pack()
        self.ctrlPanel.pack(expand=True, fill="both")

    def initLoop(self):
        try:
            self.ctrlPanel.connLabel.config(text="CONNECTING")
            wlbt.Connect()
            self.ctrlPanel.connLabel.config(text="CALIBRATING")
            wlbt.Calibrate()
            self.ctrlPanel.connLabel.config(text="CONNECTED")
            self.loopId = self.after_idle(self.loop)
        except wlbt.WalabotError:
            self.stopLoop()

    def loop(self):
        try:
            if wlbt.isTargets():
                self.statusPanel.statusLabel.config(
                    text="Treasure Found!", bg="gold"
                )
            else:
                self.statusPanel.statusLabel.config(
                    text="Scanning", bg="snow1"
                )
            self.loopId = self.after_idle(self.loop)
        except wlbt.WalabotError:
            self.stopLoop()

    def stopLoop(self):
        wlbt.stopAndDisconnect()
        self.statusPanel.statusLabel.config(text="")
        self.ctrlPanel.connLabel.config(text="DISCONNECTED")
        self.after_cancel(self.loopId)


class StatusPanel(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.statusLabel = tk.Label(self, width=30, height=5, bg="snow1")
        self.statusLabel.pack()


class ControlPanel(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.strtBtn = tk.Button(
            self, text="Start", width=6, command=self.master.initLoop
        )
        self.stopBtn = tk.Button(
            self, text="Stop", width=6, command=self.master.stopLoop
        )
        self.connLabel = tk.Label(self, text="DISCONNECTED")
        self.strtBtn.pack(side="left")
        self.stopBtn.pack(side="left")
        self.connLabel.pack(side="right")


class Walabot:

    def __init__(self):
        self.wlbt = WalabotAPI
        self.WalabotError = self.wlbt.WalabotError
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()

    def Connect(self):
        self.wlbt.ConnectAny()
        self.isConnected = True
        self.wlbt.SetProfile(self.wlbt.PROF_SHORT_RANGE_IMAGING)
        self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_NONE)
        self.wlbt.SetArenaX(-4, 4, 0.8)
        self.wlbt.SetArenaY(-6, 4, 0.8)
        self.wlbt.SetArenaZ(3, 8, 0.5)
        self.wlbt.SetThreshold(50)
        self.wlbt.Start()

    def Calibrate(self):
        self.wlbt.StartCalibration()
        while self.wlbt.GetStatus()[0] == self.wlbt.STATUS_CALIBRATING:
            self.wlbt.Trigger()

    def isTargets(self):
        self.wlbt.Trigger()
        return True if self.wlbt.GetImagingTargets() else False

    def stopAndDisconnect(self):
        self.wlbt.Stop()
        self.wlbt.Disconnect()


if __name__ == '__main__':
    wlbt = Walabot()
    guiApp = GUI()
    guiApp.mainloop()

#!/usr/bin/python3
# file: pylvinox.py
# content: kelvinox interface
# created: 2020 october 11 Sunday
# modified: 2022 september 07 Wednesday
# modification:
# author: roch schanen
# comment: introduction of vertical scrolling

from pyvigi.tools import header
header()

from sys import version
print(f"run Python version {version.split(' ')[0]}")

from pyvigi import version
print(f"using pyvigi version {version}")

from pyvigi.base import app
from pyvigi.theme import imageCollect
from pyvigi.theme import imageSelect
from pyvigi.controls import vScroll

from pyvigi.buttons import Switch
from pyvigi.buttons import LEDSwitch
from pyvigi.buttons import Wheel

from pyvigi.display import bitmapControl
from pyvigi.display import digitalFixedPointDisplay

class myapp(app):

    def Start(self):

        # create vScroll control for smaller screen
        # all the controls have now to be placed on
        # the vScroll control and not on the Panel
        self.content = vScroll(self.Panel)
        self.content.SetBackground(imageCollect("drawing"))
        self.content.SetFrameContainerHeight(750)

        # ------------------------------------------------------

        # declare leds dictionary
        self.leds = {}
        # get leds image collection
        ledc = imageCollect("leds", "green")
        # create, place, bind and register led buttons
        for name, x, y in [
                ("V1",   384, 222), ("V2",   498, 286),
                ("V3",   612, 286), ("V4",   726, 286),
                ("V5",   840, 286), ("V7",   498, 487),
                ("V8",   612, 490), ("V10",  840, 490),
                ("V9",   738, 637), ("V14",  678, 637),
                ("V11A", 719, 718), ("V11B", 719, 869),
                ("V12A", 398, 767), ("V12B", 398, 919),
                ("V13A", 922, 767), ("V13B", 922, 919),
                ("V1A",  197, 237), ("V4A",  182, 480),
                ("V5A",  249, 544), ("V2A",  309, 544),
            ]:
            # create
            l = Switch(self.content, imageSelect(ledc))
            # place
            l.SetPosition((x+23, y+50))
            # bind
            l.BindEvent(self.ValveOperate)
            # config valve name
            l.name = name
            # register for external access (to explore)
            self.leds[name] = l

        # ------------------------------------------------------

        # declare leds dictionary
        self.leds = {}
        # get leds image collection
        ledc = imageCollect("leds", "green")
        # create, place, bind and register led buttons
        for name, x, y in [
                ("V1",   384, 222), ("V2",   498, 286),
                ("V3",   612, 286), ("V4",   726, 286),
                ("V5",   840, 286), ("V7",   498, 487),
                ("V8",   612, 490), ("V10",  840, 490),
                ("V9",   738, 637), ("V14",  678, 637),
                ("V11A", 719, 718), ("V11B", 719, 869),
                ("V12A", 398, 767), ("V12B", 398, 919),
                ("V13A", 922, 767), ("V13B", 922, 919),
                ("V1A",  197, 237), ("V4A",  182, 480),
                ("V5A",  249, 544), ("V2A",  309, 544),
            ]:
            # create
            l = Switch(self.content, imageSelect(ledc))
            # place
            l.SetPosition((x+23, y+50))
            # bind
            l.BindEvent(self.ValveOperate)
            # config valve name
            l.name = name
            # register for external access (to explore)
            self.leds[name] = l

        # ------------------------------------------------------

        # declare switches dictionary
        self.switches = {}
        # get leds image collection
        switchc = imageCollect("switches", "blue")
        for name, x, y in [
            ("HE3", 136, 725+3), ("HE4", 921, 430+3)]:
            # create
            s = LEDSwitch(self.content, imageSelect(switchc))
            # place
            s.SetPosition((x+10, y+40))
            # bind event
            s.BindEvent(self.PumpOperate)
            # add name
            s.name = name
            # register
            self.switches[name] = s

        ###################################################### POT NEEDLE VALVE

        digitsc = imageCollect("digits", "yellow") 

        # create Needle valve interface
        self.PNV = {}
        # add interface element: name
        self.PNV["Name"] = "NV"
        # add interface element: wheels
        self.PNV["Wheels"] = []
        for n, x, y in [
                (100,  0+81, 217),
                (10,  12+81, 217),
                (1,   24+81, 217),
            ]:
            w = Wheel(
                self.content,
                imageSelect(digitsc, "normal"),
                imageSelect(digitsc,  "hover"))
            w.SetPosition((x, y))
            w.BindEvent(self.PNVOperate)
            w.weight = n
            w.group = self.PNV
            self.PNV["Wheels"].append(w)
        # add interface element: value
        v = 0
        for w in self.PNV["Wheels"]:
            v += w.weight * w.GetValue()
        self.PNV["Value"] = v

        #################################################### STILL NEEDLE VALVE

        digitsc = imageCollect("digits", "yellow") 

        # create Still valve interface
        self.SNV = {}
        # add interface element: name
        self.SNV["Name"] = "SV"
        # add interface element: all the wheels
        self.SNV["Wheels"] = []
        for n, x, y in [
                (100,  0+965, 294),
                (10,  12+965, 294),
                (1,   24+965, 294),
            ]:
            # create an individual wheel control
            w = Wheel(
                self.content,
                imageSelect(digitsc, "normal"),
                imageSelect(digitsc,  "hover"))
            # set the wheel position
            w.SetPosition((x, y))
            # bind wheel events to handler
            w.BindEvent(self.SNVOperate)
            # setup wheel configuration
            w.weight = n        # digit numerical weight
            w.group = self.SNV   # add wheel to still wheels group
            # add wheel to still interface
            self.SNV["Wheels"].append(w)
        # add interface element: value
        v = 0
        for w in self.SNV["Wheels"]:
            v += w.weight * w.GetValue()
        self.SNV["Value"] = v

        #################################################################### GN

        # load images
        collection = imageCollect("digits", "red")
        names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        images = imageSelect(collection, names)

        self.Gn = {}
        
        for data in [
                    (172, 437, "G1"),
                    (375, 698, "G2"),
                    (960, 698, "G3"),
                ]:

            x, y, name = data
            g = digitalFixedPointDisplay(self.content, "05.1f", images, names)
            g.SetPosition((x, y))
            self.Gn[name] = g


        self.Gn["G1"].SetValue(123.5657)
        self.Gn["G2"].SetValue(23.04)
        self.Gn["G3"].SetValue(3.05)

        # done
        return

    def PNVOperate(self, event):
        # get reference to wheel button
        c = event.caller
        # get variation
        dv = c.step * c.weight
        # get target value
        v = self.PNV["Value"] + dv
        # coerce to limits
        if v < 0:   v = 0
        if v > 100: v = 100 
        # check if up-to-date 
        if self.PNV["Value"] == v:
            c.Reset()
            return
        # update value
        self.PNV["Value"] = v
        # convert to digits list
        s = list(f"{v:03}")
        # check for wheel updates
        for w in self.PNV["Wheels"]: # add zip
            d = int(s.pop(0))
            if w.GetValue() == d:
                continue
            w.SetValue(d)
        c.Refresh() # why SetValue does not refresh caller
        # collect parameters
        g = event.caller.group
        n = event.caller.weight
        w = event.status % event.caller.n
        s = g['Name']
        # debug display
        print(f"wheel event from {s}:")
        print(f"wheel '{n}' set to {w},")
        print(f"new value {v:03}.")
        # send command to serial port here
        return

    def SNVOperate(self, event):
        # get reference to wheel button
        c = event.caller
        # get variation
        dv = c.step * c.weight
        # get target value
        v = self.SNV["Value"] + dv
        # coerce to limits
        if v < 0:   v = 0
        if v > 100: v = 100 
        # check if up-to-date 
        if self.SNV["Value"] == v:
            c.Reset()
            return
        # update value
        self.SNV["Value"] = v
        # convert to digits list
        s = list(f"{v:03}")
        # check for wheel updates
        for w in self.SNV["Wheels"]: # add zip
            d = int(s.pop(0))
            if w.GetValue() == d:
                continue
            w.SetValue(d)
        c.Refresh() # why SetValue does not refresh caller
        # collect parameters
        g = event.caller.group
        n = event.caller.weight
        w = event.status % event.caller.n
        s = g['Name']
        # debug display
        print(f"wheel event from {s}:")
        print(f"wheel '{n}' set to {w},")
        print(f"new value {v:03}.")
        # send command to serial port here
        return

    def PumpOperate(self, event):
        # collect parameters
        n = event.caller.name
        s = ["off", "on"][event.status]
        # debug display
        print("pump event:")
        print(f"{n} switched {s}.")
        # send command to serial port here
        return

    def ValveOperate(self, event):

        # collect parameters
        n = event.caller.name
        s = ["off", "on"][event.status]
        # debug display
        print("valve event:")
        print(f"{n} switched {s}.")
        # send command to serial port here
        return

        # done
        return

m = myapp()
m.Run()

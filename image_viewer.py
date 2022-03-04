import os
import datetime
import wx
from wx.lib.floatcanvas import NavCanvas
from pubsub import pub


# colors = ["AQUAMARINE", "BLACK", "BLUE", "BLUE VIOLET", "BROWN",
#           "CADET BLUE", "CORAL", "CORNFLOWER BLUE", "CYAN", "DARK GREY",
#           "DARK GREEN", "DARK OLIVE GREEN", "DARK ORCHID", "DARK SLATE BLUE",
#           "DARK SLATE GREY", "DARK TURQUOISE", "DIM GREY",
#           "FIREBRICK", "FOREST GREEN", "GOLD", "GOLDENROD", "GREY",
#           "GREEN", "GREEN YELLOW", "INDIAN RED", "KHAKI", "LIGHT BLUE",
#           "LIGHT GREY", "LIGHT STEEL BLUE", "LIME GREEN", "MAGENTA",
#           "MAROON", "MEDIUM AQUAMARINE", "MEDIUM BLUE", "MEDIUM FOREST GREEN",
#           "MEDIUM GOLDENROD", "MEDIUM ORCHID", "MEDIUM SEA GREEN",
#           "MEDIUM SLATE BLUE", "MEDIUM SPRING GREEN", "MEDIUM TURQUOISE",
#           "MEDIUM VIOLET RED", "MIDNIGHT BLUE", "NAVY", "ORANGE", "ORANGE RED",
#           "ORCHID", "PALE GREEN", "PINK", "PLUM", "PURPLE", "RED",
#           "SALMON", "SEA GREEN", "SIENNA", "SKY BLUE", "SLATE BLUE",
#           "SPRING GREEN", "STEEL BLUE", "TAN", "THISTLE", "TURQUOISE",
#           "VIOLET", "VIOLET RED", "WHEAT", "WHITE", "YELLOW", "YELLOW GREEN"]


wildcard = "JPG/JPEG (*.jpg)|*.jpg|" \
           "PNG (*.png)|*.png|" \
           "GIF (*.gif)|*.gif|" \
           "ICO (*.ico)|*.ico|" \
           "SVG (*.svg)|*.svg|" \
           "BMP (*.bmp)|*.bmp|" \
           "All files (*.*)|*.*"


class DrawFrame(wx.Frame):
    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self, parent, id, title, position, size)
        font_medium = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.NORMAL, False, '')

        super().SetFont(font_medium)

        self.Canvas = NavCanvas.NavCanvas(self, -1, (500, 500), Debug=False, BackgroundColor="White").Canvas
        self.Canvas.NumBetweenBlits = 1000

        self.makemenuBar()
        self.CreateStatusBar()
        now = datetime.datetime.now()
        self.SetStatusText(f"Program started at {datetime.datetime.strftime(now, '%Y, %m %d %T')} (static)")

        # event handlers:
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        pub.subscribe(self.DrawFromProduct, "Go_get_it")

        # *args
        self.image = None
        self.opentype = 0
        self.savetype = 0


    def makemenuBar(self):
        menuBar = wx.MenuBar()
        
        file_menu = wx.Menu()
        openItem = file_menu.Append(-1, "&Open\tCtrl-O", "Open the image file")
        save_asItem = file_menu.Append(-1, "&Save As\tCtrl-Shift-S", "Save as a self-named file")
        exitItem = file_menu.Append(-1, "Exit\tESC", "Terminate the program")

        view_menu = wx.Menu()
        zoomItem = view_menu.Append(-1, "Zoom in &Fit\tCtrl-F", "Zoom to fit the Window")
        clearItem = view_menu.Append(-1, "&Clear\tCtrl-C", "Clear the Canvas")

        help_menu = wx.Menu()
        aboutItem = help_menu.Append(wx.ID_ABOUT, "", "More information about the program")
        
        menuBar.Append(file_menu, "&File")
        menuBar.Append(view_menu, "&View")
        menuBar.Append(help_menu, "&Help")

        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnSave_As, save_asItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.ZoomToFit, zoomItem)
        self.Bind(wx.EVT_MENU, self.Clear, clearItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def DrawFromProduct(self, message):
        self.Canvas.ClearAll()
        image = wx.Image(message, wx.BITMAP_TYPE_JPEG)
        self.Canvas.AddScaledBitmap(image, (0, 0), Height=image.GetHeight(), Position="cc")
        self.Canvas.Draw()
        self.Canvas.ZoomToBB()

    def OnOpen(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN |
                  wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                  wx.FD_PREVIEW
        )
        dlg.SetFilterIndex(self.opentype)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.origin_path = paths[0]
            self.opentype = dlg.GetFilterIndex()

            file_type = dlg.GetFilename().split(".")[1]
            if file_type == "jpg":
                self.image = wx.Image(dlg.GetFilename(), wx.BITMAP_TYPE_JPEG)
            elif file_type == "png":
                self.image = wx.Image(dlg.GetFilename(), wx.BITMAP_TYPE_PNG)
            elif file_type == "gif":
                self.image = wx.Image(dlg.GetFilename(), wx.BITMAP_TYPE_GIF)
            elif file_type == "ico":
                self.image = wx.Image(dlg.GetFilename(), wx.BITMAP_TYPE_ICO)
            elif file_type == "bmp":
                self.image = wx.Image(dlg.GetFilename(), wx.BITMAP_TYPE_BMP)
            else:
                wx.MessageBox("Unreadable!", "Error occurred", wx.ICON_ERROR)

            if self.image:
                self.Canvas.ClearAll()
                self.Canvas.AddScaledBitmap(self.image, (0, 0), Height=self.image.GetSize()[1], Position="cc")
                self.Canvas.Draw()
                self.Canvas.ZoomToBB()

    def OnSave_As(self, event):
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        dlg.SetFilterIndex(self.savetype)
        if dlg.ShowModal() == wx.ID_OK:
            self.output_path = dlg.GetPath()
            self.savetype = dlg.GetFilterIndex()
            self.Canvas.SaveAsImage(self.output_path)

    def Clear(self, event):
        self.Canvas.ClearAll()
        self.Canvas.Draw()

    def ZoomToFit(self, event):
        self.Canvas.ZoomToBB()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is another frame with other program that\n"
                                                  "used wx.NavCanvas\n",
                                                  "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        dlg = wx.MessageDialog(None, "Do you really want to exit?", 'ExitDialog',
                               wx.YES_NO | wx.ICON_NONE)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.Destroy()

import product
import wx


class App(wx.App):
    def OnInit(self):
        frame = product.Frame(None, title="Molecular analyzer", size=(1080, 900))
        frame.Centre()
        self.SetTopWindow(frame)
        frame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
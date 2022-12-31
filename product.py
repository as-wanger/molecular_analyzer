import os
import wx
import datetime
from pubsub import pub

import xlwings as xlw
import pandas as pd
import numpy as np

import wx.lib.mixins.listctrl as listmix

import image_viewer
import analyzer

wildcard = "Python source (*.py)|*.py|" \
           "Compiled Python (*.pyc)|*.pyc|" \
           "Comma sep(csv) (*.csv)|*.csv|" \
           "Space sep (*.txt)|*.txt|" \
           "Excel workbook (*.xlsx)|*.xlsx|" \
           "All files (*.*)|*.*"

# the context is example, thus need to clear first
mw_listctrldata = {
    1: ("Hey!", "You can edit", "me!"),
    2: ("Try changing the contents", "by", "clicking"),
    3: ("in", "a", "cell"),
    4: ("See how the length columns", "change", "?"),
    5: ("You can use", "TAB,", "cursor down,"),
    6: ("and cursor up", "to", "navigate"),
    7: ("But editing", "the cells", "don't change the data !!!"),
}

types_listctrldata = {
    1: ("So this is", "another table", "!"),
    2: ("you can input", "a", "xlsx file"),
    3: ("with", "two", "sheets"),
    4: ("like", "the", "input_data.xlsx"),
    5: ("molecular weight", "sheet for", "upper table,"),
    6: ("peptide types", "sheet for", "this table"),
}

input_listctrldata = {1: ("Input data will be here.")}
matters_listctrldata = {1: ("ex: CH3", "CH3->15")}
result_listctrldata = {1: ("type number", "1")}

name_list = ['lambda=0', 'lambda=0.05', 'lambda=0.0', 'lambda=0.15']
num_list = [52.4, 57.8, 59.1, 54.6]


class TestListCtrl(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.TextEditMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)

    def Populate_mw(self):
        # for normal, simple columns, you can add them like this:
        self.InsertColumn(0, "A")
        self.InsertColumn(1, "B")
        self.InsertColumn(2, "C")

        items = mw_listctrldata.items()
        for key, data in items:
            index = self.InsertItem(self.GetItemCount(), str(data[0]))
            self.SetItem(index, 1, str(data[1]))
            self.SetItem(index, 2, str(data[2]))
            self.SetItemData(index, key)

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        self.currentItem = 0

    def Populate_type(self):
        self.InsertColumn(0, "A")
        self.InsertColumn(1, "B")
        self.InsertColumn(2, "C")

        items = types_listctrldata.items()
        for key, data in items:
            index = self.InsertItem(self.GetItemCount(), str(data[0]))
            self.SetItem(index, 1, str(data[1]))
            self.SetItem(index, 2, str(data[2]))
            self.SetItemData(index, key)

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        self.currentItem = 0

    def Populate_input(self):
        self.InsertColumn(0, "A")

        items = input_listctrldata.items()
        for key, data in items:
            index = self.InsertItem(self.GetItemCount(), str(data[0]))
            self.SetItemData(index, key)

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)

        self.currentItem = 0

    def Populate_result(self):
        self.InsertColumn(0, "A")
        self.InsertColumn(1, "B")

        items = result_listctrldata.items()
        for key, data in items:
            index = self.InsertItem(self.GetItemCount(), str(data[0]))
            self.SetItem(index, 1, str(data[1]))
            self.SetItemData(index, key)

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        self.currentItem = 0

    def Populate_Matters(self):
        self.InsertColumn(0, "Matters")
        self.InsertColumn(1, "Formula")

        items = matters_listctrldata.items()
        for key, data in items:
            index = self.InsertItem(self.GetItemCount(), str(data[0]))
            self.SetItem(index, 1, str(data[1]))
            self.SetItemData(index, key)

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.currentItem = 0

    # well... This function didn't be used, but search for self.GetItem only
    def SetStringItem(self, index, col, data):
        if col in range(3):
            wx.ListCtrl.SetItem(self, index, col, data)
            wx.ListCtrl.SetItem(self, index, 3 + col, str(len(data)))
        else:
            try:
                datalen = int(data)
            except:
                return

            wx.ListCtrl.SetItem(self, index, col, data)

            data = self.GetItem(index, col - 3).GetText()
            wx.ListCtrl.SetItem(self, index, col - 3, data[0:datalen])


class Frame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font_large = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL, False, '')
        font_medium = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.NORMAL, False, '')

        super().SetFont(font_medium)

        pnl = wx.Panel(self)
        pnl.SetFont(font_large)

        mw_list = TestListCtrl(pnl, 10, size=(1080, 250),
                               style=wx.LC_REPORT
                                     | wx.BORDER_NONE
                                     # | wx.LC_SORT_ASCENDING
                                     # Content of list as instructions is nonsense with auto-sort enabled
                                     | wx.LC_HRULES | wx.LC_VRULES
                               )
        mw_list.Populate_mw()
        types_list = TestListCtrl(pnl, 11, size=(1080, 250),
                                  style=wx.LC_REPORT
                                        | wx.BORDER_NONE
                                        # | wx.LC_SORT_ASCENDING
                                        | wx.LC_HRULES | wx.LC_VRULES
                                  )
        types_list.Populate_type()
        input_list = TestListCtrl(pnl, 12, size=(280, 200),
                                  style=wx.LC_REPORT
                                        | wx.BORDER_NONE
                                        # | wx.LC_SORT_ASCENDING
                                        | wx.LC_HRULES | wx.LC_VRULES
                                  )
        input_list.Populate_input()
        matter_list = TestListCtrl(pnl, 13, size=(400, 200),
                                   style=wx.LC_REPORT
                                         | wx.BORDER_NONE
                                         # | wx.LC_SORT_ASCENDING
                                         | wx.LC_HRULES | wx.LC_VRULES
                                   )
        matter_list.Populate_Matters()
        result_list = TestListCtrl(pnl, 14, size=(400, 200),
                                   style=wx.LC_REPORT
                                         | wx.BORDER_NONE
                                         # | wx.LC_SORT_ASCENDING
                                         | wx.LC_HRULES | wx.LC_VRULES
                                   )
        result_list.Populate_result()
        self.mw_list = mw_list
        self.types_list = types_list
        self.input_list = input_list
        self.matter_list = matter_list
        self.result_list = result_list

        for_mw = wx.StaticText(pnl, label="Molecular weight of Amino acid")
        for_types = wx.StaticText(pnl, label="Types of Peptide")
        for_input = wx.StaticText(pnl, label="Input data")
        for_matters = wx.StaticText(pnl, label="Matters")
        for_result = wx.StaticText(pnl, label="Result data")

        sizer = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.VERTICAL)
        box1.Add(for_mw)
        box1.Add(mw_list, 20, wx.EXPAND)
        box1.Add(for_types)
        box1.Add(types_list, 20, wx.EXPAND)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        sub_box = wx.BoxSizer(wx.VERTICAL)
        sub_box2 = wx.BoxSizer(wx.VERTICAL)
        sub_box3 = wx.BoxSizer(wx.VERTICAL)
        sub_box.Add(for_input)
        sub_box.Add(input_list, 22)
        sub_box2.Add(for_matters)
        sub_box2.Add(matter_list, 23)
        sub_box3.Add(for_result)
        sub_box3.Add(result_list, 24)
        box2.Add(sub_box, 21)
        box2.Add(sub_box2, 21)
        box2.Add(sub_box3, 21)

        sizer.Add(box1)
        sizer.Add(box2)
        pnl.SetSizer(sizer)

        self.makemanuBar()
        self.CreateStatusBar()
        now = datetime.datetime.now()
        self.SetStatusText(f"Program started at {datetime.datetime.strftime(now, '%Y, %m %d %T')} (static)")

        # event handlers
        self.analyzer = analyzer.Control()
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        # *args
        self.opentype = 4
        self.savetype = 4
        self.input_df = None
        self.query_type = "1"
        self.query_type2 = ""
        self.origin_path = None
        self.output_path = None

    def makemanuBar(self):
        file_menu = wx.Menu()
        introItem = file_menu.Append(-1, "&Introduction\tCtrl-I", "The introduction about this program")
        openItem = file_menu.Append(-1, "&Open\tCtrl-O", "Open the file")
        save_asItem = file_menu.Append(-1, "&Save As\tCtrl-Shift-S", "Save as a self-named file")
        file_menu.AppendSeparator()
        exitItem = file_menu.Append(wx.ID_EXIT, "Exit\tESC", "Terminate the program")

        work_menu = wx.Menu()
        analyzeItem = work_menu.Append(-1, "&Analyze\tCtrl-A",
                                       "Analyze a series of molecular and rank the possible types")
        appendMatterItem = work_menu.Append(-1, "Append &Matter\tCtrl-M", "tail added matter")
        queryItem = work_menu.Append(-1, "&Query the type\tCtrl-Q", "To see information about single type peptide")
        work_menu.AppendSeparator()
        drawItem = work_menu.Append(-1, "&Draw\tCtrl-D", "Draw the diagram")
        viewItem = work_menu.Append(-1, "&View\tCtrl-V", "Open the image viewer")

        help_menu = wx.Menu()
        aboutItem = help_menu.Append(wx.ID_ABOUT, "", "Who created this?")

        menuBar = wx.MenuBar()
        menuBar.Append(file_menu, "&File")
        menuBar.Append(work_menu, "&Work")
        menuBar.Append(help_menu, "&Help")

        self.SetMenuBar(menuBar)

        # menu event
        self.Bind(wx.EVT_MENU, self.OnIntro, introItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnSave_As, save_asItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAnalyze, analyzeItem)
        self.Bind(wx.EVT_MENU, self.OnAppend, appendMatterItem)
        self.Bind(wx.EVT_MENU, self.OnQuerySingleType, queryItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnDraw, drawItem)
        self.Bind(wx.EVT_MENU, self.OnView, viewItem)

    def OnOpen(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            # if needed: wx.FD_MULTIPLE | to load many files
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
            if file_type == "csv":
                df = pd.read_csv(self.origin_path, header=None, sep=",")
            elif file_type == "txt":
                df = pd.read_csv(self.origin_path, header=None, sep=" ")
            elif file_type == "xlsx":
                xlw_app = xlw.App(visible=False)
                wb = xlw.Book(self.origin_path)
                mw_sheet = wb.sheets[0].used_range.value
                types_sheet = wb.sheets[1].used_range.value
                input_sheet = wb.sheets[2].used_range.value
                mw_df = pd.DataFrame(mw_sheet)
                types_df = pd.DataFrame(types_sheet)
                input_df = pd.DataFrame(input_sheet)
                wb.close()
                xlw_app.kill()
            else:
                raise Exception("It's not usable yet!")
            global mw_listctrldata
            global types_listctrldata
            global input_listctrldata
            global matters_listctrldata
            mw_listctrldata.clear()
            types_listctrldata.clear()
            matters_listctrldata.clear()
            for val in mw_df.itertuples():
                mw_listctrldata[val[0]] = val[1:]
            for val in types_df.itertuples():
                types_listctrldata[val[0]] = val[1:]
            for val in input_df.itertuples():
                input_listctrldata[val[0]] = val[1:]
            self.mw_list.ClearAll()
            self.mw_list.Populate_mw()
            self.types_list.ClearAll()
            self.types_list.Populate_type()
            self.input_list.ClearAll()
            self.input_list.Populate_input()
            self.matter_list.ClearAll()
            self.matter_list.Populate_Matters()

            # pretreat the mw, types df for analyzing
            self.analyzer.aa = analyzer.pretreat_mw(mw_listctrldata)
            self.analyzer.pep = analyzer.pretreat_types(types_listctrldata)
            self.input_df = list(input_listctrldata.values())
        dlg.Destroy()

    def OnSave_As(self, event):
        mw_text = self.gettext(self.mw_list, self.mw_list.GetItemCount, self.mw_list.GetColumnCount)
        types_text = self.gettext(self.types_list, self.types_list.GetItemCount, self.types_list.GetColumnCount)
        input_text = self.gettext(self.input_list, self.input_list.GetItemCount, self.input_list.GetColumnCount)
        result_text = self.gettext(self.result_list, self.result_list.GetItemCount, self.result_list.GetColumnCount)
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        dlg.SetFilterIndex(self.savetype)
        if dlg.ShowModal() == wx.ID_OK:
            self.output_path = dlg.GetPath()
            mw_output = pd.DataFrame(mw_text).to_string(index=False, header=False)
            types_output = pd.DataFrame(types_text).to_string(index=False, header=False)
            input_output = pd.Series(input_text).to_string(index=False, header=False)
            result_output = pd.Series(result_text).to_string(index=False, header=False)
            self.savetype = dlg.GetFilterIndex()

            file_type = dlg.GetFilename().split('.')[1]
            if file_type == "csv":
                result_output.to_csv(self.output_path)
            elif file_type == "txt":
                np_arr = result_output.to_numpy()
                np.savetxt(self.output_path, np_arr, fmt="%s")
            elif file_type == "xlsx":
                xlw_app = xlw.App(visible=False)
                wb = xlw.Book(self.origin_path)
                result_sheet = None
                for i in range(3, 11):
                    try:
                        result_sheet = wb.sheets[i]
                        continue
                    except:
                        wb.sheets.add()
                        result_sheet = wb.sheets[i]
                        result_sheet.name = f"result{i - 2}"
                        break

                result_sheet.range("A1").value = result_output
                wb.save(self.output_path)
                wb.close()
                xlw_app.kill()
            else:
                raise Exception("It's not usable yet!")
        dlg.Destroy()

    def gettext(self, list, GetItemCount, GetColumnCount):
        rows = GetItemCount()
        cols = GetColumnCount()
        # initialize the array
        text = [[0 for _ in range(cols)] for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                item = list.GetItem(itemIdx=r, col=c)
                text[r][c] = item.GetText()
        return text

    def OnIntro(self, event):
        """The introduction about this program"""
        wx.MessageBox("You can open/save same file (csv, txt, xlsx allowed only)\n"
                      "to check the input data, analyze and export the result with diagram.")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This version is < 1.0.0 >\n"
                      "This program created by as_wanger\nDeveloped 2022.02.17-",
                      "Who created this",
                      wx.OK | wx.ICON_INFORMATION)

    def OnAppend(self, event):
        dlg = AppendTextEntryDialog(self, -1, "Input the matter's common name and formula")

        if dlg.ShowModal() == wx.ID_OK:
            if self.input_df:
                matter_name = dlg.name_text.GetValue()
                formula_name = dlg.formula_text.GetValue()
                mw_name = dlg.mw_text.GetValue()
                self.analyzer.add_matter(matter_name, formula_name, mw_name)
                self.analyzer.enlarge_types()

                global matters_listctrldata
                i = 0
                for k, v in self.analyzer.matter.items():
                    matters_listctrldata[i] = (k, v)
                    i += 1
                self.matter_list.ClearAll()
                self.matter_list.Populate_Matters()

                wx.MessageBox(f"Save the appending matter Name:  {matter_name}\n"
                              f"Formula:  {formula_name}\n"
                              f"Molecular weight:  {mw_name}",
                              "Check Dialog")
            else:
                wx.MessageBox("There's no data to append", "Error occurred!", wx.ICON_ERROR)

    def OnQuerySingleType(self, evnet):
        self.analyzer.output_log = ""
        self.query_type2 = ""
        dlg = wx.TextEntryDialog(
            self, 'Which type did you want to check (1~31) or (+) to see with what matter?',
            'Input a type number', self.query_type)

        if dlg.ShowModal() == wx.ID_OK:
            self.query_type = dlg.GetValue()
            if self.analyzer.query(self.query_type, self.query_type2):
                if self.analyzer.output_log:
                    wx.MessageBox(self.analyzer.output_log)
                else:
                    dlg2 = wx.TextEntryDialog(
                        self, f"There's {list(self.analyzer.matter.values())}.\nWhich one you want to select? \n",
                        'Input a matter type', self.query_type2)
                    if dlg2.ShowModal() == wx.ID_OK:
                        self.query_type2 = dlg2.GetValue()
                        if self.analyzer.query(self.query_type, self.query_type2):
                            re_dlg = wx.TextEntryDialog(
                                self, f'Which type did you want to check (1~31, with {self.query_type2})?',
                                'Input a type number', self.query_type)
                            if re_dlg.ShowModal() == wx.ID_OK:
                                self.query_type = re_dlg.GetValue()
                                if self.query_type == "+":
                                    wx.MessageBox(f"+ is not valid", "Error occurred!", wx.ICON_ERROR)
                                elif self.analyzer.query(self.query_type, self.query_type2):
                                    wx.MessageBox(self.analyzer.output_log)
                                else:
                                    wx.MessageBox(f"{self.query_type}-{self.query_type2} is not found", "Error occurred!",
                                                  wx.ICON_ERROR)
                        else:
                            wx.MessageBox(f"matter {self.query_type2} is not found", "Error occurred!", wx.ICON_ERROR)

            else:
                wx.MessageBox(f"type{self.query_type} is not found", "Error occurred!", wx.ICON_ERROR)

        dlg.Destroy()

    def OnAnalyze(self, event):
        self.analyzer.all_compounds()
        dlg = AnalyzeTextEntryDialog(self, -1, "Some args need to get")

        if dlg.ShowModal() == wx.ID_OK:
            most_nums = dlg.most_nums_text.GetValue()
            first_v = dlg.fv_text.GetValue()
            near_v = dlg.nv_text.GetValue()
            most_nums = int(most_nums)
            first_v = float(first_v)
            near_v = float(near_v)

            if self.input_df:
                print(self.input_df)
                print(self.analyzer.part)
                if self.analyzer.check_the_parts(self.input_df, most_nums, first_v, near_v, self.analyzer.part):
                    wx.MessageBox("Result shows under:\n" + self.analyzer.output_log,
                                  "All possibilities", wx.ICON_NONE)
                    global result_listctrldata
                    result_listctrldata.clear()
                    for i in range(len(self.analyzer.counter)):
                        result_listctrldata[i] = list(self.analyzer.counter.items())[i]

                    self.result_list.ClearAll()
                    self.result_list.Populate_result()
                else:
                    if most_nums <= 0 or first_v <= 0 or near_v <= 0:
                        wx.MessageBox(f"most_nums should be positive integer\n"
                                      f"first_v, near_v should be greater than zero\n"
                                      f"Input:\nmost_nums: {most_nums}, first_v: {first_v}, near_v: {near_v}",
                                      "Error occurred!", wx.ICON_ERROR)
                    else:
                        wx.MessageBox(
                            f"Invalid value! (Bigger than biggest or smaller than smallest amino_acid/matter)",
                            "Error occurred!", wx.ICON_ERROR)
            else:
                wx.MessageBox("There's no data to compare", "Error occurred!", wx.ICON_ERROR)

    def OnDraw(self, event):
        if self.analyzer.counter:
            self.analyzer.draw()
            frame = image_viewer.DrawFrame(None, -1, "Image viewer", (1200, 100), (700, 700))
            frame.Show()
            pub.sendMessage("Go_get_it", message=self.analyzer.buf)
        else:
            wx.MessageBox(f"Invalid value! can't get axis x, axis y data",
                          "Error occurred!", wx.ICON_ERROR)

    def OnView(self, event):
        frame = image_viewer.DrawFrame(None, -1, "Image viewer", (1200, 100), (700, 700))
        frame.Show()

    def OnExit(self, event):
        dlg = wx.MessageDialog(None, "Do you really want to exit?", 'ExitDialog',
                               wx.YES_NO | wx.ICON_NONE)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.Destroy()
        dlg.Destroy()


class AppendTextEntryDialog(wx.Dialog):
    def __init__(
            self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog'
    ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1,
        f"Add a matter to Append all types (now have {len(types_listctrldata)*(len(matters_listctrldata)+1)} types)")
        label.SetHelpText("The peptides' tail append these matter")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        name_label = wx.StaticText(self, -1, "Name")
        name_label.SetHelpText("The common name of the matter")
        box.Add(name_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        name_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        name_text.SetHelpText("Input the matter's name")
        self.name_text = name_text
        box.Add(name_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)

        box2 = wx.BoxSizer(wx.HORIZONTAL)

        formula_label = wx.StaticText(self, -1, "Chemical formula")
        formula_label.SetHelpText("The formula of the matter(water -> H2O)")
        box2.Add(formula_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        formula_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        formula_text.SetHelpText("Input the matter's formula")
        self.formula_text = formula_text
        box2.Add(formula_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box2, 0, wx.EXPAND | wx.ALL, 5)

        box3 = wx.BoxSizer(wx.HORIZONTAL)

        mw_label = wx.StaticText(self, -1, "Molecular weight")
        mw_label.SetHelpText("Molecular weight of the matter(H2O -> 18)")
        box3.Add(mw_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        mw_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        mw_text.SetHelpText("Input the matter's mw")
        self.mw_text = mw_text
        box3.Add(mw_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box3, 0, wx.EXPAND | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.EXPAND | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


class AnalyzeTextEntryDialog(wx.Dialog):
    def __init__(
            self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog'
    ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Before analyzing, you have to set some arguments")
        label.SetHelpText("Set most_numbers_one_side, first_variation, near_variation")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        box = wx.BoxSizer(wx.VERTICAL)

        most_nums_label = wx.StaticText(self, -1, "Most numbers from one side")
        most_nums_label.SetHelpText("At most getting the numbers")
        box.Add(most_nums_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        most_nums_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        most_nums_text.SetHelpText("Input the matter's name")
        self.most_nums_text = most_nums_text
        box.Add(most_nums_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)

        box2 = wx.BoxSizer(wx.VERTICAL)

        fv_label = wx.StaticText(self, -1, "First variation")
        fv_label.SetHelpText("If not, that side won't get any number")
        box2.Add(fv_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        fv_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        fv_text.SetHelpText("Input the matter's formula")
        self.fv_text = fv_text
        box2.Add(fv_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box2, 0, wx.EXPAND | wx.ALL, 5)

        box3 = wx.BoxSizer(wx.VERTICAL)

        nv_label = wx.StaticText(self, -1, "Near variation")
        nv_label.SetHelpText("As most getting largest gap number")
        box3.Add(nv_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        nv_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        nv_text.SetHelpText("Input the matter's mw")
        self.nv_text = nv_text
        box3.Add(nv_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box3, 0, wx.EXPAND | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.EXPAND | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

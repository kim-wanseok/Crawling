__author__ = 'Wanseok Kim'

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from threading import Event, Thread
from getData import get_Naver_Data

VER = 'v0.0'


# GUI for MyLand
class MyLand():
    def __init__(self):
        self.flag = True  # flag for terminate thread
        global MY_LOGO
        self.saveto = ''

        self.root = Tk()
        self.root.title('네이버 부동산 정보 %s' % VER)
        self.root.resizable(width=FALSE, height=FALSE)

        self.areamsg = StringVar()
        self.areamsg.set('Waiting..')
        self.stitlemsg = StringVar()
        self.stitlemsg.set('Saved Filename is... ')
        self.statusmsg = StringVar()
        self.statusmsg.set('Waiting..')

        self.radVar = StringVar(value='A1')
        self.checkVar1 = IntVar(value=1)
        self.checkVar2 = IntVar(value=1)
        self.checkVar3 = IntVar(value=1)

        # Main Frame & Panels
        content = ttk.Frame(self.root, padding=(6, 6, 6, 6))
        content.grid(column=0, row=0, sticky=(N, W, E, S))

        logo_panel = ttk.Frame(content, padding=(3, 3, 3, 3))
        select_panel = ttk.Frame(content, relief='groove', padding=(6, 6, 6, 6))
        select_1_panel = ttk.Frame(content, relief='groove', padding=(6, 6, 6, 6))
        status_panel = ttk.Frame(content, relief='groove', padding=(6, 6, 10, 10))
        progress_panel = ttk.Frame(content, relief='groove', padding=(6, 6, 6, 6))

        logo_panel.grid(column=0, row=0, sticky=(N, W, E, S))
        select_panel.grid(column=0, row=1, sticky=(N, W, E, S))
        select_1_panel.grid(column=0, row=2, sticky=(N, W, E, S))
        status_panel.grid(column=0, row=3, sticky=(N, W, E, S))
        progress_panel.grid(column=0, row=4, sticky=(N, W, E, S))

        # Create Logo
        try:
            MY_LOGO = ImageTk.PhotoImage(Image.open('./resources/converter.jpg'))
        except:
            pass

        # logolabel = ttk.Label(logo_panel, image='')
        logolabel = ttk.Label(logo_panel, image=MY_LOGO)
        logolabel.grid(column=0, row=0, padx=10, pady=2, sticky=(N, W, E, S))

        # Create Label
        area_label = ttk.Label(select_panel, text='Area : ', anchor=W)
        asset_label = ttk.Label(select_1_panel, text='Realasset : ', anchor=W)
        saveto_label = ttk.Label(select_panel, text='Save to :', anchor=W)
        area_code_label = ttk.Label(status_panel, text='Area code :', anchor=W)
        stitle_label = ttk.Label(status_panel, text='File Title :', anchor=W)
        status_label = ttk.Label(status_panel, text='Status :', anchor=W)
        progress_label = ttk.Label(progress_panel, text='Progress : ', anchor=W)

        # Create Entry Widget for input infomation
        self.areaentry = ttk.Entry(select_panel, width=45)
        self.savetoentry = ttk.Entry(select_panel, width=45)

        # Create Radiobutton for select trade infomation
        self.trade_act1 = ttk.Radiobutton(select_1_panel, text='ALL', variable= self.radVar, value='all')
        self.trade_act2 = ttk.Radiobutton(select_1_panel, text='매매', variable= self.radVar, value='A1')
        self.trade_act3 = ttk.Radiobutton(select_1_panel, text='전세', variable= self.radVar, value='B1')
        self.trade_act4 = ttk.Radiobutton(select_1_panel, text='월세', variable= self.radVar, value='B2')
        self.trade_act5 = ttk.Radiobutton(select_1_panel, text='단기임대', variable= self.radVar, value='B3')

        # Create Checkbox for select asset infomation
        self.asset_act1 = ttk.Checkbutton(select_1_panel, text='아파트', variable=self.checkVar1)
        self.asset_act2 = ttk.Checkbutton(select_1_panel, text='주상복합', variable=self.checkVar2)
        self.asset_act3 = ttk.Checkbutton(select_1_panel, text='재건축', variable=self.checkVar3)

        # Create Progressbar
        self.progress = ttk.Progressbar(progress_panel, orient=HORIZONTAL, length=380, mode='determinate')

        # Create Message (area, stitle, Status)
        self.area = ttk.Label(status_panel, textvariable=self.areamsg, anchor=W)
        self.stitle = ttk.Label(status_panel, textvariable=self.stitlemsg, anchor=W)
        self.status = ttk.Label(status_panel, textvariable=self.statusmsg, anchor=W)

        # Create Buttons
        saveto_button = ttk.Button(select_panel, text="Folder", command=self.folder)
        start_button = ttk.Button(progress_panel, text="Start", command=self.start)
        # cancel_button = ttk.Button(progress_panel, text="Cancel", command=self.cancel)

        # Locate widges for select Panel
        area_label.grid(column=0, row=0, sticky=W)
        self.areaentry.grid(column=1, row=0, sticky=W)
        saveto_label.grid(column=0, row=4, sticky=W)
        self.savetoentry.grid(column=1, row=4, sticky=W)
        saveto_button.grid(column=2, row=4, padx=5, stick=W)

        # Locate Widges for select_1 Panel(radiobutton & checkbox)
        asset_label.grid(column=0, row=0, sticky=W)
        self.trade_act1.grid(column=0, row=1, sticky=W)
        self.trade_act2.grid(column=1, row=1, sticky=W)
        self.trade_act3.grid(column=2, row=1, sticky=W)
        self.trade_act4.grid(column=3, row=1, sticky=W)
        self.trade_act5.grid(column=4, row=1, sticky=W)
        self.asset_act1.grid(column=0, row=2, sticky=W)
        self.asset_act2.grid(column=1, row=2, sticky=W)
        self.asset_act3.grid(column=2, row=2, sticky=W)

        # Locate widgets for Status Panel
        area_code_label.grid(column=0, row=0, padx=5, sticky=W)
        self.area.grid(column=1, row=0, sticky=W)
        stitle_label.grid(column=0, row=1, padx=5, sticky=W)
        self.stitle.grid(column=1, row=1, sticky=W)
        status_label.grid(column=0, row=2, padx=5, sticky=W)
        self.status.grid(column=1, row=2, sticky=W)

        # Locate Widges for Progressbar
        progress_label.grid(column=0, row=0, sticky=W)
        self.progress.grid(column=1, row=0, sticky=W)
        start_button.grid(column=2, row=0, padx=5, sticky=W)
        # cancel_button.grid(column=2, row=1, padx=5, sticky=W)

        #self.root.columnconfigure(0, weight=1)
        #self.root.rowconfigure(0, weight=1)
        #content.columnconfigure(0, weight=1)
        #content.columnconfigure(1, weight=1)
        #content.rowconfigure(0, weight=1)
        #content.rowconfigure(1, weight=1)
    
    def getAsset(self, *args):
        '''
        hscpTypeCd (매물종류): 아파트=A01, 주상복합=A03, 재건축=A04 (복수 선택 가능)
        '''
        asset =''
        if self.checkVar1.get() == 1:
            asset = asset + 'A01'
            if self.checkVar2.get() == 1:
                asset = asset + '%3A' + 'A03'
                if self.checkVar3.get() == 1:
                    asset = asset + '%3A' + 'A04'
                else:
                    asset = asset
            else:
                asset = asset
                if self.checkVar3.get() == 1:
                    asset = asset + '%3A' + 'A04'
                else:
                    asset = asset
        else:
            asset = asset
            if self.checkVar2.get() == 1:
                asset = asset + 'A03'
                if self.checkVar3.get() == 1:
                    asset = asset + '%3A' + 'A04'
                else:
                    asset = asset
            else:
                asset = asset
                if self.checkVar3.get() == 1:
                    asset = asset + 'A04'
                else:
                    asset = asset
        return asset

    # Function for Folder Button
    def folder(self, *args):
        self.saveto = fd.askdirectory()

        if self.saveto == '':
            return

        self.savetoentry.delete(0, END)
        self.savetoentry.insert(0, self.saveto)

    # Start Thread for downloading function
    def start(self, *args):
        asset = self.getAsset()
        trade = self.radVar.get() #tradeTypeCd(거래종류): all=전체, A1=매매, B1=전세, B2=월세, B3=단기임대
        areaname = self.areaentry.get()

        if areaname == '':
            self.statusmsg.set('Please input Area information')
            return

        thread = Thread(target=get_Naver_Data, args=[self, areaname, trade, asset, self.saveto])
        thread.setDaemon(False)
        thread.start()

    # Function for Cancel Button
    # def cancel(self, *args):
    #     self.flag = False
    #     self.root.destroy()
    #     return

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    obj = MyLand()
    obj.run()

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
        global MYCONVERT_LOGO
        # self.openfrom = ''
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

        # Main Frame & Panels
        content = ttk.Frame(self.root, padding=(6, 6, 6, 6))
        content.grid(column=0, row=0, sticky=(N, W, E, S))

        logo_panel = ttk.Frame(content, padding=(3, 3, 3, 3))
        select_panel = ttk.Frame(content, relief='groove', padding=(6, 6, 6, 6))
        status_panel = ttk.Frame(content, relief='groove', padding=(6, 6, 10, 10))
        progress_panel = ttk.Frame(content, relief='groove', padding=(6, 6, 6, 6))

        logo_panel.grid(column=0, row=0, sticky=(N, W, E, S))
        select_panel.grid(column=0, row=1, sticky=(N, W, E, S))
        status_panel.grid(column=0, row=2, sticky=(N, W, E, S))
        progress_panel.grid(column=0, row=3, sticky=(N, W, E, S))

        # Create Logo
        try:
            MYCONVERT_LOGO = ImageTk.PhotoImage(Image.open('resources/converter.jpg'))
        except:
            pass

        # logolabel = ttk.Label(logo_panel, image='')
        logolabel = ttk.Label(logo_panel, image=MYCONVERT_LOGO)
        logolabel.grid(column=0, row=0, padx=10, pady=2, sticky=(N, W, E, S))

        # Create Label
        select_label = ttk.Label(select_panel, text='Area info : ', anchor=W)
        saveto_label = ttk.Label(select_panel, text='Save to :', anchor=W)
        stitle_label = ttk.Label(status_panel, text='File Title :', anchor=W)
        status_label = ttk.Label(status_panel, text='Status :', anchor=W)
        progress_label = ttk.Label(progress_panel, text='Progress : ', anchor=W)

        # Create Entry Widget for input video URL
        self.selectentry = ttk.Entry(select_panel, width=45)
        self.savetoentry = ttk.Entry(select_panel, width=45)

        # Create Progressbar
        self.progress = ttk.Progressbar(
            progress_panel, orient=HORIZONTAL, length=380, mode='determinate')

        # Create sTitle & Status Message
        self.stitle = ttk.Label(status_panel, textvariable=self.stitlemsg, anchor=W)
        self.status = ttk.Label(status_panel, textvariable=self.statusmsg, anchor=W)

        # Create Buttons
        saveto_button = ttk.Button(select_panel, text="Folder", command=self.folder)
        start_button = ttk.Button(progress_panel, text="Start", command=self.start)
        # cancel_button = ttk.Button(progress_panel, text="Cancel", command=self.cancel)

        # Locate widges for select Panel
        select_label.grid(column=0, row=0, sticky=W)
        self.selectentry.grid(column=1, row=0, sticky=W)
        saveto_label.grid(column=0, row=1, sticky=W)
        self.savetoentry.grid(column=1, row=1, sticky=W)
        saveto_button.grid(column=2, row=1, padx=5, stick=W)

        # Locate widgets for Status Panel
        stitle_label.grid(column=0, row=0, padx=5, pady=10, sticky=W)
        self.stitle.grid(column=1, row=0, sticky=W)
        status_label.grid(column=0, row=1, padx=5, sticky=W)
        self.status.grid(column=1, row=1, sticky=W)

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

    # Function for Folder Button
    def folder(self, *args):
        self.saveto = fd.askdirectory()

        if self.saveto == '':
            return

        self.savetoentry.delete(0, END)
        self.savetoentry.insert(0, self.saveto)

    # Start Thread for downloading function
    def start(self, *args):
        areaname = self.selectentry.get()

        if areaname == '':
            self.statusmsg.set('Please input Area information')
            return

        thread = Thread(target=get_Naver_Data, args=[self, areaname, self.saveto])
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

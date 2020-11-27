import tkinter as tk
from tkinter import ttk, filedialog, constants
import object
import os

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

data = None

class Skeletonization(tk.Frame):
    """A friendly little module"""
    net = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.topcolor = '#c2d9ff'
        topbar = tk.Frame(self, bg=self.topcolor, width=280, height=120, borderwidth=2)
        topbar.pack(expand=False, fill='both', side='top', anchor='n')

        self.filename = tk.StringVar()

        self.inputlabel = tk.Label(topbar, text = 'Inputfile: ', bg=self.topcolor, padx=5, pady=20)
        self.filename_label = tk.Entry(topbar, width=60)
        self.button = tk.Button(topbar, text="Browse", command=self.load_file, width=10)

        self.inputlabel.grid(row=0, column=0)
        self.filename_label.grid(row=0, column=1)
        self.button.grid(row=0, column=3)


        container = tk.Frame(self, bg='white', width=500, height=200, borderwidth=2)
        container.pack(expand=True, fill='both', side='top')
        self.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Empty, Skel_general, Node_attachment):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Empty)



    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def load_file(self):

        fname = tk.filedialog.askopenfilename(filetypes=(('INP', '*.inp'), ('Text', '*.txt')))

        if fname:
            try:
                data = object.Network(fname)
                self.filename_label.delete(0, 'end')
                self.filename_label.insert(0, os.path.basename(fname))
                Skel_general(data)
                self.show_frame(Skel_general)

            except:  # <- naked except is a bad idea
                #showerror("Open Source File", "Failed to read file\n'%s'" % fname)
                popupmsg('Loading error: {}'.format(fname))


class Empty(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        container = tk.Frame(self, bg='white', width=500, height=200, borderwidth=2)
        container.pack(expand=True, fill='both')

class Skel_general(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, data, parent)

        label = tk.Label(self, text="File information")
        label.grid(row=0, column=0)
        if data != None:
            print(len(data.nodes))

class Node_attachment(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Node attachment!!!")
        label.pack(pady=10,padx=10)



class MyApplication(tk.Tk):
    """Hello World Main Application"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the window properties
        self.title("INP Tool")
        self.geometry("1000x600")
        self.frame()

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=lambda: popupmsg("Not supported just yet"))
        filemenu.add_command(label="Export settings", command = lambda: popupmsg("Not supported just yet"))
        filemenu.add_command(label="Import settings", command=lambda: popupmsg("Not supported just yet"))
        filemenu.add_command(label="Standard settings", command=lambda: popupmsg("Not supported just yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        info_tab = tk.Menu(menubar, tearoff=0)
        info_tab.add_command(label="File configure", command=lambda: popupmsg("Not supported just yet"))
        info_tab.add_command(label="Map configure", command=lambda: popupmsg("Not supported just yet"))
        menubar.add_cascade(label="Info", menu=info_tab)

        help_tab = tk.Menu(menubar, tearoff=0)
        help_tab.add_command(label="About", command=lambda: popupmsg("Not supported just yet"))
        menubar.add_cascade(label="Help", menu=help_tab)

        tk.Tk.config(self, menu=menubar)

        sidebar = tk.Frame(self, bg='#c2d9ff', width=280, height=500, relief='raised', borderwidth=2)
        sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        # Define the UI
        Skeletonization(self).pack(expand=True, fill='both', side='right')
        self.columnconfigure(0, weight=1)


def popupmsg(msg):
    popup = tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("Error")

    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10, padx=10)
    B1 = ttk.Button(popup, text="Okay", command=leavemini)
    B1.pack()

    popup.mainloop()

if __name__ == '__main__':
    app = MyApplication()
    app.mainloop()
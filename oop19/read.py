import tkinter as tk
import object
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Arial", 10, 'bold')
SMALL_FONT = ("Arial", 10)

net = object.Network('Ledninger2019.inp')

def pie_nodes():
    data = {'Junctions': len(net.junctions),
            'Reservoirs': len(net.reservoirs),
            'Tanks': len(net.tanks)}
    return data

class root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1100x600")
        self.orange = '#ffb978'
        self.xshift = 10
        self.frame()

        node_label = ttk.Label(self, text='Information', font=LARGE_FONT)
        node_label.grid(row=0, column=0, sticky='NW', pady=(10,0) , padx=15)
        frame = tk.Frame(self, highlightbackground='grey', highlightcolor='green', highlightthickness=1, height=500, width=1000, borderwidth=20, bd=0)
        frame.grid(row=1, column=0, sticky='NW', padx=5, pady=(0,5))
        frame.configure(height=frame["height"], width=frame["width"])
        frame.grid_propagate(0)

        datapoint_label = tk.Label(frame, text='Datapoints', font=NORM_FONT)
        datapoint_label.grid(row=0, column=0, sticky='NW', padx=20, pady=(15, 0))


        datapoints = tk.Frame(frame, bg=self.orange, height=150, width=250)
        datapoints.grid(row=1, column=0, sticky='NW', padx=20)
        datapoints.configure(height=datapoints["height"], width=datapoints["width"])
        datapoints.grid_propagate(0)


        junctions = tk.Label(datapoints, text='Junctions:', bg=self.orange, font=SMALL_FONT)
        junctions.grid(row=1, column=0, sticky='NW', padx=10)
        junc_number = tk.Label(datapoints, text=len(net.junctions), bg=self.orange, font=SMALL_FONT)
        junc_number.grid(row=1, column=1, sticky='NW')

        reservoirs = tk.Label(datapoints, text='Reservoirs:', bg=self.orange, font=SMALL_FONT)
        reservoirs.grid(row=2, column=0, sticky='NW', padx=10)
        res_number = tk.Label(datapoints, text=len(net.reservoirs), bg=self.orange, font=SMALL_FONT)
        res_number.grid(row=2, column=1, sticky='NW')

        tanks = tk.Label(datapoints, text='Tanks:', bg=self.orange, font=SMALL_FONT)
        tanks.grid(row=3, column=0, sticky='NW', padx=10)
        tank_number = tk.Label(datapoints, text=len(net.tanks), bg=self.orange, font=SMALL_FONT)
        tank_number.grid(row=3, column=1, sticky='NW')

        nodes = tk.Label(datapoints, text='Total nodes:', bg=self.orange, font=SMALL_FONT)
        nodes.grid(row=4, column=0, sticky='NW', padx=10)
        node_number = tk.Label(datapoints, text=len(net.nodes), bg=self.orange, font=SMALL_FONT)
        node_number.grid(row=4, column=1, sticky='NW')

        #node_plot = tk.Frame(frame).grid(row=1, column=1)

        df1 = pie_nodes()
        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, frame)
        bar1.get_tk_widget().grid(row=1, column=1)
        df1.plot(kind='pie', legend=True, ax=ax1)
        ax1.set_title('Nodes')

        def add():
            tk.Entry(frame).grid()

        def disable():
            frame.configure(height=frame["height"], width=frame["width"])
            frame.grid_propagate(0)

        def enable():
            frame.grid_propagate(1)



if __name__ == '__main__':
    app = root()
    app.mainloop()
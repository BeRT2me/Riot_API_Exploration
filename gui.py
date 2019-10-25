import tkinter as tk
from tkinter import ttk
from league_lists import champions
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    df = pd.read_pickle('all_base_stats.pkl')
except FileNotFoundError:
    import create_patch_datafile
    df = pd.read_pickle('all_base_stats.pkl')

def Graph(y):
    ax1 = figure1.add_subplot(111).remove()
    ax1 = figure1.add_subplot(111)
    if var.get() != 'All Champions':
        data = df[df.champion == var.get()].groupby('version').mean().reset_index()
    else:
        data = df.groupby('version').mean().reset_index()
    sb.scatterplot(data=data, y=y, x='version', ax=ax1)
    ax1.set_xticks(['4.01', '5.01', '6.01', '7.01', '8.01', '9.01', '9.20'])
    ax1.axvline(x='4.01')
    ax1.axvline(x='5.01')
    ax1.axvline(x='6.01')
    ax1.axvline(x='7.01')
    ax1.axvline(x='8.01')
    ax1.axvline(x='9.01')
    ax1.set_title(var.get())
    plt.legend('')
    scatter1.draw()


def Buttons(button):

    if button == 'attack_speed':
        y = 'attackspeed'
    elif button == 'attack_damage':
        y = 'attackdamage'
    elif button == 'armor':
        y = 'armor'
    elif button == 'hp':
        y = 'hp'
    elif button == 'move_speed':
        y = 'movespeed'
    elif button == 'attack_damage_level':
        y = 'attackdamageperlevel'
    Graph(y)


root = tk.Tk()
champ_names = tk.StringVar(value=champions)
top = tk.Frame(root)
bottom = tk.Frame(root)
top.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

var = tk.StringVar(root)
var.set('All Champions')
champ_list = tk.OptionMenu(root, var, *champions)
champ_list.pack(in_=top, side=tk.LEFT)

attack_speed = ttk.Button(root, text='Attack Speed', command=lambda: Buttons('attack_speed'))
attack_speed.pack(in_=top, side=tk.LEFT)

attack_damage = ttk.Button(root, text='Attack Damage', command=lambda: Buttons('attack_damage'))
attack_damage.pack(in_=top, side=tk.LEFT)

attack_damage_level = ttk.Button(root, text="Attack Dmg/Level", command=lambda: Buttons('attack_damage_level'))
attack_damage_level.pack(in_=top, side=tk.LEFT)

armor = ttk.Button(root, text='Armor', command=lambda: Buttons('armor'))
armor.pack(in_=top, side=tk.LEFT)

hp = ttk.Button(root, text='Hitpoints', command=lambda: Buttons('hp'))
hp.pack(in_=top, side=tk.LEFT)

move_speed = ttk.Button(root, text='Movement Speed', command=lambda: Buttons('move_speed'))
move_speed.pack(in_=top, side=tk.LEFT)

figure1 = plt.Figure(figsize=[14.70, 8.27], dpi=100)
scatter1 = FigureCanvasTkAgg(figure1, root)
scatter1.get_tk_widget().pack(in_=bottom, fill=tk.BOTH)


root.mainloop()

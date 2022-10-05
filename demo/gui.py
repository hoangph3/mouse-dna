# importing whole module
from tkinter import * 
from tkinter.ttk import *
  
# importing strftime function to
# retrieve system's time
from time import strftime
import random
  
# creating tkinter window
root = Tk()
root.title('Clock')
  
# This function is used to 
# display time on the label
def time():
    string = "Trust Score: {}".format(random.randint(0, 123))
    lbl.config(text = string)
    lbl.after(1000, time)
  
# Styling the label widget so that clock
# will look more attractive
lbl = Label(root, font = ('calibri', 20, 'bold'),
            background = 'black',
            foreground = 'white')
  
# Placing clock at the centre
# of the tkinter window
lbl.pack(anchor = 'center')
time()
  
mainloop()
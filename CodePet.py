import random
import tkinter as tk
from pathlib import Path
from pynput import *

import argparse

parser = argparse.ArgumentParser(description='puppet programm.')

parser.add_argument("-c", "--comp_prob", help="list of probabilities to get comportment", type=int, nargs='*')
parser.add_argument("-s", "--size_prob", help="list of probabilities to get size", type=int, nargs='*')

args = parser.parse_args()


impath = '.\\Assets\\'

x = 1400
cycle = 0
animation = 0

frameCount = 0

x_m = 50
y_m = 50

# on assign un gif a un numero.
## Plus on il y a de numero plus il y a de chance de commencer par ce gif.
## dans gif_work, il recalcul le event_number en changeant les parametre de l'aleatoir voir gif_work
### Dans l'idee ton randrange devra etre sur 100, a chaque fois que tu assign un gif a un numero \
### tu lui donne 10% de chance detre executer

probality=0
for i in args.comp_prob:
    probality += i

accumulator = 0;
accumulatorOld = 0
accumulator+= args.comp_prob[0]
idle_num = list(range(accumulatorOld, accumulator))
accumulatorOld=accumulator
accumulator+= args.comp_prob[1]
cry_num = list(range(accumulatorOld, accumulator))
#accumulatorOld=accumulator
#accumulator+= args.comp_prob[2]
#exe_num = list(range(accumulatorOld, accumulator))

#pleur_num = list(range(7,11))
#print("idle list", idle_num)
#print("cry list", cry_num)
event_number = random.randrange(probality)

def get_coords (x, y):
    global x_m
    global y_m
    x_m = x
    y_m = y
    #print(x_m, y_m)

#transfer random no. to event
def event(cycle, animation, event_number, x):
    if event_number in idle_num:
        animation = 0
        #print('idle')
        window.after(5, update, cycle, animation, event_number, x)

    elif event_number in cry_num:
        animation = 1
        #print('cry')
        window.after(5, update, cycle, animation, event_number, x)

# make the gif work
def gif_work(cycle, frames, event_number):
    global frameCount
    if frameCount%3 == 0:
        if cycle < len(frames) -1:
            cycle += 1
        else:
            cycle = 0
            ### ici on relance le choix de lanimation
            #  event_number = random.randrange(first_num, last_num + 1, 1) # ce recall est incomprehensible
            event_number = random.randrange(probality)

    return cycle, event_number


with mouse.Listener(on_move = get_coords) as listen:
    def update(cycle, animation, event_number, x):
        global frameCount

        # idle
        if animation == 0:
            frame = idle[cycle]
            cycle, event_number = gif_work(cycle, idle, event_number)

        # cry
        elif animation == 1:
            frame = cry[cycle]
            cycle, event_number = gif_work(cycle, cry, event_number)


        #print("animation ::" + str(animation))
        window.geometry('842' 'x' '842+' + str(x_m-421) + "+" + str(y_m-421))
        #window.geometry(str(frameCount)+'x''842+' + str(x_m-421) + "+" + str(y_m-421))
        label.configure(image=frame)

        frameCount = frameCount + 1
        window.after(1, event, cycle, animation, event_number, x)

    window = tk.Tk()

    # call buddy's action .gif to an array
    idle = [tk.PhotoImage(file=file, format='png') for file in Path("./Assets/place_png").iterdir() if file.suffix.lower() == ".png"]
    cry = [tk.PhotoImage(file=file, format='png') for file in Path("./Assets/exister_png").iterdir() if file.suffix.lower() == ".png"]
    #pleur = [tk.PhotoImage(file=file, format='png') for file in Path("./Assets/pleure_png").iterdir() if file.suffix.lower() == ".png"]

    label = tk.Label(window)
    window.overrideredirect(True)
    window.attributes('-transparentcolor','#f0f0f0')
    window.attributes('-topmost',True)

    label.pack()

    #loop the program
    window.after(1,update,cycle,animation,event_number,x)

    window.mainloop()

    listen.join()

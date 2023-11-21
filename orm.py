import tkinter as tk
import random

personas = []
numeropersonas = 20

class Persona:
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.radio = 30
    def dibuja(self):
        lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill="red")

raiz = tk.Tk()

lienzo = tk.Canvas(width=1024,height=1024)
lienzo.pack()

for i in range(0,numeropersonas):
    personas.append(Persona())

for persona in personas:
    persona.dibuja()


raiz.mainloop()

import tkinter as tk

class Persona:
    def __init__(self):
        self.posx = 512
        self.posy = 512
    def dibuja(self):
        lienzo.create_oval(30,30,60,60,fill="red")

raiz = tk.Tk()

lienzo = tk.Canvas(width=1024,height=1024)
lienzo.pack()

persona = Persona()
persona.dibuja()

raiz.mainloop()

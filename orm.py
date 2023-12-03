import tkinter as tk
import random
import math
import json
import sqlite3

# Declaración de variables globales

personas = []
numeropersonas = 50

class Recogible():
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.color = "blue"
    def serializar(self):
        recogible_serializado = {
            "posx":self.posx,
            "posy":self.posy,
            "color":self.color
            }
        return recogible_serializado
class Persona():
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.color = "blue"
        self.radio = 30
        self.direccion = random.randint(0,360)
        
        self.entidad = ""
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
        self.inventario = []
        for i in range(0,10):
            self.inventario.append(Recogible())
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
        self.entidadenergia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-10,
            self.posx+self.radio/2,
            self.posy-self.radio/2-8,
            fill="green"
            )
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-16,
            self.posx+self.radio/2,
            self.posy-self.radio/2-14,
            fill="blue"
            )
    def mueve(self):
        if self.energia > 0:
            self.energia -= 0.1
        if self.descanso > 0:
            self.descanso -= 0.1
        self.colisiona()
        lienzo.move(
            self.entidad,
            math.cos(self.direccion),
            math.sin(self.direccion))
        anchuradescanso = (self.descanso/100)*self.radio
        lienzo.coords(
            self.entidaddescanso,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 16,
            self.posx - self.radio/2 + anchuradescanso,
            self.posy - self.radio/2 - 14
        )
        anchuraenergia = (self.energia/100)*self.radio
        lienzo.coords(
            self.entidadenergia,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 10,
            self.posx - self.radio/2 + anchuraenergia,
            self.posy - self.radio/2 - 8
        )
        
        self.posx += math.cos(self.direccion)
        self.posy += math.sin(self.direccion)
    def colisiona(self):
        if self.posx < 0 or self.posx > 1024 or self.posy < 0 or self.posy > 1024:
            self.direccion += math.pi
    def serializar(self):
        persona_serializada = {
            "posx":self.posx,
            "posy":self.posy,
            "radio":self.radio,
            "direccion":self.direccion,
            "color":self.color,
            "energia":self.energia,
            "descanso":self.descanso,
            "inventario":[item.serializar() for item in self.inventario]
            }
        return persona_serializada
            
def guardarPersonas():
    print("guardo a los jugadores")
    #También guardo en json con fines demostrativos
    personas_serializadas = [persona.serializar() for persona in personas]
##    cadena = json.dumps(personas_serializadas)
##    archivo = open("jugadores.json",'w')
##    archivo.write(cadena)
    with open("jugadores.json","w") as archivo:
        json.dump(personas_serializadas,archivo,indent=4)

    # Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()
    cursor.execute('''
            DELETE FROM jugadores 
            ''')
    cursor.execute('''
            DELETE FROM recogibles 
            ''')
    conexion.commit()
    for persona in personas:
        cursor.execute('''
            INSERT INTO jugadores
            VALUES (
                NULL,
                '''+str(persona.posx)+''',
                '''+str(persona.posy)+''',
                '''+str(persona.radio)+''',
                '''+str(persona.direccion)+''',
                "'''+str(persona.color)+'''",
                "'''+str(persona.entidad)+'''",
                '''+str(persona.energia)+''',
                '''+str(persona.descanso)+''',
                "'''+str(persona.entidadenergia)+'''",
                "'''+str(persona.entidaddescanso)+'''",
                "'''+str(persona.inventario)+'''"
            )
            ''')
        for recogible in persona.inventario:
            peticion = '''
            INSERT INTO recogibles
            VALUES (
                NULL,
                '''+str(persona.entidad)+''',
                "'''+str(recogible.posx)+'''",
                "'''+str(recogible.posy)+'''",
                "'''+str(recogible.color)+'''"
            )
            '''

            cursor.execute(peticion)
    conexion.commit()
    conexion.close()
    
# Creo una ventana
raiz = tk.Tk()

#En la ventana creo un lienzo
lienzo = tk.Canvas(raiz,width=1024,height=1024)
lienzo.pack()

#Boton de guardar
boton = tk.Button(raiz,text="Guarda",command=guardarPersonas)
boton.pack()

# cargar personas desde SQL
try:
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()

    cursor.execute('''
            SELECT *
            FROM jugadores
            
            ''')
    while True:
        fila = cursor.fetchone()
        if fila is None:
            break
        #print(fila)
        persona = Persona()
        persona.posx = fila[1]
        persona.posy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.entidad = fila[6]
        persona.energia = fila[7]
        persona.descanso = fila[8]
        persona.entidadenergia = fila[9]
        persona.entidaddescanso = fila[10]
        
        cursor2 = conexion.cursor()
        nuevapeticion = '''
            SELECT *
            FROM recogibles
            WHERE persona = '''+persona.entidad+'''
            '''
        print(nuevapeticion)
        cursor2.execute(nuevapeticion)
        while True:
            fila2 = cursor2.fetchone()
            if fila2 is None:
                break
            nuevorecogible = Recogible()
            nuevorecogible.posx = fila2[2]
            nuevorecogible.posy = fila2[3]
            nuevorecogible.color = fila2[4]
            persona.inventario.append(nuevorecogible)
            #pass
           
        personas.append(persona)
    conexion.close()
    print(personas)
except sqlite3.Error as error:
    print("error al leer base de datos",error)

# En la colección introduzco instancias de personas en el caso de que no existan
print(len(personas))
if len(personas) == 0:
    numeropersonas = 5
    for i in range(0,numeropersonas):
        personas.append(Persona())

# Para cada una de las personas en la colección las pinto
for persona in personas:
    persona.dibuja()
    
# Creo un bucle repetitivo
def bucle():
    # Para cada persona en la colección
    for persona in personas:
        persona.mueve()
    raiz.after(10,bucle)
    
#Ejecuto el bucle
bucle()

raiz.mainloop()

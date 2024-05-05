from tkinter import *
from PIL import Image
import random


GAME_ANCHO = 700
GAME_ALTO = 700

SPEED = 100
SPACE_SIZE = 25

BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND = "#0000FF"

GAMEOVER = False



class Serpiente:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordenadas = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordenadas.append([0, 0])


        for x, y in self.coordenadas: 
            squares = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
            self.squares.append(squares)

class Manzana:
    
    def __init__(self):

        x = random.randint(0, 27) * SPACE_SIZE # 28 = GAME_ANCHO/SPACE_SIZE - 1 --> el "-1" es para que la manzana se dibuje en la última posición de ancho y no supere el borde
        y = random.randint(0, 27) * SPACE_SIZE # 28 = GAME_ALTO/SPACE_SIZE - 1 --> el "-1" es para que la manzana se dibuje en la última posición de altura y no supere el borde

        self.coordenadas = [x, y]

        canvas.create_oval (x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tag = "manzana")



def siguiente_turno(serpiente, manzana):
    
    x, y = serpiente.coordenadas[0]

    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    serpiente.coordenadas.insert(0, (x, y))

    squares = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)

    serpiente.squares.insert(0, squares)

    if x == manzana.coordenadas[0] and y == manzana.coordenadas[1]:

        global score

        score += 1
        
        label.config(text = "Puntuación:{}".format(score))

        canvas.delete("manzana")

        manzana =  Manzana()

    else: 
        del serpiente.coordenadas[-1]

        canvas.delete(serpiente.squares[-1])

        del serpiente.squares[-1]

    if colision(serpiente):
        gameover()

    else:
        window.after(SPEED, siguiente_turno, serpiente, manzana)




def cambiar_direccion(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    if new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    if new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    if new_direction == 'down':
        if direction != 'up':
            direction = new_direction



def colision(serpiente):
    x, y = serpiente.coordenadas[0]

    if x < 0 or x >= GAME_ANCHO:
        print("GAME_OVER")
        return True
    
    elif y < 0 or y >= GAME_ALTO:
        print("GAME OVER")
        return True

    for body_part in serpiente.coordenadas[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
        
    return False



def gameover():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ('consola', 70), text = "GAME OVER", fill = "red", tag = "gameover")
    GAMEOVER = True



window = Tk()
window.title("El juego de la serpiente")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text = "Puntuación:{}".format(score), font = ('consolas', 40))
label.pack()

canvas = Canvas(window, bg = BACKGROUND, height = GAME_ALTO, width = GAME_ANCHO)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: cambiar_direccion('left'))
window.bind('<Right>', lambda event: cambiar_direccion('right'))
window.bind('<Up>', lambda event: cambiar_direccion('up'))
window.bind('<Down>', lambda event: cambiar_direccion('down'))

serpiente = Serpiente()
manzana = Manzana()

siguiente_turno(serpiente, manzana)

window.mainloop()
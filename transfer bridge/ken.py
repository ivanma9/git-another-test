import tkinter as tk # importing tkinter library so we can use graphics
from PIL import ImageTk, Image
import random # for randoming position

# NOTE: Tkinter window's top left corner is (0,0). 
# X-axis increases when goes right. Y-axis increases when goes down

# global variables for specifying window's size
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500

pac_queue = [] # list/array for storing pacman
dot_canvas_list = [] # list/array for storing dot
ghost_canvas_list = [] # list/array for storing ghost

class Pacman:
    def __init__(self, canvas):
        # initialize position of pacman and draw on canvas
        # <self> refers to the class itself. Below codes are essentially "attributes" for Pacman's class
        self.x = 100
        self.y = 100
        self.draw(canvas)

    def draw(self, canvas):
        # remove pacman from the list if the list is not empty
        if len(pac_queue) != 0: # len() return amount of data in the parameter
            canvas.delete(pac_queue[0]) # delete pacman from canvas. If don't do this, then previous pacman will stay there
            pac_queue.pop()
        
        size = 30
        # create yellow pacman on canvas. create_oval(x1, y1, x2, y2) draws a circle. 
        # Topleft is at (x1,y1). Bottomright at (x2,y2)
        x = canvas.create_oval(self.x - size, self.y - size, self.x + size, self.y + size, fill='yellow')
        # store pacman at the list
        pac_queue.append(x)
    
    def moveLeft(self, event, canvas):
        self.x -= 10
        self.draw(canvas)
    
    def moveRight(self, event, canvas):
        self.x += 10
        self.draw(canvas)

    def moveUp(self, event, canvas):
        self.y -= 10
        self.draw(canvas)

    def moveDown(self, event, canvas):
        self.y += 10
        self.draw(canvas)

class Dot:
    def __init__(self, canvas):
        # initialize position by randomization
        # call randrange() function from random library. Random number in range (0, WINDOW_WIDTH)
        self.x = random.randrange(WINDOW_WIDTH)
        self.y = random.randrange(WINDOW_HEIGHT)
        self.draw(canvas) # draw the dot on canvas

    # draw a dot on canvas
    def draw(self, canvas):
        size = 5
        # create a circle on canvas
        x = canvas.create_oval(self.x - size, self.y - size, self.x + size, self.y + size, fill='white')
        # append the dot to dot list
        dot_canvas_list.append(x)
    
    # reassign random position
    def changePos(self):
        self.x = random.randrange(WINDOW_WIDTH)
        self.y = random.randrange(WINDOW_HEIGHT)

class Ghost:
    def __init__(self, canvas, img):
        # initialize position by randomization
        # call randrange() function from random library. Random number in range (0, WINDOW_WIDTH)
        self.x = random.randrange(WINDOW_WIDTH)
        self.y = random.randrange(WINDOW_HEIGHT)
        self.draw(canvas, img) # draw the ghost on canvas

    # draw a ghost on canvas
    def draw(self, canvas, img):
        # create a circle on canvas
        x = canvas.create_image(self.x, self.y, image = img)
        # append the ghost to ghost list 
        ghost_canvas_list.append(x)

# check if pacman is on top of dot or not
def check(pacman, dot, canvas, window):
    if pacman.x - 30 <= dot.x <= pacman.x + 30\
        and pacman.y - 30 <= dot.y <= pacman.y + 30:
        canvas.delete(dot_canvas_list[0]) # erase dot from canvas
        dot_canvas_list.pop() # remove dot from list
        dot.changePos() # reassign a new position and draw on canvas
        dot.draw(canvas)

    window.after(100, check, pacman, dot, canvas, window) # use check() every 100 milliseconds
    # tk.after(<time-interval>, <function>, argument1, argument2, ...) call the <function> in every <time-interval>
    # and passing argument1, argument2, ... into the function
    
# check if pacman is on top of ghost or not
def gameOver(pacman, ghost, canvas, window):
    if pacman.x - 30 <= ghost.x <= pacman.x + 30\
        and pacman.y - 30 <= ghost.y <= pacman.y + 30:
        canvas.delete(ghost_canvas_list[0]) # erase ghost from canvas
        ghost_canvas_list.pop() # remove ghost from list
        canvas.delete(dot_canvas_list[0]) # erase dot from canvas
        dot_canvas_list.pop() # remove dot from list
        canvas.delete(pac_queue[0])
        window.unbind("<KeyPress-Left>") # need to pass event, otherwise won't work
        window.unbind("<KeyPress-Right>")
        window.unbind("<KeyPress-Up>")
        window.unbind("<KeyPress-Down>")
        canvas.configure(bg='white')
        canvas.create_text(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,fill="darkblue",font=("Times 20 italic bold",70),
                        text="GAME OVER")

    window.after(100, gameOver, pacman, ghost, canvas, window)
 
def main():
    window = tk.Tk() # create window pop-up
    canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='black') # create Canvas widget for drawing
    canvas.pack() # pack() organize, aka update, widgets onto canvas

    pacman = Pacman(canvas) # pass in canvas so pacman can be drawn
    window.bind("<KeyPress-Left>", lambda event: pacman.moveLeft(event, canvas)) # need to pass event, otherwise won't work
    window.bind("<KeyPress-Right>", lambda event: pacman.moveRight(event, canvas))
    window.bind("<KeyPress-Up>", lambda event: pacman.moveUp(event, canvas))
    window.bind("<KeyPress-Down>", lambda event: pacman.moveDown(event, canvas))

    dot = Dot(canvas)
 
    path = "ghost.png"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(Image.open(path).resize((30, 30), Image.ANTIALIAS))
    ## The (250, 250) is (height, width)
    ghost = Ghost(canvas, img)

#The Pack geometry manager packs widgets in rows or columns.
    #panel.pack(side = "bottom", fill = "both", expand = "yes")

    window.after(100, check, pacman, dot, canvas, window) # call check() to check dot&pacman after 100 milliseconds
    window.after(100, gameOver, pacman, ghost, canvas, window)
    window.mainloop() # tk.mainloop() -> keep looping until there's an update

main()
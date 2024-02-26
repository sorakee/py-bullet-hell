# Window resolution is set to 1280x720
import tkinter as tk
import random
import math
from os import system
from os.path import exists
from tkinter import Text, Entry, Tk, PhotoImage, Button, Frame
from tkinter import Canvas, Label, IntVar, StringVar, Toplevel

mouse = True
whichBG = 0
whichShip = 0
gameOver = False
pause = False
mousePos = [[640,360]]
mouseCoords = []
charLIST = ['w','a','s','d','q','e']
w = 720
h = 720
diff = 0
npb = 0 # nth player bullet
neb = 0 # nth enemy bullet

# Functions start
def bossKey(event):
    spreadsheet = Toplevel(window)
    spreadsheet.title("Microsoft Excel")
    spreadsheet.geometry("1600x900")
    canv = Canvas(spreadsheet, bg='white', width=1600, height=900)
    canv.pack()
    create_spreadsheet = canv.create_image(0, 0, image=spreadsheetIMG, anchor='nw')

# Ends the player's play session
def dead():
    global gameOver
    gameOver = True
    playArea.unbind("<Escape>")
    playArea.unbind("<Motion>")
    with open("save.txt", 'w') as f:
        print("10 0", file=f)
    button = Button(playArea, text="GAME OVER", fg='black', bg='white',
                    font=("Helvetica", 30), command=create_new_window)
    button.pack(ipadx = 200, ipady = 460)

# Closes the window
def exit():
    window.destroy()

# Creates a new window upon clicking the game over screen
def create_new_window():
    global new_window, submit
    new_window = Toplevel(window)
    new_window.geometry("200x170")
    new_window.title("Nice Try")
    yourscore1 = Label(new_window, text="Your score was ")
    yourscore1.pack()
    yourscore2 = Label(new_window, textvariable=score)
    yourscore2.pack()
    enter = Label(new_window, text="Enter your username :")
    enter.pack()
    reminder = Label(new_window, text="(Limit : 5 characters)")
    reminder.pack()
    user = Entry(new_window, textvariable=username)
    user.pack()
    submit = Button(new_window, text="Submit", fg='black', bg='white',
                    font=("Helvetica", 10), command=save_to_leaderboard)
    submit.pack()
    restartButton = Button(new_window, text="Restart Game", fg='black', bg='white',
                           font=("Helvetica", 10), command=restartGame)
    restartButton.pack()

# Save the player's score to a .txt file upon entering the player's username
def save_to_leaderboard():
    if username.get() == "" or len(username.get()) > 5:
        create_error()
    else:
        new_window.destroy()
        window.destroy()
        nameToBoard = username.get()
        scoreToBoard = str(score.get())
        with open('leaderboard.txt', 'a') as f:
            print(nameToBoard + ' : ' + scoreToBoard, file=f)

# Returns error if the player's name does meet the conditions
def create_error():
    global submit
    submit.config(text="ERROR")

# Increases the score every 100 ms by 1
def scoreOvertime():
    global SOT
    score.set(score.get() + 1)
    if not pause and not gameOver:
        SOT = playArea.after(100, scoreOvertime)
    else:
        playArea.after_cancel(SOT)

# Loads the leaderboard
def load_leaderboard():
    if exists('leaderboard.txt'):
        fetchScores = []
        with open('leaderboard.txt', 'r') as f:
            for line in f:
                fetchName, fetchScore = line.split(':')
                fetchScore = int(fetchScore)
                fetchScores.append((fetchName, fetchScore))
        fetchScores.sort(key=lambda s: s[1], reverse=True)
        yOffset = 0
        leaderboardFrame = Frame(window, width=235, height=400,
                                 bg="black", borderwidth=2,
                                 relief='raised',
                                 highlightcolor='white')
        leaderboardFrame.place(x=25,y=230)
        hallOfFame = Label(window, text = "Hall of Fame",
                           font=('Helvetica', 22), bg='black', fg='white')
        hallOfFame.place(x=50, y=250)
        for fetchName, fetchScore in fetchScores[:10]:
            fetchName1 = fetchName + "\n"
            fethcScore1 = str(fetchScore) + "\n"
            Name = tk.StringVar()
            Name.set(fetchName)
            UserScore = tk.StringVar()
            UserScore.set(fetchScore)
            leaderboardName = Label(window, textvariable = Name,
                                    font=('Helvetica',20),
                                    bg='black', fg='white')
            leaderboardScore = Label(window, textvariable = UserScore,
                                     font=('Helvetica',20),
                                     bg='black', fg='white')
            leaderboardName.place(x=50, y=300+yOffset)
            leaderboardScore.place(x=175, y=300+yOffset)
            yOffset += 30
    else:
        with open('leaderboard.txt', 'x') as f:
            pass

# Restart the game (everything is set to its default state)
def restartGame():
    window.destroy()
    with open("save.txt", 'w') as f:
        print("10 0",  file=f)
    system('python3 "./qte-shoot.py"')

# The cheat menu
def cheatmenu():
    cheatFrame = Frame(window, width=220, height=300,
                       bg="white", borderwidth=2,
                       relief='raised',
                       highlightcolor='white')
    cheatFrame.place(x=1030,y=230)
    cheatname = Label(window, text="Cheat Menu", fg='white', bg='black',
                      font=("Helvetica", 18))
    cheatname.place(x=1070, y=200)
    livesCheat = Button(window, text="999 Lives", fg='white', bg='black',
                        font=("Helvetica", 15), command=lives999)
    livesCheat.place(x=1080, y=300)
    cheat.config(text="CHEATS ENABLED")
    bulletSpam = Button(window, text="Bullet Spam \n(Warning: May Lag) \nPress z to shoot",
                        fg='white', bg='black', font=("Helvetica", 15),
                        command=bullet_Spam)
    bulletSpam.place(x=1035, y=350)

# Set lives to 999
def lives999():
    lives.set(999)

# Spams bullet when 'z' key is pressed
def bullet_Spam():
    global qte, repeat, randomChar
    playArea.after_cancel(qte)
    playArea.bind("z", create_bullets)

# Pauses the game
def pauseGame(event):
    global pause, button, save, restart, cheat
    global exitGame, backgroundEDIT, shipCONTROL, shipDesign
    pause = True
    playArea.unbind("<Escape>")
    playArea.unbind("<Motion>")
    exitGame = Button(playArea, text="Exit", fg='black', bg='white', width=15,
                      font=("Helvetica", 22), command=exit)
    exitGame.place(x = 240, y = 410)
    save = Button(playArea, text="Save Game", fg='black', bg='white', width=15,
                  font=("Helvetica", 22), command=saveGame)
    save.place(x = 240, y = 310)
    button = Button(playArea, text="Continue", fg='black', bg='white', width=15,
                    font=("Helvetica", 22), command=unpause)
    button.place(x = 240, y = 360)
    cheat = Button(playArea, text="Cheat Menu (Noob)", fg='red', bg='white',
                   width=15, font=("Helvetica", 22), command=cheatmenu)
    cheat.place(x = 240, y = 210)
    restart = Button(playArea, text="Reset", fg='black', bg='white', width=15,
                    font=("Helvetica", 22), command=restartGame)
    restart.place(x = 240, y = 260)
    backgroundEDIT = Button(playArea, text="Change Background", fg='black', bg='white',
                            font=("Helvetica", 22), width=15, command=bgChange)
    backgroundEDIT.place(x = 240, y = 460)
    shipCONTROL = Button(playArea, text="Change Ship Control", fg='black', bg='white',
                         font=("Helvetica", 22), width=15, command=controlChange)
    shipCONTROL.place(x = 240, y = 510)
    shipDesign = Button(playArea, text="Change Ship", fg='black', bg='white',
                        font=("Helvetica", 22), width=15, command=shipChange)
    shipDesign.place(x = 240, y = 560)

# Change the appearance of the ship
def shipChange():
    global whichShip
    if whichShip == 0:
        playArea.itemconfig(player, image=ship2)
        whichShip = 1
    else:
        playArea.itemconfig(player, image=ship)
        whichShip = 0

# Changes control of player
def controlChange():
    global mouse
    if mouse == True:
        mouse = False
    else:
        mouse = True

# Controls the player ship with arrow keys if control is changed
def moveShip(event):
    if event.keysym == 'Up':
        playArea.move(player, 0, -50)
    elif event.keysym == 'Down':
        playArea.move(player, 0, 50)
    elif event.keysym == 'Left':
        playArea.move(player, -50, 0)
    elif event.keysym == 'Right':
        playArea.move(player, 50, 0)

# Change background color
def bgChange():
    global whichBG
    if whichBG == 0:
        playArea.config(bg='black')
        whichBG = 1
    elif whichBG == 1:
        playArea.config(bg='darkblue')
        whichBG = 2
    elif whichBG == 2:
        playArea.config(bg='orange')
        whichBG = 3
    else:
        playArea.config(bg='lightgreen')
        whichBG = 0

# Save data to .txt file
def saveGame():
    global score, lives, diff, whichBG, whichShip
    save.config(text="Saved!")
    saveScore = score.get()
    saveLives = lives.get()
    with open('save.txt', 'w') as f:
        print(saveLives, saveScore, str(diff), whichBG, whichShip, file=f)

# Load data upon starting the game
def loadGame():
    global lives, score, diff, whichBG, whichShip
    if exists('save.txt'):
        with open('save.txt', 'r') as f:
            loadData = f.read().strip().split(" ")
        try:
            lives.set(loadData[0])
            score.set(loadData[1])
            diff = int(loadData[2])
            whichBG = int(loadData[3])
            if whichBG == 1:
                whichBG = 0
            elif whichBG == 2:
                whichBG = 1
            elif whichBG == 3:
                whichBG = 2
            else:
                whichBG = 3
            bgChange()
            whichShip = int(loadData[4])
            if whichShip == 1:
                whichShip = 0
            elif whichShip == 0:
                whichShip = 1
            shipChange()
        except Exception:
            pass
    else:
        pass

# Unpauses the game
def unpause():
    global pause, angle, neb, a, b, button, mouse, place
    global shipCONTROL, save, restart, cheat, backgroundEDIT, shipDesign
    pause = False
    button.place_forget()
    save.place_forget()
    restart.place_forget()
    cheat.place_forget()
    exitGame.place_forget()
    backgroundEDIT.place_forget()
    shipCONTROL.place_forget()
    shipDesign.place_forget()
    enemymove = playArea.after(100, enemy_movement)
    playArea.bind("<Escape>", pauseGame)
    if mouse == True:
        playArea.bind("<Motion>", follow_cursor)
        placeCharText()
        playArea.update()
    else:
        playArea.bind("<Key>", moveShip)
        placeCharText()
        playArea.update()
    enemybullet = playArea.after(1000, enemy_bullets)
    for i in range(neb):
        move_enemy_bullets(random.randint(0,360), i, a ,b)
    qte = playArea.after(1000, quicktimeEvent)
    colorchange = playArea.after(1000, ChangeColor)
    SOT = playArea.after(100, scoreOvertime)

# Get the player ship to follow the mouse cursor
def follow_cursor(event):
    global mousePos
    global mouseCoords
    mouseCoords = event.x, event.y
    mousePos = list(mouseCoords)
    playArea.coords(player, mouseCoords)
    placeCharText()
    update_mousePos()

def get_mousePos():
    return mousePos

def get_mouseCoords():
    return list(mouseCoords)

def update_mousePos():
    mouseCoords = get_mouseCoords()
    mousePos = get_mousePos()
    if len(mousePos) > 2:
        mousePos[0] = mouseCoords
        mousePos.pop()

# Spawns enemy
def boss_spawn():
    global w, h
    randomPosX = random.randint(0, w)
    randomPosY = random.randint(0, h//2)
    randomCoords = [[randomPosX, randomPosY]]
    if randomCoords != get_mousePos:
        bossShip = playArea.create_image(randomPosX, randomPosY, image=enemy,
                                         anchor="center", tag="enemy")
    else:
        pass

# Check for collision : Type A
def overlappingA(a, b):
    try:
        if (abs(a[0] - b[0]) < 15 and abs(a[1] - b[1]) < 15) or (abs(a[0] - b[2]) < 15 and abs(a[1] - b[3]) < 15):
            return True
    except Exception:
        return False

# Check for collision : Type B
def overlappingB(a, b):
    try:
        if math.sqrt(((a[0]-b[0])**2) + ((a[1]-b[1])**2)) < 50 or math.sqrt(((a[2]-b[0])**2) + ((a[3]-b[1])**2)) < 50:
            return True
    except Exception:
        return False

def playerenemycollision():
    global lives
    if overlappingB(playArea.coords(player), playArea.coords("enemy")):
        lives.set(lives.get() - 1)
        score.set(score.get() - 5)
        if lives.get() == 0:
            dead()

# Move enemy's position every 100 ms
def enemy_movement():
    global w, h, enemymove, pause
    enemyCoords = playArea.coords("enemy")
    enemyPosX = enemyCoords[0]
    enemyPosY = enemyCoords[1]
    numGen = random.randint(0, 3)
    if numGen == 0:
        playArea.move("enemy", random.randint(-60, 0), 0)
        if enemyPosX > w:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosX < 0:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosY < 100:
            playArea.coords("enemy", enemyPosX, 100)
        elif enemyPosY > h/2:
            playArea.coords("enemy", enemyPosX, h/2)
    elif numGen == 1:
        playArea.move("enemy", random.randint(0, 45), 0)
        if enemyPosX > w:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosX < 0:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosY < 100:
            playArea.coords("enemy", enemyPosX, 100)
        elif enemyPosY > h/2:
            playArea.coords("enemy", enemyPosX, h/2)
    elif numGen == 2:
        playArea.move("enemy", 0, random.randint(-65, 0))
        if enemyPosX > w:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosX < 0:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosY < 100:
            playArea.coords("enemy", enemyPosX, 100)
        elif enemyPosY > h/2:
            playArea.coords("enemy", enemyPosX, h/2)
    elif numGen == 3:
        playArea.move("enemy", 0, random.randint(0, 45))
        if enemyPosX > w:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosX < 0:
            playArea.coords("enemy", 360, enemyPosY)
        elif enemyPosY < 100:
            playArea.coords("enemy", enemyPosX, 100)
        elif enemyPosY > h/2:
            playArea.coords("enemy", enemyPosX, h/2)
    playerenemycollision()
    if not pause and not gameOver:
        enemymove = playArea.after(100, enemy_movement)
        # The rate at which the enemy moves
    else:
        playArea.after_cancel(enemymove)

# Check collision
def check_playercollision(neb):
    global lives
    playerCoords = playArea.coords(player)
    if overlappingA(playerCoords, playArea.coords(f"enemybullet{neb}")):
        lives.set(lives.get() - 1)
        score.set(score.get() - 5)
        playArea.delete(f"enemybullet{neb}")
        if lives.get() == 0:
            dead()

# Slightly increases the difficulty every 2 seconds
def difficulty_overtime():
    global diff
    if diff < 1400:
        diff += 10
    else:
        diff = 0
    return diff
    if not pause and not gameOver:
        diffOT = playArea.after(2000, difficulty_overtime)
    else:
        playArea.after_cancel(diffOT)

# Create's enemy bullets
def enemy_bullets():
    global neb, enemybullet, a, b
    r = list(range(-1,0)) + list(range(1,2)) # Generates a list of numbers
    a = random.choice(r)
    b = random.choice(r)
    enemyCoords = playArea.coords("enemy")
    if not pause and not gameOver:
        playArea.create_oval(enemyCoords[0]-10, enemyCoords[1]-10,
                             enemyCoords[0]+10, enemyCoords[1]+10,
                             fill="yellow", tag=f"enemybullet{neb}")
        move_enemy_bullets(0, neb, a, b)
        neb += 1
        enemybullet = playArea.after(1500-difficulty_overtime(), enemy_bullets)
        # Controls the rate of enemy's bullet creation
    else:
        playArea.after_cancel(enemybullet)

# Move enemy's bullets with a fixed pattern
def move_enemy_bullets(angle, neb, a, b):
    global enemybulletmove
    if angle >= 360:
        angle = 0
    x = 25 * math.cos(math.radians(angle))
    y = 25 * math.sin(math.radians(angle))
    angle += 4
    playArea.move(f"enemybullet{neb}", b+a*x, a+b*y)
    check_playercollision(neb)
    if not pause and not gameOver:
        enemybulletmove = playArea.after(random.randint(30,60), move_enemy_bullets,
                                         angle, neb, a, b)
    else:
        playArea.after_cancel(enemybulletmove)

# When the key button is pressed, shoot bullets
def create_bullets(event):
    global bulletPos, npb, charLIST
    mousePos = get_mousePos()
    playerCoords = playArea.coords(player)
    if mouse == True:
        bullet1 = playArea.create_line(mousePos[0]+10, mousePos[1],
                                       mousePos[0]+10, mousePos[1]+20,
                                       width="5", fill="cyan", tag=f"bullet1{npb}")
        bullet2 = playArea.create_line(mousePos[0]-10, mousePos[1],
                                       mousePos[0]-10, mousePos[1]+20,
                                       width="5", fill="cyan", tag=f"bullet2{npb}")
    else:
        bullet1 = playArea.create_line(playerCoords[0]+10, playerCoords[1],
                                       playerCoords[0]+10, playerCoords[1]+20,
                                       width="5", fill="cyan", tag=f"bullet1{npb}")
        bullet2 = playArea.create_line(playerCoords[0]-10, playerCoords[1],
                                       playerCoords[0]-10, playerCoords[1]+20,
                                       width="5", fill="cyan", tag=f"bullet2{npb}")
    moveBullets(npb)
    npb += 1
    for i in charLIST:
        playArea.unbind(i)

# Delete player's bullets when it exits the canvas or hits the enemy
def destroy_pbullets(npb):
    bulletA = playArea.coords(f"bullet1{npb}")
    bulletB = playArea.coords(f"bullet2{npb}")
    try:
        if bulletA[1] < 0 and bulletA[3] < 0 and bulletB[1] < 0 and bulletB[3] < 0:
            playArea.delete(f"bullet1{npb}")
            playArea.delete(f"bullet2{npb}")
        if overlappingB(bulletA, playArea.coords("enemy")) or overlappingB(bulletB, playArea.coords("enemy")):
            playArea.delete(f"bullet1{npb}")
            playArea.delete(f"bullet2{npb}")
            score.set(score.get() + 125)
    except Exception:
        pass

# Change color of char text on screen
def ChangeColor():
    color = ['lightblue', 'white', 'red', 'lightgreen']
    randomColor = random.choice(color)
    CharText.config(fg=f'{randomColor}')

def unbind_button():
    global randomChar
    playArea.unbind(randomChar)

# Change character on screen every 1 second
def quicktimeEvent():
    global randomChar, qte, colorchange
    randomChar = random.choice(charLIST)
    CharOnScreen.set(randomChar)
    playArea.bind(randomChar, create_bullets)
    if not pause and not gameOver:
        qte = playArea.after(1000, quicktimeEvent)
        colorchange = playArea.after(1000, ChangeColor)
    else:
        playArea.after_cancel(qte)
        playArea.after_cancel(colorchange)

# Move player's bullets
def moveBullets(npb):
    mousePos = get_mousePos()
    playArea.move(f"bullet1{npb}", 0, -50)
    playArea.move(f"bullet2{npb}", 0, -50)
    destroy_pbullets(npb)
    playArea.after(60, moveBullets, npb)

# Place char text on screen
def placeCharText():
    global place
    playerCoords = playArea.coords(player)
    if mouse == True:
        try:
            CharText.place(x = get_mouseCoords()[0] - 10,
                           y = get_mouseCoords()[1] - 100)
        except Exception:
            pass
    else:
        try:
            CharText.place(x = 340, y = 340)
        except Exception:
            pass
# Functions end

# Window creation start
window = Tk()
window.title("Space Pandemonium")
window.geometry("1280x720")

# Game Variables
username = tk.StringVar()
randomChar = ""
CharOnScreen = tk.StringVar()
score = tk.IntVar()
score.set(0)
lives = tk.IntVar()
lives.set(10)

# Preload images
background = PhotoImage(file="space.png")
ship = PhotoImage(file="spaceship.png")
enemy = PhotoImage(file="enemy.png")
spreadsheetIMG = PhotoImage(file="blank_spreadsheet.png")
ship2 = PhotoImage(file="spaceship2.png")

# Background
bg = Label(window, image=background)
bg.place(x=0, y=0)

# Canvas, key binds and player creation
playArea = Canvas(window, bg="black", width=w, height=h,
                  borderwidth=2, relief='sunken')
player = playArea.create_image(0, 0, image=ship, anchor="center")
playArea.pack()
playArea.bind("<Motion>", follow_cursor)
playArea.bind("<Escape>", pauseGame)
playArea.bind("r", bossKey) # Boss Key

# Create text and labels
livesText = Label(window, textvariable = lives, font=('Helvetica',22),
                  bg='black', fg='white', borderwidth=1, relief='raised')
livesText.place(x = 1170, y = 640)
livesLabel = Label(window, text = "Lives: ", font=('Helvetica',22),
                   bg='black', fg='white', borderwidth=1, relief='raised')
livesLabel.place(x = 1070, y = 640)
CharText = Label(playArea, textvariable = CharOnScreen, font=('Helvetica',22),
                 bg='black', fg='white', borderwidth=2, relief='groove')
CharText.place(x = 0, y = 0)
scoreText = Label(playArea, textvariable = score, font=('Helvetica',22),
                  bg='black', fg='white', borderwidth=2, relief='raised')
scoreText.place(x = 400, y = 20)
scoreLabel = Label(playArea, text = "Score :", font=('Helvetica',22),
                   bg='black', fg='white', borderwidth=2, relief='raised')
scoreLabel.place(x = 300, y = 20)
HowToText = Label(window, text="How to play?\n Dodge the bullets and \npress the key shown \non screen to shoot!",
                  font=('Helvetica',18), bg='black', fg='white', borderwidth=2,
                  relief='raised')
HowToText.place(x = 15, y = 50)

load_leaderboard()
loadGame()
quicktimeEvent()
scoreOvertime()
boss_spawn()
enemy_movement()
enemy_bullets()

playArea.focus_set()
window.mainloop()

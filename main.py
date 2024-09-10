import pygame as pg
import sys
from drawer import DrawingGrid, Point
from constants import *
from ui import WindowManager, Window, Button, Text
from neuralnet import *

pg.init()
CLOCK = pg.time.Clock()

FPS = 60

WIN = pg.display.set_mode((WIDTH, HEIGHT))
WINDOW_MANAGER = WindowManager(WIN)
DATA_FILE = "data.txt"
model = Network([400, 30, 5, 3])

def getData(data_file):
    with open(data_file, "r") as file:
        trainingSamples = []
        trainingLabels = []

        data = []

        for line in file:
            line.strip()
            sample, label = line.split("|")
            data.append(([eval(sample)], [oneHot(int(label), 3)]))
            trainingSamples.append([eval(sample)])
            trainingLabels.append([oneHot(int(label), 3)])
        
        return data, trainingSamples, trainingLabels
        
data, samples, labels = getData(DATA_FILE)
model.load("saved_model.txt")
# model.train(data, 1000, 0.01, 450)

def testAccuracy(testDataURL):
    testData, testSamples, testLabels = getData(testDataURL)
    counts = [0, 0, 0]
    totals = [0, 0, 0]
    for sample, label in zip(testSamples, testLabels):
        guess, confidence = model.guess(sample)
        totals[guess] += 1
        if label[0][guess] == 1:
            counts[guess] += 1
    print(f"Accuracy: {np.round(sum(counts) / sum(totals), 2) * 100}%")
    print(f"Circle: {np.round(counts[0] / totals[0], 2) * 100}%")
    print(f"Triangle: {np.round(counts[1] / totals[1], 2) * 100}%")
    print(f"Rectangle: {np.round(counts[2] / totals[2], 2) * 100}%")

testAccuracy("test_data.txt")
grid = DrawingGrid(Point(100, 100), (20, 20), tileSize=20)

guessText = "DRAW A SHAPE"
def guessShape():
    global guessText
    prediction, confidence = model.guess(grid.generateMap())

    if prediction == 0:
        print(f"{confidence}% CIRCLE")
        guessText = f"{confidence}% CIRCLE"
    elif prediction == 1:
        print(f"{confidence}% TRIANGLE")
        guessText = f"{confidence}% TRIANGLE"
    elif prediction == 2:
        print(f"{confidence}% RECTANGLE")
        guessText = f"{confidence}% RECTANGLE"

def updateGuess():
    return guessText

def logCircle():
    map = grid.generateMap()
    with open(DATA_FILE, "a") as dataFile:
        dataFile.write(str(map) + f"|{0}" + "\n")

def logTriangle():
    map = grid.generateMap()
    with open(DATA_FILE, "a") as dataFile:
        dataFile.write(str(map) + f"|{1}" + "\n")

def logRectangle():
    map = grid.generateMap()
    with open(DATA_FILE, "a") as dataFile:
        dataFile.write(str(map) + f"|{2}" + "\n")

Window(WINDOW_MANAGER, 
       [Button("Log Data", (190, 50), lambda : WINDOW_MANAGER.setActiveWindow(2), textColor=WHITE, centerX=(0, WIDTH)),
        Button("Guess", (420, 550), guessShape, textColor=WHITE, centerX=(WIDTH / 2, WIDTH)),
        Button("Clear", (100, 550), lambda: grid.resetGrid(), textColor=WHITE, centerX=(0, WIDTH / 2)),
        Text("DRAW A SHAPE", (180, 520), textUpdate=updateGuess, textColor=WHITE, centerX=(0, WIDTH)) 
], background=BACKGROUND)

Window(WINDOW_MANAGER, 
       [Button("Log CIRCLE", (10, 50), logCircle, textColor=RED),
        Button("Log TRIANGLE", (190, 50), logTriangle, textColor=GREEN),
        Button("Log RECTANGLE", (390, 50), logRectangle, textColor=BLUE),
        Button("Clear", (100, 550), lambda: grid.resetGrid(), textColor=WHITE, centerX=(0, WIDTH / 2)),
        Button("Return To Guessing", (420, 550), lambda: WINDOW_MANAGER.setActiveWindow(1), textColor=WHITE, centerX=(WIDTH / 2, WIDTH))
], background=BACKGROUND)
WINDOW_MANAGER.setActiveWindow(1)

running = True
while running:
    events = pg.event.get()
    
    WINDOW_MANAGER.update(events)

    grid.draw(WIN)
    grid.update(events)

    pg.display.update()
    CLOCK.tick(FPS)
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
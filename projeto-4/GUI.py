import matplotlib.pyplot as plt
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

WUMPUS_COLOR = "red"
PIT_COLOR = "black"
EMPTY_COLOR = "white"
ARROW_COLOR = "blue"
GOLD_COLOR = "yellow"


def fromMatrixPositionToXYCoordinates(matrixPosition):
    # XY from the rectangle left bottom
    return (0.2 + matrixPosition[1]*0.2, 0.8 - matrixPosition[0]*0.2)

def createArrows(matrixPosition, action):
    xy = fromMatrixPositionToXYCoordinates(matrixPosition)
    centerXY = (xy[0]+0.1, xy[1]+0.1)
    arrow = mpatches.Arrow(centerXY[0], centerXY[1], action[1]*0.09, -1*action[0]*0.09, width=0.05)
    return arrow

def label(xy, text):
    x = xy[0]+0.13
    y = xy[1]-0.01 
    plt.text(x, y, text, ha="center", family='sans-serif', size=10)

def drawWorldWithPolicy(policy=[], wumpusList=[], pitList=[], goldList=[]):
    fig, ax = plt.subplots()
    grid = np.mgrid[0.2:1.6:8j, 0.2:0.8:4j].reshape(2, -1).T

    patches = []
    arrowPatches = []
    wumpusPatches = []
    pitPatches = []
    goldPatches = []

    # add empty path
    for i in range(32):
        rect = mpatches.Rectangle(grid[i], 0.2, 0.2, 0.0)
        patches.append(rect)
        # label(grid[i], "Rectangle")
    
    # add wumpus positions
    for position in wumpusList:
        xy = fromMatrixPositionToXYCoordinates(position)
        xyCenter = (xy[0]+0.1, xy[1]+0.1)
        rect = mpatches.Circle(xyCenter, 0.09)
        wumpusPatches.append(rect)
    
    # add pit positions
    for position in pitList:
        xy = fromMatrixPositionToXYCoordinates(position)
        xyCenter = (xy[0]+0.1, xy[1]+0.1)
        rect = mpatches.Circle(xyCenter, 0.09)
        pitPatches.append(rect)
    
    # add gold positions
    for position in goldList:
        xy = fromMatrixPositionToXYCoordinates(position)
        xyCenter = (xy[0]+0.1, xy[1]+0.1)
        rect = mpatches.Circle(xyCenter, 0.09)
        goldPatches.append(rect)
    
    # add arrows positions:
    for position,action in policy:
        arrow = createArrows(position, action)
        arrowPatches.append(arrow)
    
    # add legend:
    p = (0.3,0.1)
    wumpus = mpatches.Circle(p, 0.017)
    wumpusPatches.append(wumpus)
    label(p, "wumpus")

    p = (0.7,0.1)
    gold = mpatches.Circle(p, 0.017)
    goldPatches.append(gold)
    label(p, "gold")

    p = (1.1,0.1)
    pit = mpatches.Circle(p, 0.017)
    pitPatches.append(pit)
    label(p, "pit")


    # empty position colors
    emptyPositionsCollection = PatchCollection(patches, facecolor=EMPTY_COLOR, edgecolor="black")
    ax.add_collection(emptyPositionsCollection)

    # wumpus colors
    wumpusCollections = PatchCollection(wumpusPatches, facecolors=WUMPUS_COLOR)
    ax.add_collection(wumpusCollections)

    # pit colors
    pitCollections = PatchCollection(pitPatches, facecolors=PIT_COLOR)
    ax.add_collection(pitCollections)

    # gold colors
    goldCollections = PatchCollection(goldPatches, facecolors=GOLD_COLOR)
    ax.add_collection(goldCollections)

    # arrow colors
    arrowsCollections = PatchCollection(arrowPatches, facecolors=ARROW_COLOR)
    ax.add_collection(arrowsCollections)

    plt.axis('equal')
    plt.axis('off')

    plt.show()

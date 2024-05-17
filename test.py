import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pygame # Import Pygame to create an interactive graphical interface, if you choose to make the game visually dynamic
import scipy
from scipy.stats import norm
import random
import pandas as pd
from PIL import Image
from matplotlib.animation import FuncAnimation
from PIL import Image

# Definisci la classe per le celle
class cell:
    def __init__(self, x=0, y=0, dist=0, parent=None):
        self.x = x
        self.y = y
        self.dist = dist
        self.parent = parent

# Controlla se la posizione è dentro la scacchiera
def isInside(x, y, N):
    return 1 <= x <= N and 1 <= y <= N

# Calcola il percorso minimo e ritorna i passi
def minStepToReachTarget(knightpos, targetpos, N):
    dx = [2, 2, -2, -2, 1, 1, -1, -1]
    dy = [1, -1, 1, -1, 2, -2, 2, -2]
    queue = [cell(knightpos[0], knightpos[1], 0)]
    visited = [[False] * (N + 1) for _ in range(N + 1)]
    visited[knightpos[0]][knightpos[1]] = True

    while queue:
        t = queue.pop(0)
        if (t.x == targetpos[0] and t.y == targetpos[1]):
            path = []
            while t:
                path.append((t.x, t.y))
                t = t.parent
            return path[::-1]  # Return reversed path

        for i in range(8):
            x, y = t.x + dx[i], t.y + dy[i]
            if isInside(x, y, N) and not visited[x][y]:
                visited[x][y] = True
                queue.append(cell(x, y, t.dist + 1, t))

# Crea la scacchiera
def create_chessboard(N):
    return np.tile(np.array([[1, 0] * (N//2), [0, 1] * (N//2)]), (N//2, 1))

# Disegna la scacchiera
def plot_chessboard(ax, board):
    ax.imshow(board, cmap='gray', interpolation='nearest')
    ax.set_xticks([])
    ax.set_yticks([])

# Parametri
N = 8
knightpos = (1, 1)
targetpos = (8, 8)
board = create_chessboard(N)

# Trova il percorso
path = minStepToReachTarget(knightpos, targetpos, N)

# Imposta la visualizzazione
fig, ax = plt.subplots()
plot_chessboard(ax, board)

# Anima il movimento del cavaliere
def update(frame):
    print(f"Frame: {frame}, Position: {path[frame]}")  # Debugging: stampa la posizione corrente

    ax.patches = []  # Resetta i rettangoli esistenti per ridisegnarli

    # Disegna tutti i rettangoli, includendo il punto di partenza e di arrivo con colori diversi
    for i, (x, y) in enumerate(path):
        if i == 0:  # Punto di partenza
            color = 'green'
        elif i == len(path) - 1:  # Punto di arrivo
            color = 'blue'
        else:
            color = 'none'  # Il colore di default per i passaggi intermedi

        # Aggiungi il rettangolo con il colore specificato
        rect = patches.Rectangle((y-1.5, x-1.5), 1, 1, linewidth=2, edgecolor='r' if color == 'none' else color, facecolor=color)
        ax.add_patch(rect)

    # Aggiungi il rettangolo rosso per la posizione corrente del cavaliere
    knight_x, knight_y = path[frame]
    knight_circle = patches.Circle((knight_y-1, knight_x-1), 0.5, color='red', fill=True)
    ax.add_patch(knight_circle)

ani = FuncAnimation(fig, update, frames=len(path), repeat=False, interval=500)  # 500 ms tra ogni frame
plt.show()

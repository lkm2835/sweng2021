import sys
import tty
import termios
import numpy as np
import random as pr
import matplotlib.pyplot as plt
from frozen_lake import *

def getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def heatmapShow(matrix, is_blocking=True, time=0):
    plt.figure(figsize=(4,4))
    plt.xticks(np.arange(4))
    plt.yticks(np.arange(4))
    plt.imshow(history, cmap='Reds')
    plt.colorbar()
    plt.show(block=is_blocking)
    plt.pause(time)
    plt.close()

def rargmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return pr.choice(indices)

if __name__ == "__main__":
    pad = ['W', 'S', 'D', 'A', 'Q']

    Q = np.zeros([FrozenLake.env_y_, FrozenLake.env_x_, FrozenLake.action_n_])
    history = np.zeros([FrozenLake.env_y_, FrozenLake.env_x_], dtype = np.int32)

    num_episodes = 1000
    for i in range(num_episodes):
        print("episode : ", i + 1, "\n")
        environment = FrozenLake()
        is_game_done = False

        while not is_game_done:
            #board.printScreen()
            #action = getChar()
            #state = board.accept(action)

            y_, x_ = environment.getCurrYX()
            action = rargmax(Q[y_][x_][:].reshape(environment.action_n_))
            new_y_, new_x_, reward, done = environment.accept(pad[action])

            Q[y_][x_][action] = reward + np.max(Q[new_y_][new_x_][:])

            is_game_done = done

            if environment.state == FrozenLakeState.Failed:
                environment.printScreen()
                #print("Failed")

            elif environment.state == FrozenLakeState.Arrived:
                environment.printScreen()
                #print("Arrived")

        history += environment.getHistory()
        #environment.printHistroy()
        #print(Q)
    print(history)
    heatmapShow(history)
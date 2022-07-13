import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from functions import *
import matplotlib.pyplot as plt


def animate(data, face_data, model_type, save_path=None, subplots=None):
    if model_type == "Body":
        connections = [(8,9,11), (11,22,23), (11,24,24), (8,12,14), (14,19,20), (14,21,21), (0,1,4), (1,5,7), (1,8,8), (0,15,15), (15,17,17), (0,16,16), (16,18,18)]
        frame = data[0]
        lines = []
        colors = []
    if model_type == "Hand":
        connections = [(0, 17, 20), (0, 13, 16), (0, 9, 12), (0, 5, 8), (0, 1, 4)]
        frame = data[0]
        lines = []
        colors = []
    # if model_type == "Eyes":
    #     connections = [(0,16,18), (0,15,17)]
    if model_type == "Eyes":
        #connections = [(36, 68, 38), (39,68,41),(42, 69, 44), (45,69,47)]
        connections = [(36, 39, 68), (42, 45, 69)]
        data = face_data
        frame = data[0]
        lines = []
        colors = []

    for n in range(len(connections)):
        branch = connections[n]
        lines.append([(frame[branch[0]][0], frame[branch[0]][1]), (frame[branch[1]][0], frame[branch[1]][1])])
        # creates a touple of values where we pull 2 of the joint points and their x and y values from the frame
        colors.append(1 - (frame[branch[0]][2] + frame[branch[1]][2])/2)
        # colors is average of the confidences of two points
        for j in range(branch[1], branch[2]):
            lines.append([(frame[j][0], frame[j][1]), (frame[j + 1][0], frame[j + 1][1])])
            # defines the line between every point between connection point 1 and connection point 2 in x/y domain)
            colors.append(1 - (frame[j][2] + frame[j+1][2])/2)
            #defines confidence of that line with a color


    colors = np.array(colors)

    if subplots is not None:
        fig = subplots[0]
        ax = subplots[1]
    else:
        fig, ax = plt.subplots()

    col = LineCollection(lines, array=colors)
    ax.add_collection(col)
    if model_type == "Body":
        ax.set_xlim([0, 854])
        ax.set_ylim([0, 480])
    ax.set_title('Animation of Openpose Output')
    ax.set_xlabel('x position (pixels)')
    ax.set_ylabel('y position (pixels)')
    ax.invert_yaxis()

    def update(i):
        frame = data[i]
        lines = []
        colors = []

        for n in range(len(connections)):
            branch = connections[n]
            lines.append([(frame[branch[0]][0], frame[branch[0]][1]), (frame[branch[1]][0], frame[branch[1]][1])])
            colors.append(1 - (frame[branch[0]][2] + frame[branch[1]][2]) / 2)  # colors is average of confidences of two points
            for j in range(branch[1], branch[2]):
                lines.append([(frame[j][0], frame[j][1]), (frame[j + 1][0], frame[j + 1][1])])
                colors.append(1 - (frame[j][2] + frame[j+1][2])/2)

        colors = np.array(colors)
        col.set_segments(lines)
        col.set_array(colors)
        return col,


    ani = animation.FuncAnimation(fig, update, frames=len(data)-1, interval=25)
    if save_path == None:
        plt.show(block=True)
    else:
        ani.save(save_path)

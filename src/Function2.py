import math
import os
import json
import vector
from math import sqrt


def dist_from_frame(joint, frame, dist_prev):
    # creates array of the output of dist function
    # print(frame)
    # print(*[frame[x][0:2] for x in joint])

    result_temp = 0
    p1 = frame[joint[0]][0:2]
    p2 = frame[joint[1]][0:2]
    p3 = frame[joint[2]][0:2]
    result, result_dif = calc_dist(p1, p2, p3, dist_prev)
    # print('result', result, 'result_dif', result_dif)
    return result, result_dif


def angle_from_frame(joint, frame):
    # creates array of the output of calc_angle function
    # print(frame)
    # print(*[frame[x][0:2] for x in joint])
    return calc_angle(*[frame[x][0:2] for x in joint])


# Calculates angle between segments 12 and 23, P2 is the vertex
def calc_angle(p1, p2, p3, degrees=True): # calculate lengths
    result = 0
    d12 = math.dist(p1, p2)
    d23 = math.dist(p2, p3)
    d13 = math.dist(p1, p3)
    # print('d12: %i', d12)
    # print('d23: %i', d23)
    # print('d13: %i', d13)
    # print('p1', p1)
    # print('p2', p2)
    # print('p3', p3)
    # if (abs((d12 ** 2 + d23 ** 2 - d13 ** 2) / (2 * d12 * d23)) > 1) and (d12 != 0 and d23 != 0):
    #     print((d12 ** 2 + d23 ** 2 - d13 ** 2) / (2 * d12 * d23))
    # if d12 != 0 and d23 != 0: #temporary fix --> real solution --> delete a whole frame (how to delete a json from a file --> check nto see if we can change for loop in gui, spread it out)
    #     if (abs((d12 ** 2 + d23 ** 2 - d13 ** 2) / (2 * d12 * d23)) > 1):
    #         print((d12 ** 2 + d23 ** 2 - d13 ** 2) / (2 * d12 * d23))
    #     result = math.acos((d12 ** 2 + d23 ** 2 - d13 ** 2) / (2 * d12 * d23))
    # else:
    #     result = 90
    mag_one = sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))
    mag_two = sqrt(((p3[0] - p2[0]) ** 2) + ((p3[1] - p2[1]) ** 2))
    adotb = (vector.obj(x = (abs(p2[0] - p1[0])), y = (abs(p2[1] - p1[1]))).dot(vector.obj(x = (abs(p3[0] - p2[0])), y = (abs(p3[1] - p2[1])))))
    if mag_one != 0 and mag_two != 0:
        cos = (adotb)/((mag_one) * (mag_two))
        if abs(cos) < 1:
            result = math.acos(cos)
        # if not degrees:
        #     return result
    return math.degrees(result)


def calc_dist(p1, p2, p3, result_prev, degrees=True): # calculate lengths
    # print('p1', p1, 'p2', p2, 'p3', p3)
    d12 = math.dist(p1, p2)
    d23 = math.dist(p2, p3)
    d13 = math.dist(p1, p3)
    result = [d12, d23, d13]
    result_dif = []
    for i in range(len(result_prev)):
        result_dif.append(result[i]-result_prev[i])

    return result, result_dif


# Utility function to split data
def split_to_points(lst):
    CHUNK_SIZE = 3  # A point is (x, y, confidence)
    return [tuple(lst[i:(i + CHUNK_SIZE)]) for i in range(0, len(lst), CHUNK_SIZE)]


def load_openpose(folder):
    data = []
    face_data = []
    # Load from each file in folder
    for file in sorted(os.listdir(folder)):
        with open(os.path.join(folder, file)) as infile:
            data.append(json.load(infile))
        # data being reused here, refactor later
    # print(data)
    data = [x["people"][0]["pose_keypoints_2d"] for x in data]
    data = [split_to_points(x) for x in data]

    for file in sorted(os.listdir(folder)):
        with open(os.path.join(folder, file)) as infile:
            face_data.append(json.load(infile))

    face_data = [y["people"][0]["face_keypoints_2d"] for y in face_data]
    face_data = [split_to_points(y) for y in face_data]

    return data, face_data

import math
import os
import json


def angle_from_frame(joint, frame):
	# creates array of the output of calc_angle function
	# print(frame)
	# print(*[frame[x][0:2] for x in joint])
	return calc_angle(*[frame[x][0:2] for x in joint])


# Calculates angle between segments 12 and 23, P2 is the vertex
def calc_angle(p1, p2, p3, degrees=True):

	# calculate lengths
	d12 = math.dist(p1, p2)
	d23 = math.dist(p2, p3)
	d13 = math.dist(p1, p3)

	result = math.acos((d12**2 + d23**2 - d13**2) / (2 * d12 * d23))

	if not degrees:
		return result

	return math.degrees(result)


# Utility function to split data
def split_to_points(lst):
	CHUNK_SIZE = 3 # A point is (x, y, confidence)
	return [tuple(lst[i:(i + CHUNK_SIZE)]) for i in range(0, len(lst), CHUNK_SIZE)]


def load_openpose(folder):
	data = []
	face_data = []
	# Load from each file in folder
	for file in sorted(os.listdir(folder)):
		with open(os.path.join(folder, file)) as jsonfile:
			data.append(json.load(jsonfile))
			# data being reused here, refactor later

	data = [x["people"][0]["pose_keypoints_2d"] for x in data]
	data = [split_to_points(x) for x in data]

	for file in sorted(os.listdir(folder)):
		with open(os.path.join(folder, file)) as jsonfile:
			face_data.append(json.load(jsonfile))

	face_data = [y["people"][0]["face_keypoints_2d"] for y in face_data]
	face_data = [split_to_points(y) for y in face_data]

	return data, face_data
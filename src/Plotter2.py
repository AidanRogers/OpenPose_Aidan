import matplotlib.pyplot as plt
from functions import *

# Joints
L_EYE = (42, 69, 45)  # (0,16,18)
R_EYE = (36, 68, 39)  # (0,15,17)
L_ELBOW = (5, 6, 7)
R_ELBOW = (2, 3, 4)
L_SHOULDER = (1, 5, 6)
R_SHOULDER = (1, 2, 3)
L_HIP = (8, 12, 13)
R_HIP = (8, 9, 10)
L_KNEE = (12, 13, 14)
R_KNEE = (9, 10, 11)
L_ANKLE = (10, 11, 23)
R_ANKLE = (13, 14, 20)

JOINTS = {
    L_ELBOW: "Left Elbow",
    R_ELBOW: "Right Elbow",
    L_SHOULDER: "Left Shoulder",
    R_SHOULDER: "Right Shoulder",
    L_HIP: "Left Hip",
    R_HIP: "Right Hip",
    L_KNEE: "Left Knee",
    R_KNEE: "Right Knee",
    L_ANKLE: "Left Ankle",
    R_ANKLE: "Right Ankle",
    L_EYE: "Left Eye",
    R_EYE: "Right Eye"
}


def plot_joint_over_time(joint, data, face_data, show=True, save=False, save_dir="plot.png", axis=None):
    if joint == L_EYE or joint == R_EYE:
        angles = [angle_from_frame(joint, frame) for frame in face_data]
    else:
        angles = [angle_from_frame(joint, frame) for frame in data]
    for i in range(len(angles)):
        if angles[i] == 90:
            angles[i] = angles[i - 1] #if angle is blank (90) it gets turned into previous to smooth out curve
    # if axis is not None:
    #     axis.plot(range(len(angles)), angles)
    #     axis.set_title("Graph of Angle of " + JOINTS[joint] + " Over Time")
    #     axis.set_xlabel("Frame")
    #     axis.set_ylabel("Angle of " + JOINTS[joint] + " (degrees)")
    #     axis.set_xlim([0, 300])
    #     axis.set_ylim([0, 180])
    # else:
    #     plt.figure()
    #     # plots the x and y coordinates of the pixels in blue circles
    #     plt.plot(range(len(angles)), angles, 'b')
    #     plt.title("Graph of Angle of " + JOINTS[joint] + " Over Time")
    #     plt.xlabel("Frame")
    #     plt.ylabel("Angle of " + JOINTS[joint] + " (degrees)")
    #     plt.xlim([0, 300])
    #     plt.ylim([0, 180])
    #     if save:
    #         plt.savefig(save_dir)
    #     if show:
    #         plt.show()
    #     plt.close()

    angle_in_time = []
    angle_temp = 0
    ### MOVE THINGS INTO SECONDS FROM FRAMES (IF 24FPS)
    for i in range(len(angles)):
        if i % 24 == 0:
            angle_in_time.append(angle_temp / 30)
            angle_temp = 0
            angle_temp = angle_temp + angles[i]
        else:
            angle_temp = angle_temp + angles[i]


    angles_base = []
    for i in range(len(angles)):
        angles_base.append(angles[i])

    if axis is not None:
        # plots the x and y coordinates of the pixels in blue circles
        axis.plot(range(len(angle_in_time)), angle_in_time, 'b')

        axis.set_title("Angle of " + JOINTS[joint] + " Over Time")
        axis.set_xlabel("Frame")
        axis.set_ylabel("Angle of " + JOINTS[joint] + " (cm)")
        axis.set_xlim([0, len(angle_in_time)])
        axis.set_ylim([0, max(angle_in_time)])
        # axis.plot(angle_in_time, range(len(angle_in_time)))
        #
        # axis.set_title("Angle of " + JOINTS[joint] + " Over Time")
        # axis.set_ylabel("Time(sec)")
        # axis.set_xlabel("Angle of " + JOINTS[joint] + " (cm)")
        # axis.set_ylim([0, len(angle_in_time)])
        # axis.set_xlim([0, max(angle_in_time)])
    else:
        plt.figure()
        # plots the x and y coordinates of the pixels in blue circles
        plt.plot(range(len(angle_in_time)), angle_in_time, 'b')

        plt.title("Angle of " + JOINTS[joint] + " Over Time")
        plt.xlabel("Time(sec)")
        plt.ylabel("Angle of " + JOINTS[joint] + " (cm)")
        axis.set_xlim([0, len(angle_in_time)])
        axis.set_ylim([0, max(angle_in_time)])

        if save:
            plt.savefig(save_dir)
        if show:
            plt.show()
        plt.close()

def plot_joint_dist_over_time(joint, data, face_data, show=True, save=False, save_dir="plot.png", axis=None):
    if joint == L_EYE or joint == R_EYE:
        dist = []
        dist_dif = []
        dist_temp = [0, 0, 0]
        for frame in face_data:
            dist_temp, dist_dif_temp = dist_from_frame(joint, frame, dist_temp)
            dist.append(dist_temp)
            dist_dif.append(dist_dif_temp)
    else:
        dist = []
        dist_dif = []
        dist_temp = [0, 0, 0]
        for frame in data:
            dist_temp, dist_dif_temp = dist_from_frame(joint, frame, dist_temp)
            dist.append(dist_temp)
            dist_dif.append(dist_dif_temp)

    J1_2_dist = []
    J2_3_dist = []
    J1_3_full_dist = []
    for i in range(len(dist)):
        J1_2_dist.append(dist[i][0])
        J2_3_dist.append(dist[i][1])
        J1_3_full_dist.append(dist[i][2])

    holder12 = 0
    holder23 = 0
    holder13 = 0
    J1_2_dist_intime = []
    J2_3_dist_intime = []
    J1_3_full_dist_intime = []
    ### MOVE THINGS INTO SECONDS FROM FRAMES (IF 24FPS)
    for i in range(len(J1_2_dist)):
        if i % 24 == 0:
            J1_2_dist_intime.append(holder12 / 30)
            J2_3_dist_intime.append(holder23 / 30)
            J1_3_full_dist_intime.append(holder13 / 30)
            holder12 = 0
            holder23 = 0
            holder13 = 0
            holder12 = holder12 + J1_2_dist[i]
            holder23 = holder23 + J2_3_dist[i]
            holder13 = holder13 + J1_3_full_dist[i]
        else:
            holder12 = holder12 + J1_2_dist[i]
            holder23 = holder23 + J2_3_dist[i]
            holder13 = holder13 + J1_3_full_dist[i]

    J1_2_dist = []
    J2_3_dist = []
    J1_3_full_dist = []
    for i in range(len(dist)):
        J1_2_dist.append(dist[i][0])
        J2_3_dist.append(dist[i][1])
        J1_3_full_dist.append(dist[i][2])

    if axis is not None:
        # axis.plot(range(len(J1_2_dist_intime)), J1_2_dist_intime)
        # axis.plot(range(len(J2_3_dist_intime)), J2_3_dist_intime)
        # axis.plot(range(len(J1_3_full_dist_intime)), J1_3_full_dist_intime)
        #
        # axis.set_title("Dist b/w 'joints' in " + JOINTS[joint] + " Over Time")
        # axis.set_xlabel("Frame")
        # axis.set_ylabel("Dist of " + JOINTS[joint] + " (cm)")
        # axis.set_xlim([0, len(J1_3_full_dist_intime)])
        # axis.set_ylim([0, max(J1_3_full_dist_intime)])
        # axis.legend(['1st to 2nd joint', '2nd to 3rd joint', '1st to 3rd joint'])
        axis.plot(J1_2_dist_intime,range(len(J1_2_dist_intime)))
        axis.plot(J2_3_dist_intime, range(len(J2_3_dist_intime)))
        axis.plot(J1_3_full_dist_intime, range(len(J1_3_full_dist_intime)))

        axis.set_title("Dist b/w 'joints' in " + JOINTS[joint] + " Over Time")
        axis.set_ylabel("Time(sec)")
        axis.set_xlabel("Dist of " + JOINTS[joint] + " (cm)")
        axis.set_ylim([0, len(J1_3_full_dist_intime)])
        axis.set_xlim([0, max(J1_3_full_dist_intime)])
        axis.legend(['1st to 2nd joint', '2nd to 3rd joint', '1st to 3rd joint'])
    else:
        plt.figure()
        # plots the x and y coordinates of the pixels in blue circles
        plt.plot(range(len(J1_2_dist_intime)), J1_2_dist_intime, 'b')
        plt.plot(range(len(J2_3_dist_intime)), J2_3_dist_intime, 'g')
        plt.plot(range(len(J1_3_full_dist_intime)), J1_3_full_dist_intime, 'm')

        plt.title("Graph of Dist of " + JOINTS[joint] + " Over Time")
        plt.xlabel("Time(sec)")
        plt.ylabel("Dist of " + JOINTS[joint] + " (cm)")
        axis.set_xlim([0, len(J1_3_full_dist_intime)])
        axis.set_ylim([0, max(J1_3_full_dist_intime)])
        plt.legend(['1st to 2nd joint', '2nd to 3rd joint', '1st to 3rd joint'])

        if save:
            plt.savefig(save_dir)
        if show:
            plt.show()
        plt.close()


def plot_joint_dist_change_over_time(joint, data, face_data, show=True, save=False, save_dir="plot.png", axis=None):
    if joint == L_EYE or joint == R_EYE:
        dist = []
        dist_dif = []
        dist_temp = [0, 0, 0]
        for frame in face_data:
            dist_temp, dist_dif_temp = dist_from_frame(joint, frame, dist_temp)
            dist.append(dist_temp)
            dist_dif.append(dist_dif_temp)
    else:
        dist = []
        dist_dif = []
        dist_temp = [0, 0, 0]
        for frame in data:
            dist_temp, dist_dif_temp = dist_from_frame(joint, frame, dist_temp)
            dist.append(dist_temp)
            dist_dif.append(dist_dif_temp)

    J1_2_dist_dif = []
    J2_3_dist_dif = []
    J1_3_full_dist_dif = []

    for i in range(len(dist_dif)):
        J1_2_dist_dif.append(dist_dif[i][0])
        J2_3_dist_dif.append(dist_dif[i][1])
        J1_3_full_dist_dif.append(dist_dif[i][2])
    holder12_dif = 0
    holder23_dif = 0
    holder13_dif = 0

    J1_2_dist_intime_dif = []
    J2_3_dist_intime_dif = []
    J1_3_full_dist_intime_dif = []

    ### MOVE THINGS INTO SECONDS FROM FRAMES (IF 24FPS)
    for i in range(len(J1_2_dist_dif)):
        if i % 24 == 0:
            J1_2_dist_intime_dif.append(holder12_dif / 30)
            J2_3_dist_intime_dif.append(holder23_dif / 30)
            J1_3_full_dist_intime_dif.append(holder13_dif / 30)
            holder12_dif = 0
            holder23_dif = 0
            holder13_dif = 0
            holder12_dif = holder12_dif + J1_2_dist_dif[i]
            holder23_dif = holder23_dif + J2_3_dist_dif[i]
            holder13_dif = holder13_dif + J1_3_full_dist_dif[i]
        else:
            holder12_dif = holder12_dif + J1_2_dist_dif[i]
            holder23_dif = holder23_dif + J2_3_dist_dif[i]
            holder13_dif = holder13_dif + J1_3_full_dist_dif[i]

    if axis is not None:
        axis.plot(range(len(J1_2_dist_intime_dif)), J1_2_dist_intime_dif)
        axis.plot(range(len(J2_3_dist_intime_dif)), J2_3_dist_intime_dif)
        axis.plot(range(len(J1_3_full_dist_intime_dif)), J1_3_full_dist_intime_dif)
        print(len(J1_3_full_dist_intime_dif))

        axis.set_title("Change in distance of joints in the " + JOINTS[joint] + " Over Time")
        axis.set_xlabel("Time(sec)")
        axis.set_ylabel("Dist of " + JOINTS[joint] + " (cm)")
        axis.set_xlim([0, len(J1_3_full_dist_intime_dif)])
        #axis.set_ylim([min(dist_dif), max(dist_dif)])
        axis.legend(['1st to 2nd joint', '2nd to 3rd joint', '1st to 3rd joint'])

    else:
        plt.figure()
        # plots the x and y coordinates of the pixels in blue circles
        plt.plot(range(len(J1_2_dist_intime_dif)), J1_2_dist_intime_dif, 'b')
        plt.plot(range(len(J2_3_dist_intime_dif)), J2_3_dist_intime_dif, 'g')
        plt.plot(range(len(J1_3_full_dist_intime_dif)), J1_3_full_dist_intime_dif, 'm')

        plt.title("Change in Distance of joints in the " + JOINTS[joint] + " Over Time")
        plt.xlabel("Time(sec)")
        plt.ylabel("Dist of " + JOINTS[joint] + " (cm)")
        axis.set_xlim([0, len(J1_3_full_dist_intime_dif)])
        axis.set_ylim([0, max(J1_3_full_dist_intime_dif)])
        plt.legend(['1st to 2nd joint', '2nd to 3rd joint', '1st to 3rd joint'])

        if save:
            plt.savefig(save_dir)
        if show:
            plt.show()
        plt.close()


def plot_line(p1, p2):
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'ro-')

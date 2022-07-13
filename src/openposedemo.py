import os
import subprocess
from pathlib import Path


def openposedemo(options):
    openposedir = "C:/Users/ARC/code/Openpose"  # Path(__file__).parent.parent / 'openpose'
    subprocess.run([openposedir + '/bin/OpenPoseDemo.exe', *options], cwd=openposedir, shell = True)  # + USED TO BE A /


def run_openpose(input_video, speedup=True, use_hand=False, use_face=True):
    video_name = os.path.split(input_video)[1].split('.')[0]
    folder_path = Path(__file__).parent.parent / 'output' / video_name
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    json_path = os.path.abspath(os.path.join(folder_path, 'json'))    #os.mkdir(json_path)
    openposedemo(['--video', input_video, '--write_json', json_path, '--write_video', os.path.join(folder_path ,video_name + '_saved.avi')]
                 + (['--net_resolution=-1x320', '--tracking', '1', '--number_people_max', '1'] if speedup else [])
                 + (['--net_resolution=-1x160', '--hand'] if use_hand else [])  # os.path.abspath(input_video)
                 + (['--net_resolution=-1x160', '--face'] if use_face else []))
    print(video_name)
    print('--------')
    print(json_path)
    print('--------')
    return folder_path


if __name__ == "__main__":
    input_video = input("what is your video file location:")
    # C:\Users\ARC\code\openpose-pipeline\Play_Safety_Concussion_Data\Clean\06_Keira_Siskind\6_saccades
    # C:/Users/ARC/code/openpose-pipeline/Play_Safety_Concussion_Data/Clean/06_Keira_Siskind/6_saccades
    options = input('would you like to track subjects face?: ')
    face = False
    if options.lower() == 'yes':
        face = True
    new_folder = run_openpose(input_video, True, False, face)
    print(new_folder)

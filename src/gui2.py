import tkinter as tk
from tkinter.filedialog import askdirectory
from plotter import *
from animate import animate
from openposedemo import run_openpose
import os


def create_batch_window():
    def choose_video():
        folder = askdirectory()
        chosen_videos_label.config(text=folder)
        batch_window.lift()

    def run_openpose_on_folder():
        folder = chosen_videos_label.cget("text")
        for videofile in [os.path.join(folder, file) for file in os.listdir(folder)]:
            if videofile.lower().endswith(('.mp4', '.mov', '.avi')):
                run_openpose(videofile, speedup=(use_speedup_var.get() == 1), use_hand=(use_hand_var.get() == 1))
        batch_window.lift()

    batch_window = tk.Toplevel()
    batch_window.title("Openpose Batch Video Processor")
    batch_window.minsize(800, 600)

    choose_videos_frame = tk.Frame(batch_window, borderwidth=2, relief="solid")
    choose_videos_label = tk.Label(master=choose_videos_frame, text="Select the folder containing the video files")
    choose_videos_button = tk.Button(master=choose_videos_frame, text="Choose", command=choose_video)
    chosen_videos_label = tk.Label(master=choose_videos_frame)
    choose_videos_frame.pack(pady=10)
    choose_videos_label.pack(pady=10, padx=10)
    choose_videos_button.pack(pady=10, padx=10)
    chosen_videos_label.pack(pady=10, padx=10)

    use_hand_var = tk.IntVar()
    use_speedup_var = tk.IntVar()

    run_openpose_frame = tk.Frame(batch_window, borderwidth=2, relief="solid")
    use_hand_check = tk.Checkbutton(master=run_openpose_frame, text="Use Hand Model", variable=use_hand_var, onvalue=1, offvalue = 0).pack(padx=10, pady=10)
    use_speedup_check = tk.Checkbutton(master=run_openpose_frame, text="Use Experimental Speedup", variable=use_speedup_var, onvalue=1,
                                    offvalue=0).pack(padx=10, pady=10)
    run_openpose_button = tk.Button(master=run_openpose_frame, text="Run", command=run_openpose_on_folder).pack(padx=10, pady=10)
    run_openpose_frame.pack(pady=10)


def create_plot_window():
    def choose_video():
        folder = askdirectory()
        chosen_folder_label.config(text=folder)
        plot_window.lift()

    def show():
        data, face_data = load_openpose(chosen_folder_label.cget("text"))
        fig, axes = plt.subplots(3, 3, figsize=(15, 15), constrained_layout = True)
        ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9 = axes.flatten()
        # fig.tight_layout()
        plt.subplots()
        fig.suptitle("Joint Tracking data Metrics")  # Title?
        if chosen_joint1.get() != "Select a Joint":
            # print(list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint1.get())])
            plot_joint_over_time(list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint1.get())], data, face_data, axis=ax1)
            plot_joint_dist_over_time(list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint1.get())], data, face_data,
                                 axis=ax4)
            plot_joint_dist_change_over_time(list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint2.get())], data, face_data,
                                 axis=ax7)
        if chosen_joint2.get() != "Select a Joint":
            plot_joint_over_time(list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint2.get())], data, face_data, axis=ax2)
            plot_joint_dist_over_time(list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint2.get())], data, face_data,
                                 axis=ax5)
            plot_joint_dist_change_over_time(list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint2.get())], data, face_data,
                                 axis=ax8)
        if ((chosen_joint1.get() or chosen_joint2.get()) == "Left EYE") or ((chosen_joint1.get() or chosen_joint2.get()) == "Right EYE"):
            animate(data, face_data, "EYES", subplots=(fig, ax3))
            # plot_joint_dist_over_time
            plt.show()
        else:
            animate(data, face_data, chosen_model3.get(), subplots=(fig, ax3))
            plt.show()


    def save():  # Saves each plot individually
        data, face_data = load_openpose(chosen_folder_label.cget("text"))
        if chosen_joint1.get() != "Select a Joint":
            plot_joint_over_time(
                list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint1.get())],
                data, face_data,
                show=False,
                save=True,
                save_dir=os.path.join(os.path.split(chosen_folder_label.cget("text"))[0], os.path.split(os.path.split(
                    chosen_folder_label.cget("text"))[0])[1] + "_" + chosen_joint1.get().lower().replace(" ",
                                                                                                         "_") +
                                      "_plot.png")
            )
        if chosen_joint2.get() != "Select a Joint":
            plot_joint_over_time(
                list(JOINTS.keys())[list(JOINTS.values()).index(chosen_joint2.get())],
                data, face_data,
                show=False,
                save=True,
                save_dir=os.path.join(os.path.split(chosen_folder_label.cget("text"))[0], os.path.split(os.path.split(
                    chosen_folder_label.cget("text"))[0])[1] + "_" + chosen_joint2.get().lower().replace(" ",
                                                                                                         "_") +
                                      "_plot.png")
            )
        animate(data, face_data, chosen_model3.get(),
                save_path=os.path.join(os.path.split(chosen_folder_label.cget("text"))[0],
                                       os.path.split(os.path.split(chosen_folder_label.cget("text"))[0])[
                                               1] + "_animation.gif"))

    def show_save():
        show()
        save()

    plot_window = tk.Toplevel()
    plot_window.title("Openpose Plot Creator")
    plot_window.minsize(800, 600)

    #chosen_model3 = tk.StringVar(value="Body")  # Change when hand animation is available
    chosen_model3 = tk.StringVar(value="Select a Body Area")  # Change when hand animation is available
    chosen_joint1 = tk.StringVar(value="Select a Joint")
    chosen_joint2 = tk.StringVar(value="Select a Joint")

    choose_folder_frame = tk.Frame(plot_window, borderwidth=2, relief="solid")
    choose_folder_label = tk.Label(master=choose_folder_frame, text="Select the folder containing the JSON files", pady=10, padx=10)
    choose_folder_button = tk.Button(master=choose_folder_frame, text="Choose", command=choose_video)
    chosen_folder_label = tk.Label(master=choose_folder_frame, pady=10, padx=10)
    choose_folder_frame.pack(pady=10)
    choose_folder_label.pack()
    choose_folder_button.pack()
    chosen_folder_label.pack()

    choose_joint_frame = tk.Frame(plot_window, borderwidth=2, relief="solid")
    choose_joint_frame.pack(pady=10)
    choose_joint_label = tk.Label(master=choose_joint_frame, text="Select up to 2 joints to graph").pack(padx=5, pady=5, side="top")

    choose_joint_frame1 = tk.Frame(master=choose_joint_frame)
    choose_joint_menu1 = tk.OptionMenu(choose_joint_frame1, chosen_joint1, *JOINTS.values())
    choose_joint_menu2 = tk.OptionMenu(choose_joint_frame1, chosen_joint2, *JOINTS.values())
    joint_areas = ["Body", "Eyes", "Hand"]
    choose_body_area_menu = tk.OptionMenu(choose_joint_frame1, chosen_model3, *joint_areas)

    choose_joint_frame1.pack(padx=10, pady=10)
    choose_body_area_menu.pack(padx=5, pady=9)
    choose_joint_menu1.pack(padx=5, pady=5, side='left')
    choose_joint_menu2.pack(padx=5, pady=5, side='right')

    plot_frame = tk.Frame(plot_window, borderwidth=2, relief="solid")
    plot_label = tk.Label(master=plot_frame, text="Plot options")
    show_save_button = tk.Button(master=plot_frame, text="Show and Save", command=show_save)
    save_button = tk.Button(master=plot_frame, text="Save", command=save)
    show_button = tk.Button(master=plot_frame, text="Show", command=show)
    plot_frame.pack(padx=5, pady=10)
    plot_label.pack()
    show_save_button.pack(padx=5, pady=5)
    save_button.pack(padx=5, pady=5)
    show_button.pack(padx=5, pady=5)


window = tk.Tk()
window.title("Openpose-Pipeline")
window.minsize(800, 600)

main_frame = tk.Frame(window, borderwidth=2, relief="solid")
main_label = tk.Label(master=main_frame, text="What would you like to do?", height = 3, padx=10)
batch_process_window_button = tk.Button(main_frame, text="Convert a folder of videos into JSON files", command=create_batch_window)
plot_window_button = tk.Button(main_frame, text="Create graphs from a processed video", command=create_plot_window)
main_frame.pack(pady=100)
main_label.pack(side="top")
batch_process_window_button.pack(padx=10, pady=10)
plot_window_button.pack(padx=10, pady=10)

window.mainloop()
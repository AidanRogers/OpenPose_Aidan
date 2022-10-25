A project to automate calculation of joint angles frop openpose JSON output. 

### Prerequisites:  
This project requires openpose to be installed https://github.com/CMU-Perceptual-Computing-Lab/openpose  
Ensure that tkinter, numpy and matplotlib are installed: `pip3 install tk numpy	 matplotlib`  

### Installation Instructions:  
Clone the repository using git `git clone https://github.com/kembr/openpose-pipeline.git` or altneratively download as a zip file.  

### Usage:  
1. After running openpose on a video file using the flag `--write_json [output_folder]`   
	you will have a folder containing the JSON files which our project can analyze.
2. Navigate to the root directory of the project which was cloned or unzipped and run using:  
	`python3 src/gui.py`
3. You should see the GUI pop up and be able to select the JSON folder to analyze,   
	with the option to display and save output graphs.

### Heplful flags for use with openpose:  
  `--write_json <path>`: specify path to save json output files.  
  `--write_video <path>`: specifiy path to save rendered video output.  
  `--write_video_with_audio false`: if input is a video, rendered video output will not be saved with audio  
  `--disable_blending true`: renders keypoint skeletons on black background instead of original video  

If using hand model, change net resolution and add hand flag:   
`--net_resolution="-1x160" --hand`

Command to run quickly on one person:  
`bin\OpenPoseDemo.exe --video [video_file] --write_json [output_folder] --tracking 1 --number_people_max 1`

NB: the json output in each file is printed to one line, which is unwieldy.
  If using vim you can use `:%!python -m json.tool` to pretty print the json
  in a more human readable form, or if using VSCode or similar try using an
  extension like "Prettify JSON".
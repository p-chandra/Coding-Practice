# Matlab-Video-Processor
### You need to use matlab to run this and knowledge of 3D arrays for the speacial features. 
##### Using Matlab to create a small video processor that allows users to open a video format file and then extract information from it

The program utilizes various functions in order to process the video file.
In the LOAD callback, I use the uigetfile function in order to prompt the user into selecting an
appropriate video file format such as .mp4, .avi, and .amv. The VideoReader function then extracts
information from the video file such as the file’s name, duration, and framerate. All this informatio n is
translated into strings that are displayed in the GUI’s static text box. The background turns black to
indicate the file has been loaded and the videoboxand saturation axes immediately display the first
frame.

In the PLAY/PAUSE callback, I use the string comparison function within an if-elseifstatement.
Basically, when the string “Play” is displayed in the GUI, the video is paused and when “Pause” is
displayed in the GUI, the video is playing. It is here that I also have the while loop that contains the
code for the saturation, audio, and histogram special features because they need to be updated
continuously while the video is in playing mode.
In the STOP callback, I simply set the play/pause button to ‘play’ and set the current frame
equal to 1.

In the STEP FORWARD and STEP BACKWARD callback, I use the get function to obtain the
position of video. Clicking on step forward adds 1 to the current frame while step back subtracts one.
The read, draw, and image functions display the frame on the GUI.
In the SCROLLBAR callback, I use the get function to obtain the scrollbar’s position and then
set the current frame equal to its position. I then used the read function to store the slider’s position
and the image function to display it in the GUI. The if-else statement makes it so that if the scrollbar is
moved the video automatically pauses and sets the play/pause button to play. In the load callback I
have to set the maximum and minimum of the scrollbar. The minimum is set to 0 and the maximum is
set to the video’s total number of frames. In order to make the scrollbar move with the video, I set
the scrollbar’s value to the current frame and updated it with guidata.

For the SATURATION SLIDERS special feature, I create handles for each of the red, green, and
blue sliders. I also create a variable for the scalar value of each color. This value is determined by the
position of the colored sliders located in the GUI. For example, if the red slider is increased then the
value increases, and this value is multiplied by each red pixel to modify the intensity of the color. This
occurs for the green and blue pixels as well. This process must happen for each frame. The modified
frames are then displayed on a separate saturation axis.

For the AUDIO special feature, I use the functions audioplayer and audioread to obtain the
audio information from the loaded video file. The information from TotalSamples indicates the length of
the audio sample. In order to play the audio at any given frame, I divided the TotalSample s by the
total number of frames to get the ratio of number of audio samples played per frame. In order to mute
the audio, I used in if-else statement and string comparison to toggle between mute and unmute in
the GUI. I use the ratio obtained earlier and multiply it by the current frame. The play function is used
to start the audio from the video’s position. When mute is enable, the pause function is used.

For the RGB HISTOGRAM special feature, I use an if-elseif statement and string comparison
function since I have the option of enabling and disabling the histogram on the GUI. The frames are
separated into three red, green, and blue layers. These values are then plotted onto the same figure
using the imhist and plot function. This feature has to be constantly updated frame by frame.
A problem I ran into regarding the saturation sliders was the axis was not updating along with
the video and instead had to continuously be paused and played before the color changed. This was
solved by repositioning where ‘drawnow’ was in the while loo

# 3D-and-2D-audio-spectrum-bar

__Python based 3-Dimension and 2-Dimension audio spectrum bar analyzer__


<p align="left">
  <img src="Images/dark_1.png">
</p>

#### Screenshot with dark background [line 45]

<br>
<br>

<p align="center">
  <img src="Images/with_axis_on.png">
</p>

#### Screenshot with all axises visible [line 85]

<br>
<br>

<p align="center">
  <img src="Images/light_1.png">
</p>

#### Screenshot with light background [line 43]


## Details

 * Uses pyaudio module to collect audio stream directly from the system where it runs 
 * Makes use of  matplotlib's 3D and Animation libraries
 * Capable of displaying both 2-Dimension and 3-Dimension displays simultaneously
 * 2-Dimension display shows frequency spectrum with amplitude 
 * With 3-Dimensions X-axis displays frequency , Y-axis displays amplitude and Z-axis displays amplitude of the past  samples (time history)
 * Multiprocessing is implemented , one process  works on audio samples analysis and second process works on animating displays
 
 NB: Have tested only on Ubuntu 20.04 (must work on any other Linux & Mac flavours)

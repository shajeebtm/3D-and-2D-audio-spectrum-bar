# 3D-and-2D-audio-spectrum-bar
Python based 3-Dimension and 2-Dimension audio spectrum bar analyzer 

<p align="left">
  <img src="Images/dark_1.png">
</p>

### Screenshot with dark background [line 26]

<br>
<br>

<p align="center">
  <img src="Images/with_axis_on.png">
</p>

### Screenshot with all axises visible [line 66]

<br>
<br>

<p align="center">
  <img src="Images/light_1.png">
</p>

### Screenshot with light background [line 24]


## Details

 * Uses pyaudio module to collect audio stream directly from the system where it runs 
 * Makes use of  matplotlib's 3D and Animation libraries
 * Capable of dispaying both 2-Dimension and 3-Dimension displays simulataneously
 * 2-Dimesntsion display shows frequency spectrum with amplitude 
 * With 3-Dimensions X-axis displays frequency , Y-axis displays amplitude and Z-axis displayes amplitude of the past  samples (time history)
 * Multiprocessing is implemented , one process  works on audio samples analysys and second process works on animating displays
 
 NB: Have tested only on Ubuntu 20.04 (must work on any other Linux & Mac flavours)

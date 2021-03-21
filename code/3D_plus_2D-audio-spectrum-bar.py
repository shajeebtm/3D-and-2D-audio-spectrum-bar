#!/usr/bin/env python3

'''
Copyright (c) 2021 Shajeeb TM
https://github.com/shajeebtm/3D-and-2D-audio-spectrum-bar/
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.animation import FuncAnimation
import random
import numpy as np
import pyaudio
import math
import time
from multiprocessing import Process, Value, Array

RATE =  44100
BUFFER = 256  
decayCounterLimit = 2
decayCounter=0
decayBy = 0.8 
start_time=0
end_time=0
fig_width = 11 # inches
fig_height = 4  # inches
style.use('ggplot')
#style.use('bmh')
#style.use('dark_background')

x_no_of_bars = math.floor(math.log(BUFFER, 2))
x_width_of_bars = 0.3
x_gap_between_bars = 1.0

y_no_of_bars = 8                        # on Y axis , to show the previous items (Time)
y_width_of_bars = 0.3
y_gap_between_bars = 1.0

view_azim=-69           # for 3D view
view_elev=40 #65            # for 3D view
view_projection='ortho' # two options are 'persp' & 'ortho'
view_shade=False


# the first 10 colors are from matplotlib.colors.TABLEAU_COLORS

interested_colors=['#1f77b4', '#ff7f0e' , '#2ca02c' , '#d62728' , '#9467bd' ,  '#8c564b' , '#e377c2' , '#7f7f7f' , '#bcbd22' ,'#17becf' , '#00FF00', '#FFFF00' , '#8A2BE2' , '#0000FF' , '#00BFFF' , '#A52A2A',
                    '#FF1493', '#008000', '#8B008B', '#9932CC', '#F08080', '#FFB6C1', '#FFA07A']





def child_do_display(mag_octave):

	fig = plt.figure(figsize=(fig_width,fig_height)) 
	plt.subplots_adjust(wspace=0)
	plt.subplots_adjust(top=0.99, bottom=0.01, left=0.01, right=0.99)
	ax0 = fig.add_subplot(121)
	ax0.grid(False)
	ax1 = fig.add_subplot(122, projection='3d',azim=view_azim, proj_type=view_projection, elev=view_elev)
	ax1.set_xlim(0, 10)
	ax1.set_ylim(0, 10)
	ax1.set_zlim(0, 10)

	ax1.set_xlabel("Frequency    ")
	ax1.set_ylabel("  Time  ")
	ax1.set_zlabel("Amplitude")
	ax1.set_axis_off();	

	colors=[]
	alphas=np.linspace(1,0.1,y_no_of_bars)

	tmp_colors=interested_colors[:]
	for m in range (x_no_of_bars):
		r = random.randint(0,len(tmp_colors)-1)
		colors.append(tmp_colors[r])
		tmp_colors.remove(tmp_colors[r])

	x_max_length = x_no_of_bars * x_width_of_bars + (x_no_of_bars-1) * x_gap_between_bars
	y_max_length = y_no_of_bars * y_width_of_bars + (y_no_of_bars-1) * y_gap_between_bars
	x_pos=np.linspace(0,x_max_length,x_no_of_bars)
	y_pos=np.zeros(x_no_of_bars)
	z_pos=np.zeros(x_no_of_bars)
	x_delta = []
	y_delta = []			
	for k in range(x_no_of_bars):
		x_delta.append(x_width_of_bars)

	y_delta = []			
	for k in range(x_no_of_bars):
		y_delta.append(y_width_of_bars)

	x = 0
	y = 0
	bars=[]
	peak_x_y = [[0 for i in range(x_no_of_bars)] for j in range(y_no_of_bars)]    

	bars_x_y = []  
	print (peak_x_y)


	ax0.bar(1, 10, color='w', alpha=0)
	for k in range(x_no_of_bars):  # creating x_no_of_bars 2d bars
	   r=random.randint(3, 10)
	   bar_2d,=ax0.bar(k,r, color=colors[k],  align='center')
	   bars_x_y.append(bar_2d)

	ax1.bar3d(1, 1, 0, x_max_length, y_max_length, 10, shade=False, alpha=0)
	for y in range(y_no_of_bars):	# creating x_no_of_bars * y_no_of_bars of 3d bars
	   for k in range(x_no_of_bars):
	     z=random.randint(0, 10)
	     y3=y_pos[y]+y * (y_width_of_bars + y_gap_between_bars)
	     bar=ax1.bar3d(x_pos[k], y3, z_pos[k], x_delta[k],y_delta[k],z, alpha=alphas[y], shade=False, color=colors[k])
	     bars.append(bar)
	     bars_x_y.append(bar)

	def animate(i, bars_junk):
		global start_time
		global end_time
		global decayCounter
		start_time = time.time_ns()
		xd = x_width_of_bars
		yd = y_width_of_bars
		decayCounter += 1
		for m in range(x_no_of_bars):   # lets decide on the new data to eb shown first
			new_data = mag_octave[m]
			#print ("new_data = ",new_data)
			if new_data > 10:
				new_data = 10
			else:
				if new_data == 0:
			              new_data = 0.1
			if(new_data >= peak_x_y[0][m]):
				for y in range (y_no_of_bars-1,0,-1):    # shifting by one row only when new_data > previous data
                   			peak_x_y[y][m] = peak_x_y[y-1][m]
				peak_x_y[0][m] = new_data  # loading new data to the front row
			else:
           		   if(decayCounter == decayCounterLimit):
                		for y in range (y_no_of_bars-1,0,-1):        # shifting by one row when decayCounter reached the limit
                     			peak_x_y[y][m] = peak_x_y[y-1][m]
                		if (peak_x_y[0][m] > 0):
                     			peak_x_y[0][m] -= decayBy # front row decrement by decayBy

		if (decayCounter > decayCounterLimit):
			decayCounter = 1

		for b in range(x_no_of_bars): # Update 2d bars first with the data on first row of peak_x_y
			bar_2d = bars_x_y[b]
			z = peak_x_y[0][b]
			bar_2d.set_height(z)


		for y in range(y_no_of_bars):
			#print ("operating on row " , y)
			for b in range(x_no_of_bars):
				z = peak_x_y[y][b]
				y3=y_pos[y]+y * (y_width_of_bars + y_gap_between_bars)
				points = np.array([[x_pos[b],y3,z_pos[b]],   # botton plane point 1            : x , y , z
                      		 [x_pos[b]+xd,y3,z_pos[b]],   
                      		 [x_pos[b]+xd,y3+yd, z_pos[b]],    
                      		 [x_pos[b], y3+yd, z_pos[b]],   
                       		[x_pos[b], y3, z],   
                      		 [x_pos[b]+xd, y3, z],    
                       		[x_pos[b]+xd, y3+yd, z],     
                       		[x_pos[b],y3+yd, z]])   

				points=points/1.0
				Z =  points
				vertices = [[Z[0], Z[1], Z[2], Z[3]],   # bottom face the cube
                	[Z[4], Z[5], Z[6], Z[7]],  # top face of the cube
                	[Z[0], Z[1], Z[5], Z[4]],  # front side of the cube
                	[Z[2], Z[3], Z[7], Z[6]],  # rear side of the cube
                	[Z[1], Z[2], Z[6], Z[5]],  # right side of the cube
                	[Z[4], Z[7], Z[3], Z[0]]]  # left side of the cube


				v1 = vertices

				bar=bars_x_y[((y+1)*x_no_of_bars)+b]
				bar.set_verts(v1)
				bar.do_3d_projection(bar.axes.get_figure().canvas.get_renderer())

		end_time = time.time_ns()
		return bars_junk


	ani = FuncAnimation(fig, animate, interval=5, blit=True,  fargs=[bars_x_y]) 
	plt.show()


def mainProgram_do_fft():
    p = pyaudio.PyAudio()
    stream = p.open(
	    format = pyaudio.paFloat32,
	    channels = 1,
	    rate = RATE,
	    input = True,
	    output = False,
	    frames_per_buffer = BUFFER
    )  
    start = time.time_ns()
    k=0

    
    
    while 1:
            start_time=time.time_ns()
            try:
              data = np.fft.rfft(np.fromstring( stream.read(BUFFER), dtype=np.float32))
            except IOError:
              print ("Error")
              pass

            end_time = time.time_ns()
            N=BUFFER/2
            i=0;
            k=0;
            begin=0
            while k < N:  
               k=pow(2,i)
               end=k
               sum=0
               sqauredsum=0
               for x in range(begin,end):
                  sqauredsum+=np.real(data[x])**2+np.imag(data[x])**2
               sqaureroot=math.sqrt(sqauredsum)
               log2v=0
               if (sqaureroot != 0):
                 log2v=math.log2(sqaureroot)
               if (log2v <0 ):
                  log2v=0
               mag_octave[i]=2*(log2v)
               i+=1
               begin=k

               if  (child.is_alive() != 1):
                 print ("Child job finished!")
                 exit()
            end = time.time_ns()


if __name__ == '__main__':
    mag_octave = Array('d', x_no_of_bars)
    child = Process(target=child_do_display, args=(mag_octave,))
    child.start()
    mainProgram_do_fft()
    child.join()

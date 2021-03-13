"""
Phase Based Moveout Test Script
----------------------------------
Python 2.7.x, April 16 2019 CWM 2019
----------------------------------
Based on:
	Eugene Lichmans SEG Abstract (2005)
	Automated phase based moveout correction of reflection seismic data.
	Copies phase of selected pilot trace to all other traces in a CMP
	gather.
	
	Example real CMP gather from openFire project provided.
	
IN:
	Seismic MxN CMP gather (as numpy file)
	Pilot Trace Index (see pilot_trace_num)
OUT
	Seismic MxN CMP gather (as numpy file)
	
"""
import math
import numpy as np
import matplotlib.pyplot as plt

fname='realgather'
pilot_trace_num=5	#position of pilot trace in array

"""Import Data and Plot"""
gather = np.load(fname+'.npy')	#One Gather from OpenFIRE
#gather[:,30:100]=0 #delete some traces to ensure it is not copying over

vm = np.percentile(gather, 99)
plt.imshow(gather, cmap="gist_yarg", vmin=-vm, vmax=vm, aspect='auto')
plt.title('openFIRE CMP Gather'),plt.show()
pilot_trace = gather[:,pilot_trace_num]

"""
Get FFT of Pilot Trace and compute Phase
Phase = arctan(Imag / Real)
"""

spectrum_pilot = np.fft.fft(pilot_trace)
imag = spectrum_pilot.imag
real = spectrum_pilot.real
Phase = np.arctan2(imag, real) #* 180 / math.pi

pmo = np.zeros_like(gather)

for i in range(len(gather[1])):
	spectrum_trace = np.fft.fft(gather[:,i])
	imag, real = spectrum_trace.imag,  spectrum_trace.real

	"""
	New Real = Magnitude * cos(Phase of Pilot)
	New Imaginary = Magnitude * sin(Phase of Pilot)
	"""
	Magnitude = np.sqrt(real*real+imag*imag)
	spectrum_pilot.real = Magnitude * np.cos(Phase)
	spectrum_pilot.imag = Magnitude * np.sin(Phase)
	
	shift_trace = np.fft.ifft(spectrum_pilot)
	
	pmo[:,i] = shift_trace

vm = np.percentile(pmo, 99)
pmo = np.vstack((np.zeros_like(pmo)[500:], pmo[500:]))
np.save(fname+'_PMO',pmo)
plt.imshow(pmo, cmap="gist_yarg",vmin=-vm, vmax=vm, aspect='auto' ) #split on FFT Symmetry
plt.title('openFIRE CMP Gather - Phase Moveout Corrected');plt.show()

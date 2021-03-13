# seismic-phase-based-moveout
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

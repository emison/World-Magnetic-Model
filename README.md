NAME
WMM2015_Linux

SYNOPSIS
wmm_main.py [options]

DESCRIPTION
wmm_main.py is a Python wrapper for linux executables created by the National Oceanic and Atmspheric Administration (NOAA). Underlying executables give the earths magnetic field given a point and time, which are entered interactively. In the Python wrapper arguments are passed from the command line when the function is called (i.e. non - interactively). The user may specify point or file input, and whether or not to reformat the output. Additionally by providing magnetometer measurements the user may determine the attitude (pointing direction) of the magnetometer. 

--A
	attitude calculation, determine attitude of spacecraft using magnetometer readings

--F
	file input, specify input and output files	

--P
	point input, specify location and date as arguments
	- lattitude, degrees North
	- longitude, degrees East
	- altitude, km above mean sea level
	- date, mm/dd/yyyy [optional]

--U
	unformatted, output without reformatting (raw)

COPYRIGHT INFORMATION
WMM source code is provided by the National Oceanic and Atmospheric Administration (NOAA). Licensing information at the website states the wmm source code is "in the public domain and not licensed or under copyright." Original content is preserved in the first commit. See http://www.ngdc.noaa.gov/geomag/WMM/DoDWMM.shtml for more information.

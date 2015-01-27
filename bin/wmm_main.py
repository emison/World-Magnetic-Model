#!/usr/bin/python
import sys
import subprocess
import math

#add functionality to export values from wmm_point for global use
#make date input optional
#add catch all solution for measurements solution
#change "" to '' for input parameters
#make separate function for parsing output
#separate sections with formatting
#WMM_MAIN
#===============================================================================================================
def main ():
    option_list=["P","F","A", "U"]
    parse_args()

    for option in parameter_dict:
        if option not in option_list:
            print("ERROR: invalid option")
            return

    if "P" in parameter_dict and "F" not in parameter_dict:
        wmm_point()
    elif "F" in parameter_dict and "P" not in parameter_dict:
        wmm_file()
    else:
        print("ERROR: specify either single point(-P) or file (-F) input")
        return

    if "A" in parameter_dict:
        wmm_attitude()


#WMM_POINT
#===============================================================================================================
def wmm_point ():
    #VERIFY CORRECT NUMBER OF PARAMETERS
    if len(parameter_dict["P"]) != 4:
        print("ERROR: incorrect number of arguments for specified option")
        return

    #GET ARGUMETS
    lat = parameter_dict["P"][0]
    lon = parameter_dict["P"][1]
    alt = parameter_dict["P"][2]
    date = parameter_dict["P"][3]

    #GET OUTPUT
    command_string = "./wmm_point.exe << EOF\nc\n{0}\n{1}\n{2}\n{3}\nn\nEOF\n".format(lat, lon, alt, date)
    proc = subprocess.Popen(command_string,shell=True, stdout=subprocess.PIPE)
    output_list = proc.stdout.readlines()

    #PARSE OUTPUT AND STORE IN [VALUE, ERROR, UNITS] FORM
    o = ''.join(output_list[output_list.index(' Results For \n'):]).split()
    lat = [o[o.index('Latitude')+1][:-1], '',o[o.index('Latitude')+1][-1]]
    lon = [o[o.index('Longitude')+1][:-1], '',o[o.index('Longitude')+1][-1]]
    alt = [o[o.index('Altitude:')+1], '',' '.join(o[o.index('Altitude:')+2:o.index('Date:')])]
    Date = [o[o.index('Date:')+1], '', '']
    F = [float(o[o.index('F')+2]), float(o[o.index('F')+4]), o[o.index('F')+5]]
    Fdot = [float(o[o.index('Fdot')+2]), 0,o[o.index('Fdot')+3]]
    H = [float(o[o.index('H') + 2]), float(o[o.index('H') + 4]), o[o.index('H') + 5]]
    Hdot = [float(o[o.index('Hdot')+2]), 0, o[o.index('Hdot')+3]]
    X = [float(o[o.index('X')+2]), float(o[o.index('X')+4]), o[o.index('X')+5]]
    Xdot = [float(o[o.index('Xdot')+2]), 0, o[o.index('Xdot')+3]]
    Y = [float(o[o.index('Y')+2]), float(o[o.index('Y')+4]), o[o.index('Y')+5]]
    Ydot = [float(o[o.index('Ydot')+2]), 0, o[o.index('Ydot')+3]]
    Z = [float(o[o.index('Z')+2]), float(o[o.index('Z')+4]), o[o.index('Z')+5]]
    Zdot = [float(o[o.index('Zdot')+2]), 0, o[o.index('Zdot')+3]]
    Decl = [float(o[o.index('Decl')+2]) + float(o[o.index('Decl')+4])/60, float(o[o.index('Decl')+8])/60, o[o.index('Decl')+3] + " " + o[o.index('Decl')+6][1]]
    Ddot = [float(o[o.index('Ddot')+2]), 0, o[o.index('Ddot')+3]]
    Incl = [float(o[o.index('Incl')+2]) + float(o[o.index('Incl')+4])/60, float(o[o.index('Incl')+8])/60, o[o.index('Incl')+3] + " " + o[o.index('Incl')+6][1]]
    Idot = [float(o[o.index('Idot')+2]), 0, o[o.index('Idot')+3]]

    #PRINT OUTPUT WITH FORAMT UNALTERED IF --U OR ALTERED OTHERWISE
    if "U" in parameter_dict:
        print(''.join(output_list))
    elif "P" in parameter_dict:
        print("\nResults For \n\nInput Method:\tSingle Point \nLatitude:\t{0}\t{1}".format(lat[0],lat[2]))
        print("Longitude:\t{0}\t{1} \nAltitude:\t{2}\t{3}\nDate:\t\t{4} \n".format(lon[0],lon[2],alt[0],alt[2],Date[0]))
        print("\nMain Field\t\t\t\t\tSecular Change \nF\t= {0} +/- {1}\t{2}\t\tFdot\t= {3}\t{4}".format(F[0],F[1],F[2],Fdot[0],Fdot[2]))
        print("H\t= {0} +/- {1}\t{2}\t\tHdot\t= {3}\t{4}".format(H[0],H[1],H[2],Hdot[0],Hdot[2]))
        print("X\t= {0} +/- {1}\t{2}\t\tXdot\t= {3}\t{4}".format(X[0],X[1],X[2],Xdot[0],Xdot[2]))
        print("Y\t= {0} +/- {1}\t{2}\t\tYdot\t= {3}\t{4}".format(Y[0],Y[1],Y[2],Ydot[0],Ydot[2]))
        print("Z\t= {0} +/- {1}\t{2}\t\tZdot\t= {3}\t{4}".format(Z[0],Z[1],Z[2],Zdot[0],Zdot[2]))
        print("Decl\t= {0} +/- {1}\t\t{2}\t\tDdot\t= {3}\t{4}".format(round(Decl[0],1),round(Decl[1],1),Decl[2],Ddot[0],Ddot[2]))
        print("Incl\t= {0} +/- {1}\t\t{2}\t\tIdot\t= {3}\t{4} \n\nDone.\n".format(round(Incl[0],1),round(Incl[1],1),Incl[2],Idot[0],Idot[2]))


#WMM_FILE
#===============================================================================================================
def wmm_file ():
    if len(parameter_dict["F"]) != 2: #verify data was provided
        print("ERROR: incorrect number of arguments for specified option")
        return
    in_file = parameter_dict["F"][0]
    out_file = parameter_dict["F"][1]
    print("Input: file")
    print("Input file: " + parameter_dict["F"][0])
    print("Output file: " + parameter_dict["F"][1])

    command_string = "./wmm_file.exe " + in_file + " " + out_file
    #print(command_string)
    #subprocess.Popen(command_string,shell=True)

    
def wmm_attitude (magnetometer_data,wmm_data):
    #may be able to use common coordinate system for magnetometer and data (x,y,z)
    #sf + fe = se
    print("wmm_attitude")


#PARSE_ARGS
#===============================================================================================================
def parse_args ():
    global parameter_dict
    parameter_list = sys.argv
    file = parameter_list.pop(0)

    parameter_string = ""
    for param in parameter_list:
        parameter_string += param + " " #add field delimiter

    parameter_list = parameter_string.split("--") #spilt at record delimiter
    parameter_list.pop(0)

    parameter_dict = {}
    for param_string in parameter_list:
        option = param_string.split()[0]
        param_list = param_string.split()[1:]
        parameter_dict[option] = param_list
        

#DONE
#===============================================================================================================
if __name__=="__main__":
	main()

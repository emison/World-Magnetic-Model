#!/usr/bin/python
import sys
import subprocess
import time
import math

#add catch all solution for measurements parsing
#add --V option to be verbose
#make sure date given is in mm/dd/yyyy format
#WMM_MAIN
#===============================================================================================================
def main ():
    option_list=['A','F','P','U']
    get_args()

    for option in parameter_dict:
        if option not in option_list:
            print("ERROR: invalid option")
            quit()

    parse_args()

    if 'P' in parameter_dict and 'F' not in parameter_dict:
        wmm_point()
    elif 'F' in parameter_dict and 'P' not in parameter_dict:
        wmm_file()
    else:
        print("ERROR: specify either single point(-P) or file (-F) input")
        return

    if 'A' in parameter_dict:
        wmm_attitude()

    print_output()


#GET_ARGS
#===============================================================================================================
def get_args ():
    global parameter_dict
    parameter_list = sys.argv
    file = parameter_list.pop(0)

    parameter_list = ' '.join(parameter_list).split("--")
    parameter_list.pop(0)

    parameter_dict = {}
    for param_string in parameter_list:
        option = param_string.split()[0].upper()
        param_list = param_string.split()[1:]
        parameter_dict[option] = param_list


#PARSE_ARGS
#===============================================================================================================
def parse_args ():
    if 'P' in parameter_dict:
        global lat
        global lon
        global alt
        global date
        
        #VERIFY CORRECT NUMBER OF ARGUMENTS
        if len(parameter_dict['P']) != 4:
            #USE TODAYS DATE IF NOT PROVIDED
            if len(parameter_dict['P']) == 3:
                date = time.strftime("%m/%d/%Y")
                lat = parameter_dict['P'][0]
                lon = parameter_dict['P'][1]
                alt = parameter_dict['P'][2]
            else:
                print("ERROR: incorrect number of arguments for specified option")
                quit()
        else:
            date = parameter_dict['P'][3]
            lat = parameter_dict['P'][0]
            lon = parameter_dict['P'][1]
            alt = parameter_dict['P'][2]
        
        if 'A' in parameter_dict:
            global X_S
            global Y_S
            global Z_S

            X_S = parameter_dict['A'][0]
            Y_S = parameter_dict['A'][1]
            Z_S = parameter_dict['A'][2]
        
    elif 'F' in parameter_dict:
        global in_file
        global out_file

        #VERIFY CORRECT NUMBER OF ARGUMENTS
        if len(parameter_dict['F']) != 2:
            print("ERROR: incorrect number of arguments for specified option")
            quit()
        else:
            in_file = parameter_dict['F'][0]
            out_file = parameter_dict['F'][1]

        if 'A' in parameter_dict:
            print("A in parameter dict")


#WMM_POINT
#===============================================================================================================
def wmm_point ():
    #DECLARE GLOBAL VARIABLES
    global output_list
    global lat
    global lon
    global alt
    global date
    global F
    global Fdot
    global H
    global Hdot
    global X
    global Xdot
    global Y
    global Ydot
    global Z
    global Zdot
    global Decl
    global Ddot
    global Incl
    global Idot
    
    #GET OUTPUT
    command_string = "./wmm_point.exe << EOF\nc\n{0}\n{1}\n{2}\n{3}\nn\nEOF\n".format(lat, lon, alt, date)
    proc = subprocess.Popen(command_string,shell=True, stdout=subprocess.PIPE)
    output_list = proc.stdout.readlines()

    #PARSE OUTPUT AND STORE IN [VALUE, ERROR, UNITS] FORM
    o = ''.join(output_list[output_list.index(' Results For \n'):]).split()
    lat = [o[o.index('Latitude')+1][:-1], '',o[o.index('Latitude')+1][-1]]
    lon = [o[o.index('Longitude')+1][:-1], '',o[o.index('Longitude')+1][-1]]
    alt = [o[o.index('Altitude:')+1], '',' '.join(o[o.index('Altitude:')+2:o.index('Date:')])]
    date = [o[o.index('Date:')+1], '', '']
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


#WMM_FILE
#===============================================================================================================
def wmm_file ():
    print("wmm_file")
    #command_string = "./wmm_file.exe << EOF\n{0}\n{1}\nEOF\n".format(in_file, out_file)
    #print(command_string)
    #subprocess.Popen(command_string,shell=True)


#WMM_ATTITUDE
#===============================================================================================================
def wmm_attitude ():
    #may be able to use common coordinate system for magnetometer and data (x,y,z)
    #sf + fe = se
    print("wmm_attitude")


#PRINT_OUTPUT
#===============================================================================================================
def print_output ():
    #PRINT OUTPUT WITH FORAMT UNALTERED IF --U OR ALTERED OTHERWISE
    if 'P' in parameter_dict:
        if 'U' in parameter_dict:
            print(''.join(output_list))
        elif 'A' in parameter_dict:
            print("A in parameter dict")
        else:
            print("\nResults For \n\nInput Method:\tSingle Point \nLatitude:\t{0}\t{1}".format(lat[0],lat[2]))
            print("Longitude:\t{0}\t{1} \nAltitude:\t{2}\t{3}\nDate:\t\t{4} \n".format(lon[0],lon[2],alt[0],alt[2],date[0]))
            print("\nMain Field\t\t\t\t\tSecular Change \nF\t= {0} +/- {1}\t{2}\t\tFdot\t= {3}\t{4}".format(F[0],F[1],F[2],Fdot[0],Fdot[2]))
            print("H\t= {0} +/- {1}\t{2}\t\tHdot\t= {3}\t{4}".format(H[0],H[1],H[2],Hdot[0],Hdot[2]))
            print("X\t= {0} +/- {1}\t{2}\t\tXdot\t= {3}\t{4}".format(X[0],X[1],X[2],Xdot[0],Xdot[2]))
            print("Y\t= {0} +/- {1}\t{2}\t\tYdot\t= {3}\t{4}".format(Y[0],Y[1],Y[2],Ydot[0],Ydot[2]))
            print("Z\t= {0} +/- {1}\t{2}\t\tZdot\t= {3}\t{4}".format(Z[0],Z[1],Z[2],Zdot[0],Zdot[2]))
            print("Decl\t= {0} +/- {1}\t\t{2}\t\tDdot\t= {3}\t{4}".format(round(Decl[0],1),round(Decl[1],1),Decl[2],Ddot[0],Ddot[2]))
            print("Incl\t= {0} +/- {1}\t\t{2}\t\tIdot\t= {3}\t{4} \n\nDone.\n".format(round(Incl[0],1),round(Incl[1],1),Incl[2],Idot[0],Idot[2]))
    elif 'F' in parameter_dict:
        if 'U' in parameter_dict:
            print(''.join(output_list))
        elif 'A' in parameter_dict:
            print("A in parameter dict")
        else:
            print("Input Method: File\nInput File: {0}\nOutput File: {1}".format(parameter_dict['F'][0],parameter_dict['F'][1]))


#DONE
#===============================================================================================================
if __name__=="__main__":
	main()

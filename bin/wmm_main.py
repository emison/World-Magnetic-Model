#!/usr/bin/python
import sys
import subprocess
import math

def main ():
    option_list=["P","F","A"]
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


def wmm_point ():
    if len(parameter_dict["P"]) != 4: #verify data was provided
        print("ERROR: incorrect number of arguments for specified option")
        return
    lon = parameter_dict["P"][0]
    lat = parameter_dict["P"][1]
    alt = parameter_dict["P"][2] #km from mean sea level
    date = parameter_dict["P"][3] #date in mm/dd/yyyy format
    print("Input: \tsingle point")
    print("Latitude: " + lon + " Deg N") #these lines arent necessary, since wmm_point.exe will print these entries
    print("Longitude: " + lat + " Deg E")
    print("Altitude: " + alt + " Km") #km from mean sea level
    print("Date: " + date) #date in mm/dd/yyyy format

    command_string = "./wmm_point.exe << EOF\nc\n" + lon + "\n" + lat + "\n" + alt + "\n" + date + "\n" +"n\nEOF\n" #use formatted string
    proc = subprocess.Popen(command_string,shell=True, stdout=subprocess.PIPE)
    output_list = proc.stdout.readlines() #print lines starting at 'Results For'
    print(output_list)


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


parameter_dict = {}
def parse_args ():
    global parameter_dict
    parameter_list = sys.argv
    file = parameter_list.pop(0)

    parameter_string = ""
    for param in parameter_list:
        parameter_string += param + " " #add field delimiter

    parameter_list = parameter_string.split("-") #spilt at record delimiter
    parameter_list.pop(0)

    parameter_dict = {}
    for param_string in parameter_list:
        option = param_string.split()[0]
        param_list = param_string.split()[1:]
        parameter_dict[option] = param_list
        

if __name__=="__main__":
	main()

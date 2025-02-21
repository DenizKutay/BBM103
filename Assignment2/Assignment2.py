# Deniz Kutay Açıcı 2220356022
from copy import deepcopy

def input():        #input function
    return open("doctors_aid_inputs.txt", "r")

output = open("doctors_aid_outputs.txt", "w")
def write(file, text):
    file.write(text)   #output function

patient_data_list = []
names = []


def create_patient(line):
    if name in names:                                               #if name exists
        write(output, "{} is already recorded\n".format(name))
    else:                                                           #if name doesn't exit
        write(output, "Patient {} is recorded\n".format(name))
        details = line.split(", ")
        patient_data_list.append(details)
        names.append(name) 

def remove_patients(line):      
    if line in names:       #when name exists
        a = (names.index(line))
        patient_data_list.pop(a)
        names.pop(a)
        write(output, "{} is removed.\n".format(line))
    
    else:                   #when name doesn't exist
        write(output, "Patient {} cannot be removed due to absence.\n".format(line))


def list_patients():
    
    write(output, "Patient\tDiagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment\nName\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk")
    write(output, "\n-------------------------------------------------------------------------")
    patient_data_list_copy = deepcopy(patient_data_list)    #for list function 

    for list_row in patient_data_list_copy:
        while not ("%" in list_row[1]):        
            """""
            add "%", mul with 100, arrange the decimals of diognosis accuracy and treatment risk
            """""
            list_row[1] = (float(list_row[1]) * 100)
            list_row[1] = ("%.2f" %float(list_row[1]))
            list_row[1] = str(list_row[1]) + str("%")
            
            list_row[5] = str(float(list_row[5]) * 100)
            list_row[5] = ("%.0f" %float(list_row[5]))
            list_row[5] = str(list_row[5]) + str("%")
       
        
        write(output, "\n")
        
        """""
        manage how tabs will be used 
        """""
        # name
        if len(list_row[0]) <= 3:
            write(output, list_row[0])
            write(output, "\t\t")
        else:
            write(output, list_row[0])
            write(output, "\t")
        
        # diagnosis accuracy
        if len(list_row[1]) == 6:
            write(output, list_row[1])
            write(output, "\t\t")
        else:
            write(output, list_row[1])
            write(output, "\t\t")
        #disease name
        if len(list_row[2]) <= 7:
            write(output, list_row[2])
            write(output, "\t\t\t")
        elif len(list_row[2]) <= 11:
            write(output, list_row[2])
            write(output, "\t\t")  
        else:
            write(output, list_row[2])
            write(output, "\t")

        #disease incidence
        if len(list_row[3]) == 9:
            write(output, list_row[3])
            write(output, "\t")
        else:
            write(output, list_row[3])
            write(output, "\t")

        #treatment name
        if len(list_row[4]) <=7:
            write(output, list_row[4])
            write(output, "\t\t\t")
        elif len(list_row[4]) < 16:
            write(output, list_row[4])
            write(output, "\t")
        else:
            write(output, list_row[4])

        #treatment risk
        write(output, list_row[5])
        
    write(output, "\n")
        
    pass


def probability(name):
    if line in names:
        split = patient_data_list[names.index(name)][3].split("/")                                 #it splits count and total
        accuracy, count, total = float(patient_data_list[names.index(name)][1]), int(split[0]), int(split[1])
        return "{:.4f}".format((accuracy*count) / (accuracy*count + (total-count)*(1-accuracy)))   #Bayes theorem with 4 decimal
    else:
        write(output, "{} for {} cannot be calculated due to absence.\n".format(function, name))   #when name doesn't exist
        pass
        
        


def recommendation(line):
    if probability(name) != None:       #added this "if" because probability doesn't return when name doesn't exist
        if float(probability(name)) < float(patient_data_list[names.index(name)][5]):
            write(output, "System suggests {} NOT to have the treatment\n".format(name))
        
        else:
            write(output, "System suggests {} to have the treatment\n".format(name))
    else:
        pass        


lines = input().readlines()  
for row in lines:           
    space = row.find(' ')

    function = (row[:space])                   #finds what the fuction is
    line = (row[space + 1:])                   #strip the function
    line = line.replace('\n', '')              #strip the \n at the end    
    name = line.split(",")[0]                  #finds the name
    
    '''
    below part finds which function is used in inputs
    '''

    if space == -1:                            
        if line == "list":
            list_patients()
    else:
        pass  

    if function == "create":
        create_patient(line)
    
    if function == "remove":
        remove_patients(line)

    if function == "probability":
        try:
            output.write("Patient {} has a probability of {}% having {}.\n".format(name, (float(probability(name)) * 100), patient_data_list[names.index(name)][2]))
        except:
            pass
    
    if function == "recommendation":
        recommendation(line)

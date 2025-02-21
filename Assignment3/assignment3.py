import sys
from string import ascii_uppercase #alphabet
alphabet = list(ascii_uppercase)

category = dict()
""" column number and row number are necessary for SHOWCATEGORY"""
column_number = dict()
row_number = dict()



def printer(str):
    print(str, end = "")
    output.write(str)

"""
Checks if seat(s) are exist if it is exists func returns true 
otherwise it returns false
"""
def checker(seat):
    seat_lttr = seat[0]     #seat letter
    seat_nmbr = seat[1:]    #seat number
    if "-" in seat_nmbr:    #if input is given as range it takes the last seat 
        short_line = seat_nmbr.find("-")
        seat_nmbr = seat_nmbr[short_line + 1:]
    column_check = False
    row_check = False
    if int(alphabet.index(seat_lttr)) > int(column_number[ctgry_name]): #checks if column is exists.True when column doesn't exists
        column_check = True
    if int(seat_nmbr) > int(row_number[ctgry_name]):  #checks if row is exists.True when row doesn't exists
        row_check = True
    
    if column_check and row_check:  
        printer("Error: The category '%s' has less row and column than the specified index %s!\n"%(ctgry_name,seat))
        return False
    
    if column_check and not row_check: 
        printer("Error: The category '%s' has less row than the specified index %s!\n"%(ctgry_name,seat))
        return False
    
    if not column_check and row_check:
        printer("Error: The category '%s' has less column than the specified index %s!\n"%(ctgry_name,seat))
        return False
    
    else:
        return True



def createcategory(details):
    seperator = details.split()
    ctgry_name, size = seperator[0], seperator[1]
    
    if "category-1" or "category-2" in ctgry_name:
        rxc = (size.split("x"))  #row x column
        

        if not ctgry_name in category:  #creating the category first name   
            category[ctgry_name] = {}
            column_number[ctgry_name] = int(rxc[1])
            row_number[ctgry_name] = int(rxc[0])
            for rows in range(0, int(rxc[0])):          
                for columns in range(0, int(rxc[1])):   
                    category[ctgry_name][("%s%s" %(alphabet[rows],columns))] = "X"   #seats 'X' means empty
            printer("The category '%s' having %i seats has been created.\n"%(ctgry_name, int(rxc[0]) * int(rxc[1])))
            
        else:
            printer("Warning: Cannot create the category for the second time. The stadium has already %s\n"%ctgry_name)
    else:
        printer("Error: Cannot create the category '%s'.Category name must be in category-1x or category-2x format.\n"%ctgry_name)

def selltickets(details):
    details = details.split()
    global ctgry_name
    name, type, ctgry_name = details[0], details[1], details[2]
    seats = details[3:]
    
    """
    ticket type
    """
    if type == "student":
        letter = "S"
    elif type == "full":
        letter = "F"
    elif type == "season":
        letter = "T"
    
    for seat in seats:    

        if checker(seat) == True:    
            if "-" in seat:   # if seats are given as range
                finder = seat.find("-")
                frst = seat[1:finder]
                scnd = seat[finder + 1:]
                     
                success = True  #True when seats are empty   
                for i in range(int(frst),int(scnd) + 1):
                    seat_copy = ("%s%s"%(seat[0],i))  
                    
                    """
                    checks if seats are empty
                    """
                    if category[ctgry_name][seat_copy] != "X":
                        while success:
                            printer("Warning: The seats %s cannot be sold to %s due some of them have already been sold\n"%(seat, name))
                            success = False
                            
                if success:
                    for i in range(int(frst),int(scnd) + 1):
                        seat_copy = ("%s%s"%(seat[0],i))
                        category[ctgry_name][seat_copy] = letter
                
                    printer("Success: %s has bought %s at %s\n"%(name, seat, ctgry_name))
                

            else:    
                if category[ctgry_name][seat] == "X":    #if seat is empty
                    category[ctgry_name][seat] = letter
                    printer("Success: %s has bought %s at %s\n"%(name, seat, ctgry_name))
                else:
                    printer("Warning: The seat %s cannot be sold to %s due %s have already been sold"%(seat,name,seat))

def canceltickets(details):
    details = details.split()
    global ctgry_name
    ctgry_name, seats = details[0], details[1:]
    for seat in seats:
        if checker(seat) == True:    
            if category[ctgry_name][seat] == "X":
                printer("Error: The seat %s at '%s' has already been free! Nothing to cancel\n"%(seat, ctgry_name))
        
            else:
                category[ctgry_name][seat] = "X"
                printer("Success: The seat %s at '%s' has been canceled and now ready to sell again\n"%(seat, ctgry_name))


def balance(details):
    value = list(category[details].values())
    report = ("Category report of '%s'"%details)
    printer("%s\n"%report)
    printer( int(len(report)) * "-")
    printer("\nSum of students = %i, Sum of full pay = %i, Sum of season ticket = %i, and Revenues = %i Dollars\n"%(value.count("S"),value.count("F"),value.count("T"),int(value.count("S") * 10 + value.count("F") * 20 + value.count("T") * 250)))

def showcategory(details):
    end_of_column = None
    row_count = 0 
    start_of_column = int(column_number[details])
    list_seats = list(category[details].values())
    printer("Printing category layout of %s\n\n"%details)
    
    """
    in every while it prints 1 row
    """
    while row_count != row_number[details]:
        printer("%s "%(alphabet[row_number[details] - row_count - 1])) #prints the letter of the row
        
        """
        prints seats
        """
        for seats in list_seats[-start_of_column:end_of_column]:
            printer("%s  "%seats)
        printer("\n")  #starts new row
        row_count += 1
        end_of_column = 0
        end_of_column += -start_of_column
        start_of_column += int(column_number[details])
    for column_numbers in range (0,column_number[details]):
        printer("%3s"%column_numbers)   #prints column numbers
    printer("\n")
    
input = str(sys.argv[1])
output = open("output.txt","w")
file = open(input, "r")
lines = file.readlines()
for line in lines:    
    space = line.find(" ") 
    command = line[:space]              #first word in the input
    details = line[space + 1:]
    details = details.replace("\n", "")

    '''
    Finding the which command is given
    '''
    if command == "CREATECATEGORY":
        createcategory(details)

    elif command == "SELLTICKET":
        selltickets(details)

    elif command == "CANCELTICKET":
        canceltickets(details)

    elif command == "BALANCE":
        balance(details)

    elif command == "SHOWCATEGORY":
        showcategory(details)

    else:
        printer("Please enter a valid command")
 

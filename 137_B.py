"""
projketuppgift 137 B
"""
from kraftverk_B import Vindkraftverk
from kraftverk_B import Solkraftverk

def powerplant_type():
    print("1. Solar powerplant\n2. Wind powerplant")
    a = True
    while a == True:
        try:
            print("Enter number for corresponding powerplant type:", end="")
            pwrplnt_type = int(input())
            if pwrplnt_type == 1 or pwrplnt_type == 2: 
                return pwrplnt_type
                a = False
            else: raise ValueError
        except ValueError:
            print("Enter number 1 or 2 only")

def area_input():
    a = True
    while a == True:
        try:
            print("Enter area of powerplant[m^2]:", end="")
            area = float(input())
            if area <= 0: raise ValueError
            a = False
        except ValueError:
            print("Enter positive numerical value only")
    return int(area)

def quant_input():
    a = True
    while a == True:
        try:
            print("Enter number of wind-powerplants:", end="")
            quantity = int(input())
            if quantity <= 0: raise ValueError
            a = False
        except ValueError:
            print("Enter positive integer value only")
    return int(quantity)

def rotor_size():
    a = True
    while a == True:
        try:
            print("Enter rotor diameter between 25 and 50 [m]:", end="")
            rotor_size = float(input())
            if rotor_size < 25 or rotor_size > 50: raise ValueError
            a = False
        except ValueError:
            print("Enter positive numerical value beteween 25 and 50 only")
    return rotor_size
 
def prop_konst_input():
    a = True
    while a == True:
        try:
            print("Enter proportionality constant of powerplant [W]:", end="")
            prop_konst = float(input())
            if prop_konst <= 0: raise ValueError
            a = False
        except ValueError:
            print("Enter positive numerical value only")
    return prop_konst

def latitude_input():
    a = True
    while a == True:
        try:
            print("Enter latitude of location of powerplant:", end="")
            latitude = float(input())
            if latitude < 0 or latitude > 90: raise ValueError
            a = False
        except ValueError:
            print("Enter numerical value between 0 and 90 only")
    return latitude

def add_latitude():
    t = False
    while t == False:
        print("Add latitude(y/n):", end="") #frågar om fler latituder
        try:
            add_latitud = str(input())
            if add_latitud == "y" or add_latitud == "":
                t = True
                return True
            if add_latitud == "n":
                t = True
                return False
            else: raise ValueError
        except ValueError:
            print("Enter y for additional latitude or n to continue")

def result(w_sum_list, latitude_list):
    year_sum_dict = { }
    i = 0
    for w in w_sum_list:
        year_sum_dict[latitude_list[i]] = [i, round(w/360, 1)]
        i += 1
    sort_year_sum_dict = dict(sorted(year_sum_dict.items()))
    
    #presenterar resultat
    i = 1
    for key,value in sort_year_sum_dict.items():
        print("Powerplant Nr:", i,"Production:","{[1]}".format(value),"W/day", "Latitude:", "{}".format(key),"°")
        i += 1
    return(sort_year_sum_dict)

def write_result(sort_year_sum_dict, powerplant_list, all_powerplant_all_data_list):
    a = True
    while a == True:
        print("For daily data, enter Nr of powerplant:",end="")
        try:
            n = int(input()) 
            n = list(sort_year_sum_dict.values())[n-1][0] #tar fram original index för att anropa rätt objekt
            powerplant_list[n].write_detail_data("137.txt", all_powerplant_all_data_list[n])
            a = False
        except ValueError: print("Enter integer for corresponding powerplant")
        except IndexError: print("Powerplant does not exist, try again")

def main():

    print("POWERPLANT SIMULATOR")

    type = powerplant_type()

    if type == 1:
        powerplant_list = [ ] #lista med alla objekt
        latitude_list = [ ] #Lista med alla latituder för alla objekt
        area = area_input()
        prop_konst = prop_konst_input()

        a = True
        while a == True:
            latitude = latitude_input()
            powerplant = Solkraftverk(area, prop_konst, latitude) #skapar objekt, dvs skapar ett powerplant
    
            powerplant_list.append(powerplant)
            latitude_list.append(int(latitude))
            
            a = add_latitude() #returnerar True/False

    if type == 2:
        powerplant_list = [ ] #lista med alla objekt
        latitude_list = [ ] #Lista med alla latituder för alla objekt
        quantity = quant_input()
        prop_konst = prop_konst_input()
        rotor = rotor_size()

        a = True
        while a == True:
            latitude = latitude_input()
            powerplant = Vindkraftverk(quantity, prop_konst, latitude, rotor) #skapar objekt, dvs skapar ett powerplant
            
            powerplant_list.append(powerplant)
            latitude_list.append(int(latitude))
            
            a = add_latitude()

    w_sum_list = [ ] #årsproduktion för varje objekt(kraftverk)
    all_powerplant_all_data_list = [ ] #lista med listor av alla värden per dag för alla objek.

    for powerplant in powerplant_list: #simulerar ett år för varje kraftverk och lägger till värden i listor
        year_loop = powerplant.year_loop()
        w_year_list = year_loop[0] #w_year_list behövs bara för att beräkna std. avvikelse
        w_sum = year_loop[1]
        w_sum_list.append(round(w_sum ))
        all_data_list = year_loop[2]
        all_powerplant_all_data_list.append(all_data_list)

    sort_year_sum_dict = result(w_sum_list, latitude_list)

    write_result(sort_year_sum_dict, powerplant_list, all_powerplant_all_data_list)

main()

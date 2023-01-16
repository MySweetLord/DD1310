"""
projketuppgift 137(sol/vind-kraftverk simulator) - Nivå B

@Maximilian Karbach - 22.11.20
"""
from kraftverk_B import Kraftverk

def powerplant_type(): #frågar efter vilken typ av krafverk som ska köras
    print("1. Solar powerplant\n2. Wind powerplant")
    a = True
    while a == True:
        try:
            print("Enter number for the type of powerplant to be simulated:", end="")
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
    return area

def quant_input():
    a = True
    while a == True:
        try:
            print("Enter number of wind-turbines:", end="")
            quantity = int(input())
            if quantity <= 0: raise ValueError
            a = False
        except ValueError:
            print("Enter positive integer value only")
    return quantity

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
 
def prop_konst_input(w): #propotionalitetstkonstant
    a = True
    while a == True:
        try:
            print("Enter proportionality constant of powerplant",w,":", end="")
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
        print("Add additional latitude(y/n):", end="") #frågar om fler latituder
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
        year_sum_dict[latitude_list[i]] = [i, round(w/360, 1)] #skapar en dictionary för att inte "tappa bort" index 
        i += 1
    sort_year_sum_dict = dict(sorted(year_sum_dict.items()))
    
    #presenterar resultat
    i = 1
    for key,value in sort_year_sum_dict.items():
        print("Powerplant Nr:", i,"Production:","{[1]}".format(value),"W/day", "Latitude:", "{}".format(key),"°") 
        i += 1
    return(sort_year_sum_dict)

def write_result(sort_year_sum_dict, powerplant_list, all_powerplant_all_data_list): #skriver en tabell med värden dag för dag till fil
    a = True
    while a == True:
        print("For file with daily data, enter Nr of the powerplant you wish to view:",end="")
        try:
            n = int(input()) 
            N = n
            if n == 0: raise IndexError
            n = list(sort_year_sum_dict.values())[n-1][0] #tar fram original index för att anropa rätt objekt
            powerplant_list[n].write_detail_data("137.txt", all_powerplant_all_data_list[n])
            a = False
            print("File with daily data for powerplant Nr",N,"exist now under 137.txt on your computer")
        except ValueError: print("Enter integer for corresponding powerplant")
        except IndexError: print("Powerplant does not exist, try again")

def end_receive(): #möjligör för anvädaren att avsluta eller skapa textfil
    print("1: Recieve daily production data\n2: Leave simulator")
    a = True
    while a == True:
        print("Enter your choice:", end="")
        try:
            end_receive = int(input())
            if end_receive == 1: 
                return False
                a = False
            if end_receive == 2: 
                return True
                a = False
            else: raise ValueError
        except ValueError: print("Enter nr 1 or 2 only")

def main():

    print("POWERPLANT SIMULATOR")

    type = powerplant_type()

    powerplant_list = [ ] #lista med alla objekt
    latitude_list = [ ] #Lista med alla latituder för alla objekt

    if type == 1:
        quantity = area_input()
        prop_konst = prop_konst_input("[kW/m^2]")

    if type == 2:
        quantity = quant_input()
        prop_konst = prop_konst_input("[kW]")
        rotor = rotor_size()

    a = True
    while a == True:
        latitude = latitude_input()
        if type == 1:
            powerplant = Kraftverk(type, quantity, prop_konst, latitude) #skapar objekt, dvs skapar ett kraftverk
        if type == 2:
            powerplant = Kraftverk(type, quantity, prop_konst, latitude, rotor)

        powerplant_list.append(powerplant)
        latitude_list.append(int(latitude))
            
        a = add_latitude() #returnerar True/False

    w_sum_list = [ ] #årsproduktion för varje objekt(kraftverk)
    all_powerplant_all_data_list = [ ] #lista med listor av alla värden per dag för alla objek.

    for powerplant in powerplant_list: #simulerar ett år för varje kraftverk och lägger till värden i listor
        year_loop = powerplant.year_loop()
        w_year_list = year_loop[0] #w_year_list behövs bara för att beräkna std. avvikelse
        w_sum = year_loop[1]
        w_sum_list.append(round(w_sum ))
        all_data_list = year_loop[2]
        all_powerplant_all_data_list.append(all_data_list)

    sort_year_sum_dict = result(w_sum_list, latitude_list) #Skriver resultat för varje kraftverk och returnerar dictionary för att kunna anroppa rätt objekt

    end = end_receive()
    if end == False:
        write_result(sort_year_sum_dict, powerplant_list, all_powerplant_all_data_list)

    print("POWEPLANT SIMULATOR HAS ENDED")

main()

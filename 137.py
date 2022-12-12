

"""
projketuppgift 137
"""

import random 
import math as µ

def area_input():

    a = True
    while a == True:
        try:
            print("Enter area of powerplant(m^2):", end="")
            area = float(input())
            if area <= 0: raise ValueError
            a = False
        except ValueError:
            print("Enter positiv numerical value only")
    return int(area)
    
def prop_konst_input():
    a = True
    while a == True:
        try:
            print("Enter proportionality constant of powerplant:", end="")
            prop_konst = float(input())
            if prop_konst <= 0: raise ValueError
            a = False
        except ValueError:
            print("Enter positive numerical value only")
    return prop_konst

def latitud_input():
    a = True
    while a == True:
        try:
            print("Enter latitude of location of powerplant:", end="")
            latitud = float(input())
            if latitud < 0 or latitud > 90: raise ValueError
            a = False
        except ValueError:
            print("Enter numerical value only")
    return latitud

class Kraftverk:

    def __init__(self, area, prop_konst, latitud):
        self.area = area
        self.prop_konst = prop_konst
        self.latitud = latitud

    def faktor(self):
        faktor = random.random()
        return faktor

    def v(self, t):
        v = ((23.5 * µ.sin(( µ.pi * (t - 80) / 180)) + 90 - self.latitud)/90)
        if 0 < v < 1:
            v = v**2
        elif v >= 1:
            v = 1
        elif v <= 0:
            v = 0
        v = v
        return v

    def w(self, faktor, v):
        w = self.area * self.prop_konst * faktor * v
        return w

    def data(self, t, faktor, v, w):
        data = [t, round(self.area), round(self.latitud, 3), round(self.prop_konst), round(faktor, 4), round(v, 2), round(w, 1)]
        return data

    def std_dev(self, year_sum, w_year_list):

        daily_avg = year_sum / 360
        a = 0
        for i in w_year_list:
            #beräknar summa(a) av skillnad mellan värde och medelvärde för att sedan räkna ut standardavvikelse
            a += ((i - daily_avg) ** 2)
            std_dev = µ.sqrt(a / 359)

        return std_dev

    def detail_data(self, file, all_data_list):
        file = open(file, "w")
        n = 0
        month = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December"]
    
        x = 0
        X = 1
        for i in range(12):
            file.write("="*100+"\n")
            file.write(month[n]+"\n")
            file.write("_"*100+"\n")
            gap = "   "
            file.write(f"{'Dag' :3s} {gap} {'Area(m2)' :10s} {gap} {'Latitud' :10s} {gap} {'Prop_konst(kWh)' :10s} {gap} {'Exponering' :10s} {gap} {'v' :10s} {gap} {'Produktion(W)' :10s}"+"\n")
            file.write("_"*100+"\n")
            n += 1
            for data in all_data_list[30*x:30*X]:
                file.write(f"{data[0] :<3d} {gap} {data[1] :<10d} {gap*2} {data[2] :<10.3f} {gap*3} {data[3] :<8d} {gap} {data[4] :10.4f} {gap} {data[5] :10.2f} {gap*3} {data[6] :<10.1f}"+"\n")
            x += 1
            X += 1
            
            
def main():

    powerplant_list = [ ]
    latitud_list = [ ]
    area = area_input()
    prop_konst = prop_konst_input()

    a = True
    while a == True:
        latitud = latitud_input()
        kraftverk = Kraftverk(area, prop_konst, latitud)
        #lista med objekt av krafverk för olika latituder
        powerplant_list.append(kraftverk)
        latitud_list.append(int(latitud))
        
        print("Add latitude(y/n):", end="") #frågar om fler latituder
        add_latitud = str(input())
        if add_latitud == "y":
            a = True
        if add_latitud == "n":
            a = False

    year_sum_list = [ ] 
    all_pwrplant_all_data_list = [ ]
    
    for kraftverk in powerplant_list:
        t = 1 
        w_year_list = [ ]
        year_sum = 0
        
        all_data_list = [ ]
    
        for i in range(360):
            faktor = kraftverk.faktor()
            v = kraftverk.v(t)
            w = kraftverk.w(faktor, v)
            #lista med enbart w för varje dag
            w_year_list.append(round(w, 3))
            year_sum += w

            data = kraftverk.data(t, faktor, v, w)
            all_data_list.append(data)
            t += 1

        year_sum_list.append(round(year_sum))
        all_pwrplant_all_data_list.append(all_data_list)

    #skapar sorterad dictionary med årsproduktion och lista med latitud och "index nr"
    year_sum_dict = { }
    i = 0
    for w in year_sum_list:
        year_sum_dict[latitud_list[i]] = [i, round(w/360, 1)]
        i += 1
    sort_year_sum_dict = dict(sorted(year_sum_dict.items()))

    #presenterar resultat
    i = 1
    for key,value in sort_year_sum_dict.items():
        print("Kraftverk Nr:", i,"Snitt effekt:","{[1]}".format(value),"W/dag", "Latitud:", "{}".format(key),"°")
        i += 1
        
    print("For daily data, enter Nr of powerplant:",end="")
    n = int(input())

    # tar fram original index för att anropa rätt instans av klass
    n = list(sort_year_sum_dict.values())[n-1][0]
    
    
    powerplant_list[n].detail_data("137.txt", all_pwrplant_all_data_list[n])
    
main()

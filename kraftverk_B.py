"""
P-uppgift 137 klasser för B
"""
"""En klass för varje kraftverkstyp trotts snarlika funktioner. 
Blir på så sätt lättare att ändra hur vindkraftverk tar fram energi utan att ändra solkraftverk"""

import random 
import math as µ

class Solkraftverk:

    def __init__(self, area, prop_konst, latitude):
        self.area = area
        self.prop_konst = prop_konst
        self.latitude = latitude

    def faktor(self):
        faktor = random.random()
        return faktor

    def v(self, t):
        v = ((23.5 * µ.sin(( µ.pi * (t - 80) / 180)) + 90 - self.latitude)/90)
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
        data = [t, round(self.area), round(self.latitude), round(self.prop_konst), round(faktor, 3), round(v, 2), round(w, 1)]
        return data

    def std_dev(self, year_sum, w_year_list):

        daily_avg = year_sum / 360
        a = 0
        for i in w_year_list:
            #beräknar summa(a) av skillnad mellan värde och medelvärde för att sedan räkna ut standardavvikelse
            a += ((i - daily_avg) ** 2)
            std_dev = µ.sqrt(a / 359)

        return std_dev

    def write_detail_data(self, file, all_data_list):
        file = open(file, "w")
        n = 0
        month = ["January", "February", "Mars", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
        x = 1
        for i in range(12):
            file.write("="*100+"\n")
            file.write(month[n]+"\n")
            file.write("_"*100+"\n")
            gap = "   "
            file.write(f"{'Day' :3s} {gap} {'Area[m2]' :10s} {gap} {'Latitude' :10s} {gap} {'Prop_konst[kWh]' :10s} {gap} {'Sun exposure' :10s} {gap} {'v' :10s} {gap} {'Production[W]' :10s}"+"\n")
            file.write("_"*100+"\n")
            n += 1
            for data in all_data_list[30*(x-1):30*x]:
                file.write(f"{data[0] :<3d} {gap} {data[1] :<10d} {gap*2} {data[2] :<10.3f} {gap*3} {data[3] :<8d} {gap} {data[4] :10.4f} {gap} {data[5] :10.2f} {gap*3} {data[6] :<10.1f}"+"\n")
            x += 1

    def year_loop(self):
    
        t = 1 
        w_year_list = [ ] #lista med w för varje dag för ett objekt(kraftverk)    
        all_data_list = [ ]
        
        for i in range(360):
            faktor = self.faktor()
            v = self.v(t)
            w = self.w(faktor, v)

            w_year_list.append(round(w, 3))
            data = self.data(t, faktor, v, w)            
            all_data_list.append(data)
            t += 1
        
        year_sum = sum(w_year_list)
        return [w_year_list, year_sum, all_data_list]    

class Vindkraftverk:

    def __init__(self, quantity, prop_konst, latitude, rotor):
        self.quantity = quantity
        self.prop_konst = prop_konst
        self.latitude = latitude
        self.rotor = rotor

    def faktor(self):
        faktor = random.random()
        return faktor

    def v(self, t): #Hur vind varierar under året, blåser mest under höst och vår
        v = ((23.5 * µ.sin(( µ.pi * (t - 40) / 90)) + 90 - self.latitude)/90)
        if 0 < v < 1:
            v = v**2
        elif v >= 1:
            v = 1
        elif v <= 0:
            v = 0
        v = v
        return v
   
    def w(self, faktor, v):
        w = self.quantity * 1000 * self.prop_konst * faktor * v * self.rotor
        return w

    def data(self, t, faktor, v, w):
        data = [t, round(self.quantity), round(self.latitude, 1), round(self.rotor), round(self.prop_konst), round(faktor, 3), round(v, 2), round(w, 1)]
        return data

    def std_dev(self, year_sum, w_year_list):

        daily_avg = year_sum / 360
        a = 0
        for i in w_year_list:
            #beräknar summa(a) av skillnad mellan värde och medelvärde för att sedan räkna ut standardavvikelse
            a += ((i - daily_avg) ** 2)
            std_dev = µ.sqrt(a / 359)

        return std_dev

    def write_detail_data(self, file, all_data_list):
        file = open(file, "w")
        n = 0
        month = ["January", "February", "Mars", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
        x = 1
        for i in range(12):
            file.write("="*100+"\n")
            file.write(month[n]+"\n")
            file.write("_"*100+"\n")
            gap = "  "
            file.write(f"{'Day' :3s} {gap} {'Quantity' :10s} {gap} {'Latitude' :10s} {gap} {'Rotor size [m]' :10s} {gap} {'Prop_konst[kWh]' :10s} {gap} {'Wind' :10s} {gap} {'v' :10s} {gap} {'Production[W]' :10s}"+"\n")
            file.write("_"*100+"\n")
            n += 1
            for data in all_data_list[30*(x-1):30*x]:
                file.write(f"{data[0] :<3d} {gap} {data[1] :<10d} {gap*2} {data[2] :<10f} {gap*3} {data[3] :<10d} {gap} {data[4] :10f} {gap} {data[5] :10f} {gap} {data[6] :<10f} {gap} {data[7]}"+"\n")
            x += 1

    def year_loop(self): #kör ovan metoder för att simulera ett år 
    
        t = 1 
        w_year_list = [ ] #lista med w för varje dag för ett objekt(kraftverk)    
        all_data_list = [ ]
        
        for i in range(360):
            faktor = self.faktor()
            v = self.v(t)
            w = self.w(faktor, v)

            w_year_list.append(round(w, 3))
            data = self.data(t, faktor, v, w)            
            all_data_list.append(data)
            t += 1
        
        year_sum = sum(w_year_list)
        return [w_year_list, year_sum, all_data_list]

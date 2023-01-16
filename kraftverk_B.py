"""
projketuppgift 137(klass för sol/vind-kraftverk simulator) - Nivå B

@Maximilian Karbach - 22.11.20
"""

import random 
import math as µ

class Kraftverk:

    def __init__(self, type, quantity, prop_konst, latitude, rotor = 1):
        self.type = type
        self.quantity = quantity
        self.prop_konst = prop_konst
        self.latitude = latitude
        self.rotor = rotor

    def faktor(self):
        faktor = random.random()
        return faktor

    def energyfunction(self, t): #Energifunktion
        if self.type == 2:
            v = ((23.5 * µ.sin(( µ.pi * (t - 40) / 90)) + 90 - self.latitude)/90) #simulerar vind under ett år, maximum vinter och höst
        if self.type == 1:
            v = ((23.5 * µ.sin(( µ.pi * (t - 80) / 180)) + 90 - self.latitude)/90) #simulerar solstyrka(?) under ett år, maximum sommar

        if 0 < v < 1:
            v = v**2
        elif v >= 1:
            v = 1
        elif v <= 0:
            v = 0
        v = v
        return v
   
    def production(self, faktor, v):
        w = self.quantity * self.prop_konst * faktor * v * self.rotor
        return w

    def data(self, t, faktor, v, w):  
        if self.type == 2:
            data = [t, self.quantity, round(self.latitude,1), round(self.rotor,1), round(self.prop_konst,1), round(faktor, 3), round(v, 3), round(w, 1)]
        if self.type == 1:
            data = [t, round(self.quantity), round(self.latitude,1), round(self.prop_konst,1), round(faktor, 3), round(v, 3), round(w, 1)]
        
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
        if self.type == 2:
            for i in range(12):
                file.write("="*100+"\n")
                file.write(month[n]+"\n")
                file.write("_"*100+"\n")
                gap = ""
                file.write(f"{'Day' :3s} {gap} {'Turbine Quantity' :16s} {gap} {'Latitude' :8s} {gap} {'Rotor size [m]' :15s} {gap} {'Prop_konst[kWh]' :15s} {gap} {'Wind' :8s} {gap} {'v' :8s} {gap} {'Production[W]' :15s}"+"\n")
                file.write("_"*100+"\n")
                n += 1
                for data in all_data_list[30*(x-1):30*x]:
                    file.write(f"{data[0] :3d} {gap} {data[1] :<16d} {gap*2} {data[2] :<8.1f} {gap*3} {data[3] :<15.1f} {gap} {data[4] :<15.1f} {gap} {data[5] :<8.3f} {gap} {data[6] :<8.3f} {gap} {data[7] :<15.1f}"+"\n")
                x += 1

        if self.type == 1:
            for i in range(12):
                file.write("="*90+"\n")
                file.write(month[n]+"\n")
                file.write("_"*90+"\n")
                gap = ""
                file.write(f"{'Day' :4s} {gap} {'Area[m2]' :10s} {gap} {'Latitude' :8s} {gap} {'Prop_konst[kWh]' :18s} {gap} {'Sun' :10s} {gap} {'v' :10s} {gap} {'Production[W]' :10s}"+"\n")
                file.write("_"*90+"\n")
                n += 1
                for data in all_data_list[30*(x-1):30*x]: #formatering för raka kolumner, f/d/s anger typ av värde, siffra efter punkt anger decimaler
                    file.write(f"{data[0] :<4d} {gap} {data[1] :<10.1f} {gap*2} {data[2] :<8.1f} {gap*3} {data[3] :<18.1f} {gap} {data[4] :<10.3f} {gap} {data[5] :<10.3f} {gap*3} {data[6] :<10.1f}"+"\n")
                x += 1

    def year_loop(self):
        
        t = 1 
        w_year_list = [ ] #lista med w för varje dag för ett objekt(kraftverk)    
        all_data_list = [ ]
        
        for i in range(360):
            faktor = self.faktor()
            v = self.energyfunction(t)
            w = self.production(faktor, v)

            w_year_list.append(round(w, 3))
            data = self.data(t, faktor, v, w)            
            all_data_list.append(data)
            t += 1
        
        year_sum = sum(w_year_list)
        return [w_year_list, year_sum, all_data_list]
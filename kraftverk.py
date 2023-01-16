"""
projketuppgift 137(klass för solkraftverk simulator) - Nivå C

@Maximilian Karbach - 22.11.20

"""
import random 
import math as µ

class Kraftverk:

    def __init__(self, area, prop_konst, latitude):
        self.area = area
        self.prop_konst = prop_konst
        self.latitude = latitude

    def faktor(self):
        faktor = random.random()
        return faktor

    def energyfunction(self, t): #energyfunction, v ändras för att simulera ett år med hänsyn till sol, maximum sommar och minimum vinter
        v = ((23.5 * µ.sin(( µ.pi * (t - 80) / 180)) + 90 - self.latitude)/90)
        if 0 < v < 1:
            v = v**2
        elif v >= 1:
            v = 1
        elif v <= 0:
            v = 0
        v = v
        return v

    def production(self, faktor, v): #beräknar produktion för varje dag
        w = self.area * self.prop_konst * faktor * v
        return w

    def data(self, t, faktor, v, w): #skapar lista med värden för enskild dag
        data = [t, round(self.area, 1), round(self.latitude, 1), round(self.prop_konst, 1), round(faktor, 3), round(v, 3), round(w, 1)]
        return data

    def std_dev(self, year_sum, w_year_list):

        daily_avg = year_sum / 360
        a = 0
        for i in w_year_list:
            #beräknar (a)skillnad mellan värde och medelvärde för att räkna ut standardavikelse
            a += ((i - daily_avg) ** 2)
            std_dev = µ.sqrt(a / 359)

        return std_dev

    def write_detail_data(self, file, all_data_list): #skriver alla värden i en tabell, dag för dag, uppdelat i månader
        file = open(file, "w")
        n = 0
        month = ["January", "February", "Mars", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
        x = 1
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

    def year_loop(self): #funktion som simulerar ett år med ovan metoder, returnerar värden i listor
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
        

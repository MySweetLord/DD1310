"""
projketuppgift 137
"""

import random 
import math as µ

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

    def detail_data(self, all_data_list):
        n = 0
        month = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December"]
    
        x = 0
        X = 1
        for i in range(12):
            print("="*62)
            print(month[n])
            print("_"*100)
            gap = "   "
            print(f"{'Dag' :3s} {gap} {'Area(m2)' :10s} {gap} {'Latitud' :10s} {gap} {'Prop_konst(kWh)' :10s} {gap} {'Exponering' :10s} {gap} {'v' :10s} {gap} {'Produktion(W)' :10s}")
            print("_"*100)
            n += 1
            for data in all_data_list[30*x:30*X]:
                print(f"{data[0] :<3d} {gap} {data[1] :<10d} {gap*2} {data[2] :<10.3f} {gap*3} {data[3] :<8d} {gap} {data[4] :10.4f} {gap} {data[5] :10.2f} {gap*3} {data[6] :<10.1f}")
            x += 1
            X += 1

    def t_360(self):
        #definierar variabler för for loop
        t = 1 
        w_year_list = [ ]
        year_sum = 0
        all_data_list = [ ]
    
        for i in range(360):
            faktor = self.faktor()
            v = self.v(t)
            w = self.w(faktor, v)
            #lista med enbart w för varje dag
            w_year_list.append(round(w, 3))
            year_sum += w

            data = self.data(t, faktor, v, w)
            all_data_list.append(data)
            t += 1
                
        std_dev = round(self.std_dev(year_sum, w_year_list), 3)

        self.detail_data(all_data_list)
            
def main():
    solkraftverk = Kraftverk(500, 5, 30)
    solkraftverk_2 = Kraftverk(320, 7, 52)
    
    solkraftverk_2.t_360()
    
main()


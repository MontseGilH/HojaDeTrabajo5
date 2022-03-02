from queue import Queue
from simpy import Resource, Container, Environment
from random import Random
import numpy as np




class SimulacionRAM():
    def __init__(self, env, procesadores=1, memoria=100, velocidad=3):
        self.procesadores = Resource(env, capacity=procesadores)
        self.RAM = Container(env, init=memoria, capacity=memoria)
        self.velocidad = velocidad
        self.env = env
        self.waiting = Resource(env, capacity=1)

          
class Procesos():
    def __init__(self, total, procesadores, memoria, velocidad, interv):
        self.tiempos = []
        self.titulo = f'Procesos: {total}, procesadores: {procesadores}, memoria: {memoria}, velocidad: {velocidad}, intervalos: {interv}' 
        self.total = total
        
    def add(self, item):
        self.tiempos.append(item)
    
    def mostrarStatTitulo(self):
        print('\n' + self.titulo)
        print("Media\tDesviación estándar")
        print(f"{np.mean(self.tiempos)}\t{np.std(self.tiempos)}")
        
    def mostrarStat(self):
        print(f"{self.total}\t{np.mean(self.tiempos):2f}\t{np.std(self.tiempos):2f}")
        
        
               
def proceso(env, simRAM, num, procesos, rand):
    print(f'Proceso no. {num} en NEW')
    memoria = rand.randint(1, 10)
    instrucciones = rand.randint(1,10)
    inicio = env.now
    with simRAM.RAM.get(memoria) as reqREADY:
        yield reqREADY
        print(f'Proceso no. {num} se encuentra en READY')
        while instrucciones > 0:
            with simRAM.procesadores.request() as reqRUNNING:
                yield reqRUNNING
                yield env.timeout(1)
                print(f'Proceso no. {num} en RUNNING')
                instrucciones = instrucciones - simRAM.velocidad
                
                if rand.randint(1,2) == 2:
                    with simRAM.waiting.request() as reqWAITING:
                        yield reqWAITING
                        print(f'Procesador no. {num} en WAITING')
                        yield env.timeout(1)
                
                print(f"Proceso no. {num} se encuentra en READY")
        simRAM.RAM.put(memoria)      
        print(f"Proceso no. {num} en TERMINATED")  
        procesos.add(env.now - inicio)
            
              
def simular(memoria=100, tot_procesos=25, procesadores=1, velocidad=3, tiempo_intervalo=10):            
    env = Environment()
    procesos = Procesos(tot_procesos, procesadores, memoria, velocidad, tiempo_intervalo)
    simRAM = SimulacionRAM(env, procesadores, memoria, velocidad)
    rand = Random(123)
    cnt = 0
    total = tot_procesos
    for intervalo in range(1, 25000):
        p = int(rand.expovariate(1.0/intervalo))
        for _ in range(p):
            env.process(proceso(env, simRAM, cnt, procesos, rand))
            cnt = cnt + 1
            print(cnt)
            if cnt == total:
                break
        if cnt == total:
            break
        
        env.run(intervalo * tiempo_intervalo)
        
    env.run(env.now + 10000000000)
        
    return procesos
        
        
    

incisoA = []

for total in [25, 50, 100, 150, 200]:
    incisoA.append(simular(tot_procesos=total))

incisoB_5 = []
for total in [25, 50, 100, 150, 200]:
    incisoB_5.append(simular(tot_procesos=total, tiempo_intervalo=5))
    
incisoB_1 = []
for total in [25, 50, 100, 150, 200]:
    incisoB_1.append(simular(tot_procesos=total, tiempo_intervalo=1))
        
incisoC_i = []
for interv in [10, 5, 1]:
    temp = []
    for total in [25, 50, 100, 150, 200]:
        temp.append(simular(tot_procesos=total, memoria=200, tiempo_intervalo=interv))
    incisoC_i.append(temp)
    
incisoC_ii = []
for interv in [10, 5, 1]:
    temp = []
    for total in [25, 50, 100, 150, 200]:
        temp.append(simular(tot_procesos=total, velocidad=6, tiempo_intervalo=interv))
    incisoC_ii.append(temp)
    
incisoC_iii = []
for interv in [10, 5, 1]:
    temp = []
    for total in [25, 50, 100, 150, 200]:
        temp.append(simular(tot_procesos=total, procesadores=2, tiempo_intervalo=interv))
    incisoC_iii.append(temp)
  
print("\nInciso a)")
print('Procesos\tMedia\tDesviación estándar')
for p in incisoA:
    p.mostrarStat()
    
print('\nInciso b) intervalo 5')
print('Procesos\tMedia\tDesviación estándar')
for p in incisoB_5:
    p.mostrarStat()
    
print('\nInciso b) intervalo 1')
print('Procesos\tMedia\tDesviación estándar')
for p in incisoB_1:
    p.mostrarStat()
    
print('\nInciso c) i)')
for (array, interv) in zip(incisoC_i, [10, 5, 1]):
    print(f'\nIntervalo {interv}')
    print('Procesos\tMedia\tDesviación estándar')
    for p in array:
        p.mostrarStat()
        
print('\nInciso c) ii)')
for (array, interv) in zip(incisoC_ii, [10, 5, 1]):
    print(f'\nIntervalo {interv}')
    print('Procesos\tMedia\tDesviación estándar')
    for p in array:
        p.mostrarStat()
        
print('\nInciso c) iii)')
for (array, interv) in zip(incisoC_iii, [10, 5, 1]):
    print(f'\nIntervalo {interv}')
    print('Procesos\tMedia\tDesviación estándar')
    for p in array:
        p.mostrarStat()


       
            
            


        
        
        
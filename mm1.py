import getopt
import sys
import numpy

#   Funciones

#   Introduccion de parametros por medio de getopt
def argumentosGetOpt():
    optlist, args = getopt.getopt(sys.argv[1:], 'a:d:t:')
    return optlist

#   Se obtienen las variables desde getopt 
def obtenerVariables(optlist) :
    tasaDeArribos = float(optlist[0][1])
    tasaDeServicio = float(optlist[1][1])
    tiempoEnd = float(optlist[2][1])
    
    #   Se muestran las variables
    #print(tasaDeArribos, " " , tasaDeServicio, " " , tiempoEnd)

    return [tasaDeArribos, tasaDeServicio, tiempoEnd]

#   Generador de tiempos Inter-arribos
def generadorNumerosAleatorios(a):
    y = numpy.random.uniform()
    x = -(1 / a) * numpy.log(1 - y)
    return x
def incrementarConteoTiempoCola(cantidadEnCola, tiempo, lista):
    if(cantidadEnCola + 1 > len(lista)):
        tiempoCantidadCola.append(tiempo)
    else:
        tiempoCantidadCola[cantidadEnCola] += tiempo
    return lista
#   Medidas de Rendimiento

#   Inicia el Simulador
#def iniciarSimulador():


#   Main
time = 0.0
queuetime = 0.0
cola = []
actualqueue = 0
tiemposDeServicio = []
tiempoCantidadCola = [0]

args = argumentosGetOpt()
args = obtenerVariables(args)

jobsQueSalieron = 0
jobsQueLlegaron = 1

tiempotrabajo = args[1]
jobsEnCola = 0
jobsEnColaMax = 0
tiempoMaxColaMax = 0.0
#Simular tiempos interarribos
while queuetime <= args[2]:
    jobarrival = float(generadorNumerosAleatorios(args[0]))
    if((queuetime + jobarrival)> args[2]):
        break
    jobsQueLlegaron += 1
    queuetime += jobarrival
    cola.append(queuetime)
#Simular tiempos de servicio
while time <= args[2]:
    tiempoServicio = float(generadorNumerosAleatorios(args[1]))
    time += tiempoServicio
    tiemposDeServicio.append(tiempoServicio)
#Simulación
time = 0.0
if(tiemposDeServicio == []):
    tiempoServicioActual = 2020202002.0
else:
    tiempoServicioActual = tiemposDeServicio.pop(0)
if(cola == []):
    arriboJob = 0.0
else:
    arriboJob = cola.pop(0)
while time <= args[2]:
    while (arriboJob > time):
        if((time + tiempoServicioActual) > arriboJob and (time + tiempoServicioActual) <= args[2]):
            tiempoServicioActual -= arriboJob - time
            break

        if(actualqueue > 0):
            tiempoCantidadCola = incrementarConteoTiempoCola(actualqueue, tiempoServicioActual, tiempoCantidadCola)
            time += tiempoServicioActual
            actualqueue -= 1
            jobsQueSalieron += 1
            if(len(tiemposDeServicio) == 0):
                break
            tiempoServicioActual = tiemposDeServicio.pop(0)
        else:
            tiempoCantidadCola[0] += arriboJob - time
            time = arriboJob

    if(cola != []):
        tiempoCantidadCola = incrementarConteoTiempoCola(actualqueue, arriboJob - time, tiempoCantidadCola)
        time = arriboJob
        actualqueue += 1
        arriboJob = cola.pop(0)
    else:
        tiempoCantidadCola[0] += args[2] - time
        break

print(tiempoCantidadCola)


#   Medidas de Rendimiento
print("Numero de jobs que llegaron: ", jobsQueLlegaron)
print("Numero de jobs que salieron: ", jobsQueSalieron)
print("Tiempo total de cola vacıa: ", tiempoCantidadCola[0])
print("Largo maximo de la cola: ", len(tiempoCantidadCola)-1)
print("Tiempo total de la cola con largo maximo: ", tiempoCantidadCola[len(tiempoCantidadCola)-1])
print("Utilizacion computada: ", -1)
print("Utilizacion teorica: ", -1)
print("Largo promedio computado de la cola: ", -1)
print("Largo promedio teorico de la cola: ", -1)
print("Tiempo promedio computado de residencia: ", -1)
print("Tiempo promedio teorico de residencia: ", -1)

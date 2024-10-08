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
    
    return [tasaDeArribos, tasaDeServicio, tiempoEnd]

#   Generador de tiempos Inter-arribos
def generadorNumerosAleatorios(a):
    y = numpy.random.uniform()
    x = -(1 / a) * numpy.log(1 - y)
    return x

def incrementarConteoTiempoCola(cantidadEnCola, tiempo, lista):
    if(cantidadEnCola + 1 > len(lista)):
        lista.append(tiempo)
    else:
        lista[cantidadEnCola] += tiempo
    return lista

def ingresarTiempoDeEspera(idJob, tiempo, lista):
    if(idJob + 1 > len(lista)):
        lista.append(tiempo)
    else:
        lista[idJob] += tiempo
    return lista

def ingresarTiempoDeResidencia(idJob, tiempo, lista):
    if(idJob + 1 > len(lista)):
        lista.append(tiempo)
    else:
        lista[idJob] += tiempo
    return lista


#   Medidas de Rendimiento

def utilizacion(tasaArribo, tasaServicio, listaTiempos):
    Utilizacion_teorica = args[0]/args[1]
    suma = 0
    for time_counted in tiempoCantidadCola:
        suma += time_counted
    Utilizacion_computada = 1-(tiempoCantidadCola[0]/suma)
    return [Utilizacion_teorica, Utilizacion_computada]

def largoPromedioCola(tiempoTotal, listaTiempos, listaTiemposEspera, tiempoUltimoJob):
    count = 0
    suma = 0
    sum1 = 0
    for time_counted in listaTiempos:
        suma += count*time_counted
        count += 1
    largoPromedioComputado = suma/tiempoTotal
    for timeofWaiting in listaTiemposEspera:
        sum1 += timeofWaiting
    largoPromedioTeorico = sum1/tiempoUltimoJob
    return [largoPromedioComputado, largoPromedioTeorico]

def tiempoPromedioResidencia(listaTiemposResidencia, cantidadDeJobs, cantidadDeJobsSalidos):
    suma = 0
    for timeCounted in listaTiemposResidencia:
        suma += timeCounted
    tiempoPromComputado = suma/cantidadDeJobsSalidos
    tiempoPromTeorico = suma/cantidadDeJobs
    return [tiempoPromComputado, tiempoPromTeorico]


#   Main
time = 0.0
queuetime = 0.0
listaTiemposArribos = []
largoDeColaActual = 0
tiemposDeServicio = []
tiempoCantidadCola = [0]
tiempoDeEspera = [0]
tiempoDeResidencia = [0]

args = argumentosGetOpt()
args = obtenerVariables(args)

jobsQueSalieron = 0
jobsQueLlegaron = 1

jobIdInSistem = 0
jobId = 1
jobsEnColaList = []
tiempoUltimoJobsSalido = 0.0

#   Simular tiempos interarribos
while queuetime <= args[2]:
    jobarrival = float(generadorNumerosAleatorios(args[0]))
    if((queuetime + jobarrival)> args[2]):
        break
    jobsQueLlegaron += 1
    queuetime += jobarrival
    listaTiemposArribos.append(queuetime)

#   Simular tiempos de servicio
while time <= args[2]:
    tiempoServicio = float(generadorNumerosAleatorios(args[1]))
    time += tiempoServicio
    tiemposDeServicio.append(tiempoServicio)

#   Simulación
time = 0.0
if(tiemposDeServicio == []):
    tiempoServicioActual = 2020202002.0
else:
    tiempoServicioActual = tiemposDeServicio.pop(0)
if(listaTiemposArribos == []):
    arriboJob = 0.0
else:
    arriboJob = listaTiemposArribos.pop(0)

#   La simulación continúa hasta el tiempo límite.
while time <= args[2]:

    #   Sección encargada del evento de salida del sistema.
    while (arriboJob > time):
        if((time + tiempoServicioActual) > arriboJob and (time + tiempoServicioActual) <= args[2]):
            tiempoServicioActual -= arriboJob - time
            break
        
        #   Si la cola no está vacía, se permite la simulación del siguiente job al sistema.
        if(largoDeColaActual > 0):
            tiempoCantidadCola = incrementarConteoTiempoCola(largoDeColaActual, tiempoServicioActual, tiempoCantidadCola)

            #   Ciclo encargado de aumentar los contadores de los tiempos de espera de cada job en la cola.
            for job in jobsEnColaList:
                tiempoDeEspera = ingresarTiempoDeEspera(job, tiempoServicioActual, tiempoDeEspera)
            jobsEnColaList.pop(0)
            time += tiempoServicioActual
            tiempoDeResidencia = ingresarTiempoDeResidencia(jobIdInSistem, tiempoDeEspera[jobIdInSistem] + tiempoServicioActual, tiempoDeResidencia)
            tiempoUltimoJobsSalido = time
            largoDeColaActual -= 1
            jobsQueSalieron += 1

            #   Si no hay tiempos de servicio dentro del rango permitido de tiempo de simulación, se termina la sección de evento de salida.
            if(len(tiemposDeServicio) == 0):
                break
            tiempoServicioActual = tiemposDeServicio.pop(0)
        else:
            tiempoCantidadCola[0] += arriboJob - time
            time = arriboJob
    
    #   Si hay tiempos de arribos simulados dentro del tiempo límite, se ingresa el job a la cola.
    if(listaTiemposArribos != []):
        tiempoCantidadCola = incrementarConteoTiempoCola(largoDeColaActual, arriboJob - time, tiempoCantidadCola)
        time = arriboJob
        largoDeColaActual += 1
        arriboJob = listaTiemposArribos.pop(0)
        jobsEnColaList.append(jobId)
        jobId += 1
    else:
        tiempoCantidadCola[0] += args[2] - time
        break


Utilizaciones = utilizacion(args[0], args[1], tiempoCantidadCola)
LargosPromedio = largoPromedioCola(args[2], tiempoCantidadCola, tiempoDeEspera, tiempoUltimoJobsSalido)
TiemposDeResidencia = tiempoPromedioResidencia(tiempoDeResidencia, jobsQueLlegaron, jobsQueSalieron)

#   Resultados Medidas de Rendimiento
print("Numero de jobs que llegaron: ", jobsQueLlegaron)
print("Numero de jobs que salieron: ", jobsQueSalieron)
print("Tiempo total de cola vacıa: ", tiempoCantidadCola[0])
print("Largo maximo de la cola: ", len(tiempoCantidadCola)-1)
print("Tiempo total de la cola con largo maximo: ", tiempoCantidadCola[len(tiempoCantidadCola)-1])
print("Utilizacion computada: ", Utilizaciones[1])
print("Utilizacion teorica: ", Utilizaciones[0])
print("Largo promedio computado de la cola: ", LargosPromedio[0])
print("Largo promedio teorico de la cola: ", LargosPromedio[1])
print("Tiempo promedio computado de residencia: ", TiemposDeResidencia[0])
print("Tiempo promedio teorico de residencia: ", TiemposDeResidencia[1])

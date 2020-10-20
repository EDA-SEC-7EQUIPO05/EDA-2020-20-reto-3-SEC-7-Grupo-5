"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
from DISClib.DataStructures import listiterator as it
from time import process_time
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# _____________________________________________

us_accidents_small = "us_accidents_small.csv"
us_accidents_2016 = "us_accidents_dis_2016.csv"
us_accidents_2017 = "us_accidents_dis_2017.csv"
us_accidents_2018 = "us_accidents_dis_2018.csv"
us_accidents_2019 = "us_accidents_dis_2019.csv"
all_accidents = [us_accidents_small, us_accidents_2016, us_accidents_2017, us_accidents_2018, us_accidents_2019]

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1")
    print("4- Requerimento 2")
    print("5- Requerimento 3")
    print("6- Requerimento 4")
    print("7- Requerimento 5")
    print("8- Requerimiento 6")
    print("0- Salir")
    print("*******************************************")

def print_severity_information_by_date(SeverityIndex_values):
    iterator = it.newIterator(SeverityIndex_values)
    while it.hasNext(iterator):
        elemento = it.next(iterator)
        print("Severity: "+str(elemento['Severity'])+" -> "+str(elemento['Accidents']['size'])+" accidentes")

def print_accidents_before_date (accidentes):
    suma=0
    lista=[]
    for i in range(1,lt.size(accidentes)):
        keyDate=lt.getElement(accidentes,i)
        cantidad=lt.size(keyDate["AccidentList"])
        suma+=cantidad
        lista.append(cantidad)
    maximo=max(lista)
    for m in range(1,lt.size(accidentes)):
        keyDate=lt.getElement(accidentes,m)
        cantidad=lt.size(keyDate["AccidentList"])
        if maximo==cantidad:
            fecha=keyDate["Date"]
        
    print("El total de accidentes ocurridos antes de la fecha indicada fueron: "+str(suma)+" "+"y la fecha en la que mas se reportaron accidentes fue: "+str(fecha))


def printAccidentsByZoneInfo(dayTable):
    k = 0
    for i in dayTable:
            print(i+": "+str(dayTable[i])+" accidents")
            k+=1
            if k == 8:
                print("Comparaciones hechas: " + str(dayTable["Comparaciones_hechas"]))                                                                                          
                print("Eficiencia: " + str(dayTable["Eficiencia"])+"%") 
                break


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes....")
        t_start = process_time()
        controller.loadData(cont, all_accidents[0])
        t_stop = process_time()
        print("El tiempo de carga total fue de "+str(t_stop-t_start)+" segundos")
        print("\nAltura del arbol de fechas: "+str(controller.heightDateIndex(cont)))
        print("Elementos del arbol: "+str(controller.sizeDateIndex(cont)))
        print("Menor llave: "+str(controller.minKey(cont)))
        print("Mayor llave: "+str(controller.maxKey(cont)))
        print("\nAltura del arbol de tiempos: "+str(controller.heightTimeIndex(cont)))
        print("Elementos del arbol: "+str(controller.sizeTimeIndex(cont)))
        print("Menor llave: "+str(controller.TimeMinKey(cont)))
        print("Mayor llave: "+str(controller.TimeMaxKey(cont)))
        print("\nAltura del arbol de distancias: "+str(controller.heightDistanceIndex(cont)))
        print("Elementos del arbol: "+str(controller.sizeDistanceIndex(cont)))
        print("Menor llave: "+str(round(controller.DistanceMinKey(cont), 3)) + "km")
        print("Mayor llave: "+str(round(controller.DistanceMaxKey(cont), 3)) + "km")


    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        while True:
            initialDate = input("Fecha (YYYY-MM-DD): ")
            value = controller.accidentsbyDate(cont,initialDate)
            if value is not None:
                SeverityIndex = value['SeverityIndex']
                SeverityIndex_values = controller.severitybyDate(SeverityIndex)
                StateIndex = value['StateIndex']
                StateIndex_values = controller.statebyDate(StateIndex)
                print("Los accidentes por severidad en esta fecha son:\n")
                print_severity_information_by_date(SeverityIndex_values)
                print("\nEl total de accidentes para esa fecha es de "+str(value["AccidentList"]["size"]))
                print("Hay "+ str(SeverityIndex["size"])+" severities")
                break
            else:
                print("No se encontró la fecha o no es un dato válido, ingrese una fecha de nuevo")


    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
        date=input("Fecha (YYYY-MM-DD): ")
        accidentes = controller.accidentsbeforeDate(cont,date)
        if accidentes is not None:
            print_accidents_before_date(accidentes)
        else:
            print("\nNo se encontró la fecha o no es un dato válido, ingrese una fecha de nuevo")

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        keylo = input("\nPrimera fecha (YYYY-MM-DD): ")
        keyhi = input("Segunda fecha (YYYY-MM-DD): ")
        print("\nBuscando accidentes en un rango de fechas: ")
        t_start = process_time()
        tupla = controller.accidentsInRangeOfDates(cont, keylo, keyhi)
        total = tupla[0]
        maxim = tupla[1]
        print("\nHubo un total de " + str(total) + " accidentes en este rango de fechas")
        print("La mayor cantidad de accidentes en este rango de fechas fueron de severity tipo " + str(maxim))
        print(tupla[2])
        t_stop = process_time()
        print("\nEl tiempo para este requerimiento fue de "+str(t_stop-t_start)+" segundos")

    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        mindate = input("Primera fecha (YYYY-MM-DD): ")
        maxdate = input("Segunda fecha (YYYY-MM-DD): ")
        max_date_acc = controller.maxDateinRange(mindate, maxdate, cont)
        max_state_acc = controller.maxStateinRange(mindate, maxdate, cont)
        print("\nEn el rango entre",mindate,"y",maxdate,"la fecha con más accidentes es",max_date_acc[0],"con", max_date_acc[1],"accidentes.")
        print("El estado con mas accidentes es",max_state_acc[1],"con",max_state_acc[0],"accidentes.")

    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        mintime = input("Primera hora (HH-MM-SS): ")
        maxtime = input("Segunda hora (HH-MM-SS): ")
        info = controller.accidentsinTimeRange(mintime, maxtime, cont)
        sevs = controller.severitybyTimeRange(mintime, maxtime, cont)
        print("En el rango entre",mintime,"y",maxtime,"el número de accidentes es",info,"\n")
        print('Severidad:\n')
        for i in range(1,5):
            data = sevs[str(i)]
            per = round((data/info)*100,2)
            print(str(i)+' -> '+ str(data)+' ('+str(per)+'%)\n')
    
    elif int(inputs[0]) == 8:
        print("\nRequerimiento No 6 del reto 3: ")
        while True:
            try:
                radio = abs(float(input("Ingrese un radio de búsqueda en kilómetros: ")))
                break
            except:
                print("Solo se permiten ingresar números, intente de nuevo")
        while True:
            try:
                longitud = float(input("Ingrese una longitud en grados: "))   
                break
            except:
                print("Solo se permiten ingresar números, intente de nuevo")
        while True:
            try:
                latitud = float(input("Ingrese una latitud en grados: "))
                print("\n")   
                break
            except:
                print("Solo se permiten ingresar números, intente de nuevo")
        print("\nAccidentes por zona geográfica dada por parámetro y día de la semana:\n")
        t_start = process_time()
        dayTable = controller.accidentsByZone(radio, longitud, latitud, cont)
        printAccidentsByZoneInfo(dayTable)
        t_stop = process_time()
        print("El tiempo para este proceso fue de "+str(t_stop-t_start)+" segundos")

    elif int(inputs[0]) == 0:
        sys.exit(0)
    
    else:
        print("Ingrese una opción válida")
sys.exit(0)
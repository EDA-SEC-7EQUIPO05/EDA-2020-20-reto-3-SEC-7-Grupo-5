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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.calculos import distances as c
from DISClib.DataStructures import listiterator as it
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria
"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    analyzer = {'DateIndex': None, 'TimeIndex': None, 'DistanceIndex': None}
    analyzer['DateIndex'] = om.newMap(omaptype='BRT', comparefunction = compareDates)
    analyzer['TimeIndex'] = om.newMap(omaptype='BRT', comparefunction = compareTimes)
    analyzer['DistanceIndex'] = om.newMap(omaptype='BRT', comparefunction = compareDistances)
    return analyzer

# Funciones para agregar informacion al catalogo

def addAccident(accident, analyzer):
    updateDateIndex(accident, analyzer['DateIndex'])
    updateTimeIndex(accident, analyzer['TimeIndex'])
    updateDistanceTree(accident, analyzer["DistanceIndex"])
    return analyzer

def newDateEntry(accdate):
    newEntry = {'Date': None, 'SeverityIndex': None, 'StateIndex': None, 'AccidentList': None}
    newEntry['Date'] = accdate
    newEntry['SeverityIndex'] = m.newMap(numelements = 5, maptype = 'PROBING', loadfactor = 0.5, comparefunction = compareSeverity)
    newEntry['StateIndex'] = m.newMap(numelements = 50, maptype = 'CHAINING', loadfactor = 2, comparefunction = compareState)
    newEntry['AccidentList'] = lt.newList('SINGLE_LINKED', compareDates)
    return newEntry

def newSeverityEntry(severity):
    sevEntry = {'Severity': None, 'Accidents': None}
    sevEntry['Severity'] = severity
    sevEntry['Accidents'] = lt.newList('SINGLE_LINKED', compareAccidentId)
    return sevEntry

def newStateEntry(state):
    stEntry = {'State': None, 'Accidents': None}
    stEntry['State'] = state
    stEntry['Accidents'] = lt.newList('SINGLE_LINKED', compareAccidentId)
    return stEntry

def addDateAccident(entry, acdnt):
    sevIndex = entry['SeverityIndex']
    lst = entry['AccidentList']
    severity = acdnt['Severity']
    lt.addLast(lst, acdnt)
    esta = m.contains(sevIndex, severity)
    if esta == False:
        sevEntry = newSeverityEntry(severity)
        m.put(sevIndex, severity, sevEntry)
    else:
        sevElement = m.get(sevIndex, severity)
        sevEntry = me.getValue(sevElement)
    lt.addLast(sevEntry['Accidents'], acdnt)
    addStateAccident(entry, acdnt)
    return entry

def addStateAccident(entry, acdnt):
    stIndex = entry['StateIndex']
    state = acdnt['State']
    esta = m.contains(stIndex, state)
    if esta == False:
        stEntry = newStateEntry(state)
        m.put(stIndex, state, stEntry)
    else:
        stElement = m.get(stIndex, state)
        stEntry = me.getValue(stElement)
    lt.addLast(stEntry['Accidents'], acdnt)

def updateDateIndex(accident, mapa):
    occurreddate = accident['Start_Time']
    accdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(mapa, accdate.date())
    if entry is None:
        dateEntry = newDateEntry(accdate.date())
        om.put(mapa, accdate.date(), dateEntry)
    else:
        dateEntry = me.getValue(entry)
    addDateAccident(dateEntry, accident)
    return mapa

def updateTimeIndex(accident, mapa):
    occurdate = accident['Start_Time']
    accdate = datetime.datetime.strptime(occurdate, '%Y-%m-%d %H:%M:%S')
    if accdate.minute < 15 or (accdate.minute > 29 and accdate.minute < 45):
        entry_time = floor_dt(accdate).time()
    else:
        entry_time = floor_dt(accdate).time()
    entry = om.get(mapa, entry_time)
    if entry is None:
        timeEntry = newTimeEntry(entry_time)
        om.put(mapa, entry_time, timeEntry)
    else:
        timeEntry = me.getValue(entry)
    addTimeAccident(timeEntry, accident)
    return mapa

def newTimeEntry(acctime):
    newEntry = {'Time': None, 'SeverityIndex': None, 'AccidentList': None}
    newEntry['Time'] = acctime
    newEntry['SeverityIndex'] = m.newMap(numelements = 5, maptype = 'PROBING', loadfactor = 0.5, comparefunction = compareSeverity)
    newEntry['AccidentList'] = lt.newList('SINGLE_LINKED', compareTimes)
    return newEntry

def addTimeAccident(entry, acdnt):
    sevIndex = entry['SeverityIndex']
    lst = entry['AccidentList']
    severity = acdnt['Severity']
    lt.addLast(lst, acdnt)
    esta = m.contains(sevIndex, severity)
    if esta == False:
        sevEntry = newSeverityEntry(severity)
        m.put(sevIndex, severity, sevEntry)
    else:
        sevElement = m.get(sevIndex, severity)
        sevEntry = me.getValue(sevElement)
    lt.addLast(sevEntry['Accidents'], acdnt)

def updateDistanceTree(accident, tree):
    longitud = float(accident["Start_Lng"])
    latitud = float(accident["Start_Lat"])
    distance = c.calcular_distancia(6378.13434441, longitud, latitud)
    node = om.get(tree, distance)
    if node is None:
        distanceValue =  newDistanceValue()
        om.put(tree, distance, distanceValue)
        addAccidentToDistanceValue(accident, distanceValue, distance)
    else:
        distanceValue = me.getValue(node)
        addAccidentToDistanceValue(accident, distanceValue, distance) 
    return tree

def addAccidentToDistanceValue(accident, distanceValue, distance):
    date = accident['Start_Time']
    element = newDistanceAccident()
    element["date"] = date
    element["accident"] = accident
    element["distance"] = distance
    lt.addLast(distanceValue, element)
    return distanceValue

def newDistanceValue():
    value = lt.newList('SINGLE_LINKED', compareDates)
    return value

def newDistanceAccident():
    element = {"distance": None, "date": None, "accident": None}
    return element


# ==============================
# Funciones de consulta
# ==============================

def sizeDateIndex(analyzer):
    return om.size(analyzer['DateIndex'])

def heightDateIndex(analyzer):
    return om.height(analyzer['DateIndex'])

def minKey(analyzer):
    return om.minKey(analyzer['DateIndex'])

def maxKey(analyzer):
    return om.maxKey(analyzer['DateIndex'])

def sizeTimeIndex(analyzer):
    return om.size(analyzer["TimeIndex"])

def heightTimeIndex(analyzer):
    return om.height(analyzer["TimeIndex"])

def TimeMinKey(analyzer):
    return om.minKey(analyzer['TimeIndex'])

def TimeMaxKey(analyzer):
    return om.maxKey(analyzer['TimeIndex'])

def sizeDistanceIndex(analyzer):
    return om.size(analyzer["DistanceIndex"])

def heightDistanceIndex(analyzer):
    return om.height(analyzer["DistanceIndex"])

def DistanceMinKey(analyzer):
    return om.minKey(analyzer['DistanceIndex'])

def DistanceMaxKey(analyzer):
    return om.maxKey(analyzer['DistanceIndex'])

def accidentsbyDate(analyzer, date):
    element = me.getValue(om.get(analyzer['DateIndex'], date))
    if element is not None:
        return element
    return None

def severitybyDate(SeverityIndex):
    return m.valueSet(SeverityIndex)

def accidentsbeforeDate(analyzer, date):
    tree=analyzer["DateIndex"]
    min_date=om.minKey(tree)
    accidents=om.values(tree, min_date, date)
    return accidents

def accidentsInRangeOfDates(analyzer, keylo, keyhi):
    tree = analyzer["DateIndex"]
    values = om.values(tree, keylo, keyhi)
    accidentsTable = countAccidentsInRangeOfDates(values)
    maxim = maxInAccidentsTable(accidentsTable)
    return (accidentsTable["Total"], maxim, accidentsTable)

def countAccidentsInRangeOfDates(values):
    accidentsTable = {"1": 0, "2": 0, "3": 0, "4": 0, "Total": 0}
    iterator = it.newIterator(values)
    while it.hasNext(iterator):
        accidents = it.next(iterator)
        map = accidents["SeverityIndex"]
        num = accidents['AccidentList']["size"]
        keys = m.keySet(map)
        for i in range(1, keys["size"]+1):
            key = lt.getElement(keys, i)
            entry = m.get(map, key)
            value = me.getValue(entry)['Accidents']["size"]
            accidentsTable[str(key)] += value
        accidentsTable["Total"] += num
    return accidentsTable

def maxInAccidentsTable(accidentsTable):
    severity = None
    keys = list(accidentsTable.keys())
    values = list(accidentsTable.values())
    values = values[0:4]
    maxim = max(values)
    pos = values.index(maxim)
    severity = keys[pos]
    return severity


def statebyDate(StateIndex):
    return m.valueSet(StateIndex)

def valuesinRange(mindate, maxdate, analyzer):
    return om.values(analyzer['DateIndex'], mindate, maxdate)

def maxStateinRange(mindate, maxdate, analyzer):
    values = valuesinRange(mindate, maxdate, analyzer)
    iterator = it.newIterator(values)
    estados = {}
    while it.hasNext(iterator):
        elemento = it.next(iterator)
        state_values = statebyDate(elemento['StateIndex'])
        iterator_2 = it.newIterator(state_values)
        while it.hasNext(iterator_2):
            elem = it.next(iterator_2)
            if elem['State'] not in estados.keys():
                estados[elem['State']] = lt.size(elem['Accidents'])
            else:
                estados[elem['State']] += lt.size(elem['Accidents'])
    max_acc = 0
    max_state = None
    for i in estados:
        if estados[i] > max_acc:
            max_acc = estados[i]
            max_state = i
    return (max_acc, max_state)

def accidentsbyTime(analyzer, time):
    element = me.getValue(om.get(analyzer['TimeIndex'], time))
    if element is not None:
        return element
    return None

def SeveritybyTime(SeverityIndex):
    return m.valueSet(SeverityIndex)

def accidentsinTimeRange(analyzer, mintime, maxtime):
    return om.values(analyzer['TimeIndex'], mintime, maxtime)

def numberAccidentsinTimeRange(analyzer, mintime, maxtime):
    num = 0
    values = accidentsinTimeRange(analyzer, mintime, maxtime)
    iterator = it.newIterator(values)
    while it.hasNext(iterator):
        element = it.next(iterator)
        num += lt.size(element['AccidentList'])

    return num

def SeveritybyTimeRange(analyzer, mintime, maxtime):
    values = accidentsinTimeRange(analyzer, mintime, maxtime)
    iterator = it.newIterator(values)
    sevs = {'1': 0,'2': 0, '3': 0, '4': 0}
    while it.hasNext(iterator):
        elemento = it.next(iterator)
        severities = SeveritybyTime(elemento['SeverityIndex'])
        iterator_2 = it.newIterator(severities)
        while it.hasNext(iterator_2):
            elem = it.next(iterator_2)
            sevs[elem['Severity']] += lt.size(elem['Accidents'])
    return sevs

def maxDateinRange(mindate, maxdate, analyzer):
    date = None
    max_acc = 0
    values = valuesinRange(mindate, maxdate, analyzer)
    iterator = it.newIterator(values)
    while it.hasNext(iterator):
        elemento = it.next(iterator)
        if lt.size(elemento['AccidentList']) > max_acc:
            max_acc = lt.size(elemento['AccidentList'])
            date = elemento['Date']
    return (date, max_acc)


def accidentsByZone(radio, longitud, latitud, analyzer):
    dayTable = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0,
    "Total":0, "Comparaciones_hechas": 0.0000001, "Eficiencia": None}
    tree = analyzer["DistanceIndex"]
    root = tree['root']
    distancia_referencia = c.calcular_distancia(6378.13434441, longitud, latitud)
    keylo = distancia_referencia - radio
    keyhi = distancia_referencia + radio
    dayTable = inorderDistancesTree(dayTable, root, longitud, latitud, radio, keylo, keyhi, compareDistances)
    dayTable["Eficiencia"] = round((dayTable["Total"]/dayTable["Comparaciones_hechas"])*100,3)
    dayTable["Comparaciones_hechas"] = int(dayTable["Comparaciones_hechas"])
    return dayTable

def inorderDistancesTree(dayTable, root, longitud, latitud, radio, keylo, keyhi, compareDistances):
    try:
        if (root is not None):
            complo = compareDistances(keylo, root['key'])
            comphi = compareDistances(keyhi, root['key'])

            if (complo < 0):
                inorderDistancesTree(dayTable, root['left'], longitud, latitud, radio, keylo, keyhi, compareDistances)
            if ((complo <= 0) and (comphi >= 0)):
                value = root["value"]
                iterator = it.newIterator(value)
                while it.hasNext(iterator):
                    elemento = it.next(iterator)
                    date = elemento["date"]
                    accident = elemento["accident"]
                    long = float(accident["Start_Lng"])
                    lat = float(accident["Start_Lat"])
                    distancia = c.calcular_distancia(6378.13434441, longitud-long, latitud-lat)
                    if distancia <= radio:
                        dayTable[c.dayBydate(date)]+=1
                        dayTable["Total"]+=1
                    dayTable["Comparaciones_hechas"]+=1
            if (comphi > 0):
                inorderDistancesTree(dayTable, root['right'], longitud, latitud, radio, keylo, keyhi, compareDistances)
        return dayTable
    except Exception as exp:
        error.reraise(exp, 'Tree: inorderDistancesTree')

# ==============================
# Funciones de Comparacion
# ==============================

def compareAccidentId(id_1, id_2):
    if id_1 == id_2:
        return 0
    elif id_1 > id_2:
        return 1
    else:
        return -1

def compareDates(date_1, date_2):
    if date_1 == date_2:
        return 0
    elif date_1 > date_2:
        return 1
    else:
        return -1

def compareSeverity(sev_1, sev_2):
    sev_entry = me.getKey(sev_2)
    if sev_1 == sev_entry:
        return 0
    elif sev_1 > sev_entry:
        return 1
    else:
        return -1

def compareState(state_1, state_2):
    st_entry = me.getKey(state_2)
    if state_1 == st_entry:
        return 0
    elif state_1 > st_entry:
        return 1
    else:
        return -1

def compareTimes(time_1, time_2):
    if time_1 == time_2:
        return 0
    elif time_1 > time_2:
        return 1
    else:
        return -1

def compareDistances(distance_1, distance_2):
    if distance_1 == distance_2:
        return 0
    elif distance_1 > distance_2:
        return 1
    else:
        return -1


def ceil_dt(dt, delta = datetime.timedelta(minutes=30)):
    return dt + (datetime.datetime.min - dt) % delta

def floor_dt(dt, delta = datetime.timedelta(minutes=30)):
    return dt - (dt - datetime.datetime.min) % delta

def time_round(time):
    if time.minute < 15 or (time.minute > 29 and time.minute < 45):
        entry_time = floor_dt(time).time()
    else:
        entry_time = ceil_dt(time).time()
    return entry_time
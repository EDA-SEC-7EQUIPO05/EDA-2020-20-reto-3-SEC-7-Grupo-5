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
    analyzer = {'accidents': None, 'DateIndex': None}
    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareAccidentId)
    analyzer['DateIndex'] = om.newMap(omaptype='BST', comparefunction = compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo

def addAccident(accident, analyzer):
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(accident, analyzer['DateIndex'])
    return analyzer

def newDateEntry():
    newEntry = {'SeverityIndex': None, 'AccidentList': None}
    newEntry['SeverityIndex'] = m.newMap(numelements = 5, maptype = 'PROBING', loadfactor = 0.5, comparefunction = compareSeverity)
    newEntry['AccidentList'] = lt.newList('SINGLE_LINKED', compareDates)
    return newEntry

def newSeverityEntry(severity):
    sevEntry = {'Severity': None, 'Accidents': None}
    sevEntry['Severity'] = severity
    sevEntry['Accidents'] = lt.newList('SINGLE_LINKED', compareSeverity)
    return sevEntry

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
    return entry

def updateDateIndex(accident, mapa):
    occurreddate = accident['Start_Time']
    accdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(mapa, accdate.date())
    if entry is None:
        dateEntry = newDateEntry()
        om.put(mapa, accdate.date(), dateEntry)
    else:
        dateEntry = me.getValue(entry)
    addDateAccident(dateEntry, accident)
    return mapa


# ==============================
# Funciones de consulta
# ==============================

def sizeAccidents(analyzer):
    return lt.size(analyzer['accidents'])

def sizeDateIndex(analyzer):
    return om.size(analyzer['DateIndex'])

def heightDateIndex(analyzer):
    return om.height(analyzer['DateIndex'])

def minKey(analyzer):
    return om.minKey(analyzer['DateIndex'])

def maxKey(analyzer):
    return om.maxKey(analyzer['DateIndex'])

def accidentsbyDate(analyzer, date):
    element = me.getValue(om.get(analyzer['DateIndex'], date))
    if element is not None:
        return element
    return None

def severitybyDate(SeverityIndex):
    return m.valueSet(SeverityIndex)

def accidentsbeforeDate(analyzer, date):
    element = me.getValue(om.get(analyzer['DateIndex'], date))
    if element is not None:
        return om.rank(analyzer['DateIndex'], date)
    return None


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
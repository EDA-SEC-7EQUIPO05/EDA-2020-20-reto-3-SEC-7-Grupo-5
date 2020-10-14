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
    analyzer = {'accidents': None, 'dateIndex': None}
    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareAccidentId)
    analyzer['DateIndex'] = om.newMap(omaptype='RBT', comparefunction = compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo


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

# ==============================
# Funciones de Comparacion
# ==============================

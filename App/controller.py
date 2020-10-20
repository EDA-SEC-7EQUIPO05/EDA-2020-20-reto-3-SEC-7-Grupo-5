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

import config as cf
from App import model
import datetime
import csv
from DISClib.DataStructures import listiterator as it

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer



# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"), delimiter=",")
    for accident in input_file:
        model.addAccident(accident, analyzer)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def sizeDateIndex(analyzer):
    return model.sizeDateIndex(analyzer)

def heightDateIndex(analyzer):
    return model.heightDateIndex(analyzer)

def minKey(analyzer):
    return model.minKey(analyzer)

def maxKey(analyzer):
    return model.maxKey(analyzer)

def sizeTimeIndex(analyzer):
    return model.sizeTimeIndex(analyzer)

def heightTimeIndex(analyzer):
    return model.heightTimeIndex(analyzer)

def TimeMinKey(analyzer):
    return model.TimeMinKey(analyzer)

def TimeMaxKey(analyzer):
    return model.TimeMaxKey(analyzer)

def sizeDistanceIndex(analyzer):
    return model.sizeDistanceIndex(analyzer)

def heightDistanceIndex(analyzer):
    return model.heightDistanceIndex(analyzer)

def DistanceMinKey(analyzer):
    return model.DistanceMinKey(analyzer)

def DistanceMaxKey(analyzer):
    return model.DistanceMaxKey(analyzer)

def accidentsbyDate(analyzer, initialDate):
    try:
        initialDate=datetime.datetime.strptime(initialDate, '%Y-%m-%d')
        return model.accidentsbyDate(analyzer, initialDate.date())
    except:
        return None

def accidentsbeforeDate (analyzer, date):
    try:
        date=datetime.datetime.strptime(date, '%Y-%m-%d')
        return model.accidentsbeforeDate(analyzer, date.date())
    except:
        return None

def accidentsInRangeOfDates(analyzer, keylo, keyhi):
    keylo = datetime.datetime.strptime(keylo, '%Y-%m-%d')
    keyhi = datetime.datetime.strptime(keyhi, '%Y-%m-%d')
    return model.accidentsInRangeOfDates(analyzer, keylo.date(), keyhi.date())

def severitybyDate(SeverityIndex):
    return model.severitybyDate(SeverityIndex)

def statebyDate(StateIndex):
    return model.statebyDate(StateIndex)

def maxDateinRange(mindate, maxdate, analyzer):
    mindate = datetime.datetime.strptime(mindate, '%Y-%m-%d')
    maxdate = datetime.datetime.strptime(maxdate, '%Y-%m-%d')
    return model.maxDateinRange(mindate.date(), maxdate.date(), analyzer)

def maxStateinRange(mindate, maxdate, analyzer):
    mindate = datetime.datetime.strptime(mindate, '%Y-%m-%d')
    maxdate = datetime.datetime.strptime(maxdate, '%Y-%m-%d')
    return model.maxStateinRange(mindate.date(), maxdate.date(), analyzer)

def accidentsinTimeRange(mintime, maxtime, analyzer):
    mintime = datetime.datetime.strptime(mintime, '%H-%M-%S')
    maxtime = datetime.datetime.strptime(maxtime, '%H-%M-%S')
    return model.numberAccidentsinTimeRange(analyzer, mintime.time(), maxtime.time())

def severitybyTimeRange(mintime, maxtime, analyzer):
    mintime = datetime.datetime.strptime(mintime, '%H-%M-%S')
    maxtime = datetime.datetime.strptime(maxtime, '%H-%M-%S')
    return model.SeveritybyTimeRange(analyzer, mintime.time(), maxtime.time())

def accidentsByZone(radio, longitud, latitud, analyzer):
    dayTable = model.accidentsByZone(radio, longitud, latitud, analyzer)
    return dayTable


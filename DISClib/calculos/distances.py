import math as m
import datetime

"""
Permite hacer cáculos de distancia en una superficie
esférica
"""

# ___________________________________________________
#  Funciones de cálculos
# ___________________________________________________

def calcular_distancia(radio, longitud, latitud):
    """
    Calcula la distancia entre dos lugares de una esfera
    """
    distancia = None
    factor_conversion = m.pi/180
    longitud = longitud*factor_conversion
    latitud = latitud*factor_conversion
    a = pow(m.sin(latitud/2),2) + m.cos(0)*m.cos(latitud)*pow(m.sin(longitud/2),2)
    c = 2*m.asin(m.sqrt(a))
    distancia = radio*c
    return distancia

def dayBydate(date):
    date = date.replace("-", "/")
    date = date.split(" ")
    del date[1]
    date = "".join(date)
    date = date.split("/")
    a = date[0]
    b = date[2]
    date[2] = a
    date[0] = b
    date = "/".join(date)
    day, month, year = (int(x) for x in date.split('/'))    
    ans = datetime.date(year, month, day)
    return ans.strftime("%A")


a = calcular_distancia(6378.13434441,-84, 39)
print(a)
import numpy as np
from Projekt1 import Transformacje

def czytanie_txt(xyz0 , l0 ,model = 'nazwa modelu', plik = 'nazwa pliku', funkcja = 'nazwa funkcji', jedn = 'dec',nazwa_wych = 'nazwa_pliku_wychodzącego'):
    """
    Program przyjmuje plik txt tylko w takim formacie:
    
    3664940.500 1409153.590 5009571.170
    3664940.510 1409153.580 5009571.167
    3664940.520 1409153.570 5009571.167
    3664940.530 1409153.560 5009571.168
    3664940.520 1409153.590 5009571.170
    3664940.514 1409153.584 5009571.166    
    
    A następnie przelicza do układu który poda użytkownik.Niedoskonałoscią tego programu jest
    to że pobiera argumenty dla wszystkich funkcji.Lecz to nie jest aż tak wileki problem, wystarczy 
    wpisać losowe warto
    
    Parameters
    ----------
    flh : LIST
        wspolrzedne geodezyjne phi, lam, h [metry]
    l0 : int
        [stopnie dziesiętne] - południk osiowy
    jedn : STR, optional
        Jednostka wspolrzednych geodezyjnych. Domyslna jest "dec".
        ["rad" - radiany, "gra" - grady, "dec" - stopnie]

    Raises
    ------
    NotImplementedError
        Jezeli podana jednostka jest poza zbiorem.

    Returns
    -------
    xy2000 : LIST
        Wspolrzedne w układzie PL-2000 [metry]
    """
    geo = Transformacje(model)
    
    dok = open(plik,'r')
    linie = dok.readlines()
    wsp = []
    for i in linie:
        a = i.split()
        wsp.append(a)
    wsp2 = []
    for i in wsp:
        wart = [float(i[0]),float(i[1]),float(i[2])]
        wsp2.append(wart)  
    if funkcja == 'xyz2flh':
        xyz = []
        for i in wsp2:
            flh = geo.xyz2flh(i,jedn)
            xyz.append(flh)
    elif funkcja == 'flh2xyz':
        xyz = []
        for i in wsp2:
            flh = geo.flh2xyz(i,jedn)
            xyz.append(flh)
    elif funkcja == 'xyz2neu':
        xyz = []
        for i in wsp2:
            flh = geo.xyz2neu(xyz0,i,jedn)
            xyz.append(flh)
    elif funkcja == 'XgkYgk':
        xyz = []
        for i in wsp2:
            flh = geo.XgkYgk(i,l0,jedn)
            xyz.append(flh)
    elif funkcja == 'XY2000':
        xyz = []
        for i in wsp2:
            flh = geo.XY2000(i,l0,jedn)
            xyz.append(flh)
    elif funkcja == 'XY1992':
        xyz = []
        for i in wsp2:
            flh = geo.XY1992(i,jedn)
            xyz.append(flh)
    else:
        raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
    plik_w = open(nazwa_wych,'w')
    plik_w.write(f'''Funkcja: {funkcja}\n''')
    for i in xyz:
        plik_w.write(f'''{i}\n''')
    plik_w.close()
    
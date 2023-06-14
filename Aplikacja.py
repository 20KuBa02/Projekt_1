import argparse
import Projekt1
import czytanie_txt
from argparse import ArgumentParser
from Projekt1 import Transformacje
from czytanie_txt import *

parser = ArgumentParser(description='Wywoływanie funkcji z klasy')

parser.add_argument('-func',type = str ,help='Wybierz funkcję:xyz2flh,flh2XYZ,xyz2neu,XgkYgk,XY2000,XY1992,czytanie_txt')
parser.add_argument('-func2',type = str ,help='Używane jesli została wybrana funckja czytanie_txt. Wybierz funkcje:xyz2flh,flh2XYZ,xyz2neu,XgkYgk,XY2000,XY1992')
parser.add_argument('-m',type = str , help = 'Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke')
parser.add_argument('-x',type = float, help = 'Zawsze podawane w [metry] wsp. x układu kartezjańskiego')
parser.add_argument('-y',type = float, help = 'Zawsze podawane w [metry] wsp. y układu kartezjańskiego')
parser.add_argument('-z',type = float, help = 'Zawsze podawane w [metry] wsp. z układu kartezjańskiego')
parser.add_argument('-f',type = float, help = 'Zawsze okreslona przez argument -func ,szerokość geodezyjna')
parser.add_argument('-l',type = float, help = 'Zawsze okreslona przez argument -func ,długość geodezyjna')
parser.add_argument('-l0',type = float, help = 'Zawsze okreslona przez argument -func ,południk zerowy')
parser.add_argument('-he',type = float, help = 'Zawsze podawane w [metry] wysokosc elipsoidalna')
parser.add_argument('-jedn',type = str, help = 'Wskaż jednsotkę z listy : rad,dec,gra. Dla funkcji xyz2flh jest to jednostka w której mają być zwrócone współrzędne, a dla funkcji flh2XYZ,XgkYgk,XY2000,XY1992 jednostki w jakich wchodzą współrzędne. ')
parser.add_argument('-x0',type = float, help = 'Zawsze podawane w [metry] wsp. x0 srodka układu kartezjańskiego ')
parser.add_argument('-y0',type = float, help = 'Zawsze podawane w [metry] wsp. y0 srodka układu kartezjańskiego')
parser.add_argument('-z0',type = float, help = 'Zawsze podawane w [metry] wsp. z0 srodka kartezjańskiego')
parser.add_argument('-xr',type = float, help = 'Zawsze podawane w [metry] wsp. x referencyjna układu układu kartezjańskiego ')
parser.add_argument('-yr',type = float, help = 'Zawsze podawane w [metry] wsp. y referencyjna układu układu kartezjańskiego')
parser.add_argument('-zr',type = float, help = 'Zawsze podawane w [metry]wsp. z referencyjna układu kartezjańskiego')
parser.add_argument('-plik',type = str, help = 'Nazwa pliku txt który chcemy użyć do funkcji czytanie_txt')
parser.add_argument('-plik_wych',type = str, help = 'Nazwa pliku txt który będzie plikem , w którym zapiszą się nam nasze wyniki')
parser.add_argument('-pomoc', type = str ,help = 'Argumenty przyjmowane przez poszczególne funkcje: xyz2flh(-x,-y,-z,-jedn),flh2XYZ(-f,-l,-he,-jedn),xyz2neu(-x0,-y0,-z0,-xr,-yr,-zr),XgkYgk(-f,-l,-he,-l0,-jedn),XY2000(-f,-l,-he,-l0,-jedn),XY1992(-f,-l,-he,-jedn),czytanie_txt(-x0,-y0,-z0,-l0,-m,-plik,-func2,-jedn,-plik_wych)      Program czytanie_txt przyjmuje plik txt tylko w takim formacie:3664940.500 1409153.590 5009571.170\\3664940.510 1409153.580 5009571.167\\3664940.520 1409153.570 5009571.167\\3664940.530 1409153.560 5009571.168\\3664940.520 1409153.590 5009571.170\\3664940.514 1409153.584 5009571.166\\A następnie przelicza do układu który poda użytkownik.Niedoskonałoscią tego programu jest to że pobiera argumenty dla wszystkich funkcji.Lecz to nie jest aż tak wileki problem, wystarczy wpisać losowe wartosci, nie będą one miały wplywu na wynik końcowy.')
args = parser.parse_args()

if args.func == 'xyz2flh':
    geo = Transformacje(model = args.m)
    print(geo.xyz2flh([args.x,args.y,args.z],args.jedn))
elif args.func == 'flh2XYZ':
    geo = Transformacje(model = args.m)
    print(geo.flh2XYZ([args.f,args.l,args.he],args.jedn))
elif args.func == 'xyz2neu':
    geo = Transformacje(model = args.m)
    print(geo.xyz2neu([args.x0,args.y0,args.z0],[args.xr,args.yr,args.zr]))
elif args.func == 'XgkYgk':
    geo = Transformacje(model = args.m)
    print(geo.XgkYgk([args.f,args.l,args.he],args.l0,args.jedn))
elif args.func == 'XY2000':
    geo = Transformacje(model = args.m)
    print(geo.XY2000([args.f,args.l,args.he],args.l0,args.jedn))
elif args.func == 'XY1992':
    geo = Transformacje(model = args.m)
    print(geo.XY1992([args.f,args.l,args.he],args.jedn))
elif args.func == 'czytanie_txt':
    czytanie_txt([args.x0,args.y0,args.z0],args.l0,args.m,args.plik,args.func2,args.jedn,args.plik_wych)
    
    


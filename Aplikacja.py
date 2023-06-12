import argparse
import Projekt1
from argparse import ArgumentParser
from Projekt1 import Transformacje


'''parser = ArgumentParser()
parser.add_argument('-m' , '--m', type = str , help = 'Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke')
parser.add_argument('-x','--x',type = float)
parser.add_argument('-y','--y',type = float)
parser.add_argument('-z','--z',type = float)
parser.add_argument('-jedn', '--jedn',type = str)
args = parser.parse_args()

geo = Transformacje(model = args.m)
flh = geo.xyz2flh([args.x,args.y,args.z],args.jedn)
print(flh)'''


parser = ArgumentParser(description='Wywoływanie funkcji z klasy')

parser.add_argument('-func',type = str ,help='Wybierz funkcję:xyz2flh,flh2XYZ,xyz2neu,XgkYgk,XY2000,XY1992')
parser.add_argument('-m',type = str , help = 'Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke')
parser.add_argument('-x',type = float, help = 'wsp. x układu kartezjańskiego')
parser.add_argument('-y',type = float, help = 'wsp. y układu kartezjańskiego')
parser.add_argument('-z',type = float, help = 'wsp. z układu kartezjańskiego')
parser.add_argument('-f',type = float)
parser.add_argument('-l',type = float)
parser.add_argument('-l0',type = float)
parser.add_argument('-he',type = float)
parser.add_argument('-jedn',type = str)
parser.add_argument('-x0',type = float, help = 'wsp. x0 srodka układu kartezjańskiego ')
parser.add_argument('-y0',type = float, help = 'wsp. y0 srodka układu kartezjańskiego')
parser.add_argument('-z0',type = float, help = 'wsp. z0 srodka kartezjańskiego')
parser.add_argument('-xr',type = float, help = 'wsp. x referencyjna układu układu kartezjańskiego ')
parser.add_argument('-yr',type = float, help = 'wsp. y referencyjna układu układu kartezjańskiego')
parser.add_argument('-zr',type = float, help = 'wsp. z referencyjna układu kartezjańskiego')
args = parser.parse_args()

if args.func == 'xyz2flh':
    geo = Transformacje(model = args.m)
    print(geo.xyz2flh([args.x,args.y,args.z],args.jedn))
elif args.func == 'flh2XYZ':
    geo = Transformacje(model = args.m)
    print(geo.flh2XYZ([args.f,args.l,args.he],args.jedn))
elif args.func == 'xyz2neu':
    geo = Transformacje(model = args.m)
    print(geo.xyz2neu([args.x0,args.y0,args.z0],[args.xr,args.yr,args.zr],args.jedn))
elif args.func == 'XgkYgk':
    geo = Transformacje(model = args.m)
    print(geo.XgkYgk([args.f,args.l,args.he],args.l0,args.jedn))
elif args.func == 'XY2000':
    geo = Transformacje(model = args.m)
    print(geo.XY2000([args.f,args.l,args.he],args.l0,args.jedn))
elif args.func == 'XY1992':
    geo = Transformacje(model = args.m)
    print(geo.XY1992([args.f,args.l,args.he],args.jedn))



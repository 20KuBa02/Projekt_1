from argparse import ArgumentParser
from Projekt1 import Transformacje


parser = ArgumentParser()
parser.add_argument('-m' , '--m', type = str , help = 'Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke')
parser.add_argument('-xyz', '--xyz', type = str , help = 'Podaj nazwę pliku wynikowego dla funkcji wraz z rozszerzeniem')
parser.add_argument('-x','--x',type = float)
parser.add_argument('-y','--y',type = float)
parser.add_argument('-z','--z',type = float)
parser.add_argument('-jedn', '--jedn',type = str)
args = parser.parse_args()

geo = Transformacje(model = args.m)
flh = geo.xyz2flh([args.x,args.y,args.z],args.jedn)

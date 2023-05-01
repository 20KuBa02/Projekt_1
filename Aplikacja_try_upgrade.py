from argparse import ArgumentParser
from Projekt1 import Transformacje



parser = ArgumentParser(description='My program')

subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')


parser_func1 = subparsers.add_parser('func1', help='function 1 help')
parser_func1.add_argument('-m' , '--m', type = str , help = 'Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke')
parser_func1.add_argument('-x','--x',type = float)
parser_func1.add_argument('-y','--y',type = float)
parser_func1.add_argument('-z','--z',type = float)
parser_func1.add_argument('-jedn', '--jedn',type = str)


parser_func2 = subparsers.add_parser('func2', help='function 2 help')
parser_func2.add_argument('-m' , '--m', type = str , help = 'Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke')
parser_func2.add_argument('-f','--f',type = float)
parser_func2.add_argument('-l','--l',type = float)
parser_func2.add_argument('-h','--h',type = float)
parser_func2.add_argument('-jedn', '--jedn',type = str)


args = parser.parse_args()

if args.subcommand == 'func1':
    geo = Transformacje(model = args.m)
    flh = geo.xyz2flh([args.x,args.y,args.z],args.jedn)
    print(flh)
elif args.subcommand == 'func2':
    geo = Transformacje(model = args.m)
    xyz = geo.flh2xyz([args.f,args.l,args.h],args.jedn)
    print(xyz)   
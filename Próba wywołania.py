from Projekt1 import Transformacje
import czytanie_txt
from czytanie_txt import*
geo = Transformacje(model = "wgs84")
xyz0 = [3664940.515, 1409153.595, 5009571.169]
xyz = [3664940.500,1409153.590,5009571.170]
geo = Transformacje(model = "wgs84")

neu = geo.xyz2neu(xyz0, xyz)
print(neu)

flh = geo.xyz2flh(xyz,'dec')
print(flh)

XYZ = geo.flh2XYZ(flh,'dec')
print(XYZ)

xy92 = geo.XY1992(flh)
print(xy92)

xy00 = geo.XY2000(flh,21)
print(xy00)

czytanie_txt([4353.06678,5345,355],19, 'wgs84', 'wsp_inp.txt', 'XY1992' ,'gra' ,'sprawdzenie_funkcji'  )
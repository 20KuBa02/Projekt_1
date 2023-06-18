import math as m
from math import sin, cos, sqrt, atan, atan2, degrees, radians
import numpy as np
import argparse
class Transformacje:
    def __init__(self, model: str = "wgs84"):
        """
        Parametry elipsoid:
           
            a - duża półoś elipsoidy - promień równikowy
            b - mała półoś elipsoidy - promień południkowy
            flat - spłaszczenie
            ecc2 - mimośród^2
        + WGS84: https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        + Inne powierzchnie odniesienia: http://uriasz.am.szczecin.pl/naw_bezp/elipsoida.html
        """
        if model == "wgs84":
            self.a = 6378137.0 
            self.b = 6356752.31424518 
        elif model == "wgs72":
            self.a = 6378135.000
            self.b = 6356750.520
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "Krasowski":
            self.a = 6378245.000
            self.b = 6356863.019
        elif model == "Międzynarodowa":
            self.a = 6378160.000
            self.b = 6356774.719
        elif model == "Bessel":
            self.a = 6377397.155
            self.b = 6356078.963
        elif model == "Clarke":
            self.a = 6378249.145
            self.b = 6356514.870
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.e = sqrt(2 * self.flat - self.flat ** 2) 
        self.e2 = (2 * self.flat - self.flat ** 2) 
        
        
    def Np(self,flh, jedn = "dec"):
        """
        Największy promień krzywizny na daną pozycję uzytkownika
        
        Parameters
        ----------
        phi : float
            [stopnie dziesiętne] - szerokość geodezyjna
       
        Returns
        -------
        N : float
            [metry] - największy promień krzywizny
        """
        
        phi = float(flh[0])
        if jedn == "rad":
            pass
        elif jedn == "dec":
             phi = np.degrees(phi)
        elif jedn == "gra":
            flh = phi*m.pi/200
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
            
        N = self.a / np.sqrt(1 - self.e2 * np.sin(flh[0])**2)
        return(N)

    def xyz2flh(self, xyz, jedn = 'dec'):
        """
        Algorytm Hirvonena – algorytm służący do transformacji współrzędnych ortokartezjańskich (prostokątnych) x, y, z na współrzędne geodezyjne B, L, h.
        Jest to proces iteracyjny. W wyniku 3-4-krotnego powtarzania procedury można przeliczyć współrzędne na poziomie dokładności 1 cm.
        
        Parameters
        ----------
        xyz : [list] [metry]
            [metry] - współrzędne w układzie orto-kartezjańskim
        jedn : STR, optional
           Jednostka podawanych wartosci. The default is 'dec'.
           ["rad" - radiany, "gra" - grady, "dec" - stopnie]
        
        Raises
        ------
        NotImplementedError
        Jezeli podana jednostka jest poza zbiorem.
       
        Returns
        -------
        flh = [f,l,h]
        f : float [wybrana jednostka z listy]
            - szerokość geodezyjna
        l : float [wybrana jednostka z listy]
            - długość geodezyjna
        h : float [wybrana jednostka z listy]
            [metry] - wysokość geometryczna(elipsoidalna)
        """
       
        r = np.sqrt(xyz[0]**2 + xyz[1]**2)
        phi_prv = m.atan(xyz[2] / (r * (1 - self.e2)))
        phi = 0
        while abs(phi_prv - phi) > 0.000001/206265:    
            phi_prv = phi
            N = self.a / np.sqrt(1 - self.e2 * np.sin(phi_prv)**2)
            h = r / np.cos(phi_prv) - N
            phi = m.atan((xyz[2]/r) * (((1 - self.e2 * N/(N + h))**(-1))))
        l = m.atan(xyz[1]/xyz[0])
        N = self.a / np.sqrt(1 - self.e2 * (np.sin(phi))**2);
        h = r / np.cos(phi) - N
        flh= [phi, l,h]
        
        if jedn == 'rad':
            pass
        elif jedn == 'dec':
            flh = [float(np.degrees(flh[0])),float(np.degrees(flh[1])),float(flh[2])]
        elif jedn == 'gra':
            flh = [float(flh[0]*200/m.pi), float(flh[1]*200/m.pi), float(flh[2])]
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
            
        return (flh)
   
    def flh2XYZ(self, flh, jedn = 'dec'):
        """
        Funkcja transformujaca współrzędne geodezyjne długość szerokość i wysokośc elipsoidalna 
        na współrzędne ortokartezjańskie
        
        Parameters
        ----------
        flh - wspolrzedne geodezyjne [wybrana jednostka z listy]
        jedn : [str] , optional
             Jednostka podawanych wartosci. The default is 'dec'.
             ["rad" - radiany, "gra" - grady, "dec" - stopnie]
        
        Raises
        ------
        NotImplementedError
        Jezeli podana jednostka jest poza zbiorem.
       
        Returns
        -------
        X,Y,Z : float
            [metry] - współrzędne w układzie orto-kartezjańskim
        """
        
        if jedn == 'rad':
            pass
        elif jedn == 'dec':
            flh = [float(np.radians(flh[0])),float(np.radians(flh[1])),float(flh[2])]
        elif jedn == 'gra':
            flh = [float(flh[0]*m.pi/200), float(flh[1]*m.pi/200), float(flh[2])]
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
            
        N = self.Np(flh, 'rad')
        X = (N + flh[2])*np.cos(flh[0])*np.cos(flh[1])
        Y = (N + flh[2])*np.cos(flh[0])*np.sin(flh[1])
        Z = (N*(1-self.e2) + flh[2])*np.sin(flh[0])
        
        xyz = [round(X,3),round(Y,3),round(Z,3)]
        
        return xyz
    
    def xyz2neu(self, xyz0, xyz):
        """
        Sferyczny układ współrzędnych – układ współrzędnych w trójwymiarowej przestrzeni euklidesowej.
        
        Parameters
        ----------
        xyz0 : [list]
            [metry] - współrzędna punktu w układzie orto-kartezjańskim, która definiuje srodek układu
        xyz : [list]
            [metry] - współrzędne referencyjne w układzie orto-kartezjańskim
        
        
        Raises
        ------
        NotImplementedError
        Jezeli podana jednostka jest poza zbiorem.
       
        Returns
        -------
        neu : [list]
            [metry] - współrzędne w układzie sferycznym
        """
       
        flh = Transformacje.xyz2flh(self,xyz0)
        
        R = np.array([[-np.sin(radians(flh[1])) , -np.sin(radians(flh[0])) * np.cos(radians(flh[1])) , np.cos(radians(flh[0])) * np.cos(radians(flh[1]))],
             [np.cos(radians(flh[0]))  , -np.sin(radians(flh[0])) * np.sin(radians(flh[1])) , np.cos(radians(flh[0])) * np.sin(radians(flh[1]))],
             [0 , np.cos(flh[0]) , np.sin(flh[0])]])
        XYZT = np.array([[xyz[0] - xyz0[0]],
                         [xyz[1] - xyz0[1]],
                         [xyz[2] - xyz0[2]]])
        ENU = R.transpose() @ XYZT
        neu = [round(ENU[0][0],3), round(ENU[1][0],3), round(ENU[2][0],3)]
        return(neu)
    
    def sigma(self, flh, jedn = "dec"):
        '''
        Algorytm liczący długosć łuku południka.

        Parameters
        ----------
        flh : LIST [wybrana jednostka z listy]
            wspolrzedne geodezyjne phi, lam, h [metry]
        jedn : STR, optional
            Jednostka wspolrzednych geodezyjnych. Domyslna jest "dec".
            ["rad" - radiany, "gra" - grady, "dec" - stopnie]

        Raises
        ------
        NotImplementedError
            Jezeli podana jednostka jest poza zbiorem.

        Returns
        -------
        sigma : FLOAT
            Dlugosc luku poludnika [metry].

        '''
        
        if jedn == 'rad':
            pass
        elif jedn == 'dec':
            flh = [float(np.radians(flh[0])),float(np.radians(flh[1])),float(flh[2])]
        elif jedn == 'gra':
            flh = [float(flh[0]*m.pi/200), float(flh[1]*m.pi/200), float(flh[2])]
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
        
        phi = float(flh[0])
        
        if jedn == "rad":
            pass
        elif jedn == "dec":
            phi = np.radians(phi)
        elif jedn == "gra":
            flh = phi*m.pi/200
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
        
        A0 = 1-(self.e2/4)-(3/64)*(self.e2**2)-(5/256)*(self.e2**3);
        A2 = (3/8)*(self.e2 + (self.e2**2)/4 + (15/128)*(self.e2**3));
        A4 = (15/256)*(self.e2**2 + 3/4*(self.e2**3));
        A6 = (35/3072)*self.e2**3;
        sigma = self.a*(A0*phi - A2*np.sin(2*phi) + A4*np.sin(4*phi) - A6*np.sin(6*phi));
        return(sigma)
    
    def XgkYgk(self, flh, l0, jedn = 'dec'):
        """
        Odwzorowanie Gaussa-Krügera – odwzorowanie kartograficzne pasów południkowych na pobocznicę walca stycznego
        do południka środkowego (osiowego) każdego odwzorowywanego pasa.
        Jest to wiernokątne, walcowe, poprzeczne odwzorowanie elipsoidy, w którym każdy pas odwzorowuje się oddzielnie.
        
        Parameters
        ----------
        flh : LIST 
            wspolrzedne geodezyjne phi, lam [wybrana jednostka z listy], h [metry]
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
        xygk : LIST 
            Wspolrzedne odwzorowania Gaussa-Krugera [metry]
        """
        
        if jedn == 'rad':
            pass
        elif jedn == 'dec':
            flh = [float(np.radians(flh[0])),float(np.radians(flh[1])),float(flh[2])]
        elif jedn == 'gra':
            flh = [float(flh[0]*m.pi/200), float(flh[1]*m.pi/200), float(flh[2])]
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
    
        l0 = np.radians(l0)
       
        b2 = (self.a**2)*(1-self.e2);
        ep2 = (self.a**2-b2)/b2;
        t = np.tan(flh[0]);
        n2 = ep2*(np.cos(flh[0])**2);
        N = self.Np(flh, 'rad');
        si = self.sigma(flh,'rad');
        dL = flh[1] - l0;
       
        Xgk = si + (dL**2/2)*N*np.sin(flh[0])*np.cos(flh[0])*(1 + (dL**2/12)*np.cos(flh[0])**2*(5 - t**2 + 9*n2 + 4*n2**2) + (dL**4/360)*np.cos(flh[0])**4*(61 - 58*t**2 + t**4 + 14*n2 - 58*n2*t**2));
        Ygk = dL*N*np.cos(flh[0])*(1 + (dL**2/6)*np.cos(flh[0])**2*(1 - t**2 + n2) + (dL**4/120)*np.cos(flh[0])**4*(5 - 18*t**2 + t**4 + 14*n2 - 58*n2*t**2));
       
        xygk = [Xgk,Ygk]

        return xygk

    def XY2000(self, flh, l0, jedn = 'dec'):
        """
        Układ współrzędnych 2000 – układ współrzędnych płaskich prostokątnych zwany układem „2000”, 
        powstały w wyniku zastosowania odwzorowania Gaussa-Krügera dla elipsoidy GRS 80 w czterech trzystopniowych strefach 
        o południkach osiowych 15°E, 18°E, 21°E i 24°E, oznaczone odpowiednio numerami – 5, 6, 7 i 8.
       
        Parameters
        ----------
        flh : LIST
            wspolrzedne geodezyjne phi, lam [wybrana jednostka z listy], h [metry]
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
        
        if jedn == 'rad':
            flh = [float(np.degrees(flh[0])),float(np.degrees(flh[1])),float(flh[2])]
        elif jedn == 'dec':
            pass
        elif jedn == 'gra':
            flh = [float(flh[0]*9/10), float(flh[1]*9/10), float(flh[2])]
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
       
        xygk = self.XgkYgk(flh, l0, 'dec')
        X2000 = xygk[0] * 0.999923 
        Y2000 = xygk[1] * 0.999923 + l0/3 * 1000000 + 500000
        xy2000 = [X2000,Y2000]
        return(xy2000)

    def XY1992(self, flh, jedn = 'dec'):
        """
        Układ współrzędnych 1992 – układ współrzędnych płaskich prostokątnych oparty na odwzorowaniu Gaussa-Krügera dla elipsoidy GRS80 w jednej dziesięciostopniowej strefie.
        Początkiem układu jest punkt przecięcia południka 19°E z obrazem równika.
        
        Parameters
        ----------
        flh : LIST
            wspolrzedne geodezyjne phi, lam [wybrana jednostka z listy], h [metry]
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
        xy1992 : LIST
            Wspolrzedne w układzie PL-1992 [metry]
        """
        if jedn == 'rad':
            flh = [float(np.degrees(flh[0])),float(np.degrees(flh[1])),float(flh[2])]
        elif jedn == 'dec':
            pass
        elif jedn == 'gra':
            flh = [float(flh[0]*9/10), float(flh[1]*9/10), float(flh[2])]
        else:
            raise NotImplementedError(f"{jedn} nie jest w zbiorze okreslen")
       
        xygk = self.XgkYgk(flh, 19, 'dec')
        X1992 = xygk[0] * 0.9993 - 5300000
        Y1992 = xygk[1] * 0.9993 + 500000
        xy1992 = [X1992,Y1992]
        return(xy1992)
       
    def do_listy(x,y,z):
        lista = [x,y,z]
        return lista        
            

        
geo = Transformacje(model = "wgs84")
# dane XYZ geocentryczne
X = 3664940.500; Y = 1409153.590; Z = 5009571.170
xyz = [X,Y,Z]
flh = geo.xyz2flh(xyz,'dec')
#print(flh)
xyz0 = [X+100,Y+1000,Z+234]

neu = geo.xyz2neu(xyz0, xyz)
#print(neu)
l0 = 21
xy00 = geo.XY2000(flh, l0, jedn = 'dec')
#print(xy00)

xy92 = geo.XY1992(flh,jedn = 'dec')
#print(xy92)
print()
 
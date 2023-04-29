from math import sin, cos, sqrt, atan, atan2, degrees, radians
import numpy as np

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
        
        
    def Np(self,fi):
        """
        Największy promień krzywizny na pozycję uzytkownika
        
        Parameters
        ----------
        fi : float
            [stopnie dziesiętne] - szerokość geodezyjna
        Returns
        -------
        N : float
            [metry] - największy promień krzywizny
        """
        N = self.a / np.sqrt(1 - self.e2 * np.sin(fi)**2)
        return(N)

    def xyz2flh(self,X,Y,Z):
        """
        Algorytm Hirvonena – algorytm służący do transformacji współrzędnych ortokartezjańskich (prostokątnych) x, y, z na współrzędne geodezyjne B, L, h.
        Jest to proces iteracyjny. W wyniku 3-4-krotnego powtarzania procedury można przeliczyć współrzędne na poziomie dokładności 1 cm.
        
        Parameters
        ----------
        X,Y,Z : float
            [metry] - współrzędne w układzie orto-kartezjańskim
        Returns
        -------
        f : float
            [stopnie dziesiętne] - szerokość geodezyjna
        l : float
            [stopnie dziesiętne] - długość geodezyjna
        h : float
            [metry] - wysokość geometryczna(elipsoidalna)
        """
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/p * (1-self.e2))
        while True:
            N = Transformacje.Np(self,f)
            h= ( p / np.cos(f)) - N
            fp = f
            f=np.arctan(Z/(p*(1-self.e2 * N / (N+h))))
            if abs(fp-f)<(0.000001/206265):
                break
        l=np.arctan2(Y,X)
        return(f,l,h) 
   
    def flh2XYZ(self,fi,la,h):
        """
        Parameters
        ----------
        f : float
            [stopnie dziesiętne] - szerokość geodezyjna
        l : float
            [stopnie dziesiętne] - długość geodezyjna
        h : float
            [metry] - wysokość geometryczna(elipsoidalna)
        Returns
        -------
        X,Y,Z : float
            [metry] - współrzędne w układzie orto-kartezjańskim
        """
        N = Transformacje.Np(self,fi)
        X = (N + h) * np.cos(fi) * np.cos(la)
        Y = (N + h) * np.cos(fi) * np.sin(la)
        Z =(N*(1-self.e2)+h) * np.sin(fi) 
        return(X,Y,Z)
    
    def xyz2neu(self,X0,Y0,Z0,X,Y,Z):
        """
        Sferyczny układ współrzędnych – układ współrzędnych w trójwymiarowej przestrzeni euklidesowej.
        Parameters
        ----------
        X0,Y0,Z0 : float
            [metry] - współrzędne punktu w układzie orto-kartezjańskim
        X,Y,Z : float
            [metry] - współrzędne referencyjne w układzie orto-kartezjańskim
        Returns
        -------
        N,E,U : float
            [metry] - współrzędne w układzie sferycznym
        """
        fi,la,ha = Transformacje.xyz2flh(self, X0, Y0, Z0)
        R = np.array([[-np.sin(radians(la)) , -np.sin(radians(fi)) * np.cos(radians(la)) , np.cos(radians(fi)) * np.cos(radians(la))],
             [np.cos(radians(fi))  , -np.sin(radians(fi)) * np.sin(radians(la)) , np.cos(radians(fi)) * np.sin(radians(la))],
             [0 , np.cos(fi) , np.sin(fi)]])
        XYZT = np.array([[X - X0],
                         [Y - Y0],
                         [Z - Z0]])
        ENU = R.transpose() @ XYZT
        return (ENU[0][0],ENU[1][0],ENU[2][0])
    
    def sigma(self,f):
        f = radians()
        A0 = 1 - (self.e2 / 4) - (3 * self.e2**2 / 64) - (5 * self.e2**3 / 256)
        A2 = (3/8) * (self.e2 + self.e2**2 / 4 + 15 * self.e2**3 / 128)
        A4 = (15/256) * (self.e2**2 + (3 * self.e2**3 / 4))
        A6 = 35 * self.e2**3 / 3072
        sigma = self.a * (A0 * f - A2 * np.sin(2 * f) + A4 * np.sin(4 * f) - A6 * np.sin(6 * f))
        return(sigma)
    
    def XgkYgk(self,f,l,l0):
        """
        Odwzorowanie Gaussa-Krügera – odwzorowanie kartograficzne pasów południkowych na pobocznicę walca stycznego
        do południka środkowego (osiowego) każdego odwzorowywanego pasa.
        Jest to wiernokątne, walcowe, poprzeczne odwzorowanie elipsoidy, w którym każdy pas odwzorowuje się oddzielnie.
        Parameters
        ----------
        f : float
            [stopnie dziesiętne] - szerokość geodezyjna
        l : float
            [stopnie dziesiętne] - długość geodezyjna
        l0 : float
            [stopnie dziesiętne] - południk osiowy
        Returns
        -------
        Xgk : float
            [metry] - Współrzędna x w układzie Gaussa-Krugera
        Ygk : float
            [metry] - Współrzędna y w układzie Gaussa-Krugera
        """
        f = radians(f)
        l = radians(l)
        l0 = radians(l0)
        b2 = (self.a**2) * (1 - self.e2) 
        ep2 = (self.a**2 - b2)
        dl = l - l0
        t = np.tan(f)
        n2 = ep2 * (np.cos(f))**2 
        N = Transformacje.Np(self,f)
        sigma0 = Transformacje.sigma(self,f)
        Xgk = sigma0 + (dl**2 / 2) * N * np.sin(f) * np.cos(f) * (1 + (dl**2 / 12) * (np.cos(f))**2 * (5 - t**2 + 9 * n2 + 4 * n2**2) + (dl**4 / 360) * (np.cos(f))**4 * (61 - 58 * t**2 + t**4 + 270 * n2 - 330 * n2 * t**2))
        Ygk = dl * N * np.cos(f) * (1 + (dl**2 / 6) * (np.cos(f))**2 * (1 - t**2 + n2) + (dl**4 / 120) * (np.cos(f))**4 * (5 - 18 * t**2 + t**4 + 14 * n2 - 58 * n2 * t**2))
        return(Xgk,Ygk)

    def XY2000(self,fi,la,l0):
        Xgk,Ygk = Transformacje.XgkYgk(self, fi, la, l0)
        X2000 = Xgk * 0.999923 
        Y2000 = Ygk * 0.999923 + l0/3 * 1000000 + 500000
        return(X2000,Y2000)

    def XY1992(self,fi,la):
        Xgk,Ygk = Transformacje.XgkYgk(self, fi, la, 19)
        X1992 = Xgk * 0.9993 - 5300000
        Y1992 = Ygk * 0.9993 + 500000
        return(X1992,Y1992)
       
        
geo = Transformacje(model = "wgs84")
# dane XYZ geocentryczne
X = 3664940.500; Y = 1409153.590; Z = 5009571.170
phi, lam, h = geo.xyz2flh(X, Y, Z)
print(phi, lam, h)
E,N,U = geo.xyz2neu(X,Y,Z,(X + 1000),(Y + 2000),(Z + 3000))
print(E,N,U)


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
        + Inne powierzchnie odniesienia: https://en.wikibooks.org/wiki/PROJ.4#Spheroid
        + Parametry planet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
        """
        if model == "wgs84":
            self.a = 6378137.0 
            self.b = 6356752.31424518 
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "mars":
            self.a = 3396900.0
            self.b = 3376097.80585952
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.e = sqrt(2 * self.flat - self.flat ** 2) 
        self.e2 = (2 * self.flat - self.flat ** 2) 
        
        
    def Np(self,fi):
        N = self.a / np.sqrt(1 - self.e2 * np.sin(fi)**2)
        return(N)

    def xyz2flh(self,X,Y,Z):
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
        N = Transformacje.Np(self,fi)
        X = (N + h) * np.cos(fi) * np.cos(la)
        Y = (N + h) * np.cos(fi) * np.sin(la)
        Z =(N*(1-self.e2)+h) * np.sin(fi) 
        return(X,Y,Z)
    
    def xyz2neu(self,X0,Y0,Z0,X,Y,Z):
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
       f = radians(f)
       l = radians(l)
       l0 = radians(l0)
       b2 = (self.a**2) * (1 - self.e2) 
       ep2 = (self.a**2 - b2)
       dl = l - l0
       t = np.tan(f)
       n2 = ep2 * (np.cos(f))**2 
       N = Transformacje.Np(self,f)
       sigma0 = sigma(self,f)
       Xgk = sigma0 + (dl**2 / 2) * N * np.sin(f) * np.cos(f) * (1 + (dl**2 / 12) * (np.cos(f))**2 * (5 - t**2 + 9 * n2 + 4 * n2**2) + (dl**4 / 360) * (np.cos(f))**4 * (61 - 58 * t**2 + t**4 + 270 * n2 - 330 * n2 * t**2))
       Ygk = dl * N * np.cos(f) * (1 + (dl**2 / 6) * (np.cos(f))**2 * (1 - t**2 + n2) + (dl**4 / 120) * (np.cos(f))**4 * (5 - 18 * t**2 + t**4 + 14 * n2 - 58 * n2 * t**2))
       return(Xgk,Ygk)

geo = Transformacje(model = "wgs84")
# dane XYZ geocentryczne
X = 3664940.500; Y = 1409153.590; Z = 5009571.170
phi, lam, h = geo.xyz2flh(X, Y, Z)
print(phi, lam, h)
E,N,U = geo.xyz2neu(X,Y,Z,(X + 1000),(Y + 2000),(Z + 3000))
print(E,N,U)


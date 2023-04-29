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

geo = Transformacje(model = "wgs84")
# dane XYZ geocentryczne
X = 3664940.500; Y = 1409153.590; Z = 5009571.170
phi, lam, h = geo.xyz2flh(X, Y, Z)
print(phi, lam, h)
E,N,U = geo.xyz2neu(X,Y,Z,(X + 1000),(Y + 2000),(Z + 3000))
print(E,N,U)


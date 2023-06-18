# Program transforamcje
## Nasz program służący do transformacji współrzędnych pomiędzy układami składa się z trzech plików Python.
- Plik "Projekt1.py" zawiera parametry elipsoidy oraz dużą liczbę funkcji do transformacji między układami. 
- Plik "czytanie_txt.py" zawiera funkcję, która pobiera dane z pliku tekstowego (dane muszą być w odpowiednim formacie) i korzystając z funkcji z pliku "Projekt1.py" przekształca je do odpowiedniego układu. Współrzędne są zwracane w postaci pliku tekstowego. 
- Plik "Aplikacja.py" został stworzony, aby umożliwić korzystanie z wszystkich funkcji zawartych w pliku "Projekt1.py" oraz "czytanie_txt" poprzez okno konsoli (cmd)

## Aby wszystkie programy zawarte w tym repozytorium mogły działać bez zarzutów trzeba mieć na swoim komputerze zainstalowane następujące aplikacje,programy i biblioteki:
- Python - czyli język programowania wysokiego poziomu , w wersji nie młodszej niż 3.10
- Spyder - wieloplatformowe zintegrowane środowisko programistyczne
- biblioteka NumPy – otwartoźródłowa biblioteka programistyczna dla języka Python, dodająca obsługę dużych, wielowymiarowych tabel i macierzy
- biblioteka math - otwartoźródłowa biblioteka programistyczna dla języka Python , obługuje większość zagadnień matematycznych
- biblioteka argparse

# Funkcje zawarte pliku Projekt1.py
- __init__(self, model: str = "wgs84"): Inicjalizuje obiekt Transformacje przyjmując nazwę modelu elipsoidy jako argument. Dostępne modele elipsoidy to "wgs84", "wgs72", "grs80", "Krasowski", "Międzynarodowa", "Bessel" i "Clarke".

- Np(self, flh, jedn = "dec"): Oblicza największy promień krzywizny na danej pozycji użytkownika.

- xyz2flh(self, xyz, jedn = 'dec'): Przekształca współrzędne ortokartezjańskie (x, y, z) na współrzędne geodezyjne (B, L, h).

- flh2XYZ(self, flh, jedn = 'dec'): Przekształca współrzędne geodezyjne (B, L, h) na współrzędne ortokartezjańskie (x, y, z).

- xyz2neu(self, xyz0, xyz): Przekształca współrzędne ortokartezjańskie (x, y, z) na współrzędne sferyczne (N, E, U) względem punktu referencyjnego.

- sigma(self, flh, jedn = "dec"): Oblicza długość łuku południka.

- XgkYgk(self, flh, l0, jedn = 'dec'): Przekształca współrzędne geodezyjne (B, L, h) na współrzędne odwzorowania Gaussa-Krügera (Xgk, Ygk).

# Charakterystyka poszczególnych funkcji zawartych w pliku Projekt1.py
## __init__

 Parametry elipsoid:
 - a - duża półoś elipsoidy - promień równikowy
 - b - mała półoś elipsoidy - promień południkowy
 - flat - spłaszczenie
 - ecc2 - mimośród^2
       
Dostępne modele elipsoid:

 - wgs84:
 a = 6378137.0 
 b = 6356752.31424518 
 - wgs72:
 a = 6378135.000
 b = 6356750.520
 - grs80:
 a = 6378137.0
 b = 6356752.31414036
 - Krassowski: UWAGA(Biorąc tą elipsoidę możemy uzyskać błędne wyniki)
 a = 6378245.000
 b = 6356863.019
 - Międzynarodowa:
 a = 6378160.000
 b = 6356774.719
 - Bessel:
 a = 6377397.155
 b = 6356078.963
 - Clarke:
 a = 6378249.145
 b = 6356514.870

Żródło informacji na temat elipsoid:
 + WGS84: https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
 + Inne powierzchnie odniesienia: http://uriasz.am.szczecin.pl/naw_bezp/elipsoida.html

        
## Np 
### Największy promień krzywizny na daną pozycję uzytkownika
     
#### Parameters
phi : float[stopnie dziesiętne] - szerokość geodezyjna
       
#### Returns
N : float [metry] - największy promień krzywizny
                          
## xyz2flh 
### Algorytm Hirvonena – algorytm służący do transformacji współrzędnych ortokartezjańskich (prostokątnych) x, y, z na współrzędne geodezyjne B, L, h.Jest to proces iteracyjny. W wyniku 3-4-krotnego powtarzania procedury można przeliczyć współrzędne na poziomie dokładności 1 cm.
        
#### Parameters
xyz =[x,y,z]: [list]
- x [metry] - współrzędna "x" w układzie orto-kartezjańskim
- y [metry] - współrzędna "y" w układzie orto-kartezjańskim
- x [metry] - współrzędna "z" w układzie orto-kartezjańskim
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
        f : float
            - szerokość geodezyjna
        l : float
            - długość geodezyjna
        h : float
            [metry] - wysokość geometryczna(elipsoidalna)
  
           
 flh2XYZ :
  
        Funkcja transformujaca współrzędne geodezyjne długość szerokość i wysokośc elipsoidalna 
        na współrzędne ortokartezjańskie
        
        Parameters
        ----------
        flh - wspolrzedne geodezyjne
        jedn : [str] , optional
             Jednostka podawanych wartosci. The default is 'dec'.
             ["rad" - radiany, "gra" - grady, "dec" - stopnie]
        
        Raises
        ------
        NotImplementedError
        Jezeli podana jednostka jest poza zbiorem.
       
        Returns
        -------
        [X,Y,Z] : list
            [metry] - współrzędne w układzie orto-kartezjańskim


Sigma:
    
        Algorytm liczący długosć łuku południka.

        Parameters
        ----------
        flh : LIST
            wspolrzedne geodezyjne phi, lam, h [metry]
        jedn : STR, optional
            Jednostka wspolrzednych geodezyjnych. Domyslna jest "dec".
XgkYgk
       
        Odwzorowanie Gaussa-Krügera – odwzorowanie kartograficzne pasów południkowych na pobocznicę walca stycznego
        do południka środkowego (osiowego) każdego odwzorowywanego pasa.
        Jest to wiernokątne, walcowe, poprzeczne odwzorowanie elipsoidy, w którym każdy pas odwzorowuje się oddzielnie.
        
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
        xygk : LIST
            Wspolrzedne odwzorowania Gaussa-Krugera [metry]
   
PL2000         
         Układ współrzędnych 2000 – układ współrzędnych płaskich prostokątnych zwany układem „2000”, 
        powstały w wyniku zastosowania odwzorowania Gaussa-Krügera dla elipsoidy GRS 80 w czterech trzystopniowych strefach 
        o południkach osiowych 15°E, 18°E, 21°E i 24°E, oznaczone odpowiednio numerami – 5, 6, 7 i 8.
       
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
       
Pl1992       
      Układ współrzędnych 1992 – układ współrzędnych płaskich prostokątnych oparty na odwzorowaniu Gaussa-Krügera dla elipsoidy GRS80 w jednej dziesięciostopniowej strefie.
        Początkiem układu jest punkt przecięcia południka 19°E z obrazem równika.
        
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
        xy1992 : LIST
            Wspolrzedne w układzie PL-1992 [metry]
       
  
  Informacje o funkcjach zawartych w pliku czytanie_txt.py
  
  
  Program przyjmuje plik txt tylko w takim formacie:
    
    3664940.500 1409153.590 5009571.170
    3664940.510 1409153.580 5009571.167
    3664940.520 1409153.570 5009571.167
    3664940.530 1409153.560 5009571.168
    3664940.520 1409153.590 5009571.170
    3664940.514 1409153.584 5009571.166    
    
    A następnie przelicza do układu który poda użytkownik.Niedoskonałoscią tego programu jest
    to że pobiera argumenty dla wszystkich funkcji.Lecz to nie jest aż tak wileki problem, wystarczy 
    wpisać losowe wartosci, nie będą one miały wplywu na wynik końcowy.
    
    Parameters
    ----------
    
    xyz0 : [list]
        [metry] - współrzędne punktu w układzie orto-kartezjańskim
    l0 : int
        [stopnie dziesiętne] - południk osiowy
    jedn : STR, optional
        Jednostka wspolrzednych geodezyjnych. Domyslna jest "dec".
        ["rad" - radiany, "gra" - grady, "dec" - stopnie]
    model : 'nazwa modelu'
        Model elipsoidy.
    plik : 'nazwa pliku'
        Nazwa pliku o rozszerzeniu txt który wczytujemy.
    funkcja = 'nazwa funkcji',
        Nazwa funkcji według której chcemy przeliczyć współrzędne między układami.
    Returns
    -------
    plik o rozszerzeniu txt z przeliczonymi współrzędnymi
    """
       

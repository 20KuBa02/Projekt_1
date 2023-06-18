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

        
## Np([f,l,h],jedn) 
### Największy promień krzywizny na daną pozycję uzytkownika
     
#### Parameters
flh = [f,l,h]: [list]
- f[float][jedn] - szerokość geodezyjna
- l[float][jedn] - długość geodezyjna
- h[float][metry] - wysokość geometryczna(elipsoidalna)
Funkcja pobiera tylko szerokość geodezyjną
jedn = [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie]      
#### Raises
NotImplementedError
- Jezeli podana jednostka jest poza zbiorem.
#### Returns
N : float [metry] - największy promień krzywizny
                          
## xyz2flh([x,y,z],jedn) 
### Algorytm Hirvonena – algorytm służący do transformacji współrzędnych ortokartezjańskich (prostokątnych) x, y, z na współrzędne geodezyjne B, L, h.Jest to proces iteracyjny. W wyniku 3-4-krotnego powtarzania procedury można przeliczyć współrzędne na poziomie dokładności 1 cm.
        
#### Parameters
xyz = [x,y,z]: [list]
- x [float][metry] - współrzędna "x" w układzie orto-kartezjańskim
- y [float][metry] - współrzędna "y" w układzie orto-kartezjańskim
- z [float][metry] - współrzędna "z" w układzie orto-kartezjańskim
jedn = [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie]
#### Raises
NotImplementedError
- Jezeli podana jednostka jest poza zbiorem.
#### Returns
flh = [f,l,h]: [list]
- f[float][jedn] - szerokość geodezyjna
- l[float][jedn] - długość geodezyjna
- h[float][metry] - wysokość geometryczna(elipsoidalna)
  
## flh2XYZ([f,l,h],jedn)
### Funkcja transformujaca współrzędne geodezyjne długość szerokość i wysokośc elipsoidalna na współrzędne ortokartezjańskie
        
#### Parameters
flh = [f,l,h]: [list]
- f[float][jedn] - szerokość geodezyjna
- l[float][jedn] - długość geodezyjna
- h[float][metry] - wysokość geometryczna(elipsoidalna)    
jedn = [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie]   
#### Raises
NotImplementedError
- Jezeli podana jednostka jest poza zbiorem.
#### Returns
xyz = [x,y,z]: [list]
- x [float][metry] - współrzędna "x" w układzie orto-kartezjańskim
- y [float][metry] - współrzędna "y" w układzie orto-kartezjańskim
- z [float][metry] - współrzędna "z" w układzie orto-kartezjańskim

##  xyz2neu([x0,y0,z0], [x,y,z])
### Sferyczny układ współrzędnych – układ współrzędnych w trójwymiarowej przestrzeni euklidesowej.
     
#### Parameters
xyz0 = [x0,y0,z0]: [list]
- x0 [float][metry] - współrzędna "x" w układzie orto-kartezjańskim, która definiuje środek układu
- y0 [float][metry] - współrzędna "y" w układzie orto-kartezjańskim, która definiuje środek układu
- z0 [float][metry] - współrzędna "z" w układzie orto-kartezjańskim, która definiuje środek układu

xyz = [x,y,z]: [list]
- x [float][metry] - współrzędna "x" w układzie orto-kartezjańskim, którą przeliczamy do układu neu
- y [float][metry] - współrzędna "y" w układzie orto-kartezjańskim, którą przeliczamy do układu neu
- z [float][metry] - współrzędna "z" w układzie orto-kartezjańskim, którą przeliczamy do układu neu   
#### Raises
NotImplementedError
- Jezeli podana jednostka jest poza zbiorem.
#### Returns
neu = [n,e,u]: [list]
- n [float][metry] - współrzędna "n" w układzie sferycznym
- e [float][metry] - współrzędna "e" w układzie sferycznym
- u [float][metry] - współrzędna "u" w w układzie sferycznym

## Sigma([f,l,h],jedn)
### Algorytm liczący długosć łuku południka.

#### Parameters
flh = [f,l,h]: [list]
- f[float][jedn] - szerokość geodezyjna
- l[float][jedn] - długość geodezyjna
- h[float][metry] - wysokość geometryczna(elipsoidalna)    
jedn = [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie]   
#### Raises
NotImplementedError
- Jezeli podana jednostka jest poza zbiorem.
#### Returns
sigma [float][metry] - długość łuku południka 

## XgkYgk([f,l,h],l0,jedn)
### Odwzorowanie Gaussa-Krügera – odwzorowanie kartograficzne pasów południkowych na pobocznicę walca stycznego do południka środkowego (osiowego) każdego odwzorowywanego pasa. Jest to wiernokątne, walcowe, poprzeczne odwzorowanie elipsoidy, w którym każdy pas odwzorowuje się oddzielnie.
        
#### Parameters
flh = [f,l,h]: [list]
- f[float][jedn] - szerokość geodezyjna
- l[float][jedn] - długość geodezyjna
- h[float][metry] - wysokość geometryczna(elipsoidalna)    
jedn = [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie]  
- l0[int][jedn] - długość geodezyjna , południk osiowy
#### Raises
NotImplementedError
- Jeżeli podana jednostka jest poza zbiorem.
#### Returns
XgkYgk = [Xgk,Ygk]: [list]
- Xgk [float][metry] - współrzędna "x" w układzie współrzędnych płaskich Gaussa-Krügera
- Ygk [float][metry] - współrzędna "y" w układzie współrzędnych płaskich Gaussa-Krügera 

## PL2000([f,l,h],l0,jedn)        
### Układ współrzędnych 2000 – układ współrzędnych płaskich prostokątnych zwany układem „2000”, powstały w wyniku zastosowania odwzorowania Gaussa-Krügera dla elipsoidy GRS 80 w czterech trzystopniowych strefach o południkach osiowych 15°E, 18°E, 21°E i 24°E, oznaczone odpowiednio numerami – 5, 6, 7 i 8.
       
#### Parameters
flh = [f,l,h]: [list]
- f[float][jedn] - szerokość geodezyjna
- l[float][jedn] - długość geodezyjna
- h[float][metry] - wysokość geometryczna(elipsoidalna)    
jedn = [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie]  
- l0[int][jedn] - długość geodezyjna , południk osiowy
#### Raises
NotImplementedError
- Jeżeli podana jednostka jest poza zbiorem.
#### Returns
XY2000 = [X2000,Y2000]: [list]
- X2000 [float][metry] - współrzędna "x" w układzie współrzędnych płaskich PL2000
- Y2000 [float][metry] - współrzędna "y" w układzie współrzędnych płaskich PL2000
       
## PL1992([f,l,h],jedn)       
### Układ współrzędnych 1992 – układ współrzędnych płaskich prostokątnych oparty na odwzorowaniu Gaussa-Krügera dla elipsoidy GRS80 w jednej dziesięciostopniowej strefie. Początkiem układu jest punkt przecięcia południka 19°E z obrazem równika.
        
#### Parameters
flh = [f,l,h]: [list]
- f[float][jedn] - szerokość geodezyjna
- l[float][jedn] - długość geodezyjna
- h[float][metry] - wysokość geometryczna(elipsoidalna)    
jedn = [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie]  
#### Raises
NotImplementedError
- Jeżeli podana jednostka jest poza zbiorem.
#### Returns
XY1992 = [X1992,Y1992]: [list]
- X1992 [float][metry] - współrzędna "x" w układzie współrzędnych płaskich PL1992
- Y1992 [float][metry] - współrzędna "y" w układzie współrzędnych płaskich PL1992
       
  
# Informacje o funkcji zawartej w pliku czytanie_txt.py
  

Program czytanie_txt przyjmuje plik txt tylko w takim formacie:
        
        3664940.500 1409153.590 5009571.170
        3664940.510 1409153.580 5009571.167
        3664940.520 1409153.570 5009571.167
        3664940.530 1409153.560 5009571.168
        3664940.520 1409153.590 5009571.170
        3664940.514 1409153.584 5009571.166
        
A następnie przelicza do układu który poda użytkownik.Niedoskonałoscią tego programu jest to że pobiera argumenty dla wszystkich funkcji.Lecz to nie jest aż tak wileki problem, wystarczy wpisać losowe wartosci, nie będą one miały wplywu na wynik końcowy.

#### Parameters
xyz0 = [x0,y0,z0]: [list]
- x0 [float][metry] - współrzędna "x" w układzie orto-kartezjańskim, która definiuje środek układu
- y0 [float][metry] - współrzędna "y" w układzie orto-kartezjańskim, która definiuje środek układu
- x0 [float][metry] - współrzędna "z" w układzie orto-kartezjańskim, która definiuje środek układu


l0 [int], południk osiowy

jedn [STR], Jednostka podawanych wartosci. Do wyboru:["rad" - radiany, "gra" - grady, "dec" - stopnie] 

model [str], Model elipsoidy,Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke

plik [str], Nazwa pliku o rozszerzeniu txt który wczytujemy.

funkcja [str], Nazwa funkcji według której chcemy przeliczyć współrzędne między układami. Wybór funkcji: xyz2flh,flh2XYZ,xyz2neu,XgkYgk,XY2000,XY1992.

#### Returns
Plik o rozszerzeniu txt z przeliczonymi współrzędnymi
   
    Plik txt który zwraca funkcja wygląda następujaco:
        
        Funkcja: xyz2flh
        [52.09727221841272, 21.03153333279777, 141.398586823605]
        [52.09727216111064, 21.031533144230153, 141.39974895119667]
        [52.097272120371336, 21.031532955662534, 141.4032782446593]
        [52.097272085152944, 21.031532767094923, 141.40759659186006]
        [52.09727208603574, 21.031533228061544, 141.41005479265004]
        [52.09727211893464, 21.031533177762707, 141.40213536750525]
    
# Opis działania pliku Aplikacja.py
Plik ten został stworzony na potrzeby możliwości skorzystania z funkcji zawartych w plikach Projekt.py oraz czytanie_txt poprzez interpreter poleceń (cmd).
### Opis użycia cmd.
1. Otwórz wiersz poleceń (cmd) na swoim komputerze.
2. Przejdź do katalogu, w którym znajduje się plik Python, którego chcesz uruchomić. Możesz użyć polecenia cd (change directory), aby nawigować po systemie plików. Na przykład, jeśli plik znajduje się na pulpicie, wpisz: cd C:\Users\TwojaNazwaUżytkownika\Pulpit
3. Po wejściu do odpowiedniego katalogu, wpisz polecenie python nazwa_pliku.py, gdzie "nazwa_pliku.py" to nazwa twojego pliku Python. Na przykład, jeśli twój plik nazywa się "Aplikacja.py", wpisz: python Aplikacja.py
Jeśli używasz Pythona w wersji 3.x, możliwe, że będziesz musiał użyć polecenia python3 zamiast python.
4. Naciśnij klawisz Enter, aby uruchomić plik Python. W wyniku tego powinien zostać wykonany kod zawarty w pliku, a ewentualne wyniki lub wyjście zostaną wyświetlone w konsoli.

Upewnij się, że masz zainstalowany interpreter Python na swoim komputerze i że ścieżka do interpretera jest dodana do zmiennej środowiskowej PATH. W przeciwnym razie komenda python nie zostanie rozpoznana w wierszu poleceń.

### Wywołanie funckji w cmd.
Aby uruchomić poszczególne funckje zawarte w plikach Projekt1.py oraz czytanie_txt.py nazleży po komendzie "python Aplakcja.py" dopisać poszczególne argumenty przypisane do danych funkcji z plików.
### Argumenty w pliku Aplikacja.py
Pierwszy argument jaki należy wybrać to:
- '-func',type = str, Wybór funkcji: xyz2flh,flh2XYZ,xyz2neu,XgkYgk,XY2000,XY1992,czytanie_txt

Reszta argumentów uzależniona jest od wyboru funckji.Pozostałe argumenty:
- '-func2',type = str, Jeżeli została wybrana funckja czytanie_txt. to trzeba wybierać funkcje:xyz2flh,flh2XYZ,xyz2neu,XgkYgk,XY2000,XY1992
- '-m',type = str, Wskaż elipsoidę z listy: wgs84 , wgs72 , grs80 , Krasowski , Międzynarodowa , Bessel , Clarke
- '-x',type = float, Zawsze podawane w [metry] współrzędna "x" w układzie orto-kartezjańskim
- '-y',type = float, Zawsze podawane w [metry] współrzędna "y" w układzie orto-kartezjańskim
- '-z',type = float, Zawsze podawane w [metry] współrzędna "z" w układzie orto-kartezjańskim
- '-jedn',type = str, 'Wskaż jednsotkę z listy : rad,dec,gra. Dla funkcji xyz2flh jest to jednostka w której mają być zwrócone współrzędne, a dla funkcji flh2XYZ,XgkYgk,XY2000,XY1992 jednostki w jakich wchodzą współrzędne. 
- '-f',type = float, Zawsze okreslona przez argument -jedn ,szerokość geodezyjna
- '-l',type = float, Zawsze okreslona przez argument -jedn ,długość geodezyjna
- '-l0',type = float, Zawsze okreslona przez argument -jedn ,południk zerowy
- '-he',type = float, Zawsze podawane w [metry] wysokość elipsoidalna
- '-x0',type = float, Zawsze podawane w [metry] wsp. x0 srodka układu kartezjańskiego
- '-y0',type = float, Zawsze podawane w [metry] wsp. y0 srodka układu kartezjańskiego
- '-z0',type = float, Zawsze podawane w [metry] wsp. z0 srodka kartezjańskiego')
- '-xr',type = float, Zawsze podawane w [metry] wsp. x referencyjna układu układu kartezjańskiego
- '-yr',type = float, Zawsze podawane w [metry] wsp. y referencyjna układu układu kartezjańskiego
- '-zr',type = float, Zawsze podawane w [metry] wsp. z referencyjna układu kartezjańskiego
- '-plik',type = str, Nazwa pliku txt który chcemy użyć do funkcji czytanie_txt
- '-plik_wych',type = str, Nazwa pliku txt który będzie plikem , w którym zapiszą się nam nasze wyniki



### Argumenty przyjmowane przez poszczególne funkcje: 
- xyz2flh(-x,-y,-z,-jedn)
- flh2XYZ(-f,-l,-he,-jedn)
- xyz2neu(-x0,-y0,-z0,-xr,-yr,-zr)
- XgkYgk(-f,-l,-he,-l0,-jedn)
- XY2000(-f,-l,-he,-l0,-jedn)
- XY1992(-f,-l,-he,-jedn)
- czytanie_txt(-x0,-y0,-z0,-l0,-m,-plik,-func2,-jedn,-plik_wych)


       

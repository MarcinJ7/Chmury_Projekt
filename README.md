# Programowanie usług w chmurze

Projekt: rozpoznawanie wieku na podstawie zdjęcia

Autorzy:
*   Marcin Jurczak
*   Marek Knosala
*   Malwina Kubas
*   Magdalena Kuna
*   Edward Sucharda


## Architektura aplikacji w Azure

![Image](images/schemat_chmury2.jpg)

Użytkownik wchodzi na stronę internetową, gdzie można wgrać zdjęcie z komputera lub podać link do zdjęcia. Następnie przekazywane jest ono do Azure Function App. Tymczasowo zjęcie zapisywane jest do Azure Blob Storage by łatwiej na nim operować. Następnie zdjęcie jest przekazywane w dwa miejsca. Pierwszym z nich jest usułga Coginitive Servieces, gdzie na podsatwie wycinka zdjęcia z wykrytą twarzą wyznaczany jest wiek i zwracany do Function App. 
Drugie miejsce, do którego przekazywane jest zdjcie z Function App, to dockerowy kontener. Tam jest ładowany model, który został przez nas wcześniej wytrenowany. Zostają wycięte za pomocą funkcji z bibioteki OpenCV fragmenty zdjęcia zawierające twarz, które następnie zostają poddane analizie przez wcześniej wspomniany model. W kontenerze wywoływana jest również funkcja zapisująca zdjęcie wraz z oszacowanym wynikiem do Azure SQL Database. Na koniec program umieszczony w kontenerze zwraca wiek do Function App. Na sam koniec Function App zwraca otrzymane wyniki do Web App'a. Dzięki temu na stronie internetowej pojawiają się dwa wyniki: wyliczony za pomocą Cognitive Servieces oraz wyliczony przez stworzoną przez nas sieć.
Gdy na przesyłanym zdjęciu znajdują się dwie lub więcej osób obie metody szacujące wiek są tak zaprojektowane by zwracać wektor wyliczonego wieku osób na zdjęciu. W takiej sytuacji na stronie internetowej pojawi się kilka wyników odzielonych przecinkiem.
Dzięki zapisanym zdjęciom w Azure SQL Database istnieje w przyszłości możliwość dotrenowania modelu na podstawie nowych zdjęć oraz sprawdzania poprawności obliczanych wyników przez naszą sieć na podstawie zdjęć udostępnianych przez użytkowników.


## Diagram przypadków użycia

![Image](images/UMLv2.png)

Jest to aktualna wersja diagramu UML. Istnieje możlwiość rozbudowy diagramu o nowe funkcjonalności takie jak logowanie do systemu, głosowanie dotyczące trafności przewidywania czy przeglądanie historii analizowanych zdjęć. 

## Playlista

https://www.youtube.com/playlist?list=PLCpsFIg2cqnjOLTCMcnG9uikYz1YYkgjl

## Cognitive Services

Do rozpoznawania wieku z wykorzystaniem narzędzi platformy Azure wykorzystano Face Cognitive Service w bezpłatnej wersji umożliwiającej do 30k wywołań miesięcznie. Więcej informacji na temat samego serwisu Face oraz jego możliwości można znaleźć w [dokumentacji](https://docs.microsoft.com/en-us/azure/cognitive-services/face/overview).

Na potrzeby projektu została utworzona aplikacja desktopowa napisana w języku Python. Aplikacja umożliwia wykrycie wieku osób znajdujących się na zdjęciu z wykorzsytaniem endpointa Azure Face Cognitive Service. Analizowane zdjęcia podawane są do serwisu jako adresy URL. Odpowiedź zwrotna z Azura zawarta jest w formacie JSON - należy odpowiednio przetworzyć otrzymane dane, w których zawarte są informacje zwrotne na temat analizowanego obrazu. Dokonywane jest zaznaczenie położenia twarzy na obrazie za pomocą ramki oraz wypisywany jest wiek osoby/osób znajdujących się na zdjęciu (zarówno w konsoli, jak i na zdjęciu). Kolejnym krokiem jest wyświetlenie zdjęcia (już z zaznaczoną ramką i wypisanym wiekiem). Program jest dobrym narzędziem do weryfikacji  jakości tworzoengo modelu, podczas jego testowania - może stanowić odniesienie jako już dobrze wytrenowany model.

## Kontener

Wszystkie pliki użyte do wyliczania wieku znajdujące się w kontenerze zostały umieszczone w folderze DockerInstance.

## Model sieci neuronowej

Kod potrzebny do przetworzenia zdjęć, budowy i wytrenowania modelu sieci neuronowej znajduje
się w folderze NN_Model.


### Dataset

IMDb-Wiki dataset: https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/

Dataset zawiera wiele źle wyskalowanych/wyciętych zdjęć, więc został użyty tylko podzbiór 
"Faces only". Znajduje się w nim 640 tys. zdjęć, część z nich jest zbyt niewyraźna lub błędnie
opisana (brak informacji lub wiek ujemny). Po modyfikacjach pozostało około 300 tys zdjęć.

### Model

Model sieci neuronowej składa się z warstw:
1. Warstwa konwolucyjna, głębia jądra: 32
2. Warstwa konwolucyjna, głębia jądra: 64
3. Warstwa konwolucyjna, głębia jądra: 128
4. Warstwa konwolucyjna, głębia jądra: 256
5. Warstwa spłaszczająca dane (Flatten)
6. Warstwa Dropout 20%
7. Warstwa 256 gęsto połączonych neuronów
8. Warstwa wyjściowa - 1 neuron, bez funkcji aktywacji

Wszystkie warstwy konwolucyjne mają rozmiar okna równy 3x3

Optymalizator: Adam, lr = 0.001

Innym sprawdzanym rozwiązaniem było użycie modelu InceptionV3 (załadowanie modelu z argumentem freeze=true, następnie dotrenowanie dwóch warstw gęsto połączonych. 

### Pliki

*  data_preparation:
   *   wypakowanie danych z pliku .mat (Matlab)
   *   usunięcie pustych zdjęć
   *   wycięcie twarzy ze zdjęć (klasyfikator HaarCascade z OpenCV) - funkcja Marcina
   *   ujednolicenie rozmiaru zdjęć
   *   obliczenie wieku osób na podstawie nazwy zdjęcia
   *   zapis danych do nowych plików csv

*  fix_csv - usunięcie wierszy, które:
   *   wskazywały na pliki, w których nie wykryto żadnej twarzy
   *   wiek był liczbą ujemną
   *   płeć nie była stwierdzona
   
*  model - model sieci neuronowej

*  inception_model - wytrenowanie modelu sieci korzystającego z modelu InceptionV3

*  test_new_photos - ocena zdjęć testowych

*  test_model - test sieci neuronowej 

*  test_inception - test sieci zawierającej model InceptionV3

### Wytrenowany model

Link do modelu: https://drive.google.com/drive/folders/1Dr8UX2PS-iZbj1CPeX1rJfHnYGnkejGI

Struktura sieci znajduje się w pliku JSON, a wagi w pliku h5. Model należy umieści w konterze razem z zawartoscią folderu DockerInstance.

### Colab

Notatnik w Colabie (pierwsza wersja kodu, niestety dataset był zbyt duży aby wytrenować model 
w Colabie):
https://colab.research.google.com/drive/1rPGtVji4odywJwv0ufEYi2BS-GPq7x-F?fbclid=IwAR32i5pVgd4cqhmMFU7KR-PjpRFOOyPKMrO7Oo8IVF1uD9cWK_oLN7XJ2As#scrollTo=ee0p1L0DpzXs

### Biblioteki

- TensorFlow 2.12.0
- Keras 2.3.1
- opencv-python 4.2.0
- NumPy 1.18.2
- Pandas 1.0.3
- matplotlib 3.2.1

## Strona internetowa

Pierwotnie strona internetowa została postawiona na maszynie wirtualnej, na której zainstalowano Apache, PHP oraz 
cURL PHP do przesyłania obrazów do blob storage. Pliki strony na maszyynie wirtualnej znajduja sie w folderze www/html, w tym folderze należy umieścić je na maszynie wirtualnej w katalogu root ("/"). Następnie postawiono Web app, w którym zaimplementowano skrypt w JavaScripcie do przesyłania zdjęcia do modelua jak również zwracania wyniku na strone. Wieka cześc kodu strony w Web app została wykorzystana ze strony znajadującej sie na maszynie wirtualnej. Pliki znajdują sie w folderze "Webapp".

## Template grupy zasobów

znajduje się w pliku ExportedTemplate-Projekt_Chmury.zip

## Zadania

Zrobione:

*  przygotowanie danych uczących - Malwina
*  obróbka przesyłanych zdjęć (wycinanie twarzy, walidacja) - Marcin
*  wgrywanie plików ze zdjęciem na stronę - Marek
*  stworzenie modelu + wytrenowanie sieci neuronowej - Malwina
*  wyświetlanie przesłanych zdjęć na stronie - Marek
*  zapisywanie wyników w Azure SQL Database - Edward
*  obsłużenie Cognitive Services - Marcin
*  zwracanie wyniku na stronę internetową - Magda
*  zapisywanie zdjęć do Azure Blob Storage - Marek
*  utworzenie nowego AD, grupy zasobów i przypisanie uprawnień - Malwina
*  utworzenie strony internetowej - Marek
*  połączenie aplikacji w Function App - Magda
*  uruchamianie Azure Databricks (lub innego serwisu) w celu określenia wieku - Edward + Magda

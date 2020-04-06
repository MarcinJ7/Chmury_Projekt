# Programowanie usług w chmurze

Projekt: rozpoznawanie wieku na podstawie zdjęcia

Autorzy:
*   Marcin Jurczak
*   Marek Knosala
*   Malwina Kubas
*   Magdalena Kuna
*   Paweł Niewęgłowski
*   Edward Sucharda


## Architektura aplikacji w Azure

![Image](images/architektura.png)

Użytkownik loguje się na stronę poprzez Azure Active Directory za pomocą konta Microsoft lub Google. Na stronie można wgrać zdjęcie, które jest wysyłane przez API Management do Azure Function App. Tam zdjęcie jest poddawane obróbce, która polega na wycięciu fragmentu zdjęcia, w którym znajduje się twarz (i ewentualne zgłoszenie błedu, jeśli na zdjęciu nie ma człowieka). Wycięta twarz wysyłana jest do Azure Machine Learning Services, gdzie przekazywana jest na wejście modelu sieci neuronowej. Zwracanym wynikiem jest wiek osoby, który jest wyświetlany na stronie internetowej użytkownikowi, który to zdjęcie wysłał. Azure Blob Storage przechowuje cały dataset (chyba, że model nie będzie douczany), a baza Cosmos DB przechowuje model sieci neuronowej.

Ewentualnym rozszerzeniem aplikacji będzie użycie Azure Cognitive Services (z Face API), które również będzie zwracało wiek osoby na zdjęciu, dzięki czemu będzie można porównywać wyniki.


## Diagram przypadków użycia

<do wstawienia>


## Model sieci neuronowej

https://colab.research.google.com/drive/1rPGtVji4odywJwv0ufEYi2BS-GPq7x-F?fbclid=IwAR32i5pVgd4cqhmMFU7KR-PjpRFOOyPKMrO7Oo8IVF1uD9cWK_oLN7XJ2As#scrollTo=ee0p1L0DpzXs

Trzy podejścia:
1. Sieć składająca się z trzech warstw sieci konwolucyjnej o rozmiarze okna 3x3 i głębii 32, 64, 128

2. Użycie dolnych warstw modeli takich jak ResNet lub InceptionV3

3. Skorzystanie z gotowych klasyfikatorów OpenCV, np. HaarCascade

Zdjęcia będą poddane wcześniejszej obróbce, która wytnie fragment zdjęcia, w którym znajduje się twarz (za pomocą OpenCV).


## Dataset

IMDb-Wiki dataset: https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/

Zbiór zawiera wiele nieporawnych zdjęć, więc użyjemy tylko części "faces only" (8 GB).


## Zadania

*  logowanie przez Azure AD
*  utworzenie strony internetowej
*  wgrywanie plików ze zdjęciem na stronę
*  zapisywanie zdjęć do Azure Blob Storage
*  obróbka przesyłanych zdjęć (wycinanie twarzy, walidacja)
*  wyświetlanie przesłanych zdjęć na stronie
*  uruchamianie Azure ML w celu określenia wieku
*  stworzenie modelu sieci neuronowej
*  wgranie modelu do Azure ML
*  zwracanie wyniku na stronę internetową
*  zapisywanie wyników w Cosmos DB


## Pytania

1. Architektura aplikacji w Azure

2. Douczanie modelu: Czy model będzie "douczany" za pomocą nowych zdjęć, czy użyjemy wcześniej wytrenowanego modelu sieci neuronowej.

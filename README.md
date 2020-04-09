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

Użytkownik loguje się na stronę poprzez Azure Active Directory za pomocą konta Microsoft lub Google. Na stronie można wgrać zdjęcie, które jest wysyłane przez API Management do Azure Function App. Tam zdjęcie jest poddawane obróbce, która polega na wycięciu fragmentu zdjęcia, w którym znajduje się twarz (i ewentualne zgłoszenie błedu, jeśli na zdjęciu nie ma człowieka). Wycięta twarz wysyłana jest do Azure Databricks Services, gdzie przekazywana jest na wejście modelu sieci neuronowej. Zwracanym wynikiem jest wiek osoby, który jest wyświetlany na stronie internetowej użytkownikowi, który to zdjęcie wysłał. Azure Blob Storage przechowuje cały dataset (chyba, że model nie będzie douczany), a baza PostgreeQSL DB przechowuje model sieci neuronowej.

Ewentualnym rozszerzeniem aplikacji będzie użycie Azure Cognitive Services (z Face API), które również będzie zwracało wiek osoby na zdjęciu, dzięki czemu będzie można porównywać wyniki.


## Diagram przypadków użycia

![Image](images/UML.png)

Jest to robocza wersja diagramu UML. Nie dodawałem administratora gdyż wykorzystywałby on dokładnie te same funkcjonalności co użytkownik. Jeżeli są jakieś sugestie, to piszcie i będę na bieżąco aktualizował diagram. 

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

*  logowanie przez Azure AD - Marek
*  utworzenie strony internetowej - Marek
*  wgrywanie plików ze zdjęciem na stronę - Marek
*  zapisywanie zdjęć do Azure Blob Storage - Marcin
*  obróbka przesyłanych zdjęć (wycinanie twarzy, walidacja) - Magda
*  wyświetlanie przesłanych zdjęć na stronie - Paweł
*  uruchamianie Azure Dataabricks w celu określenia wieku - Marcin
*  stworzenie modelu sieci neuronowej - Malwina
*  wgranie modelu do Azure Databricks - Malwina
*  zwracanie wyniku na stronę internetową - Magda
*  zapisywanie wyników w PostreSQL DB - Edward
*  obsłużenie Cognitive Services - Edward

## Pytania



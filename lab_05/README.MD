# Lab 05 – Symulacja lotu statku 2D z użyciem PyRay

## Co zostało zrealizowane
Zaimplementowałem/am prostą symulację fizyki statku kosmicznego w przestrzeni 2D przy użyciu biblioteki PyRay (Raylib). Aplikacja została podzielona na dwa moduły: logikę statku (`Ship`) oraz główną pętlę gry.

Główne elementy implementacji obejmują:
* **Wektorowy model ruchu:** Obliczanie pozycji na podstawie wektora prędkości aktualizowanego co klatkę z uwzględnieniem czasu (`dt`).
* **Fizykę i sterowanie:** Przyspieszanie w kierunku, w którym zwrócony jest nos statku (strzałka w górę), obrót (strzałki lewo/prawo) oraz hamulec awaryjny (klawisz Z). Zastosowałem/am również tarcie (płynne wytracanie prędkości) i limit maksymalnej prędkości (`MAXSPEED`).
* **Transformacje geometryczne:** Przeliczanie lokalnych współrzędnych wierzchołków statku i płomienia na współrzędne globalne (ekranowe) za pomocą macierzy rotacji 2D i translacji.
* **Kolizje z oknem:** Odbijanie statku od krawędzi ekranu o wymiarach 800x600 pikseli poprzez odwracanie odpowiednich składowych wektora prędkości.
* **Tryb Debug:** Opcjonalne wyświetlanie wektora prędkości (czerwona linia) oraz aktualnej wartości prędkości.

## Sterowanie 
Instrukcja sterowania
Po uruchomieniu symulacji możesz kontrolować statek za pomocą następujących klawiszy:
* **Strzałka w Górę: Uruchomienie silnika głównego (przyspieszenie w kierunku dziobu).
* **Strzałka w Lewo / Prawo: Obrót statku wokół własnej osi.
* **Klawisz Z: Hamulec awaryjny (szybkie wytracanie prędkości).

## Uruchomienie
Projekt wymaga zainstalowanego środowiska Python 3 oraz biblioteki `pyray` (Pythonowe wiązania dla Raylib).

Program składa się z dwóch modułów, ale punktem wejścia do symulacji jest plik główny. Aby uruchomić aplikację, wykonaj polecenie:
   ```bash
   python main.py

  ## Upewnij się, że masz zainstalowaną wymaganą bibliotekę. Możesz to zrobić poleceniem:
   
   pip install raylib

# Lab 06 – Topologia Świata i Asteroidy

## Co zostało zrealizowane
W ramach tego laboratorium zaimplementowałem mechanikę przestrzeni toroidalnej (tzw. efekt zawijania ekranu) oraz zaludniłem świat gry proceduralnie generowanymi asteroidami. Główne elementy, które udało się zrealizować, to:
* **Zawijanie krawędzi (Wrap):** Zarówno statek, jak i asteroidy płynnie przechodzą przez krawędzie ekranu, pojawiając się po przeciwnej stronie.
* **Renderowanie widm (Ghost rendering):** Aby przejście przez krawędź było gładkie wizualnie, obiekty znajdujące się blisko granicy ekranu są rysowane wielokrotnie. Logikę tę wydzieliłem do uniwersalnej funkcji `ghost_positions` w nowym pliku `utils.py`.
* **Klasa Asteroid i kształty proceduralne:** Stworzyłem klasę reprezentującą asteroidy. Zamiast idealnych okręgów, ich wierzchołki są generowane proceduralnie z losowymi zniekształceniami promienia, co tworzy nieregularne wielokąty. Obiekty te obracają się wokół własnej osi podczas ruchu.
* **Warianty rozmiarów (Zadanie dodatkowe):** Asteroidy przyjmują podczas inicjalizacji rozmiar (`small`, `medium`, `large`), na podstawie którego automatycznie dobierany jest ich promień oraz prędkość poruszania się (większe obiekty są wolniejsze).
* **Refaktoryzacja:** Przeniosłem stałe konfiguracyjne (wymiary ekranu, parametry fizyki statku) do pliku `utils.py`, co ułatwia zarządzanie balansem gry w jednym miejscu.

## Uruchomienie
Projekt wymaga zainstalowanego języka Python oraz biblioteki Raylib w wersji dla Pythona (`raylib-python-cffi`). 

Aby uruchomić grę, upewnij się, że jesteś w odpowiednim środowisku wirtualnym (jeśli takiego używasz) i posiadasz zainstalowane zależności, a następnie wykonaj w terminalu polecenie:

```bash
python main.py



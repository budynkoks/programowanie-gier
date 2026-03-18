* **Maszyna Stanów Gry (Game States):**
  * Dodano płynne przejścia między ekranami bez konieczności odświeżania strony.
  * Dostępne stany: `Menu Główne`, `Rozgrywka`, `Ekran Zwycięstwa (Win)` oraz `Ekran Porażki (Lose)`.
  * Sterowanie stanami odbywa się za pomocą delegatów funkcji (`current_update` i `current_draw`).

* **System UI / HUD:**
  * Wyświetlanie aktualnego wyniku (Score) w lewym górnym rogu w trakcie gry.
  * Wizualna reprezentacja punktów życia gracza w postaci ikon statku (serc) w prawym górnym rogu.

* **Trwały Zapis Danych (Leaderboard - Zadanie **):**
  * Gra zapamiętuje **5 najlepszych wyników**, korzystając z lokalnej pamięci przeglądarki (obiekt `storage`).
  * System automatycznie sortuje wyniki po zakończeniu gry (sortowanie bąbelkowe) i aktualizuje tablicę.
  * Tabela Top 5 widoczna jest na ekranie Menu Głównego.

* **Funkcja Resetowania (Game Loop):**
  * Zaimplementowano funkcję `reset_game()`, która przywraca wartości początkowe zmiennych (pozycję gracza, stan wrogów, pociski) po wciśnięciu klawisza `R` na ekranie końcowym.




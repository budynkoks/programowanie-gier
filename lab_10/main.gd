extends Node3D

var score: int = 0


# Funkcja wywoływana z target.gd
func add_score() -> void:
	score += 1
	print("Wynik: ", score)

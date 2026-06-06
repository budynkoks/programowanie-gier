extends Area3D

@export var speed: float = 50.0
@export var direction: Vector3 = Vector3.ZERO # Domyślnie wektor zerowy
@export var lifetime: float = 3.0

func _process(delta: float) -> void:
	# Przesuwanie pocisku "do przodu" (wzdłuż osi -Z)
	global_position += direction * speed * delta
	
	# Odliczanie czasu życia
	lifetime -= delta
	if lifetime <= 0.0:
		queue_free() # Usunięcie pocisku ze sceny, gdy czas minie

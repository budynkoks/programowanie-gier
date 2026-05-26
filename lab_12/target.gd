extends Node3D

func _ready() -> void:
	$Area3D.area_entered.connect(_on_hit)

func _on_hit(_area: Area3D) -> void:
	print("trafiony!")
	$"..".add_score()
		
	_area.queue_free()
	# Niszczymy cel
	queue_free()

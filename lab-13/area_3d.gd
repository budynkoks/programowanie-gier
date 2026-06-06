extends Area3D

func _ready() -> void:
	# Łączymy sygnał wejścia w strefę (area_entered) z naszego Area3D do funkcji _on_hit
	$Area3D.area_entered.connect(_on_hit)

func _on_hit(area: Area3D) -> void:
	print("Trafiony!")
	
	var main_scene = get_tree().current_scene
	if main_scene.has_method("add_score"):
		main_scene.add_score()
		
	area.queue_free() # Niszczymy pocisk, który w nas uderzył
	queue_free()      # Niszczymy ten cel

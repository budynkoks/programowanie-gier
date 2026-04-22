extends MeshInstance3D 

@export var ship_speed: float = 10.0
@export var limit_x: float = 2.0
@export var limit_y: float = 2.0

func _process(delta: float) -> void:
	var input_x = Input.get_axis("ui_left", "ui_right")
	var input_y = Input.get_axis("ui_down", "ui_up") 
	
	position.x += input_x * ship_speed * delta
	position.y += input_y * ship_speed * delta
	
	position.x = clamp(position.x, -limit_x, limit_x)
	position.y = clamp(position.y, -limit_y, limit_y)

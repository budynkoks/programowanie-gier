extends MeshInstance3D 

@export var ship_speed: float = 5.0
@export var limit_x: float = 2.0
@export var limit_y: float = 2.0
@export var bullet_scene: PackedScene
var _shoot_cooldown: float = 0.3

func _process(delta: float) -> void:
	var input_x = Input.get_axis("ui_right","ui_left")
	var input_y = Input.get_axis("ui_down", "ui_up") 
	
	position.x += input_x * ship_speed * delta
	position.y += input_y * ship_speed * delta
	position.x = clamp(position.x, -limit_x, limit_x)
	position.y = clamp(position.y, -limit_y, limit_y)
	
	# Obsługa cooldownu
	if _shoot_cooldown > 0.0:
		_shoot_cooldown -= delta
		
	# Reakcja na przycisk strzału
	if Input.is_action_just_pressed("ui_accept") and _shoot_cooldown <= 0.0:
		shoot()
		_shoot_cooldown = 0.3 # Reset cooldownu na 0.3 sekundy

func shoot() -> void:
		
	var bullet = bullet_scene.instantiate()
	get_tree().root.add_child(bullet)
	bullet.global_position = global_position

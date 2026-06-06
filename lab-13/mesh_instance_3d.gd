extends MeshInstance3D 

var hp: int = 100
@export var ship_speed: float = 5.0
@export var limit_x: float = 2.0
@export var limit_y: float = 2.0
@export var bullet_scene: PackedScene
var _shoot_cooldown: float = 0.3
var is_invincible: bool = false
@onready var anim_player = $AnimationPlayer # Dopasuj ścieżkę do swojego węzła
func _ready() -> void:
	add_to_group("player")
	
func _process(delta: float) -> void:
	var input_x = Input.get_axis("ui_right","ui_left")
	var input_y = Input.get_axis("ui_down", "ui_up") 
	
	position.x += input_x * ship_speed * delta
	position.y += input_y * ship_speed * delta
	# position.x = clamp(position.x, -limit_x, limit_x)
	# position.y = clamp(position.y, -limit_y, limit_y)
	
	# Obsługa cooldownu
	if _shoot_cooldown > 0.0:
		_shoot_cooldown -= delta
		
	# Reakcja na przycisk strzału
	if Input.is_action_just_pressed("ui_accept") and _shoot_cooldown <= 0.0:
		shoot()
		_shoot_cooldown = 0.3 # Reset cooldownu na 0.3 sekundy
		
	if Input.is_action_just_pressed("ui_select") and not is_invincible:
		perform_barrel_roll()

func shoot() -> void:
		
	var bullet = bullet_scene.instantiate()
	get_tree().root.add_child(bullet)
	bullet.global_position = global_position
	bullet.direction = Vector3(0, 0, 1)


func perform_barrel_roll() -> void:
	is_invincible = true
	anim_player.play("barrel_roll")
	
	# Czekamy na zakończenie sygnału z węzła AnimationPlayer
	await anim_player.animation_finished
	
	is_invincible = false

func _on_area_3d_body_entered(body: Node3D) -> void:
	if body is StaticBody3D:
		take_damage(20)

func take_damage(amount: int) -> void:
	if is_invincible:
		print("Unik! Brak obrażeń.")
		return
		
	hp -= amount
	
		
	print("Kolizja! Otrzymano obrażenia. Aktualne HP: ", hp)

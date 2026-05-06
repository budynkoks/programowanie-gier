extends Node3D

@export var hp: int = 2
@export var speed: float = 3.0
@export var score_value: int = 100
@export var shoot_interval: float = 2.5
@export var bullet_scene: PackedScene

signal died(points: int)

func _on_area_entered(area: Area3D) -> void:
	area.queue_free() # Niszczymy pocisk gracza po trafieniu
	hp -= 1           # Odejmujemy 1 punkt życia wrogowi
	
	if hp <= 0:
		died.emit(score_value)
		queue_free() # Niszczymy wroga dopiero, gdy HP spadnie do 0


@export var sway_amplitude: float = 3.0
@export var sway_period: float = 2.0

func _ready() -> void:
	$Area3D.area_entered.connect(_on_area_entered)
	var start_x = global_position.x
	
	# Tworzymy zapętlonego Tweena
	var tween = create_tween().set_loops()
	
	# Faza 1: Wychylenie w prawo (+ amplituda)
	tween.tween_property(self, "global_position:x", start_x + sway_amplitude, sway_period / 2.0) \
		 .set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		 
	tween.tween_property(self, "global_position:x", start_x - sway_amplitude, sway_period / 2.0) \
		 .set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		
		

var shoot_timer: float = 0.0

func _process(delta: float) -> void:
	shoot_timer += delta
	if shoot_timer >= shoot_interval:
		shoot_timer = 0.0
		shoot_at_player()

func shoot_at_player() -> void:
	var players = get_tree().get_nodes_in_group("player")
	if players.size() > 0:
		var player = players[0]
		
		# Obliczenie wektora kierunku
		var direction = (player.global_position - global_position).normalized()
		
		var bullet = bullet_scene.instantiate()
		get_tree().root.add_child(bullet)
		
		bullet.global_position = global_position
		bullet.direction = direction
		

extends Node

@export var enemy_scene: PackedScene
@export var path_follow_node: PathFollow3D 

var waves: Array[Dictionary] = [
	{ "count": 3, "x_positions": [-3.0, 0.0, 3.0], "z_offset": 30.0, "delay": 2.0 },
	{ "count": 2, "x_positions": [-4.0, 4.0], "z_offset": 40.0, "delay": 5.0 },
	{ "count": 5, "x_positions": [-4.0, -2.0, 0.0, 2.0, 4.0], "z_offset": 50.0, "delay": 10.0 }
]

var _spawned: Array[bool]
var time_elapsed: float = 0.0

func _ready() -> void:
	_spawned.resize(waves.size())
	_spawned.fill(false)

func _process(delta: float) -> void:
	time_elapsed += delta
	
	for i in range(waves.size()):
		if not _spawned[i] and time_elapsed >= waves[i]["delay"]:
			spawn_wave(waves[i])
			_spawned[i] = true

func spawn_wave(wave_data: Dictionary) -> void:
	for i in range(wave_data["count"]):
		var enemy = enemy_scene.instantiate()
		
		var offset = Vector3(wave_data["x_positions"][i], 0, wave_data["z_offset"])
		enemy.position = path_follow_node.global_position + offset
		
		get_tree().root.add_child(enemy)
		

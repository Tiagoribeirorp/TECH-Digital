extends Control

@onready var title_label: Label = $Label
@onready var start_button: Button = $Button
@onready var vida_bar: ProgressBar = $VidaBar
@onready var fadiga_bar: ProgressBar = $FadigaBar
@onready var vida_label: Label = $VidaLabel
@onready var fadiga_label: Label = $FadigaLabel


func _ready() -> void:
	load_character_from_engine()


func load_character_from_engine() -> void:
	var bridge_path := ProjectSettings.globalize_path(
		"res://../../engine/rpg/bridge.py"
	)

	var output: Array = []
	var exit_code := OS.execute(
		"python",
		[bridge_path],
		output,
		true
	)

	if exit_code != 0:
		title_label.text = "Erro ao carregar personagem"
		print("Erro ao executar RPG Engine. Código: ", exit_code)
		print("Saída: ", output)
		return

	if output.is_empty():
		title_label.text = "Engine não retornou dados"
		return

	var json_text: String = str(output[0]).strip_edges()
	var json := JSON.new()

	if json.parse(json_text) != OK:
		title_label.text = "Erro ao interpretar dados do Engine"
		print("JSON recebido: ", json_text)
		return

	var character: Dictionary = json.data

	vida_bar.max_value = character["hp_max"]
	vida_bar.value = character["hp"]

	fadiga_bar.max_value = character["fatigue_max"]
	fadiga_bar.value = character["fatigue"]

	vida_label.text = "Vida: %d/%d" % [
		character["hp"],
		character["hp_max"]
	]

	fadiga_label.text = "Fadiga: %d/%d" % [
		character["fatigue"],
		character["fatigue_max"]
	]

	title_label.text = character["name"]


func _on_button_pressed() -> void:
	title_label.text = "Ação realizada!"

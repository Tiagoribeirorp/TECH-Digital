extends Control

@onready var title_label: Label = $Label
@onready var start_button: Button = $Button
@onready var vida_bar: ProgressBar = $VidaBar
@onready var fadiga_bar: ProgressBar = $FadigaBar
@onready var vida_label: Label = $VidaLabel
@onready var fadiga_label: Label = $FadigaLabel


var character_state: Dictionary = {}


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

	if not apply_engine_response(output[0]):
		title_label.text = "Erro ao interpretar dados do Engine"


func execute_basic_action() -> void:
	var bridge_path := ProjectSettings.globalize_path(
		"res://../../engine/rpg/bridge.py"
	)

	var fatigue := int(character_state.get("fatigue", 0))
	var hp := int(character_state.get("hp", 0))

	var output: Array = []

	var exit_code := OS.execute(
		"python",
		[
			bridge_path,
			"--action",
			"basic",
			"--hp",
			str(hp),
			"--fatigue",
			str(fatigue),
		],
		output,
		true
	)

	if exit_code != 0:
		title_label.text = "Erro ao executar ação"
		print("Erro ao executar ação. Código: ", exit_code)
		print("Saída: ", output)
		return

	if output.is_empty():
		title_label.text = "Engine não retornou dados"
		return

	if apply_engine_response(output[0]):
		title_label.text = "Ação realizada!"


func apply_engine_response(raw_response: Variant) -> bool:
	var json := JSON.new()

	if json.parse(str(raw_response).strip_edges()) != OK:
		print("JSON inválido recebido do Engine: ", raw_response)
		return false

	if not (json.data is Dictionary):
		print("Engine retornou dados em formato inesperado.")
		return false

	character_state = json.data

	vida_bar.max_value = int(character_state["hp_max"])
	vida_bar.value = int(character_state["hp"])

	fadiga_bar.max_value = int(character_state["fatigue_max"])
	fadiga_bar.value = int(character_state["fatigue"])

	vida_label.text = "Vida: %d/%d" % [
		character_state["hp"],
		character_state["hp_max"],
	]

	fadiga_label.text = "Fadiga: %d/%d" % [
		character_state["fatigue"],
		character_state["fatigue_max"],
	]

	return true


func _on_button_pressed() -> void:
	execute_basic_action()

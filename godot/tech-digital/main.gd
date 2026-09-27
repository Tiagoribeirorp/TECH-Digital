extends Control

@onready var title_label: Label = $Label
@onready var title_background: TextureRect = $Background
@onready var battle_background: TextureRect = $BattleBackground
@onready var start_button: Button = $Button
@onready var defense_button: Button = $DefenseButton
@onready var special_button: Button = $SpecialButton
@onready var recover_button: Button = $RecoverButton
@onready var save_button: Button = $SaveButton
@onready var load_button: Button = $LoadButton
@onready var start_menu: Control = $StartMenu
@onready var start_game_button: Button = $StartMenu/StartGameButton
@onready var enemy_select_button: Button = $StartMenu/EnemySelectButton
@onready var vida_bar: ProgressBar = $VidaBar
@onready var fadiga_bar: ProgressBar = $FadigaBar
@onready var vida_label: Label = $VidaLabel
@onready var fadiga_label: Label = $FadigaLabel
@onready var enemy_vida_bar: ProgressBar = $EnemyVidaBar
@onready var enemy_vida_label: Label = $EnemyVidaLabel
@onready var enemy_name_label: Label = $EnemyNameLabel
@onready var die_label: Label = $DieLabel
@onready var initiative_label: Label = $InitiativeLabel
@onready var roll_label: Label = $RollLabel
@onready var combat_log_label: Label = $CombatLogLabel
@onready var round_label: Label = $RoundLabel


var character_state: Dictionary = {}
var enemy_state: Dictionary = {
	"hp": 10,
	"hp_max": 10,
}
var round_number: int = 1
var combat_history: Array[String] = []
var initiative_first: String = "hero"
var initiative_rolls: Dictionary = {}
var enemy_type: String = "training_dummy"
var enemy_profiles: Dictionary = {
	"training_dummy": {"name": "Alvo de treino", "hp": 10},
	"raider": {"name": "Saqueador", "hp": 12},
}


func _ready() -> void:
	title_background.visible = true
	battle_background.visible = false
	set_combat_visible(false)
	start_menu.visible = true
	load_character_from_engine()
	update_enemy_ui()


func set_combat_visible(is_visible: bool) -> void:
	for control in [
		title_label,
		start_button,
		defense_button,
		special_button,
		recover_button,
		save_button,
		load_button,
		vida_bar,
		fadiga_bar,
		vida_label,
		fadiga_label,
		enemy_vida_bar,
		enemy_vida_label,
		enemy_name_label,
		die_label,
		initiative_label,
		roll_label,
		combat_log_label,
		round_label,
	]:
		control.visible = is_visible


func _on_start_game_pressed() -> void:
	start_menu.visible = false
	title_background.visible = false
	battle_background.visible = true
	start_game_button.text = "Iniciar Jogo"
	round_number = 1
	combat_history.clear()
	enemy_state = {
		"hp": enemy_profiles[enemy_type]["hp"],
		"hp_max": enemy_profiles[enemy_type]["hp"],
	}
	load_character_from_engine()
	update_enemy_ui()
	set_combat_visible(true)
	title_label.text = "Escolha sua acao"
	combat_log_label.text = "Sua vez."
	await resolve_initiative()


func _on_enemy_select_pressed() -> void:
	enemy_type = "raider" if enemy_type == "training_dummy" else "training_dummy"
	enemy_select_button.text = "Inimigo: %s" % enemy_profiles[enemy_type]["name"]


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


func execute_action(action_name: String) -> void:
	start_button.disabled = true
	defense_button.disabled = true
	special_button.disabled = true
	recover_button.disabled = true

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
			action_name,
			"--hp",
			str(hp),
			"--fatigue",
			str(fatigue),
			"--enemy-hp",
			str(int(enemy_state.get("hp", 10))),
			"--round",
			str(round_number),
			"--enemy-type",
			enemy_type,
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

	if await apply_combat_response(output[0]):
		if bool(character_state.get("enemy_active", true)):
			start_button.text = "Atacar"
			start_button.disabled = false
			defense_button.disabled = false
			special_button.disabled = false
			recover_button.disabled = false
		else:
			start_button.disabled = true
			defense_button.disabled = true
			special_button.disabled = true
			recover_button.disabled = true


func execute_attack() -> void:
	execute_action("attack")


func execute_defend() -> void:
	execute_action("defend")


func execute_special() -> void:
	execute_action("special")


func execute_recover() -> void:
	execute_action("recover")


func resolve_initiative() -> void:
	var bridge_path := ProjectSettings.globalize_path(
		"res://../../engine/rpg/bridge.py"
	)
	var output: Array = []
	var exit_code := OS.execute(
		"python",
		[bridge_path, "--action", "initiative"],
		output,
		true
	)
	if exit_code != 0 or output.is_empty():
		initiative_label.text = "Iniciativa indisponivel"
		return

	var json := JSON.new()
	if json.parse(str(output[0]).strip_edges()) != OK or not (json.data is Dictionary):
		initiative_label.text = "Iniciativa invalida"
		return

	initiative_rolls = json.data
	initiative_first = str(initiative_rolls.get("first", "hero"))
	var hero_roll := int(initiative_rolls.get("hero_roll", 0))
	var enemy_roll := int(initiative_rolls.get("enemy_roll", 0))
	await animate_roll("Voce", hero_roll, 20)
	await animate_roll("Alvo", enemy_roll, 20)
	if initiative_first == "hero":
		initiative_label.text = "Iniciativa: voce começa (%d x %d)" % [hero_roll, enemy_roll]
	else:
		initiative_label.text = "Iniciativa: alvo começa (%d x %d)" % [enemy_roll, hero_roll]
	combat_log_label.text = "Ordem definida. Sua vez."


func save_combat_state() -> void:
	var payload := {
		"character_state": character_state,
		"enemy_state": enemy_state,
		"enemy_type": enemy_type,
		"round": round_number,
		"initiative_first": initiative_first,
		"initiative_rolls": initiative_rolls,
		"history": combat_history,
	}
	var file := FileAccess.open("user://combat_save.json", FileAccess.WRITE)
	if file == null:
		combat_log_label.text = "Nao foi possivel salvar o combate."
		return
	file.store_string(JSON.stringify(payload))
	combat_log_label.text = "Combate salvo."


func load_combat_state() -> void:
	if not FileAccess.file_exists("user://combat_save.json"):
		combat_log_label.text = "Nenhum combate salvo."
		return
	var file := FileAccess.open("user://combat_save.json", FileAccess.READ)
	if file == null:
		combat_log_label.text = "Nao foi possivel carregar o combate."
		return
	var payload = JSON.parse_string(file.get_as_text())
	if not (payload is Dictionary):
		combat_log_label.text = "Arquivo de combate invalido."
		return

	character_state = payload.get("character_state", {}).duplicate()
	enemy_state = payload.get("enemy_state", {"hp": 10, "hp_max": 10}).duplicate()
	enemy_type = str(payload.get("enemy_type", "training_dummy"))
	round_number = int(payload.get("round", 1))
	initiative_first = str(payload.get("initiative_first", "hero"))
	initiative_rolls = payload.get("initiative_rolls", {}).duplicate()
	combat_history = Array(payload.get("history", []))
	start_menu.visible = false
	title_background.visible = false
	battle_background.visible = true
	set_combat_visible(true)
	apply_character_ui()
	update_enemy_ui()
	round_label.text = "Rodada %d" % round_number
	combat_log_label.text = "Combate carregado."


func _on_save_button_pressed() -> void:
	save_combat_state()


func _on_load_button_pressed() -> void:
	load_combat_state()


func apply_combat_response(raw_response: Variant) -> bool:
	var json := JSON.new()

	if json.parse(str(raw_response).strip_edges()) != OK:
		combat_log_label.text = "Resposta invalida do Engine."
		return false

	if not (json.data is Dictionary):
		combat_log_label.text = "Engine retornou dados inesperados."
		return false

	var final_state: Dictionary = json.data
	if str(final_state.get("phase", "")) == "blocked":
		title_label.text = "Acao bloqueada"
		combat_log_label.text = str(final_state.get("message", "Acao bloqueada."))
		return true

	character_state = final_state.duplicate()
	character_state["hp"] = int(final_state.get("hp_after_player_action", final_state.get("hp", 0)))
	character_state["enemy_hp"] = int(final_state.get("enemy_hp_after_player_action", final_state.get("enemy_hp", 0)))
	round_number = int(character_state.get("round", round_number))
	enemy_state = {
		"hp": int(character_state.get("enemy_hp", 0)),
		"hp_max": int(character_state.get("enemy_hp_max", 10)),
	}
	apply_character_ui()
	update_enemy_ui()
	round_label.text = "Rodada %d" % round_number

	var action := str(character_state.get("action", "attack"))
	var roll_value: Variant = character_state.get("roll", null)
	var target_value: Variant = character_state.get("target", null)
	var roll := 0
	var target := 0
	if roll_value != null:
		roll = int(roll_value)
	if target_value != null:
		target = int(target_value)
	var damage := int(character_state.get("damage", 0))
	var success := bool(character_state.get("success", false))
	var enemy_roll_value: Variant = character_state.get("enemy_roll", null)
	var enemy_roll := 0
	if enemy_roll_value != null:
		enemy_roll = int(enemy_roll_value)
	var enemy_target := int(character_state.get("enemy_target", 0))
	var enemy_damage := int(character_state.get("enemy_damage", 0))
	var enemy_success := bool(character_state.get("enemy_success", false))
	var enemy_active := bool(character_state.get("enemy_active", true))
	var hero_active := bool(character_state.get("hero_active", true))
	if roll_value != null and (action == "attack" or action == "special"):
		await animate_roll("Voce", roll, target)
	if action == "defend":
		if enemy_active:
			roll_label.text = "Voce: postura defensiva +%d\nAguardando resposta do alvo" % int(character_state.get("defense_bonus", 0))
		else:
			roll_label.text = "Voce: postura defensiva +%d\nAlvo derrotado" % int(character_state.get("defense_bonus", 0))
		title_label.text = "Postura defensiva"
	elif action == "special" and success:
		if enemy_active:
			roll_label.text = "Voce: golpe forte d20 %d/%d\nAguardando resposta do alvo" % [roll, target]
		else:
			roll_label.text = "Voce: golpe forte d20 %d/%d\nAlvo derrotado" % [roll, target]
		title_label.text = "Golpe forte: %d de dano" % damage
	elif action == "recover":
		roll_label.text = "Voce recuperou %d de fadiga\nAguardando resposta do alvo" % int(character_state.get("fatigue_recovered", 0))
		title_label.text = "Recuperacao"
	elif success:
		if enemy_active:
			roll_label.text = "Voce: d20 %d/%d\nAguardando resposta do alvo" % [roll, target]
		else:
			roll_label.text = "Voce: d20 %d/%d\nAlvo derrotado" % [roll, target]
		title_label.text = "Voce acertou: %d de dano" % damage
	else:
		roll_label.text = "Voce: d20 %d/%d\nAguardando resposta do alvo" % [roll, target]
		title_label.text = "Voce errou o ataque"

	if enemy_active:
		await get_tree().create_timer(0.7).timeout
		if enemy_roll_value != null:
			await animate_roll("Alvo", enemy_roll, enemy_target)

	character_state = final_state
	enemy_state = {
		"hp": int(final_state.get("enemy_hp", 0)),
		"hp_max": int(final_state.get("enemy_hp_max", 10)),
	}
	apply_character_ui()
	update_enemy_ui()
	if enemy_active:
		var player_summary := "postura defensiva" if action == "defend" else "d20 %d/%d" % [roll, target]
		if action == "recover":
			player_summary = "recuperacao +%d fadiga" % int(character_state.get("fatigue_recovered", 0))
		roll_label.text = "Voce: %s\nAlvo: d20 %d/%d" % [
			player_summary,
			enemy_roll,
			enemy_target,
		]
		if enemy_success:
			append_combat_history("R%d: %s | alvo causou %d dano" % [round_number, player_summary, enemy_damage])
			combat_log_label.text = "O alvo respondeu e causou %d de dano. Fadiga gasta: %d." % [
				enemy_damage,
				int(character_state.get("fatigue_spent", 0)),
			]
		else:
			append_combat_history("R%d: %s | alvo errou" % [round_number, player_summary])
			combat_log_label.text = "O alvo errou. Fadiga gasta: %d." % int(character_state.get("fatigue_spent", 0))
	else:
		append_combat_history("R%d: acao | alvo derrotado" % round_number)
		combat_log_label.text = "Alvo derrotado. Fadiga gasta: %d." % int(character_state.get("fatigue_spent", 0))

	if not hero_active or not enemy_active:
		if hero_active:
			title_label.text = "Vitoria!"
			combat_log_label.text = "O alvo foi derrotado."
		else:
			title_label.text = "Derrota"
			combat_log_label.text = "Seu personagem caiu."
		start_game_button.text = "Jogar novamente"
		start_menu.visible = true
		start_button.disabled = true
		defense_button.disabled = true
		special_button.disabled = true
		recover_button.disabled = true
		return true

	round_number += 1

	return true


func apply_engine_response(raw_response: Variant) -> bool:
	var json := JSON.new()

	if json.parse(str(raw_response).strip_edges()) != OK:
		print("JSON inválido recebido do Engine: ", raw_response)
		return false

	if not (json.data is Dictionary):
		print("Engine retornou dados em formato inesperado.")
		return false

	character_state = json.data

	apply_character_ui()

	return true


func apply_character_ui() -> void:
	vida_bar.max_value = int(character_state.get("hp_max", 0))
	vida_bar.value = int(character_state.get("hp", 0))
	fadiga_bar.max_value = int(character_state.get("fatigue_max", 0))
	fadiga_bar.value = int(character_state.get("fatigue", 0))
	vida_label.text = "Vida: %d/%d" % [
		int(character_state.get("hp", 0)),
		int(character_state.get("hp_max", 0)),
	]
	fadiga_label.text = "Fadiga: %d/%d" % [
		int(character_state.get("fatigue", 0)),
		int(character_state.get("fatigue_max", 0)),
	]


func update_enemy_ui() -> void:
	enemy_name_label.text = str(character_state.get("enemy_name", enemy_profiles[enemy_type]["name"]))
	enemy_vida_bar.max_value = int(enemy_state.get("hp_max", 10))
	enemy_vida_bar.value = int(enemy_state.get("hp", 0))
	enemy_vida_label.text = "Alvo: %d/%d" % [
		int(enemy_state.get("hp", 0)),
		int(enemy_state.get("hp_max", 10)),
	]


func append_combat_history(entry: String) -> void:
	combat_history.append(entry)
	while combat_history.size() > 4:
		combat_history.pop_front()
	combat_log_label.text = "\n".join(combat_history)


func animate_roll(actor: String, final_roll: int, target: int) -> void:
	for _step in range(5):
		var preview_roll := randi_range(1, 20)
		die_label.text = "D20\n%d" % preview_roll
		roll_label.text = "%s: d20 %d/%d" % [actor, preview_roll, target]
		await get_tree().create_timer(0.08).timeout
	die_label.text = "D20\n%d" % final_roll
	roll_label.text = "%s: d20 %d/%d" % [actor, final_roll, target]


func _on_button_pressed() -> void:
	execute_attack()


func _on_defense_button_pressed() -> void:
	execute_defend()


func _on_special_button_pressed() -> void:
	execute_special()


func _on_recover_button_pressed() -> void:
	execute_recover()

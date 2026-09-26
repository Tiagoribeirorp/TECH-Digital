extends Control

@onready var title_label: Label = $Label
@onready var start_button: Button = $Button
@onready var vida_bar: ProgressBar = $VidaBar
@onready var fadiga_bar: ProgressBar = $FadigaBar

func _on_button_pressed() -> void:
	title_label.text = "Ação realizada!"
	vida_bar.value = max(0, vida_bar.value - 10)
	fadiga_bar.value = min(100, fadiga_bar.value + 10)
	start_button.text = "Executar ação"

run_parser:
	python -m parser
export_requirements:
	poetry export -f requirements.txt --output requirements.txt
run_bot:
	python -m bot

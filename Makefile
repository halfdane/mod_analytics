SHELL := /bin/bash
REQUIREMENTS_TXT=python/requirements.txt

.PHONY: run test clean setup force_pull bot
run: setup
	$(VENV)/python python/historical_mod_data.py

bot: force_pull run

force_pull:
	git fetch --all
	git reset --hard origin/main
	git pull --rebase

clean: clean-venv
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete
	rm -rf .pytest_cache

install:
	mkdir -p ~/.config/systemd/user/
	cp python/mod_analytics.service ~/.config/systemd/user/
	systemctl --user daemon-reload
	systemctl --user enable mod_analytics.service
	systemctl --user start mod_analytics.service
	loginctl enable-linger

setup: venv

include Makefile.venv
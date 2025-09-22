include .env
export $(shell sed 's/=.*//' .dev.env)
.PHONY: run stop

run:
	uvicorn app.main:app --host $(HOST) --port $(PORT) --reload --env-file .dev.env

format:
	./format.sh

stop:
	@echo "Stopping server"
	@taskkill /F /IM python.exe /T > nul 2>&1 || echo "No processes found"
	@echo "Server stopped"
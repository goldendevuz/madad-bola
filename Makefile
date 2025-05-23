init-env:
	uv run3 -m venv env
act-env:
	. env/bin/activate
i:
	pip install --upgrade pip && pip install -r requirements.txt
mig:
	uv run manage.py makemigrations && uv run manage.py migrate
cru:
	uv run manage.py createsuperuser --username=goldendev --email=goldendev@gmail.com
webhook:
	uv run manage.py setwebhook
run:
	uv run uvicorn core.asgi:application --host 0.0.0.0 --port 1025 --reload
clear:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
no-db:
	rm -rf db.sqlite3
re-django:
	pip3 uninstall Django -y && pip3 install Django
re-mig:
	make no-db && make clear && make re-django && make mig && make cru && make run
collect:
	uv run manage.py collectstatic --noinput

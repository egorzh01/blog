tw:
	cd theme/ && npx @tailwindcss/cli -i ./style.css -o ./static/css/style.css --watch && cd ../../

run:
	python manage.py migrate && python manage.py runserver
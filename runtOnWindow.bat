python -m venv .venv
. ./.venv/Scripts/activate
pip install -r ./requirements.txt
echo "yes" | python manage.py flush
python manage.py runserver

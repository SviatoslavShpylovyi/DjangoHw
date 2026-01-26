# Car Rental Web Application
## Setup
```bash
git clone <repo-url>
cd DjangoHw/Rent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create // CREATES Fake Data
python manage.py runserver
http://127.0.0.1:8000/
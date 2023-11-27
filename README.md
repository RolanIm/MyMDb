# MyMDb API
### API для сервиса оценки произведений

<p align="center">
<img src="https://img.shields.io/badge/Python-100000?style=for-the-badge&logo=python&logoColor=FFFFFF&labelColor=306998&color=black">
<img alt='django' src='https://img.shields.io/badge/django-100000?style=for-the-badge&logo=django&logoColor=white&labelColor=123524&color=black'/>
<img alt='DRF' src='https://img.shields.io/badge/Rest framework-100000?style=for-the-badge&logo=django&logoColor=white&labelColor=a52a2a&color=black'/>
</p>

Clone the repository to your computer:

```
git clone https://github.com/RolanIm/MyMDb.git
```

Install and create the virtual environment:

```
python3 -m venv venv
```

Activate a virtual environment:
- for windows:

  ```
  source venv/Scripts/activate
  ```
- for Unix/macOS:

  ```
  source venv/bin/activate
  ```

Install dependencies from the file requirements.txt: 

```
pip install -r requirements.txt
```

Make migrations

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Run the `manage.py` file: 

```
python manage.py runserver
```

API Documentation: http://127.0.0.1:8000/redoc

---
## Author
### [_Rolan Imangulov_](https://github.com/RolanIm)

---
## License

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
# Terminology - сервис терминологии 
Сервис предоставляет API доступа и администрирования НСИ.

### Используемые технологии:
Python 3.8.6  
Django 3.2.12  
Django REST Framework 3.12.4  
drf-yasg==1.20.0 

## Запуск приложения локально через сервер разработки Django:

Клонируйте репозиторий и перейдите в него в командной строке:
```bash
git clone git@github.com:uprofound/terminology.git
cd terminology
```

Перейдите в каталог backend, создайте и активируйте виртуальное окружение:
```bash
cd backend
python3 -m venv .venv
source env/bin/activate
```

Установите зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Подготовьте файл переменных окружения .env -  
скопируйте шаблон из файла .env.template:  
```bash
cp .env.template .env
```

заполните его следующими данными:  
```
SECRET_KEY=your_key  # секретный ключ Django (укажите свой)

# Опционально:
# DEBUG=True  # default=False
# ALLOWED_HOSTS=localhost, 127.0.0.1  # перечислить через запятую,
                                        default='127.0.0.1'

# Если не заполнять следующее - БД запустится на движке sqlite3
# DB_ENGINE=django.db.backends.postgresql_psycopg2  # движок базы данных
# POSTGRES_DB=postgres_db  # имя базы данных (укажите своё)
# POSTGRES_USER=postgres  # логин для подключения к базе данных (укажите свой)
# POSTGRES_PASSWORD=postgres  # пароль для подключения к БД (установите свой)
# DB_HOST=localhost  # хост сервиса
# DB_PORT=5432  # порт для подключения к БД
```

Выполните миграции:
```bash
python3 manage.py migrate
```

Запустите проект:
```bash
python3 manage.py runserver
```

Теперь сервис доступен по адресу <http://127.0.0.1:8000/api/>,  
а документация по API - по адресам:  
<http://127.0.0.1:8000/api/docs/swagger/> - в формате Swagger и  
<http://127.0.0.1:8000/api/docs/redoc/> - в формате ReDoc.

### Создание суперпользователя

Администрирование сервиса доступно только пользователю с правами админа.  
Для создания суперпользователя выполните команду:
```bash
python3 manage.py createsuperuser
```

Теперь возможна авторизация в админ-зоне по адресу <http://127.0.0.1:8000/admin/>.

Для наполнения базы данных тестовыми данными выполните команду:
```bash
python3 manage.py load_data
```


## Запуск приложения локально в docker-контейнерах:

Опционально:  
установка docker и docker-compose:
```bash
sudo apt install docker.io
sudo apt install docker-compose
```

Клонируйте репозиторий и подготовте файл переменных окружения .env 
в каталоге backend, заполнив его полностью в соответствии с 
шаблоном .env.template (см. пункты выше) 
 
Перейдите в каталог infra :
 ```bash
cd ../infra
```

Запустите приложение в docker-контейнерах:
```bash
docker-compose up -d --build
```

Выполните миграции и сбор статики:
```bash
docker-compose exec backend python3 manage.py migrate
docker-compose exec backend python3 manage.py collectstatic --no-input
```

Теперь сервис доступен по адресу <http://127.0.0.1/api/>,  
а документация по API - по адресам:  
<http://127.0.0.1/api/docs/swagger/> - в формате Swagger и  
<http://127.0.0.1/api/docs/redoc/> - в формате ReDoc.

### Создание суперпользователя
```bash
docker-compose exec backend python3 manage.py createsuperuser
```

Теперь возможна авторизация в админ-зоне по адресу <http://127.0.0.1/admin/>.

Для наполнения базы данных тестовыми данными выполните команду:
```bash
docker-compose exec backend python3 manage.py load_data
```

### Остановка работы всех контейнеров

Выполните команду:

```bash
docker-compose down
```

Остановка работы контейнеров с удалением volumes и images:
```bash
docker-compose down --volumes --rmi <all|local>
```
___________________________________

*Реализовано: uprofound*

# Установка и запуск

Нужны Python 3.14 и запущенный PostgreSQL 18. Команды выполняются в PowerShell. База — `pc_architect`, пользователь — `postgres`, адрес — `127.0.0.1:5432`.

## Получение проекта

Скачайте репозитории `pc-architect-frontend`, `pc-architect-backend`, `pc-architect-docs` в соседние папки `frontend`, `backend`, `documentation`. Загрузчик `get_project.py` делает это одной командой — см. [README](README.md).

## Первая установка

Из общей папки с репозиториями:

```powershell
cd backend
& "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

$pgPassword = Read-Host "Пароль PostgreSQL" -AsSecureString
$env:PGPASSWORD = [System.Net.NetworkCredential]::new("", $pgPassword).Password
Remove-Variable pgPassword

& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres -h 127.0.0.1 -p 5432 -E UTF8 pc_architect
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_catalog
.\.venv\Scripts\python.exe manage.py runserver
```

Если `.venv` на Python 3.14 уже создано, пропустите создание окружения. Если база существует, пропустите `createdb`. При другой папке установки Python или PostgreSQL измените путь к программе.

`migrate` создаёт таблицы. `seed_catalog` читает `backend/core/fixtures/components.json` и добавляет 7 категорий и 21 комплектующее; повторный запуск не создаёт дубликаты и не перезаписывает записи.

Откройте `http://127.0.0.1:8000/`. Остановка сервера — `Ctrl+C`.

## Обычный запуск

Запустите PostgreSQL. Из общей папки с репозиториями выполните:

```powershell
cd backend
$pgPassword = Read-Host "Пароль PostgreSQL" -AsSecureString
$env:PGPASSWORD = [System.Net.NetworkCredential]::new("", $pgPassword).Password
Remove-Variable pgPassword
.\.venv\Scripts\python.exe manage.py runserver
```

Пароль роли `postgres` вводится скрыто и действует в этом окне терминала. В новом окне его нужно задать снова. Активация `.venv` не задаёт пароль БД. При другом подключении задайте `PGHOST`, `PGPORT`, `PGUSER` и `PGDATABASE`. Файл `.env` автоматически не читается.

## После обновления проекта

Остановите сервер и из `backend`, с заданным паролем БД, выполните:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

## Частые ошибки

| Ошибка | Что сделать |
| --- | --- |
| `no password supplied` | Введите пароль по блоку «Обычный запуск» в текущем терминале |
| `password authentication failed` | Проверьте пользователя и пароль PostgreSQL |
| `connection refused` | Запустите PostgreSQL, проверьте адрес и порт |
| Нет базы / таблиц | Выполните `createdb` / `migrate` |
| `no pq wrapper available` | При смене версии Python переименуйте старое `.venv`, создайте чистое и установите зависимости |
| Пустой каталог | Выполните `seed_catalog` и повторите загрузку на сайте |

Если фронтенд находится не в соседней папке `frontend`, задайте `$env:FRONTEND_DIR = "D:\путь\к\фронтенду"` перед запуском Django. Документация для запуска сайта не требуется.

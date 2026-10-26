"""Clone all PC ARCHITECT repositories into one workspace; do not overwrite files."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess


REPOSITORIES = {
    "frontend": "pc-architect-frontend",
    "backend": "pc-architect-backend",
    "documentation": "pc-architect-docs",
}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Скачать три репозитория PC ARCHITECT одной командой. Требуется Git.")
    parser.add_argument("--user", required=True, help="Владелец репозиториев на GitHub")
    parser.add_argument("--directory", default="pc-architect", help="Новая или пустая папка проекта")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", args.user):
        parser.error("Укажите логин GitHub, а не URL.")
    destination = Path(args.directory).expanduser().resolve()
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        parser.error("Папка назначения должна быть новой или пустой; существующие файлы не изменяются.")
    git = shutil.which("git")
    if git is None and os.name == "nt":
        candidate = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/cmd/git.exe"
        if candidate.is_file():
            git = str(candidate)
    if git is None:
        parser.error("Не найден Git. Установите Git и повторите запуск.")
    destination.mkdir(parents=True, exist_ok=True)
    for folder, repository in REPOSITORIES.items():
        url = f"https://github.com/{args.user}/{repository}.git"
        subprocess.run([git, "clone", "--", url, str(destination / folder)], check=True)
    print(f"Готово: {destination}")
    print("Настройка и запуск: backend/README.md")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        raise SystemExit("Не удалось клонировать репозиторий. Проверьте доступ и названия. Уже скачанные файлы сохранены.")

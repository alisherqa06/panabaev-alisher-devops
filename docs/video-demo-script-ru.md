# Сценарий видеодемонстрации (10-20 минут)

**Статус подготовки (19 октября 2026):** четыре пользовательских аудиозаписи оставались только на этом компьютере. Подходящей локальной модели клонирования голоса нет. Обычные русские голоса Windows перечисляются системой, но локальная попытка синтеза завершилась ошибкой, поэтому готовой озвучки нет. Средства записи экрана и кодирования MP4 не обнаружены; готового видео и реальных файлов захвата экрана нет. Черновые субтитры `video-demo-subtitles-ru.srt` содержат оценочные тайм-коды и требуют синхронизации с фактической записью. Используйте собственный голос для сдачи, если методичка требует именно его.

Запишите одно непрерывное видео с экраном и своим голосом. Перед началом откройте Windows Terminal, Docker Desktop и Jenkins в браузере. Убедитесь, что приложение доступно на `http://localhost:8080`, Jenkins - на `http://localhost:8081`, а build #2 job `Panabaev_Alisher_DevOps` завершился с `Finished: SUCCESS`. Не показывайте пароли, токены и секретные настройки.

## План записи

1. **Вступление (около 1 минуты).** Скажите: «Меня зовут Alisher Panabaev, группа It2-2308, ID 37332. Я покажу DevOps лабораторную: Linux, Git и GitHub, Docker и Jenkins».
2. **Linux (2 минуты).** В Ubuntu выполните:

   ```bash
   cd /home/acer/devops/panabaev_alisher
   pwd
   find . -maxdepth 2 -type f
   ./scripts/Panabaev_Alisher_system.sh
   grep -c ERROR logs/application.log
   grep -c WARNING logs/application.log
   stat -c '%a %n' private.txt public.txt
   ps aux | head
   ```

   Коротко объясните назначение каталогов, поиск по журналу и разницу прав `600` и `644`.
3. **Git и GitHub (1 минута).** Покажите `git status --short --branch`, `git log --oneline --decorate -6` и страницу репозитория на GitHub. Объясните, что Git фиксирует версии, а GitHub хранит удалённую копию и даёт Jenkins источник по выбранному коммиту.
4. **Приложение и тесты (1-2 минуты).** Покажите `app/server.py`, затем выполните `python3 -m unittest discover -s tests -v`. Объясните, что значения берутся из переменных среды и отображаются через HTTP.
5. **Docker (2 минуты).** Покажите `docker images`, `docker ps`, `docker ps -a`, `docker logs panabaev-alisher-container`; затем откройте `http://localhost:8080`. При необходимости выполните `docker exec panabaev-alisher-container python -c 'print("container exec works")'`. Объясните: image - шаблон, container - запущенный экземпляр.
6. **Docker Compose (около 1 минуты).** Покажите `docker compose ps` и `docker compose logs`. Если нужно повторить запуск, сначала используйте `docker compose down`, потом `docker compose up --build -d`.
7. **Jenkins (2-3 минуты).** Покажите Dashboard, job `Panabaev_Alisher_DevOps`, все пять зелёных стадий и Console Output build #2. Найдите в выводе значения студента, исходный Git commit `d60133d` и `Finished: SUCCESS`. Коротко расскажите, что в первом запуске URL `127.0.0.1` из контейнера Jenkins указывал на сам Jenkins; проверка приложения исправлена на `host.docker.internal` и повторный запуск прошёл. Объясните, что падение обязательной команды останавливает последующие стадии и делает сборку неуспешной.
8. **Завершение (около 1 минуты).** Покажите страницу приложения, репозиторий и чек-лист. Скажите, какие части процесса выполняются автоматически.

## Репетиция команд перед записью

```bash
git status --short --branch
git log --oneline --decorate -6
python3 -m unittest discover -s tests -v
docker images
docker ps
docker ps -a
docker logs panabaev-alisher-container
```

Проверьте, что вкладки браузера не показывают учётные данные. Видео записывает сам студент; этот файл является только сценарием.

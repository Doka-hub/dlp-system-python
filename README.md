# DLP System on Python

---
### Description
Минимальная версия системы по поиску потенциально важных данных в Slack,
основанная на регулярных выражениях и написанная на Django. 

Сервис написан с учетом возможности расширения. 

На данный момент для поиска данных в файлах подерживаются следующие
типы:
- csv
- docx
- txt

После нахождения потенциально важных данных сообщение изменяется,
а файлы, содержащие эти данные удаляются.

### Quickstart


1. Скопировать .envs
```
cp .env.local.dist .env.local
cp .env.local.db.dist .env.local.db
```
2. Заполнить `SLACK_USER_TOKEN` (User OAuth Token) в .env.local
![](../../Desktop/Снимок экрана 2023-02-12 в 09.48.02.png)
3. Запустить
```
docker-compose -f docker-compose.local.yml up -d --build
```
4. Создать суперпользователя, regex-шаблон в админке
5. Чтобы посмотреть на результат работы системы нужно написать текст, отправить поддерживаемый файл (системой) в Slack
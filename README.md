# DLP System on Python

---
### Description
MVP service to search potentionality important data in Slack channels based on regular expresses and written in Django.

Service developed with the capability to easily expand it.

Now, it supports these types of files:
- csv
- docx
- txt


After finding important data the message is altered, and files and the files containing these data are deleted.
### Quickstart


1. Copy .envs
```
cp .env.local.dist .env.local
cp .env.local.db.dist .env.local.db
```
2. Fill `SLACK_USER_TOKEN` (User OAuth Token) in .env.local
![](../../Desktop/Снимок экрана 2023-02-12 в 09.48.02.png)
3. Start
```
docker-compose -f docker-compose.local.yml up -d --build
```
4. Create superadmin, regex-template in admin panel `/admin`
5. To check the result of service working, you should send some important data

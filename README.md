# Доска объявлений

## Основные моменты
Приложение является API бэкэндом приложения Доска объявлений

* Есть Объявление и Отзыв(прикрепляется к объявлению)
* Реализован поиск по объявлениям по критериям: название(title), цена(price) и описание(description).
* Реализована авторизация по Bearer-токену
* У пользователя может быть 2 роли - user(обычный пользователь) и admin(администратор)
  * user может просматривать объявления/отзывы, создавать объявления/отзывы, но менять их или удалять может только admin
* Пользователь может сбросить пароль от аккаунта
  * `~/reset_password/` - запрос на зброс
  * `~/reset_password_confirm/` - подтверждение сброса по id и токену с письма на почту + новый пароль
* Реализовано уведомление через почту о новом отзыве под объявлением пользователя

### Локальный деплой
Шаги:
1. Запустить Docker приложение
2. Логин в Docker Hub (если необходим)
    * в cmd-консоле `docker login -u <docker hub username>`, потом ввести токен от Docker Hub
3. `docker compose -f docker-compose.local.yml up --build` - запустить контейнер с билдом из `docker-compose.local.yml` для локального деплоя
4. В браузере перейти на  `localhost`


### Деплой на сервер
В ДАННЫЙ МОМЕНТ деплой происходит при любом push и проект берется из ветки `feature/local_and_server_deploy`.
Проект уже задеплоен на сервер: `http://130.193.57.240`

`На сервере уже создан тестовый superuser admin@mail.com, пароль 1234`

Шаги для самостоятельного деплоя:
1. Сделать свой `.env` из `.env.samles`
2. Создать и настроить свой сервер (например на Яндекс Cloud). Прописать в консоле сервера ВМ:
   * `sudo apt update`
   * `sudo apt upgrade`
   * скачать Docker по официальному туториалу https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
   * открыть порты в файрволе:
     * `sudo ufw status` - проверка статуса
     * `sudo ufw enable` - если статус `Status: inactive` - активирует `ufw` 
     * `sudo ufw allow 80/tcp 443/tcp 22/tcp` - открытие портов 443, 80 и 22
     * `sudo ufw status` - проверка открытия портов, должно быть:
     ```
       Status: active

       To                         Action      From
       --                         ------      ----
       22,80,443/tcp              ALLOW       Anywhere
       22,80,443/tcp (v6)         ALLOW       Anywhere (v6)
     ```
3. Настройка GitHub Secrets:
   * `SSH_USER` - юзер сервера
   * `SSH_KEY` - приватный SSH
   * `SERVER_IP` - публичный IP сервера
   * `ENV_FILE` - твой .env файл с данными
   * `DOCKER_HUB_USERNAME` и `DOCKER_HUB_ACCESS_TOKEN` - юзернейм и токен от Docker Hub
   * `DEPLOY_DIR` - директория для деплоя на сервере (`/home/<SSH_USER>/<название>`)
   * `DOC_COMP_DEPLOY` - `docker-compose.deploy.yml` из корня проекта (так проще)
   * `NGINX_CONF` - `Dockerfiles/nginx/nginx.conf`
4. Также важно добавить пользователя `SSH_USER` в группу `docker` на сервере
   * `getent group docker` - проверить, есть ли группа `docker` (если нет никакого output, то создать - `sudo groupadd docker`)
   * `sudo usermod -aG docker <username>` - добавление <username> в группу
   * перезайти на сервер
   * еще раз `getent group docker` - проверка, должно быть что-то вроде `docker:x:999:<username>`

Можно пользоваться
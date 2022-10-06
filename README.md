# VKinder
## Для корректной работы
Необходимо добавить файл `.env` в основной каталог программы со следующими параметрами:
* `token='токен вашего бота'`\ - Как получить токен описанно ниже
* `VKtoken='токен вашего приложения VK'` - Как получить токен описанно ниже

Необходимо добавить файл `.env` в каталог `\db\` со следующими параметрами:
* `USER_="имя пользователя PostgreSQL"`
* `PASSWORD="пароль пользователя PostgreSQL"`
* `HOST="хост"`
* `PORT=порт`

## Получение токена
* `token`: 

> на странице https://vk.com/apps?act=manage создать новое приложение и скопировать `ID приложения`

> Перейти по ссылке 

https://oauth.vk.com/authorize?client_id=1&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,offline&response_type=token&v=5.131&state=123456

> изменив параметр `cliend_id` на `ID приложения`

* `VKtoken`:
 
> [инструкция](https://docs.google.com/document/d/1_xt16CMeaEir-tWLbUFyleZl6woEdJt-7eyva1coT3w/edit?usp=sharing)

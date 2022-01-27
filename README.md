# **VKFriendParser**:
Инструмент для парсинга друзей вконтакте, выводит необходимую информацию о друзьях выбранного 
пользователя Вконтакте с возможностью экспортирования данных в .csv, .json, .tsv или другие форматы.


## _Получение токена_: 

В первую очередь необходимо получить токен авторизированного пользователя ВКонтакте, 
для этого перейдём по ссылке https://vkhost.github.io/ , выберем "vk.com", разрешим доступ
для выбранного приложения, после чего копируем ссылку от "access_token=" до "&expires_in",
скопированный элемент и будет являться нашим токеном.

## _Инструкция по применению_:

Полученный токен передаётся параметром --token=<token>, id пользователя, по которому хотим 
выполнять парсинг передаётся через параметр --user_id=<user_id>. Пример запуска: 
>python main.py --token=123 --user_id=777

После чего необходимо составить список данных пользователя вконтакте, которые мы хотим выводить:
  1. Имя;
  2. Фамилия;
  3. Название страны;
  4. Название города;
  5. Дата рождения;
  6. Пол;

что будет соответствовать списку ['first_name', 'last_name', ('country', 'title'), ('city', 'title'), 'bdate', 'sex'].

Далее создадим объект класса VKFriendParser, в его параметры передаём полученный токен, id пользователя и список полей.
Получаем объект класса VKFriendParser, у полученного объекта вызываем метод get_friends_data(), куда будут сохранены данные друзей
в формате списка со словарями. 

Полученный список можем экспортировать в нужном формате, для этого вызовем функцию report, первым аргументом передадим список, вторым 
поля в формате списка, третьим необязательным параметром является формат экспорта данных (.csv, .json, .tsv, .yaml), четвёртым необязательным параметром
является директория сохранения отчёта, по умолчанию отчёт сохранятся в текущую директорию.

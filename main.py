# -*- coding: utf8 -*-

import csv
import os

import vk

from config import token, user_id


class VKFriendParser(object):
    def __init__(self, token, user_id, fields):
        """Инициализация токена для авторизации, id пользователя,
        по которому будет совершаться парсинг, поля
        по которым будет совершаться парсинг


        :param: token: токен пользователя для авторизации
        :param: user_id: id пользователя, по которому будет парсинг
        :param: fields: поля по которым будет парсинг, преобразованный в обычный список
        path_to_file: путь к переменным для полей country, city

        так как поля country, city, education и т.д. имеют вложенные словари
        без возможности их получение через get запрос, то 'доставать' их приходится
        непосредственно после получения, переменная path_to_file хранит путь к названию
        города и страны

        :NoReturn:


        """

        self.token = token
        self.user_id = user_id
        self.fields = fields_to_list(fields)

        self.path_to_fields = self.getting_the_path(fields)

        self.vkapi = self.auth()


    def getting_the_path(self, lst):
        """Получение пути для вложенных полей

        :param: lst: список полей или кортежей с полями
        :return: dict: возвращает словарь с путями к полям


        """
        new_dct = {}
        for x in lst:
            if len(x) == 2:
                new_dct.update({x[0]: x[1]})
        return new_dct



    def auth(self):
        """Авторизация пользователя через токен с указанием версии API


        Возвращает VK сессию, при верном токене

        :return: vk.API


        """

        session = vk.Session(access_token=self.token)
        return vk.API(session, v='5.131')

    def __raw_friends_data(self):
        """Получение 'сырых' данных


        Помимо полей указанных в fields парсер возвращает лишние
        данные, такие как 'id', 'can_access_closed', 'track_code' и т.д.,


        На данном этапе происходит авторизация пользователя по токену,
        если токен неверный, ошибка вылетит в этом месте. Также, если
        аккаунт закрытый или пользователь не имеет друзей, ошибки появятся
        в это части кода

        :return: [({'id':str, 'first_name': str, ...}, {...}, ...)] список
        словарей со всеми данными


        """
        try:
            return self.vkapi('friends.get', user_id=self.user_id,
                              fields=self.fields, order='name')['items']
        except Exception as e:
            print(e)

    def get_friends_data(self):
        """Обработка сырых данных

        lst: список полученных 'сырых' данных

        :return: [({'first_name': str, ...}, {...}, ...)]
        изменённый список без лишних данных


        """

        lst = self.__raw_friends_data()  # получение списка со словарями
        for dct in lst:  # для каждого словаря в списке
            for kv in list(dct):  # для каждой пары в словаре
                # используется копия, так как изменение словаря во время его перебора вызовет ошибку
                if kv not in self.fields:  # если ключ не в списке необходимых данных fields
                    dct.pop(kv)  # то удаляем пару
                else:
                    if kv in self.path_to_fields:  # если ключ находится в списке с вложенными данными
                        #  то вытаскиваем вложенные данные через ключ, заменяя вложенный словарь полученным значением
                        dct.update({kv: dct[kv][self.path_to_fields[kv]]})
            for field in self.fields:  # расстановка 'Null' значений, если параметр указан для парсинга, но
                # отсутствует у друга
                if field not in dct.keys():
                    dct.update({field: 'Null'})
                elif field == 'bdate':  # если поле является датой рождения, то сохраняем в iso формате
                    dct.update({field: to_isoformat(dct[field])})
        return lst


def report(list_of_dicts, fields, format='csv', directory=os.path.abspath(os.curdir)):
    """Составление отчёта в указанном формате

    :param: list_of_dicts: список со словарями для импорта
    :param: fields: список с полями, необходим для правильного порядка колонок
    :param: format: формат сохранения данных
    :param: directory: путь сохранения отчёта, по умолчанию текущая директория

    По умолчанию отчёт сохраняется в формате '.csv' в текущем каталоге,
    при изменении поля format изменится формат сохранения отчёта


    При сохранения файла в кодировке 'utf-8', может возникнуть ошибка,
    если у друга в имени или фамилии есть символы, не поддерживаемые
    форматом консоли, .csv, .json и т.д.


    :NoReturn:


    """

    FullPath = os.path.join(directory, fr'{directory}\report.{format}')  # объединение имени файла и директории

    with open(FullPath, 'w', newline='', encoding="cp1251") as file:  # сохранение файла
        # в кодировке 'cp1251'
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=',')  # за названия столбцом примем поля
        # для парсинга fields
        writer.writeheader()  # составить столбцы
        for row in list_of_dicts:  # записать строки
            writer.writerow(row)

def fields_to_list(lst):
    """Преобразование списка с вложенными полями к
    списку без вложенных полей


    :param: lst: список с кортежами

    :return: lst: список без вложенных полей


    """

    new_lst = []
    for x in lst:
        if len(x) == 2:
            new_lst.append(x[0])
        else:
            new_lst.append(x)
    return new_lst


def to_isoformat(data):
    """Переход даты формата %d.%m.%y к формату yyyy-mm-dd

    :param: data: строка с даты рождения формата %d.%m.%y


    :return: str: формат даты yyyy-mm-dd


    """
    if data != 'Null':  # вернуть 'Null' если дата рождения отсутствует
        data = data.split('.')
        for i in range(len(data)):
            if len(data[i]) < 2:
                data[i] = '0' + data[i]  # так как дата рождения полученная
                # через vkapi может иметь вид 1.6.1999, добавим '0' там, где его не хватает
        if len(data) > 2:
            return f'{data[2]}-{data[1]}-{data[0]}'  # если есть день, месяц и год рождения
        else:
            return f'{data[1]}-{data[0]}'  # если нет года рождения
    else:
        return 'Null'


if __name__ == '__main__':
    fields = ['first_name', 'last_name', ('country', 'title'), ('city', 'title'), 'bdate', 'sex']
    columns = fields_to_list(fields)
    parser = VKFriendParser(token, user_id, fields)
    data = parser.get_friends_data()
    print(data)
    report(data, fields=columns, format='csv')
    report(data, fields=columns, format='json')
    report(data, fields=columns, format='tsv')
    report(data, fields=columns, format='yaml')




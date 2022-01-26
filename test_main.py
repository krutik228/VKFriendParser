import unittest
from main import VKFriendParser, report, to_isoformat, fields_to_list
from config import token, user_id


class TestVKFriendParser(unittest.TestCase):
    def setUp(self) -> None:
        fields = ['first_name', 'last_name', ('country', 'title'), ('city', 'title'),
                  'bdate', 'sex']
        self.parser = VKFriendParser(token, user_id, fields)

    def test_getting_the_path(self):
        self.parser.getting_the_path(self.parser.fields)

    def test_get_friends_data(self):
        self.data = self.parser.get_friends_data()

    def test_report_csv(self):
        data = [{1: 'test', 2: 'test2'}, {3: 'test3', 4: 'test4'}]
        fieldsnames = [1, 2, 3, 4]
        report(data, fieldsnames, 'csv', name='test_report')

    def test_report_json(self):
        data = [{1: 'test', 2: 'test2'}, {3: 'test3', 4: 'test4'}]
        fieldsnames = [1, 2, 3,4]
        report(data, fieldsnames, 'json', name='test_report')

    def test_report_tsv(self):
        data = [{1: 'test', 2: 'test2'}, {3: 'test3', 4: 'test4'}]
        fieldsnames = [1, 2, 3,4]
        report(data, fieldsnames, 'tsv', name='test_report')

    def test_to_isoformat(self):
        isodata = to_isoformat('1.5.2000')
        self.assertEquals(isodata, '2000-05-01')

    def test_fields_to_list(self):
        test_list = ['1', '2', ('3', '4'), '5']
        new_list = fields_to_list(test_list)
        self.assertEquals(new_list, ['1', '2', '3', '5'])

    def tearDown(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, Mock, MagicMock
import requests

from aot.trello import TrelloApiClient


class TestTrelloAPIClient(unittest.TestCase):
    def test__RequestApi(self):
        client = TrelloApiClient('apikey', 'apitoken')
        resp = client._RequestApi('', 'DELETE')
        self.assertEqual(resp, 0)

    @patch('requests.post')
    def test__add_card(self, mock: MagicMock):
        client = TrelloApiClient('apikey', 'apitoken')

        resp: requests.Response = requests.Response()
        resp.status_code = 400
        mock.return_value = resp
        self.assertIsNone(client._add_card('title', 'list_id'))

        json_mock = Mock()
        json_mock.return_value = {'id': 'xxx', 'name': 'title'}
        resp.json = json_mock
        resp.status_code = 200
        mock.return_value = resp

        actual = client._add_card('title', 'list_id')
        self.assertEqual(actual, 'title')

    def test_add_cards(self):
        client = TrelloApiClient('apikey', 'apitoken')

        card_titles = ['title1', 'title2', 'title3']
        client._add_card = Mock(side_effect=lambda x,
                                y: x if x != 'title3' else None)
        expected = ['title1', 'title2']
        actual = client.add_cards(card_titles, 'list_id')
        self.assertEqual(expected, actual)

    @patch('requests.get')
    def test_get_cards_on_list(self, mock):
        client = TrelloApiClient('apikey', 'apitoken')
        resp: requests.Response = requests.Response()
        resp.status_code = 400
        mock.return_value = resp
        self.assertEqual([], client.get_cards_on_list('list_id'))

        resp.status_code = 200
        resp.json = Mock(return_value=[{'id': 'xxx', 'name': 'title1'}, {
                         'id': 'yyy', 'name': 'title2'}])
        expected = [{'id': 'xxx', 'name': 'title1'},
                    {'id': 'yyy', 'name': 'title2'}]
        self.assertEqual(expected, client.get_cards_on_list('list_id'))

    @patch('requests.put')
    def test__close_card_by_id(self, mock):
        client = TrelloApiClient('apikey', 'apitoken')

        resp: requests.Response = requests.Response()
        resp.status_code = 400
        mock.return_value = resp
        self.assertIsNone(client._close_card_by_id('list_id'))

        resp.status_code = 200
        resp.json = Mock(return_value={'id': 'xxx', 'name': 'title1'})
        mock.return_value = resp
        expected = 'title1'
        self.assertEqual(expected, client._close_card_by_id('card_id'))

    def test_close_cards_by_title(self):
        client = TrelloApiClient('apikey', 'apitoken')

        cards_on_list = [
            {'id': 'xxx1', 'name': 'title1'},
            {'id': 'xxx2', 'name': 'title2'},
            {'id': 'xxx3', 'name': 'title1'}
        ]
        client.get_cards_on_list = Mock(return_value=cards_on_list)

        def _close_by_id(id):
            for cards in cards_on_list:
                if cards['id'] == id:
                    return cards['name']
            return None
        client._close_card_by_id = Mock(side_effect=_close_by_id)

        card_title = ['title1', 'title2', 'title3']
        expected = ['title1', 'title2']
        actual = client.close_cards_by_titles(card_title, 'list_id')
        self.assertEqual(expected, actual)

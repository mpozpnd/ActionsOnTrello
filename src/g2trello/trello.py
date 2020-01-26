from typing import List

import requests
import logging

logger = logging.getLogger(__file__)

BASE_ENTRY_POINT = 'https://api.trello.com/1'


class TrelloApiClient:
    def __init__(self, key, token):
        self._key = key
        self._token = token

    def _RequestApi(self, url, method, data={}):
        data['key'] = self._key
        data['token'] = self._token

        resp = 0
        if method == 'GET':
            resp = requests.get(url, data=data)
        elif method == 'POST':
            resp = requests.post(url, data=data)
        elif method == 'PUT':
            resp = requests.put(url, data=data)
        else:
            resp = 0

        return resp

    def _add_card(self, card_title: str, list_id: str):
        url = '%s/%s' % (BASE_ENTRY_POINT, 'cards')
        data = {
            'idList': list_id,
            'name': card_title
        }
        resp = self._RequestApi(url, 'POST', data=data)
        if resp.status_code == 200:
            card_title = resp.json()['name']
            logger.info('create card: %s' % card_title)
            return card_title
        else:
            logger.warning('')
            return None

    def add_cards(self, card_titles, list_id):
        added_cards = []
        for title in card_titles:
            added_cards.append(self._add_card(title, list_id))
        return list(filter(lambda x: x, added_cards))

    def get_cards_on_list(self, list_id: str):
        url = '%s/%s/%s/%s' % (BASE_ENTRY_POINT, 'list', list_id, 'cards')
        data = {
            'idList': list_id
        }
        resp = self._RequestApi(url, 'GET', data=data)
        if resp.status_code == 200:
            return [{'id': card['id'], 'name': card['name']} for card in resp.json()]
        else:
            return []

    def _close_card_by_id(self, card_id: str):
        url = '%s/%s/%s' % (BASE_ENTRY_POINT, 'cards', card_id)
        data = {
            'closed': 'true'
        }
        resp = self._RequestApi(url, 'PUT', data)
        if resp.status_code == 200:
            return resp.json()['name']
        else:
            return None

    def close_cards_by_titles(self, card_titles: List[str], list_id: str):
        cards = self.get_cards_on_list(list_id)
        closed_cards = []
        for title in card_titles:
            for card in cards:
                if card['name'] == title:
                    closed_cards.append(self._close_card_by_id(card['id']))
        return list(set(list(filter(lambda x: x, closed_cards))))

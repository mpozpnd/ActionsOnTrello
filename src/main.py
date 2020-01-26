import os
from logging import getLogger

from g2trello.trello import TrelloApiClient
from g2trello.utils import generate_response

logger = getLogger(__file__)


def add_card_to_trello(request):
    req = request.get_json()
    params = req['queryResult']['parameters']
    target_list = params['list']
    action = params['action']
    items = params['items'][0].split()

    if target_list not in ['shopping', 'todo']:
        return generate_response('リスト名が間違っています')

    if action not in ['add', 'delete', 'get']:
        return generate_response('追加, 削除, 一覧取得 が可能です')

    key = os.environ.get("TRELLO_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    shopping_list_id = os.environ.get("TRELLO_LIST_ID_SHOPPING")
    todo_list_id = os.environ.get("TRELLO_LIST_ID_TODO")
    client = TrelloApiClient(key, token)

    list_id = shopping_list_id if target_list == 'shopping' else todo_list_id
    if action == 'add':
        added_cards = client.add_cards(items)
        return generate_response('%sを追加しました' % ' '.format(added_cards))
    elif action == 'delete':
        deleted_cards = client.close_card_by_titles(list_id, items)
        return generate_response('%sを削除しました' % ' '.format(deleted_cards))
    elif action == 'gets':
        return generate_response(' '.format(client.get_cards_on_list(list_id)))

    return generate_response('')

class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    def __eq__(self, other): 
        return self.id == other.id and self.name == other.name and self.status == other.status

    @classmethod
    def from_trello_card(cls, card, list):
        return Item(card['id'], card['name'], list['name'])
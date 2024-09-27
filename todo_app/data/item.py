class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    def __eq__(self, other): 
        return self.id == other.id and self.name == other.name and self.status == other.status
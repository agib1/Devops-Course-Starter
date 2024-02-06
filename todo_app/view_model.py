class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items
    
    @property
    def done_items(self):
        return self.allocate_items("Done")
    
    @property
    def doing_items(self):
        return self.allocate_items("Doing")
    
    @property
    def todo_items(self):
        return self.allocate_items("To Do")
    
    def allocate_items(self, status):
        status_items = []
        for item in self._items:
            if item.status == status:
                status_items.append(item)
        return status_items

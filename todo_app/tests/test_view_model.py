import pytest
from todo_app.view_model import ViewModel
from todo_app.data.item import Item

@pytest.fixture
def view_model():
    items = [Item(1, "Write documentation" , "Done"), Item(2, "Program Function 1", "To Do"), Item(3, "Write unit tests", "Doing"),
             Item(4, "Create requirements" , "Done"), Item(5, "Program Function 2", "To Do"), Item(6, "Write integration tests", "Doing")]
    view_model = ViewModel(items)
    return view_model

correct_done_items = [Item(1, "Write documentation" , "Done"), Item(4, "Create requirements" , "Done")]
correct_doing_items = [Item(3, "Write unit tests", "Doing"), Item(6, "Write integration tests", "Doing")]
correct_todo_items = [Item(2, "Program Function 1", "To Do"), Item(5, "Program Function 2", "To Do")]

@pytest.mark.parametrize("correct_done_item", correct_done_items)
def test_view_model_done_property(view_model, correct_done_item):
    assert correct_done_item in view_model.done_items

@pytest.mark.parametrize("correct_doing_item", correct_doing_items)
def test_view_model_doing_property(view_model, correct_doing_item):
    assert correct_doing_item in view_model.doing_items

@pytest.mark.parametrize("correct_todo_item", correct_todo_items)
def test_view_model_todo_property(view_model, correct_todo_item):
    assert correct_todo_item in view_model.todo_items

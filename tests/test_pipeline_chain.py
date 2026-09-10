import sys

sys.path.insert(0, "scripts")
from pipeline_chain import LinkedList, UndoStack, Pipeline  # noqa: E402


def test_linked_list_append_order():
    chain = LinkedList()
    chain.append(1)
    chain.append(2)
    chain.append(3)
    assert chain.to_list() == [1, 2, 3]


def test_undo_stack_reverses_order():
    history = UndoStack()
    history.push("a")
    history.push("b")
    assert history.undo() == "b"
    assert history.undo() == "a"
    assert history.undo() is None


def test_pipeline_chains_stages():
    pipe = Pipeline()
    pipe.add_stage("double", lambda x: x * 2)
    pipe.add_stage("add_one", lambda x: x + 1)
    result = pipe.run(5)
    assert result == 11

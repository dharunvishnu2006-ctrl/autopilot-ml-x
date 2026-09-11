class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


chain = LinkedList()
chain.append(10)
chain.append(20)
chain.append(30)
print(chain.to_list())


class DNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class UndoStack:
    def __init__(self):
        self.top = None

    def push(self, action):
        new_node = DNode(action)
        new_node.prev = self.top
        self.top = new_node

    def undo(self):
        if self.top is None:
            return None
        action = self.top.value
        self.top = self.top.prev
        return action


history = UndoStack()
history.push("loaded data")
history.push("trained model")
history.push("evaluated model")
print(history.undo())
print(history.undo())
print(history.undo())
print(history.undo())


class Stage:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.next = None


class Pipeline:
    def __init__(self):
        self.head = None

    def add_stage(self, name, func):
        new_stage = Stage(name, func)
        if self.head is None:
            self.head = new_stage
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_stage

    def run(self, data):
        current = self.head
        while current is not None:
            print("running:", current.name)
            data = current.func(data)
            current = current.next
        return data


def load(_):
    return [5, 3, 9, 1]


def clean(data):
    return [x for x in data if x > 0]


def train(data):
    return sum(data) / len(data)


pipe = Pipeline()
pipe.add_stage("load", load)
pipe.add_stage("clean", clean)
pipe.add_stage("train", train)
result = pipe.run(None)
print("final result:", result)


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        self.tail = new_node

    def dequeue(self):
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value


runs = Queue()
runs.enqueue("run_1")
runs.enqueue("run_2")
runs.enqueue("run_3")
print(runs.dequeue())
print(runs.dequeue())
runs.enqueue("run_4")
print(runs.dequeue())
print(runs.dequeue())
print(runs.dequeue())

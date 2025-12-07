from tasknode import TaskNode
from datetime import date


class TaskTree:

    def __init__(self):
        self.root = TaskNode(0, "dummy", 30)
        self.last_id = 0
        self.max_level = 0
        self.max_length = 0

    def print(self):
        def print_task(task, level):
            task.print(level, self.max_level, self.max_length)
            for child in task.get_children():
                print_task(child, level + 1)

        print_task(self.root, 0)

    def add(self, parent: TaskNode = None, title: str = "", estimated_cost: int = None):
        existing_task = self.find_task(title)
        if existing_task:
            return existing_task
        if not parent:
            child = TaskNode(self.last_id + 1, title, estimated_cost, self.root)
            self.root.add_child(child)
            self.last_id += 1
            return child
        child = TaskNode(self.last_id + 1, title, estimated_cost, parent)
        parent.add_child(child)
        self.last_id += 1
        return child

    def find_task(self, title):
        def look(current_task, title):
            if current_task.title.lower().strip() == title.lower().strip():
                return current_task
            for child in current_task.get_children():
                return look(child, title)

        return look(self.root, title)

    def to_dict(self):
        task_tree = {"tasks": []}

        for child in self.root.get_children():
            task_tree["tasks"].append(child.to_dict())
        return task_tree

    def serialize_node(self, node, parent=None):
        due_date = date.fromisoformat(node["due_date"]) if node.get("due_date") else None
        node = TaskNode(self.last_id + 1, node["title"], node["estimated_cost"], parent, node["time_unit"], due_date)
        self.max_length = max(len(node.title), self.max_length)
        parent.add_child(node)
        self.last_id += 1
        return node

    def serialize(self, tree):
        def load(tree, parent):
            if len(tree) > 0:
                self.max_level += 1
            for node in tree:
                serialized_node = self.serialize_node(node, parent)
                load(node["children"], serialized_node)

        load(tree["tasks"], self.root)

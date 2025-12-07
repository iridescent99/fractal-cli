class TaskNode:

    def __init__(self, id, title, estimated_cost, parent=None):
        """

        :param title:
        :param estimated_cost: Estimated cost in minutes
        :return:
        """
        self.task_id = id
        self.title = title
        self.estimated_cost = estimated_cost
        self.actual_cost = None
        self.parent = parent
        self._children = []

    def add_child(self, task):
        self._children.append(task)

    def has_children(self):
        return len(self.get_children()) > 0

    def get_children(self):
        return self._children

    def set_children(self, children):
        self._children = children

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "estimated_cost": self.estimated_cost,
            "children": [child.to_dict() for child in self.get_children()]
        }






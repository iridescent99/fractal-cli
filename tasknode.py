class TaskNode:

    def __init__(self, title, estimated_cost, parent=None):
        """

        :param title:
        :param estimated_cost: Estimated cost in minutes
        :return:
        """
        self.title = title
        self.estimated_cost = estimated_cost
        self.actual_cost = None
        self.parent = parent
        self.children = []

    def add_child(self, task):
        self.children.append(task)


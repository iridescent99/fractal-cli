from fractalcli.colors import Colors
from fractalcli.status import Status
from fractalcli.time_unit import TimeUnit
from fractalcli.utils import strip_ansi
from datetime import date
import typer


class UpdateException(Exception):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.message = "Invalid Update: " + self.value + " is not a valid value for " + self.key
        super().__init__(self.message)


class TaskNode:
    ALLOWED_STATUSES = [Status.WONT_DO, Status.COMPLETED, Status.IN_PROGRESS, Status.NOT_STARTED]
    ALLOWED_TIME_UNITS = [TimeUnit.DAY, TimeUnit.HOUR, TimeUnit.MINUTE]
    COST_WIDTH = 24

    def __init__(self, id, title, estimated_cost, parent=None, time_unit=None, due_date=None,
                 status=Status.NOT_STARTED, actual_cost=None):
        """

        :param title:
        :param estimated_cost: Estimated cost in minutes
        :return:
        """
        self.task_id = id
        self.title = title
        self.time_unit = time_unit
        if not self.time_unit:
            self.time_unit = typer.prompt(
                f"Please specify a time unit (min, hours, or days) for task '{self.title}'",
                default=TimeUnit.MINUTE,
                type=TimeUnit,
                show_choices=True,
            )
            typer.echo(f"Time unit set to: {self.time_unit}")
        self.estimated_cost = estimated_cost
        if not self.estimated_cost:
            self.estimated_cost = int(typer.prompt(
                f"Please specify an estimated cost in {self.time_unit} for task '{self.title}",
                default=10,
                type=int,
            ))
            typer.echo(f"Estimated cost set to: {self.estimated_cost}")
        self.status = "not started"
        self.actual_cost = actual_cost
        self.parent = parent
        self.status = status
        self.due_date = due_date
        self._children = []

    def add_child(self, task):
        self._children.append(task)

    def update(self, key, value):
        if key in ('estimated_cost', 'actual_cost'):
            self.update_cost(key, int(value))
        if key == 'title':
            setattr(self, key, value.strip())
        if key == 'status':
            self.update_status(value)
        if key == 'time_unit':
            self.update_time_unit(value)
        if key == 'due_date':
            self.update_due_date(value)

    def update_status(self, status):
        if status not in self.ALLOWED_STATUSES:
            raise UpdateException('status', status)
        if status == Status.COMPLETED:
            if self.status == Status.COMPLETED:
                print("This task has already been completed.")
                return

            if not typer.confirm(f"Are you sure you want to mark '{self.title}' as COMPLETED?"):
                print(f"Completion of '{self.title}' cancelled.")
                return

            total_cost = None
            while not total_cost:
                total_cost = int(typer.prompt(f"How many {self.time_unit} did you spend on this task?", type=int))
                self.actual_cost = total_cost
                print(f"Updated {self.title} with actual cost: {total_cost} {self.time_unit}")

        self.status = status
        print(f"Marked task '{self.title}' as {self.status}")

    def update_due_date(self, due_date):
        try:
            ddate = date.fromisoformat(due_date)
            self.due_date = ddate
        except:
            raise UpdateException('due_date', due_date)

    def update_cost(self, key, value):
        setattr(self, key, value)

    def update_time_unit(self, unit):
        if unit not in self.ALLOWED_TIME_UNITS:
            raise UpdateException('time_unit', unit)
        self.time_unit = unit

    def has_children(self):
        return len(self.get_children()) > 0

    def get_children(self):
        return self._children

    def set_children(self, children):
        self._children = children

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title.strip(),
            "estimated_cost": self.estimated_cost,
            "actual_cost": self.actual_cost,
            "status": self.status,
            "children": [child.to_dict() for child in self.get_children()],
            "time_unit": self.time_unit,
            "due_date": self.due_date
        }

    def print(self, level, max_level, max_length):
        if level == 0:
            return
        title_width = max_length + max_level * 9 + 16
        complete = "x" if self.status == Status.COMPLETED else " "
        prefix = f"{(level - 1) * 4 * ' '}|__ [{complete}] " if level > 1 else f"[{complete}] "
        title = f"{prefix}{Colors.TITLE_LEVEL}{self.title}{Colors.RESET}"
        est_cost_printed = self.print_cost_attributes("est. cost", "estimated_cost")
        padding_title = title_width - len(strip_ansi(title))

        line = (
                f"{title}"
                + padding_title * " "
                + est_cost_printed
        )
        if self.status != Status.COMPLETED:
            line += f"   {Colors.PENDING_PASTEL}STATUS: {self.status}{Colors.RESET}"
        else:
            line += " " + self.print_cost_attributes("actual cost", "actual_cost")
        print(line)

    def print_cost_attributes(self, label, key):
        cost_printed = f"{label}: {'?' if not getattr(self, key) else str(getattr(self, key))} {self.time_unit}"
        padding = self.COST_WIDTH - len(strip_ansi(cost_printed)) - 2
        padding_left = int(padding / 2)
        padding_right = padding - padding_left
        return "[" + padding_left * " " + cost_printed + padding_right * " " + "]"

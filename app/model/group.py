from datetime import timedelta


class Group:
    group_by = None

    def __init__(self, **kwargs):
        self.task_list = kwargs.get('task_list', [])
        self.name = kwargs.get('name', '/')
        self.group_list = []

    def __str__(self):
        return f'{self.name}: {len(self.task_list)} задач(и) - {self.total}'

    @property
    def detail(self):
        return '\n'.join([str(task) for task in self.task_list])

    @property
    def started(self):
        if not self.task_list:
            return
        return min(self.task_list, key=lambda p: p.start).start

    @property
    def finished(self):
        if not self.task_list:
            return
        return max(self.task_list, key=lambda p: p.end).end

    @property
    def total(self):
        total = timedelta()
        for item in self.task_list:
            total += item.duration

        return total

    def parse(self):
        d = {}
        for item in self.task_list:
            name = self._get_value(getattr(item, self.__class__.group_by))
            if name not in d:
                obj = d[name] = self.__class__(name=name)
            else:
                obj = d[name]
            obj.__append_task(item)

        self.group_list = [item[1] for item in d.items()]

    def __append_task(self, task):
        self.task_list.append(task)

    def _get_value(self, value):
        return value


class ClientGroup(Group):
    group_by = 'client'


class ProjectGroup(Group):
    group_by = 'project'


class DateGroup(Group):
    group_by = 'start'

    def _get_value(self, value):
        return value.strftime('%Y-%m-%d')


class TagGroup(Group):
    group_by = 'tag'


class TrackerGroup(Group):
    group_by = 'jira_id'


class TaskGroup(Group):
    group_by = 'name'

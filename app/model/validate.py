from datetime import timedelta

from args import Args
from model import DateGroup, Report


class Validate:
    def __init__(self, **kwargs):
        self.task_list = kwargs['task_list']
        self.result = []

    def check(self):
        raise NotImplementedError()

    def fix(self):
        raise NotImplementedError()


class WorkHoursLoad(Validate):
    def check(self):
        report = Report(task_list=self.task_list, group_structure=[DateGroup,])
        report.run()

        result_list = []
        args = Args()

        for item in report.result.group_list:
            if item.started.date() in args.exclude_validate:
                print('pass exclude date')
                continue
            if item.started.weekday() in (5, 6):
                print('pass holiday')
                continue
            if item.total.total_seconds() < 28800:
                self.result.append(item)
                result_list.append(
                    f'{str(item)} ({timedelta(seconds=(28800 - item.total.total_seconds()))})')
                for item1 in item.task_list:
                    result_list.append(f'    {str(item1)}')

        if len(result_list):
            print('Discovered the following days, '
                  'in which you worked less than 8 hours:\n  %s' % ('\n  '.join(result_list)))

    def fix(self):
        print('\nafter fix:\n')
        for item in self.result:
            if item.started.weekday() in [5, 6]:
                continue

            task_count = len(item.task_list)
            time_dif = 28800 - item.total.total_seconds()
            per_time_dif = time_dif / task_count + 60

            for task in item.task_list:
                task.duration = task.duration + timedelta(seconds=per_time_dif)

            print(str(item))
            for task in item.task_list:
                print(f'    {str(task)}')

        return self.task_list

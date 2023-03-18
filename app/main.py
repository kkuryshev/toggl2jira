from model import Toogl, Tracker, WorkHoursLoad, Report, ProjectGroup, DateGroup, TagGroup, TaskGroup
from args import Args
from model.error import Error
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def check(**kwargs):
    report = Report(task_list=kwargs['task_list'], group_structure=[
                    ProjectGroup, DateGroup, TagGroup, TaskGroup])
    report.run()
    logging.info(report.output)


def validate(**kwargs):
    val = WorkHoursLoad(task_list=kwargs['task_list'])
    val.check()
    return val.fix()


def write(**kwargs):
    tracker = Tracker(
        task_list=kwargs['task_list'], ignore_exist_workloads=True)
    tracker.prepare()
    tracker.run()


if __name__ == '__main__':

    args = Args()

    if args.since is None or args.until is None:
        exit(1)
    action = getattr(args, 'action', 'CHECK')
    try:
        task_list = Toogl.get_task_list(since=args.since, until=args.until)

        if action == 'CHECK':
            check(task_list=task_list)

        if args.validate == 'Y':
            task_list = validate(task_list=task_list)

        if action == 'WRITE':
            check(task_list=task_list)
            print('Data preparation is complete. Apply time write-off in Jira?')
            answer = input()
            if answer == 'N':
                raise BaseException('job cancellation')

            write(task_list=task_list)
    except Error as e:
        logger.error(str(e))
        exit(1)
    except BaseException as e:
        raise e

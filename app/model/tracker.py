from model import DateGroup, TrackerGroup, Report
from jira import JIRA
from config import JIRA_URL, JIRA_LOGIN, JIRA_PSWD
from config import logging
from datetime import datetime, timedelta
from model import Error

logger = logging.getLogger(__name__)


class Tracker:
    def __init__(self, **kwargs):
        self.task_list = kwargs['task_list']
        self.report = None
        self.ignore_exist_workloads = kwargs.get(
            'ignore_exist_workloads', True)
        self.tracker = JIRA(JIRA_URL, auth=(
            JIRA_LOGIN, JIRA_PSWD), options={'verify': False})

    def prepare(self):
        self.report = Report(task_list=self.task_list,
                             group_structure=[DateGroup, TrackerGroup])
        self.report.run()

    def run(self):
        for day in self.report.result.group_list:
            for track_issue in day.group_list:
                obj = self.tracker.issue(track_issue.name)
                worklogs = self.tracker.worklogs(issue=obj)
                self.workload_append(
                    worklogs=worklogs, track_issue=track_issue, issue=obj)

    def workload_append(self, worklogs, track_issue, issue):
        detail = self.get_track_issue_detail(track_issue)
        for item in worklogs:
            if item.comment == detail and self.compare_date(item.started, track_issue.started):
                if self.ignore_exist_workloads:
                    # item.delete()
                    logger.warning(
                        f'The issue {track_issue.name} already has time written off for that day in the jira. skip')
                    return
                else:
                    raise TrackError(
                        f'The issue {track_issue.name} already has time written off for this day in the jira', code=204)

        try:
            self.tracker.add_worklog(
                issue, timeSpentSeconds=track_issue.total.total_seconds(), started=track_issue.started - timedelta(hours=3), comment=detail
            )
        except BaseException as e:
            logger.warning(e)

    @staticmethod
    def get_track_issue_detail(track_issue):
        # return '\n'.join([f'{task.name} : {task.duration}' for task in track_issue.task_list])
        return '\n'.join([f'{task.name}' for task in track_issue.task_list])

    @staticmethod
    def compare_date(date1, date2):
        # @TODO переписать нормально сравнение дат
        return datetime.strptime(date1[:10], '%Y-%m-%d').date() == date2.date()


class TrackError(Error):
    def __init__(self, *args, **kwargs):
        super(TrackError, self).__init__(*args, **kwargs)
        self.code = kwargs.get('code', None)

    def __str__(self):
        return f'{self.code or ""}:{self.args[0]}'

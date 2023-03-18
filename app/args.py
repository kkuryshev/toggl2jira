import argparse
from datetime import datetime


class Args():

    args = None
    _exclude_validate = None

    def __init__(self):
        parser = argparse.ArgumentParser(description='Set args to continue')

        parser.add_argument('-s', '--since', required=True, help='date since')
        parser.add_argument('-u', '--until', required=True, help='date until')
        parser.add_argument('-v', '--validate', required=True,
                            help='the need to check working days less than 8 hours')
        parser.add_argument('-a', '--action', required=True,
                            help='working mode (CHECK - check, WRITE - write to JIRA)')
        parser.add_argument('-e', '--exclude_validate', required=False,
                            help='days for which you do not need to check the time of debiting')
        parser.add_argument('-d', '--max_dur_exclude_code', required=False,
                            help='task code for vacation write-off')
        parser.add_argument('-t', '--reqtag', required=False,
                            help='require tag')
        parser.add_argument('-p', '--reqproject', required=False,
                            help='require project')
        self.args = parser.parse_args()

    @property
    def exclude_validate(self):
        if self._exclude_validate:
            return self._exclude_validate

        str = self.args.exclude_validate
        if not str:
            return
        self._exclude_validate = [datetime.strptime(
            item, '%Y-%m-%d').date() for item in str.split(';')]

        return self._exclude_validate

    @property
    def action(self):
        return self.args.action

    @property
    def validate(self):
        return self.args.validate

    @property
    def until(self):
        return self.args.until

    @property
    def since(self):
        return self.args.since
    
    @property
    def reqtag(self):
        return self.args.reqtag == 'Y'

    @property
    def reqroject(self):
        return self.args.reqproject == 'Y'
    
    @property
    def max_dur_exclude_code(self) -> list[str]:
        if self.args.max_dur_exclude_code is None:
            return []
        return self.args.max_dur_exclude_code.split(';')

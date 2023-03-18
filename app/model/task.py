# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

from config import logging
from args import Args

from .error import Error

logger = logging.getLogger(__name__)
jira_id_reg = re.compile(r'^(\w+-\d+)\.*')
name_reg = re.compile(r'^\w+-\d+\.*(.+)')

args = Args()


class Task:
    def __init__(self, **kwargs):
        try:
            self.id = kwargs['id']
            self.origin_name = kwargs['origin_name']
            self.project = 'def' if 'project' not in kwargs else kwargs['project']
            self.tag = 'dev' if not len(kwargs['tags']) else kwargs['tags'][0]
            self.client = kwargs['client']

            self.start = datetime.fromisoformat(kwargs['start'])
            self.end = datetime.fromisoformat(kwargs['end'])

            if 'shift' in kwargs:
                start = self.start
                self.start = start + timedelta(days=kwargs['shift'])
                self.end = start + timedelta(days=kwargs['shift'])

            self.duration = timedelta(milliseconds=kwargs['duration'])

        except KeyError as e:
            raise Error(f'task initialization error: {e}, {kwargs}')

    @classmethod
    def parse(cls, **kwargs):
        error_list = []
        duration = kwargs['dur']
        try:
            origin_name = f'{kwargs.get("description","")}, {kwargs.get("start","")}'

            if args.reqroject and ('project' not in kwargs or not kwargs['project']):
                error_list.append(f'the task has no project: <{origin_name}>')

            if args.reqtag and ('tags' not in kwargs or not len(kwargs['tags'])):
                error_list.append(f'the task has no tags: <{origin_name}>')

            if duration < 60000:
                error_list.append(
                    f'Task duration cannot be less than 1 minute: <{origin_name}>')

            if duration > 32400000:
                rst = next(
                    (it for it in args.max_dur_exclude_code
                     if origin_name.startswith(it)), None)

                if not rst:
                    error_list.append(
                        f'Task duration cannot exceed 8 hours: <{origin_name}>')

            if not Task.__get_jira_id(origin_name):
                error_list.append(
                    f'Issue <{origin_name}> does not have a Jira number')
        except KeyError as e:
            error_list.append(f'required fields not specified: {e}, {kwargs}')

        if not error_list:
            rsp = []
            if duration <= 32400000:
                rsp.append(
                    cls(origin_name=kwargs['description'], duration=duration, **kwargs))
            else:
                for index in range(int(duration // 86400000) + 1):
                    rsp.append(cls(
                        origin_name=kwargs['description'],  duration=32400000, shift=index,  **kwargs))

            return rsp, None

        return None, error_list

    @property
    def name(self):
        return Task.__get_name_id(self.origin_name)

    @staticmethod
    def __get_jira_id(value):
        result = re.search(jira_id_reg, value)
        return result.group(1).strip() if result else None

    @staticmethod
    def __get_name_id(value):
        result = re.search(name_reg, value)
        return result.group(1).strip() if result else None

    @property
    def jira_id(self):
        return Task.__get_jira_id(self.origin_name)
        # try:
        #     return TAG_MAP[self.client][self.project][self.tag]
        # except KeyError as e:
        #     raise Error(f'ошибка поиска jira_id: {e}. {self.client}/{self.project}/{self.tag}')

    def __str__(self):
        return f'{self.jira_id} - {self.name}: {self.duration}'

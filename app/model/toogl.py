from model.task import Task
from utils import tooglUtils
from config import logging
from model.error import Error

logger = logging.getLogger(__name__)


class Toogl:
    @staticmethod
    def get_task_list(**kwargs):
        task_list = tooglUtils.get_detail_report(**kwargs)
        response = []
        global_error_list = []
        for item in task_list:
            task, error_list = Task.parse(**item)
            if task:
                response.extend(task)
            else:
                global_error_list.extend(error_list)

        if len(global_error_list):
            raise Error('Issue validation error:\n  -%s' % '\n  -'.join(global_error_list))

        return response


if __name__ == '__main__':
    Toogl.get_task_list(since='2019-05-10', until='2019-07-12')

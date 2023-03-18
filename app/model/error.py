import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Error(BaseException):
    def __init__(self, *args, **kwargs):
        super(Error, self).__init__(*args)
        # logger.error(self)

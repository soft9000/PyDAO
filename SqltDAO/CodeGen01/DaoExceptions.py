# Author: Soft9000.com
# 2018/03/08: Class Created


class GenException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GenOrder(Exception):
    def __init__(self, message):
        super().__init__(message)
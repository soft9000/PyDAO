# Author: Soft9000.com
# 2018/12/31: Class Created

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.CodeLevel import CodeLevel
from SqltDAO.CodeGen01.DaoExceptions import GenOrderError


class Meta:
    PRODUCT = "Soft9000/PyDAO"
    VERSION = 2.0
    
    @staticmethod
    def Title():
        return "{0}, Ver. {1} (Alpha)".format(Meta.PRODUCT, Meta.VERSION)

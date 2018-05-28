# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-05-28 14:50:28
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-28 15:48:28
# @License: MIT LICENSE

class Base(object):
    def __init__(self):
        self.b = 2

    def aa(self):
        print(self.b)

class Child(Base):

    def __init__(self):
        self.b =1
        super().__init__()

if __name__ == "__main__":
    child = Child()
    child.aa()

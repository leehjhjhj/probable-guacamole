# 4.5 추상화 클래스는 상속을 확인한다.

from abc import ABCMeta, abstractclassmethod

class MonsterBase(metaclass=ABCMeta):
    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def skill(self):
        pass

class MushRoomMonster(MonsterBase):
    def __init__(self, name):
        self.name = name

monster1 = MushRoomMonster("주황버섯")
# 🖥️ 출력 결과
'''
Traceback (most recent call last):
  File "/Users/leehyunje/IdeaProjects/reading/python-tricks-the-book/abstract_base_class.py", line 18, in <module>
    monster1 = MushRoomMonster("주황버섯")
TypeError: Can't instantiate abstract class MushRoomMonster with abstract method skill

이렇게 파이썬에서도 추상클래스를 통해서 클래스 계층을 쉽게 유지할 수 있게 도와준다.
'''
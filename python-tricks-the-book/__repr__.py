# 4.2 __repr__ 에 대하여
'''
__str__과 __repr__ 는 던더클래스로 자신의 클래스에서 문자열 변환을 제어할 수 있다.
__str__의 기본 구현은 __repr__을 불러오면 된다.
repr은 print를 하지 않아도, __str__과 다르게 해당 클래스의 정보를 불러와준다. 즉, __str__ 없어도 __repr__ 만으로도 가능하다.
'''

class Monster:
    def __init__(self, name: str, hp: int, mp: int):
        self.name = name
        self.hp = hp
        self.mp = mp
    
    def __repr__(self) -> str:
        return (
        f'{self.__class__.__name__}('
            f'{self.name!r}, {self.hp!r}, {self.mp!r})'
        )

    
mushmom = Monster("머쉬맘", 10, 20)
print(mushmom)
# 🖥️ 출력 결과
'''
Monster('머쉬맘', 10, 20)
'''
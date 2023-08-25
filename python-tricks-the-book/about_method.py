# 4.8 인스턴스 메서드, 클래스 메서드, 정적 메서드의 신비를 풀다.
'''
인스턴스 메서드는 클래스 인스턴스가 필요하며 self를 통해서 인스턴스에 접근
클래스 메서드는 클래스 인스턴스가 필요하지 않다. 인스턴스에는 접근 불가능 하지만 cls를 통해서 클래스 자체에 접근 가능
정적 메서드는 cls 또는 self에 접근 불가능. 일반 함수처럼 동작하지만 자신을 정의한 클래스의 네임스페이스에 속한다.
'''
class MyClass:
    def method(self):
        return 'instance method called', self
    
    @classmethod
    def classmethod(cls):
        return 'class method called', cls
    
    @staticmethod
    def staticmethod():
        return 'static method called'
    
print(MyClass.method()) # 오류 발생
print(MyClass.classmethod()) # ('class method called', <class '__main__.MyClass'>)
print(MyClass.staticmethod()) # static method called

# 클래스 메서드의 정적 메서드의 활용

class Monster:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp

    def __repr__(self) -> str:
        return (
        f'{self.__class__.__name__}('
            f'{self.name!r}, {self.hp!r})'
        )
    def exp(self):
        return self.make_exp(self.hp)
    
    @classmethod
    def mushmom(cls):
        return cls("mushmom", 20000)
    
    @staticmethod
    def make_exp(hp: int) -> int:
        return hp * 100
    
print(Monster.mushmom())

monster1 = Monster("좀비버섯", 300)
print(monster1.exp())
print(Monster.make_exp(400))

# 🖥️ 출력 결과
'''
Monster('mushmom', 20000)
30000
40000

이렇게 classemethod는 팩터리 메서드로 사용이 가능하며 원하는 대로 구성한 Monster 객체를 만들 수 있다. 하나의 __init__만 선언할 수 있는 파이썬의 생성자를 보완
static method는 인스턴스가 없이 일반 함수로도 호출이 가능하며 메서드에서도 활용이 가능. 이 둘을 이용하는 것은 개발자의 의도를 전달하고 유지 보수에 도움이 된다.
'''
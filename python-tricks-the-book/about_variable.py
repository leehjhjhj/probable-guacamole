# 4.7 클래스 변수 대 인스턴수 변수의 함정
'''
클래스 변수는 모든 클래스 인스턴스에서 공유하는 데이터를 위한 변수이다.
그렇기 때문에 이 변수는 특정 인스턴스에 속하는 것이 아니라 클래스에 속한다.
인스턴스 변수는 각 인스턴스에 고유한 데이터이고, 고유한 저장소를 갖는다.
클래스 변수는 동일한 이름의 인스턴스 변수에 의해 가려질 수 있다. 밑은 사례이다.
'''
class Monster:
    total_monster_counts = 0

    def __init__(self, name: str):
        self.name = name
        self.total_monster_counts += 1 # 여기서 total_monster_counts라는 인스턴스 변수가 선언된다. 여기서 클래스 변수는 가려지게 된다.

monster1 = Monster("주황버섯")
print(monster1.name, monster1.total_monster_counts)

monster2 = Monster("뿔버섯")
print(monster2.name, monster2.total_monster_counts)

# 🖥️ 출력 결과
'''
주황버섯 1
뿔버섯 1
'''
# 해결 방법 = '__class__.클래스변수'로 접근
class Monster:
    total_monster_counts = 0

    def __init__(self, name: str):
        self.name = name
        self.__class__.total_monster_counts += 1 # 인스턴스 메서드에서 클래스 변수에 접근한다.

monster1 = Monster("주황버섯")
print(monster1.name, monster1.total_monster_counts)

monster2 = Monster("뿔버섯")
print(monster2.name, monster2.total_monster_counts)

# 🖥️ 출력 결과
'''
주황버섯 1
뿔버섯 2
'''
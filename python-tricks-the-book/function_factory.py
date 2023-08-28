# 3.1 함수는 일급 객체이다.
'''
함수는 중첩될 수 있으며, 부모 함수의 일부 상태를 포착하여 전달할 수 있다. 이를 수행하는 함수를 클로저라고 한다.
'''

def make_candy_machine(base_favor):
    def add(add_favor):
        result_candy = f"{base_favor} {add_favor}맛 사탕"
        return result_candy
    return add

orange_candy_machine = make_candy_machine("오렌지")
apple_candy_machine = make_candy_machine("사과")

print("오렌지 기계: ", orange_candy_machine("치약"))
print("사과 기계: ", apple_candy_machine("홍삼"))
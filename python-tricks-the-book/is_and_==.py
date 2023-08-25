# 4.1 객체 비교: is 대 ==
'''
두 변수가 동일한 객체를 가리키는 경우 is 표현식은 True로 평가한다.
== 표현식은 변수가 참조하는 객체가 동등한 경우 True로 평가한다.
'''
a = [1, 2, 3]
b = a
print(a, b)
print(a is b)
print(a == b)
c = list(a)
print(a is c)
# 🖥️ 출력 결과
'''
[1, 2, 3] [1, 2, 3]
True
True
False
'''
# 3.3 데코레이터의 힘
"""
데코레이터는 함수의 동작을 수정할 수 있다. 데코레이터가 여러 개일 때는 밑에서 부터 먼저 적용이 된다.
"""
import socket

def print_log(func):
    def wrapper(*args, **kwargs):
        print((
            f"LOG: {func.__name__}() is called"
            f" from {socket.gethostbyname(socket.gethostname())}"
            ))
        return func(*args, **kwargs)
    return wrapper

@print_log
def pipeline(inbound_port: int, outbound_port: int):
    return f"you're enter from {inbound_port} to {outbound_port}"

print(pipeline(80, 8080))

# 🖥️ 출력 결과
"""
LOG: pipeline() is called from 127.0.0.1
you're enter from 80 to 8080

이렇게 데코레이터로 편하게 기능을 붙였다가 땔 수도 있다.
*args, **kwargs를 통해서 함수의 인자를 정상적으로 처리할 수 있다.
`@functools.wraps(func)`를 사용하면 func.__name__ 과 func.__doc__ 을 통해
원본 호출 가능 객체에서 장식된 호출 가능 객체로 메타데이터를 전달한다.
"""
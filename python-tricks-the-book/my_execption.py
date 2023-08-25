# 4.3 자신만의 예외 발생시키기
'''
파이썬의 내장 Exception 클래스 또는 ValueError나 KeyError와 같은 구체적인 예외 클래스에서 사용자 정의 예외를 파생시키자.
상속을 이용하여 논리적으로 그룹화된 예외 계층을 정의 할 수 있다.
'''

# example business error

class SignUpValidationError(ValueError):
    error_message = "회원 가입 도중 에러가 발생했습니다."

    def __init__(self, message=None) -> None:
        if message is None:
            message = self.error_message
        super().__init__(message)

class PasswordTooShortError(SignUpValidationError):
    error_message = "비밀번호가 너무 짧습니다."

class NickNameTooLongError(SignUpValidationError):
    error_message = "닉네임이 너무 깁니다."

class NameDuplicatedError(SignUpValidationError):
    error_message = "이름이 중복되었습니다."


def validate(name):
    if len(name) > 10:
        raise NickNameTooLongError

name = "안녕하세요오오반갑습니데이이이"
try:
    validate(name)
except SignUpValidationError as e:
    print(f"{e.__class__.__name__}: {e}")

# 🖥️ 출력 결과
'''
NickNameTooLongError: 닉네임이 너무 깁니다.

이렇게 BaseException을 설정하고 상속을 통해 세부 예외를 설정하면 저렇게 부모의 예외 만으로도 자식들의 예외를 모두 처리할 수 있다.
또한 error_message를 설정하여 `print(e)`를 할 경우 더욱 명확한 에러 메세지를 알 수 있다. 
'''
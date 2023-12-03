# 셸

- 셸은 커널과 사용자간의 중간 다리역할
- 사용자로부터 명령을 받고 그것을 해석

### 주요 셸

- bash: 리눅스 표준 셸, 다양한 운영체제에서 사용, sh와 호환
- C셸: c언어 기반, csh라고 부른다.
- 제 맥에서는 zsh를 쓰고 있어요 ^^

### 셸의 확인과 변경

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/eb02cee9-697b-486b-83ef-c840d061e4ab/Untitled.png)

- /etc/shells에 사용 가능한 셸들이 있음
- 셸을 변경하려면 chsh 사용
    - 다음 로그인 때부터 유효하다
    - amazon linux에서는 `sudo usermod -s /bin/bash username` 명령
    - -s는 셸을 명시할 때 사용

### 셸 변수 및 환경변수

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/b00ff6ce-94f6-4153-8086-eae83f30ba41/Untitled.png)

- 셸변수를 확인하려면 `set`을 하라는데 너무 많이 나온다.
- 환경 변수는 `env`

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/6542aa45-e4b0-45ce-8fcd-fa662f59fb0b/Untitled.png)

- 다앙한 놈들이 대문자로 환경변수에 등록되어있다.
- 환경 변수와 셸변수는 `$`를 통해서 자유롭게 쓸 수 있음
- 프롬프트가 뭐임
    
    **`PS1`은 셸 프롬프트를 정의하는 환경 변수입니다. 이 환경 변수의 값은 사용자가 새로운 명령어를 입력할 때마다 터미널에 표시되는 텍스트를 결정합니다.**
    
    **`[\u@\h \W]\$` 값은 다음과 같은 요소들을 포함하고 있습니다:**
    
    **`\u`: 현재 로그인한 사용자의 사용자명을 나타냅니다.`@`: '@' 문자를 그대로 표시합니다.`\h`: 현재 사용중인 호스트의 이름을 나타냅니다. ``: 공백 문자를 표시합니다.`\W`: 현재 작업중인 디렉토리의 이름을 나타냅니다.`]`: ']' 문자를 그대로 표시합니다.`\$`: 사용자가 관리자(root)일 경우에는 '#', 일반 사용자일 경우에는 '$'를 표시합니다.**
    
    **따라서 `[\u@\h \W]\$` 프롬프트는 "현재 사용자명@호스트명 작업디렉토리명]$" 형태로 표시됩니다. 예를 들어, 'ec2-user'라는 사용자가 'ip-172-31-45-248' 호스트에서 '~' 디렉토리에서 작업하고 있다면, 프롬프트는 `[ec2-user@ip-172-31-45-248 ~]$`로 표시됩니다.**
    

### Bash의 주요 기능

- `TAB`으로 자도완성 기능 → 몰랐음;
- history로 내가 썼던 명령어들을 볼 수 있음. `!` 로 대체 가능
    - 유용한 것: `!?문자열?` , 바로 실행 안 되게 하는 방법: `:p`를 붙인다.
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/9f4e01e6-0365-444a-8b18-34d9e1cff6f8/Untitled.png)
        
- 전역변수로 설정: `export`
    - export로 지정한 변수는 `set`이 아니라 `env`로 조회한다
- 토막 상식:
    - %F = %Y-%m-%d
    - %T = %H:%M:%S
    - ctrl + r로도 최근에 수행한 명령어를 찾을 수 있음
        - `(reverse-i-search)`my': sudo systemctl restart mysql`

### alias 기능

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/f411670e-6e83-4a45-ad05-d18488aa3e6f/Untitled.png)

- 풀 때는 `unalias`, `-a`는 모두
- 근데 재로그인, 재부팅하면 풀린다. .bashrc에서 수정하면 된다.
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/ed73b866-5a3c-4ec8-87d2-264c8d783c8b/Untitled.png)
    
    - 이후 `source ~/.bashrc` 로 다시 불러오기
    - source는 또 뭐임
        
        **일반적으로, 쉘 스크립트나 설정 파일을 수정한 후에는 해당 파일을 다시 로드해야 변경 사항이 적용됩니다. 이때 'source' 명령어를 사용하여 파일을 로드합니다. 'source' 명령어는 파일을 현재 쉘 세션에서 실행하고, 쉘의 환경을 해당 파일의 내용으로 업데이트합니다.**
        
- 근데 바꾼거 말고 원래 걸로 쓰고 싶으면 `절대 경로`나(/bin/ls) `\` (\ls) 를 이용한다.

### 명령

- 꿀 명령어 기능: `ctrl u`, `ctrl y` 행 삭제, 되돌리기
- 명령 대체: `docker rm $(docker ps -a)`
- `;`를 붙이면 한줄에 명령어 여러개를 쓸 수 있다.
- `||`, `&&` 도 존재 `||`는 앞에 것이 트루면 앞만 보여주고, `&&`은 둘다 맞아야됨
- 0 = 입력, 1=출력, 2=오류

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/14527ead-8e09-4f7c-8bf7-b2ae2a07ef4f/Untitled.png)

- >>는 파일이 없으면 생성한다.
- <는 생략을 많이 한다. cat 같은 명령어

### 파이프

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/b45bb0ba-ae42-4597-a3a9-c29ba86181af/Untitled.png)

- tee: 동시에 해라
- xargs: 인자를 주는 것 같다.
    - 추가 설명 and 질문
        
        `find -name '*.txt' | xargs rm -rf`와 `find -name '*.txt' | rm -rf` 사이에는 큰 차이가 있습니다.
        
        `find -name '*.txt' | xargs rm -rf` 명령어는 `find` 명령을 사용하여 '.txt' 확장자를 가진 모든 파일을 찾은 후, 찾아낸 파일들을 `rm -rf` 명령어에 전달하여 삭제합니다. `xargs`는 `find`로부터 출력된 파일 이름들을 `rm -rf` 명령의 인자로 전달하는 역할을 합니다.
        
        반면에, `find -name '*.txt' | rm -rf` 명령어는 제대로 동작하지 않습니다. 이는 `rm -rf` 명령어가 표준 입력을 읽지 않기 때문입니다. `rm -rf` 명령어는 인자로 전달된 파일이나 디렉토리를 삭제하는데, 파이프(|)로 연결된 `find` 명령의 결과가 표준 입력으로 전달되는 것이 아닌 인자로 전달되어야 합니다. 따라서 이 경우, `rm -rf` 명령어는 아무런 동작을 하지 않을 것입니다.
        
        따라서, '.txt' 확장자를 가진 모든 파일을 삭제하려면 `find -name '*.txt' | xargs rm -rf` 명령어를 사용해야 합니다.
        

### 셸에서 사용되는 특수문자

- [] 는 bracket, ‘~ 중에 하나’
    - !가 들어가면 부정
- {} 는 안에 제시된 문자열 중 하나로 대치
- * 는 모든 문자 대치
- ? 는 한 문자 대치

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/08938448-37f7-416e-bc61-b3b0010490e4/Untitled.png)

## 셸 프로그래밍

- 셸 스크립트 적을 때 맨 앞에 ‘#!/bin/bash’ 사용
- 실행할 때는 `./~.sh` 사용
- 어느 곳에서나 사용하고 싶으면 `mkdir ~/bin` or `mkdir ~/.local/bin` 실행 후 이 디렉토리에 넣는다
- 셸에서 변수형은 문자열만 가진다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/2d8a7708-27dd-4af4-989b-9fa1c7cab3b3/Untitled.png)

<aside>
🔥 $ 차이점

리눅스 쉘 스크립트에서 `${}`, `$()`, `$[]` 각각의 기호들은 서로 다른 역할을 수행합니다.

1. `${}`: 이 기호는 변수의 값을 참조할 때 사용됩니다. 예를 들어, `VAR="Hello"`라는 변수가 있다면 `${VAR}`를 사용하여 "Hello"라는 값을 얻을 수 있습니다.
2. `$()`: 이 기호는 명령 치환(command substitution)에 사용됩니다. 즉, `$()` 안에 있는 명령어를 실행하고 그 결과를 반환합니다. 예를 들어, `DATE=$(date)`라고 하면 `date` 명령어가 실행되고, 그 결과가 `DATE` 변수에 저장됩니다.
3. `$[]`: 이 기호는 쉘 스크립트에서 기본적인 산술 연산을 수행하는 데 사용됩니다. 예를 들어, `RESULT=$[1+2]`라고 하면 `RESULT`는 3이라는 값을 가지게 됩니다. 하지만 이 기호는 오래된 방식이고, 현재는 `$(())`를 산술 연산에 사용하는 것이 권장됩니다. 예를 들어, `RESULT=$((1+2))`와 같이 사용합니다.

이렇게 각 기호는 서로 다른 역할을 수행하므로, 적절한 상황에 따라 사용해야 합니다.

</aside>

- `````grep **^user` : 이 패턴은 'user'라는 문자열로 시작하는 모든 라인을 찾습니다. 여기서 `^`는 정규 표현식에서 문자열의 시작을 나타냅니다.**
- **만약 'user'를 포함하는 모든 라인을 찾고자 한다면, `grep user`를 사용하면 됩니다.**
- ehco에 `-e` 를 사용하여 escape 특수문자를 쓸 수 있다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/962edb8f-e544-44ec-84d8-32d0bee1d7c0/Untitled.png)

- 산술식
    - eq, ne, gt, ge, lt, le, !, a, o
- `ehco $?` 으로 결과를 출력한다.
- until은 while의 반대
- 우선순위
    - alias
    - function, if, for 같은 지정 키워드
    - 함수
    - type, export등의 내장 명령어
    - 스크립트, 프로그램, path 환경변수에 있는 디렉토리를 셸이 확인해서 실행

### 관련 명령어

- read: read flower → ehco $flower
- echo
- break
- continue
- exit: 상태코드 n과 함께 스크립트 종료
- function
- getopts
- shift: 위치 매개 변수를 n만큼 이동시키는데, 예시를 보면 개수도 줄어드는 것 같다.
- eval: 인자의 값을 구하는데 명령어라면 해당 명령을 실행시킨다?
    - **eval result=$val2와 eval result=’$’$val2의 차이점**
        
        `eval result=$var2`와 `eval result='$'$var2`는 서로 다른 동작을 합니다.
        
        1. `eval result=$var2`: 이 명령어는 `$var2`의 값이 `result`에 할당되도록 합니다. 즉, `var2`의 값이 `result`의 값이 됩니다.
        2. `eval result='$'$var2`: 이 명령어는 `$var2`의 값이 다른 변수의 이름이 되고, 그 변수의 값이 `result`에 할당되도록 합니다.
        
        예를 들어, `var2="name"`이고 `name="John"`일 때, `eval result=$var2`를 실행하면 `result`의 값은 "name"이 됩니다. 하지만 `eval result='$'$var2`를 실행하면 `result`의 값은 "John"이 됩니다.
        
        따라서, 이 두 명령어는 서로 다른 동작을 수행하며, 원하는 동작에 따라 적절한 명령어를 선택해야 합니다.
        
- expr
- type
- true

# 프로세스

- 프로그램: 어떤 문제를 해결하기 위해 사용되는 명령이나 유틸리티의 집합
- 프로세스: 실행중인 프로그램

### 프로세스 생성

- fork, exec
    - fork: 메모리를 할당 받아 복사본 형태의 프로세스를 실행
    - exec: 원래의 프로세스를 새로운 프로세스로 대체

### 프로세스 종류

- 포어그라운드
- 백그라운드: -d, &
- 포어그라운드에서 백그라운드로 변환 방법
    - ctrl + z 로 suspend 상태 만들고, bg로 전환
    - jobs로 작업의 상태를 볼 수 있다.
    - 반대는 fg를 친다. `fg 작업번호`

### 프로세스 관리의 이해

- IPC: 프로세스 간 통신
    - 시그널: `kill -l` 로 시그널을 볼 수 있다.
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/883204e9-fc42-4e4c-97f4-e0b8c491d639/Untitled.png)
        
- 데몬: 주기적이고 지속적인 서비스 요청을 처리하기 위해 계속 실행되는 프로세스, 백그라운드로 실행됨
    - standalone: 부팅시 실행, 메모리에 계속 상주
    - inetd: 클라이언트가 요청 할 때만

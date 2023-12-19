## 프로세스 관리

- ps -l를 하면 pri는 우선순위, ni는 root나 사용자가 조작하는 우선순위 값
- /proc에 시스템에 동작 중인 프로세스의 상태나 하드웨어 정보 확인 가능
- 프로세스가 생성될 때, 해당 번호와 같은 디렉터리가 생성됨

### 중요하다고 생각하는 명령어

- ps: 동작중인 프로세스의 상태를 출력
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/9d62c946-492d-45c2-8f60-752989058cc3/Untitled.png)
    
    - ps aux | grep sendmail << 좀 유용할 듯
- top: 동작중인 프로세스의 상태를 실시간으로 화면에 출력
- kill
    - 프로세스 종료 신호
    - kill -9 << 강제 종료, pkill 으로도 가능
    - pkill은 프로세스 명으로 프로세스를 종료할 수 있다.
- jobs: 백그라운드로 실행 중인 프로세스나 중지된 프로세스의 목록을 출력
- fg
    - 백그라운드 → 포어그라운드로 전환
    - bg는 그 반대
- nice
    - 프로세스 우선순위, -20~19이고 작을 수록 우선순위가 높다.
    - root만 바꿀 수 있고 일반 사용자는 NI 값을 높이기만 함
- renice
    - nice와 다르게 PID를 재활용, 실행 중인 프로세스의 우선순위를 바꿀 때 사용하는 명령이다.
    - 또한 nice는 기존의 NI 값을 증감하는 형태이지만, renice는 값을 바로 적용
- nohup
    - 로그아웃하거나 터미널 창이 닫겨도 실행 중인 프로세스를 백그라운드로 작업할 수 있게 해줌.
    - 사용자 명령 뒤에 &를 붙여야 백그라운드 프로세스 실행
- pgrep
    - 프로세스 이름을 기반으로 PID 값을 검색
    - -u, -g 등으로 유저, 그룹명으로도 PID 조회가 가능

## 소프트웨어 설치 및 관리

원래 깔기 어려웠는데 배포판에는 패키지 관리기법을 만들었다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/3760d9d5-f480-4a10-96d0-2b722364e8e2/Untitled.png)

- rpm
    - .rpm 형태로 파일을 배포
    - -i가 설치, -u는 업그레이드
    - -e는 삭제, —nodeps는 의존성이 있어도 삭제
    - -q 는 질의문이고, 다양한 옵션과 함께 정보를 얻을 수 있음
    - verify: 검증 모드, 변경된 정보를 찾아낸다
- yum
    - 소프트웨어 레파지토리에 관련 패키지들을 모아두고 네트워크를 통해서 의존성을 검사, 설치, 업데이트를 한다.
    - /etc/yum.repos.d 디렉토리가 레포이다.
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/25c5dfd4-fd84-4b43-bea5-da2d7df3a327/Untitled.png)
    
    - -y 모든 옵션에 yes
    - yum list updates: 업데이트 체크
    - search로 찾을 수도 있다
- dpkg: 데비안 패키지 관리 도구
    - .deb 형태의 파일로 배포
    - deselct는 메뉴 방식의 유틸리티. 손쉽게 패키지를 관리할 수 있다.
- apt-get

### 소스 코드 컴파일

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/a03e582f-ff56-48b7-b38c-5e88e76480a2/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/35c0f323-9045-42c5-8666-a8a8a8c3a908/Untitled.png)

- cmake는 다양한 플랫폼에 맞춰서 configure작업과 make작업을 통합해준다.

### tar

- 여러 파일들을 하나의 파일로 묶어주는 명령
- -c(파일, 디렉토리로 tar 생성), -f(파일이름), -x(풀기) 이정도가 유용한 듯
- gzip: GNU 압축 프로그램
- bzip2, bunzip2: .bz2 만들기
- xz, unxz: 무손실 압축 프로그램. 리눅스 배포판으로 쓰임
    - xz posein.tar
- zip: -r 사용하면 디렉토리까지
- gcc: c언어 컴파일러

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/e5c308f4-c9ac-47a9-84a1-4e0e033fee7f/Untitled.png)

- make와 makefile 방법

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/e92571a6-2ade-4d68-8253-e014086f250c/Untitled.png)

## 라이브러리 관리

- 동적 링크 라이브러리, 정적 링크 라이브러리
- 운영 체제는 동적 공유 라이브러리를 사용
    - 동일한 라이브러리가 정적으로 링크된 상태면 여러 프로그램들이 실행될 때 메모리 낭비가 발생

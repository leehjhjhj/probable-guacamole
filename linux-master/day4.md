# 4회차

# 일반 운영 관리

## 1.1 사용자 관리

- 리눅스에서는 사용자를 ID가 아니라 UID로 관리.
- 슈퍼유저는 0번에 해당되는 유저
- 파일 생성, 프로세스 생성시 권한을 승계하는 형태
    - root가 만든 파일이면 root권한, root가 실행한 프로세스는 root 권한
    - 따라서 데몬에 해당되는 시스템 계정이 있음
        - 1~200까지 시스템 프로세스, 201~999까지 파일을 소유하지 않는 시스템 프로세스

### 사용자 계정 관리

- useradd - 사용자 계정 생성
    - -p(패스워드), -d(홈디렉토리), -m(홈 디렉토리 생성 옵션)
    - /etc/skel에 사용자 생성시 기본적으로 제공할 파일과 디렉터리가 들어있음
- passwd: 암호 지정하지 않으면 로그인 되지 않는다.
- su: 사용자 전환
    - 아무것도 안 칠시 자동으로 root 계정 접속 시도
    - root 권한을 사용하려면 `-l` 이 필요
- /etc/passwd
    - passwd의 패스워드를 암호화해서 저장한 것이 shadow
    - username:password:UID:GID:fullname:home-directory:shell
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/1f8f4673-d50d-4fc0-807b-26ff644b670b/Untitled.png)
        
- /etc/shadow
    - 오직 root 권한
    - 패스워드 부분을 암호화하여 관리, 만기일 같은 것이 추가적으로 있음
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/f2ea7d49-d7f7-41d9-8de5-2a0200e117aa/Untitled.png)
        
    - 패스워드의 표율적인 관리와 보안측면에서는 shadow를 써라
- pwck: 위의 두개를 점검
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/884a5d57-6294-4cb8-85de-7e4739e841ef/Untitled.png)
    
- /etc/default/useradd
    - useradd 사용자명 했을 때 자동으로 적용되는 설정이 들어가있음
- /etc/login.defs : 별게 다 듦
- usermod: 대부분 정보를 변경
    - `-f`는 —inactive와 같음. 패스워드 끝난 이후에 유예 기간
    - `-l` 사용자 아이디 변경
    - `-m` 홈 디렉토리를 옮길 시 기존의 파일들도 옮겨준다.
    - 따라서 아이디 변경시 -l, -m, -d를 같이 해야함
    - `-s` /bin/false 로 하면 일시적으로 셸을 못씀
- userdel 삭제
    - `-r` 관련 모든 파일 제거
- passwd, chage - 옵션 값이 다 제각각이야 이런 통일좀
    - `-w`, `-W` 경고
    - chage는 shadow 관련 필드 설정이 가능
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/3aa58a75-abb3-43ab-b909-db07346d2f66/Untitled.png)
    
    - 통일좀요;
- chpasswd
    - 다수의 사용자의 패스워드를 바꿀 때
    - chpasswd < password.txt
    - password.txt 안에는 아이디:패스워드 값 목록
    - 자동으로 SHA-512

## 1.1.3 그룹의 개요

- 추가 설정 안 하면 GID100
- GID: 그룹아이디
    - 0~999: 시스템
    - groupadd -g 할 때는 그래서 1000번 이상으로
- /etc/group
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/50686d56-d697-4f1f-ad82-4f1a7bd51248/Untitled.png)
    
- 비밀 번호는 /etc/gshadow
- 그룹 변경 groupmod
- newgrp: 일시적으로 1차 그룹을 변경할 때 사용
    - 그룹에 속해있으면 패스워드 없이 가능
    - exit으로 나간다
- write, wall: 메시지 보내기
    - mesg로 수신한다

# 1.2 파일 시스템 관리

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/d0491f3f-51f9-43e6-8ab5-85b770dcee51/Untitled.png)

- 소유권: 디렉터리를 소유하여 지배하는 권리
- 허가권: 접근 권한
- 허가권 / ? / 소유권 / 그룹 소유권
    - 허가권: - —- —- —- 첫 번째: 파일의타입
    - 다음 첫번째 세자리: 파일을 소유한 사용자에게 권한
    - 두번째 세자리: 그룹에 속한 사용자의 권한
    - 마지막 세자리: 그 외 다른 사용자들
    - read, write, execute의 권한, 없으면 ‘-’

### 특수권한

- Set-UID: 해당 파일의 소유자 권한으로 인식. x자리 s가 붙음
    - 대표적으로 passwd
    - chmod u+s
- Set-GID: 위와 같으나 그룹이라는 차이. 디렉터리에 많이 사용하고 그룹소유권 부분에서 x가 s로 변함
    - wall, write: /dev/tty2 같은 터미널을 사용하는 사용자에게 보내야 할 때
    - chmod g+s
- Sticky-Bit: 공유 디렉토리: other 계층에게 공유 디렉터리를 만들어줌. 생성은 가능하나 다른 사람의 파일을 삭제하지 못함. other 계층 부분의 x자리에 t가 붙음
    - /tmp 디렉토리
    - chmod o+t

### 소유권 허가권 관련 명령어

- chmod
    - r, w, x와 u, g, o, a - 기본이 a, + - = 을 사용해서 설정 해제 특정 권한만 지정
        - chmod o=r example.txt 하면 기존의 권한은 초기화하고 지정한 권한만 설정한다.
        - chmod  +rwx 를 하면 기본이 a이지만 o 계층에는 w가 부여되지 않는다.
    - 4, 2, 1의 가중치. 두 개 이상이면 더한다. 아무 것도 안 주려면 0
        - ex) 7 = 모두, 6 = 읽기, 쓰기, 3=읽기 실행 등등
- chown
    - 파일이나 디렉터리의 소유권을 변경
    - chown option owner:group file
- chgrp
    - 소유 그룹을 바꿈. 특정 사용자가 여러 그룹에 속해있다면 본인 소유의 파일을 본인이 속한 그룹 내에서 소유권 변경 가능
    - 심볼릭 링크의 파일 그룹 소유권을 바꾸면 원본 파일도 변경되는데 `-h` 를 사용하면 심볼릭 링크 파일만 바뀐다.
- umask
    - 0002면 기존 디렉토리 777, 파일 666에서 0002를 빼면 됨

### 파일 링크

- 디렉토리를 만들면 I-node라는 번호가 임의로 부여.
- 하나의 파일을 여러 개의 이름으로 관리하거나 디렉터리의 접근 경로를 단축하는 것이 링크
- ln으로 만들고 하드링크와 심볼릭 링크로 나눌 수 있음. 심볼릭은 -s를 붙인다.
- `ln 원본 만드려는 파일 이름`
- 하드링크
    - 복사하는 형태
    - i node 번호가 원본과 같다
- 심볼릭링크
    - i node가 다르다
    - 링크 파일 매우 작다
    - 원본 파일 없으면 암것도 못함

## 파일 시스템

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/44beb7e5-e5eb-4262-a675-7997c8f6159b/Untitled.png)

- 순서
    - 디스크 인식 여부 확인
    - 파티션 작업
    - 시스템 재부팅
    - 파일 시스템 생성
    - 마운트 포인트 디렉토리 생성
    - 마운트 작업
    - 부팅시 자동 마운트를 위한 /etc/fstab 파일에 등록
- 파티션 정보는 /proc/partitions
- fdisk: 장치 파일명으로 설정 가능
- mkfs: 새로운 파일 시스템을 만든다
    - -t 옵션으로 파일시스템 유형을 정한다. 기본은 ext2
    - 요즘 리눅스는 mke2fs 명령으로 실행됨
- mount
    - /etc/fstab에는 마운트 정보가 있다.
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/14f363cd-e167-48ff-8a0a-80c18443b23b/Untitled.png)
        
    - -o의 옵션에 rw는 기본으로 되어있다.
- eject
    - 이동식 보조기억장치 미디어를 꺼낼 때

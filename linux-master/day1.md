## CPU

- 리눅스 설치는 하드웨어 마다 달라진다. 최적화 문제나 32비트, 64비트 호환 등등
- cpu 정보를 확인하는 명령어는 `lscpu`이다.
    - 결과
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/e1540710-5619-4f24-bd82-8a3fd8af8f0c/Untitled.png)
        
        - 대충 제온 cpu에 64비트

## RAM

- 32비트 리눅스는 4GB 이상 장착 못함 - 페이징 기법 차이 때문

## 그 외

- 대부분 하드디스크 사용 가능, USB SSD도 가능
- 하드디스크 인터페이스에 따라서 파일명이 달라진다.
    
    <aside>
    💣 예시
    IDE disk: /dev/hda, /deb/hdb등
    SCSI, S-ATA. USB, SSD: /dev/sda, /deb/sdb 등
    
    </aside>
    
- X-WINDOW를 사용하면서 모니터, 비디오카드 필요성 증가
- 네트워크 인터페이스(이더넷 등)도 대부분 지원
- 나머지 키보드 마우스 CD롬도 인식 가능

---

# RAID

- 여러개의 하드디스크가 있을 때 동일한 데이터를 다른 위치에서 중복해서 저장하는 방법 → 성능 향상
- 데이터를 기록하는 방식, 에러 체크하는 페리티(Parity), ECC 사용 등 다양함
- 하나로 묶어주는 기술 `Linear`
    - 순서를 정해줌, 다 차야 다른 디스크에 저장
    - 스트라이핑이나 미러링이 보편적
- 하드웨어 RAID가 성능 good - 핫스왑, 베이

## 레이드에서 사용하는 기술

### 스트라이핑

- 라운드로빈 방식으로 기록
- 네 개의 섹터를 동시에 읽을 수 있어서 빠름

### 미러링

- 데이터 손실을 막기 위해 하나 이상의 장치에 추가적인 중복 저장
- 결함 허용이라고도 부름

## 레이드의 종류

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/1e0f351c-f62f-4db3-9c7e-4c517478338b/Untitled.png)

### RAID-0

- 스트라이핑 기술을 사용해서 빠른 입출력 속도 제공
- 중복이니 패리티 없음
    
    <aside>
    💣 패리티 비트는 정보의 전달 과정에서 오류가 생겼는지를 검사하기 위해 추가된 비트이다. 문자열 내 1비트의 모든 숫자가 짝수 또는 홀수인지를 보증하기 위해 전송하고자 하는 데이터의 각 문자에 1 비트를 더하여 전송하는 방법으로 2가지 종류의 패리티 비트가 있다.
    
    </aside>
    

### RAID-1

- 미러링 기술 사용, 스트라이핑은 노노
- 각 드라이브를 동시에 읽을 수 있어서 읽기 능력은 향상, 쓰기는 단일
- 디스크 낭비

### RAID-2

- 스트라이핑, ECC 적용

### RAID-3

- 스트라이핑, 패리티 정보를 위한 별도 하나의 디스크를 사용
- 입출력 작업이 동시에 이루어짐, 겹치게 못한다.

### RAID-4

### RAID-5

- 가장 많이 사용
- 최소 3개의 디스크
- 패리티 정보는 디스크에 분산 기록, 그러나 데이터 중복 저장하지 않음
- 모든 읽기 쓰기 중첩 가능
- RAID-0의 결합 허용을 지원 X, RAID-1의 저장공간 비효율성 극복

### RAID-6

- RAID-5에 패리티를 위한 디스크 하나를 추가하여 2개의 고장에 대응

### RAID-7

- 실시간 운영체제, 버스 사용

### RAID-0+1

- RAID-0 2개, RAID-1으로 미러링, 4개의 디스크 필요

### RAID-53

- RAID-3에 별도의 스트라이프 어레이 구성

---

# LVM(Logical Volume Manager)

- 하드 디스크를 추가할 때 파티션을 나눈다. 그런데 이건 고정이라 바꾸기 쉽지 않음
- 그래서 LVM을 이용해서 하드디스크를 자유롭게 붙이거나 땔 수 있음

### 물리적 볼륨(Physical Volume)

- 실제 디스크에 분할된 파티션. (예: /dev/sdb1. /dev/sdc1)

### 볼륨 그룹

- 물리적 볼륨이 모여서 생성하는 덩어리
- PE(physical extent)이 모인 큰 덩어리

### 논리적 그룹

- VG에서 할당하여 만들어지는 공간
- 스냅샷, RAID기능 적용 가능

### 물리적 확장

- PV에서의 블록 역할. 4mb

# 리눅스 구조

- 부트 매니저는 부트 로더 라고도 부름, 하드디스크 섹터0에 MBR은 설치됨
- 예전에는 LILO를 사용했으나 현재는 GRUB를 사용

## GRUB

- 환경설정 파일 ‘/boot/grub2/grub.cfg’,  링크파일인 /etc/grub2.cfg 도 사용
    - 이는 /etc/grub.d와 /etc/default/grub 파일을 참고
    - 파일 수정 후 ‘`grub2-mkconfig`’ 실행 (예: `grub2-mkconfig` -o /boot/grub2/grub.cfg)
    - -o 로 파일명을 지정해서 생성한다.

## 디렉토리 구조

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/3a361b94-31a2-469f-91a3-4cb25f44f9ee/Untitled.png)

- 디렉토리: 파일을 보관하는 곳, 최상위는 ‘/’
- /bin: binary의 약자, 실행파일이 들어있음
- /boot: 부팅 파일들, grub도 여기에 있다.
    - 나의 인스턴스도 grub를 사용한다.
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/6afd4a51-df5c-4411-ae6d-9ff14c4cd401/Untitled.png)
        
- /dev: 하드디스크, 터미널, cd-rom 등등 파일화
- /etc: 시스템 환경 설정 파일 등 부팅과 관련된 스크립트 파일
- /home: 개인 사용자 파일. amazon linux는 ec2-user가 기본
- /lib: 라이브러리, 커널 모듈이 여기에
- /lib64: 64비트 기반 리눅스면 만들어짐. 대부분 여기에 라이브러리가 있단다.
- /mnt: 장치를 마운트 할 때 포인터가 되는 디렉토리
- /opt: 응용 프로그램 설치 파일
- /proc 가상 파일 시스템, 운용되고 있는 다양한 프로세스 상태, 하드웨어 정보 등등
- /root root사용자의 홈
- /sbin: 시스템 관리에 대한 명령어. root가 사용하는 명령어들
- /tmp: 임시 저장 디렉토리, 모든 사용자에게 접근 가능
- /usr: 시스템 운영에 필요한 명령, 응용 프로그램 위치
    - /usr/bin, /usr/sbin 존재
    - x windo, mysql php등등 여기에 존재
- /var: 시스템 운영 로그, 스풀링. 메일도 여기로 온다.
- /media
- /srv: 사이트에서 생성되는 데이터를 담는다.
- /sys: 계층적 구조로 정보 제공. 가상 파일 시스템 sysfs에서 사용. hutplug 하드웨어 정보 담고 있음
- /run: 프로세스의 런타임 데이터를 저장함

## 부팅과 셧다운

- BIOS 점검 → 커널 로드 → 루트를 읽기로 마운트 → 이상 없으면 쓰기로 마운트 → init 프로세스 가동 → PID가 1번으로 할당 → 그 이후 프로세스는 init의 자식 프로세스(재부팅 용이)
- init 대신 systemd 사용

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/f880a2f9-c9f5-4218-ab86-60718ea0717d/Untitled.png)

- 로그인관련 메시지: /etc/issue, .net, /etc/motd(성공시)
- 자동로그아웃: /etc/profile/ 가서 ‘TMOUT=초’로 지정한다

### SYSTEMD

- system and service manager, 시스템 부팅 및 서비스 관리 프로그램
- 뭐 많은 기능들을 한다. timedatectl, hostnamectl 등등
- 유닛이라는 일종의 대상의 파일이 핵심
    - service, socket, path등의 type이 존재
    - /etc/systemd/systemd/.wants에 환경 설정 파일이 존재
        - 저는 system에 있었습니당
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/77968d74-16e8-4f33-8573-24c67aa2b18b/Untitled.png)
    

### systmed구조

### 유닛

- `man systemd.unit` 으로 확인 가능
- service: 서버에서 제공하는 서비스, daemon이라고 부른다.
- target: 유닛을 그룹화 ex) 부팅 레벨, 특정 동기화 지점
    - /lib/systemd/system
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/36ac2b99-6919-4768-a087-a53609230e92/Untitled.png)
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/8d3a4efd-4b52-4912-a9ce-33a45657c0b5/Untitled.png)
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/f6db9ba8-4861-409d-8244-fc81955af963/Untitled.png)
    
- ctrl-alt-del.target이 시작할 때 Unit이 실행된다는 뜻. 약간 depends on의 느낌?

<aside>
❓ **systemd의 target은 설정 파일이라고 볼 수 있지만, 그것들은 단순히 설정을 저장하는 것 이상의 역할을 합니다. target 파일들은 시스템의 특정 상태를 정의하며, 해당 상태에 필요한 서비스들이 어떤 것들인지를 명시합니다.**

**즉, target은 여러 서비스(데몬)들을 그룹화하고, 이러한 그룹을 사용하여 시스템 부팅 과정에서 어떤 서비스가 실행되어야 하는지 systemd에게 알려줍니다. 예를 들어 `graphical.target`는 GUI 환경이 필요한 모든 서비스를 포함하며, 시스템이 graphical mode로 부팅되면 이 target에 속한 모든 서비스가 시작됩니다.**

**따라서 systemd의 target는 "설정" 뿐만 아니라 "상태"나 "모드"도 정의합니다. 이것은 단순히 설정 정보를 저장하는 일반적인 설정 파일과는 차별화된 점입니다.**

</aside>

- socket: IPC 소켓을 말한다. (우리가 흔히 아는 소켓 통신)
- path:특정 파일 시스템이 변경될 때 까지 서비스의 활성화를 지연

## systemd 관련 명령어

- 타겟들
    
    [ec2-user@ip-172-31-0-250 ~]$ systemctl get-default
    graphical.target 
    
- `systemctl` 사용
- 책 참고

## systemd 로그관리

- `systemd-journald`가 생성하고 관리
- 관리는 `journalctl`
- syslog 의 로그레벨 정하기 옵션 -p → emerg, alert, crit, err, warning, notice, info, debug
- 로그는 /run/log/journal에 쌓인다.
    - 그러나 휘발성임으로 /var/log에 쌓아야 된다.
    - 설정은 /etc/systemd/journald.conf 에서 제어한다.
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/90893bab-a902-4618-9118-66ffe2873c77/Untitled.png)
    

<aside>
❓ **`mkdir -p -m2775 /var/log/journal`: 이 명령어는 `/var/log/journal` 디렉터리를 생성하고, 해당 디렉터리의 권한을 2775로 설정합니다. `-p` 옵션은 필요한 경우 상위 디렉터리도 함께 생성하라는 의미이며, `-m2775` 옵션은 생성된 디렉터리의 권한을 설정하는데 사용됩니다. 여기서 2775는 소유자와 그룹에게 읽기/쓰기/실행 권한을 주고, 다른 사용자에게는 읽기/실행 권한만 부여하며, 새로운 파일이나 서브디렉터리가 생성될 때 그것들의 그룹 소유권이 이 디렉터리와 동일하게 유지되도록 합니다.
`chgrp systemd-journal /var/log/journal`: 이 명령어는 `/var/log/journal` 디렉터리의 그룹 소유권을 `systemd-journal`로 변경합니다.
`killall -USR1 systemd-journald`: 이 명령어는 모든 systemd-journald 프로세스에 USR1 신호를 보냄으로써 journald 로깅 데몬에게 로그 파일 위치가 변경되었음을 알립니다.**

**따라서 위 세 개의 명령어들은 결합하여 systemd journald 서비스가 `/var/log/journal` 위치에 로그를 저장하도록 설정하는 작업을 수행합니다.**

</aside>

## timedatectl

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/bd2ffb58-d52e-4ae4-b151-dba645059b4b/Untitled.png)

- set-timezone
- set-ntp
    
    <aside>
    ❓ **`ntp`는 Network Time Protocol의 약자로, 컴퓨터 시스템에서 시간을 동기화하기 위한 프로토콜입니다. 이 프로토콜은 네트워크를 통해 접속 가능한 서버에서 정확한 시간 정보를 가져와서 로컬 컴퓨터의 시스템 시간을 조정합니다.**
    
    **`timedatectl set-ntp` 명령어는 systemd가 제공하는 `timedatectl` 도구를 사용하여 NTP 기반의 시간 동기화를 활성화하거나 비활성화하는 데 사용됩니다. 이 명령어 뒤에 `true` 또는 `false` 값을 주면 해당 값으로 NTP 기반의 시간 동기화를 설정할 수 있습니다.**
    
    **예를 들어, `timedatectl set-ntp true` 명령은 NTP 기반의 시간 동기화를 활성화하고, `timedatectl set-ntp false` 명령은 비활성화합니다. 이러한 설정은 서버와 같이 정확한 시간 정보가 중요한 컴퓨터에서 매우 유용합니다**
    
    </aside>
    

## hostnamectl

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/ca27ae00-f9bc-4104-8b1b-dd294d52b35d/Untitled.png)

## 시스템종료

- 그냥 컴퓨터 종료와 같은 것. 여러 명령어가 존재한다.

### shutdown

- root만 가능
- 다른 방법에 비해 안전하다.
- 예: shutdown -r now(재시작), -h(종료), -c(예약취소). -k(경고 메시지만 보내기)
- shutdown -h +10 &, `&` 를 통해서 백그라운드 프로세스로 실행

### reboot

- local로 접속한 사용자 모두 가능
- reboot -f → init 호출 없이 즉시 재부팅

### halt

- local로 접속한 사용자 모두 가능
- 시스템 종료 명령어

### poweroff

- 시스템 종료 및 전원 끄기, halt -p와 같음

### init

- init 프로세스에 직접 요청해서 실행레벨을 변경할 때 사용됨.
- 그냥 종료함으로 권장 x

# 파일 시스템 이해

- 운영체제가 파티션이나 디스크에 데이터를 저장하고, 읽고, 쓰고 찾기 위해 구성하는 일련의 체계
- 운영체제가 설치되고, format을 통해서 파일 시스템 구축
- 파일이라는 단위 위에 디렉터리에 저장
- 파일시스템은 엄청 많은데 RHEL 7 버전에는 현재 XFS를 기본 파일 시스템으로 채택
- proc도 파일시스템이었다. 커널 관련된 데이터를 담는 영역

### 저널링 파일 시스템

- 로그를 통해서 장애 복구를 수월하게 해준다.
- 파일 시스템에 대한 변경사항을 저널이라는 로그에 변경 사항을 저장하여 추적 가능하게 해줌
- ext3 이후

### ext 구조

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/5c72c849-a6a6-487e-a8e3-fa54153b7de4/Untitled.png)

- 아이노드는 뭘까?
    
    <aside>
    ❓ **아이노드(inode)는 유닉스 기반 시스템의 파일 시스템에서 중요한 데이터 구조입니다. 파일 시스템은 파일에 대한 메타데이터를 저장하는 데 하나의 아이노드를 사용합니다. ext는 리눅스에서 널리 사용되는 파일 시스템 형식 중 하나입니다.**
    
    **아이노드에 저장되는 정보에는 다음과 같은 것들이 있습니다:**
    
    **파일 소유자와 그룹파일 권한 (읽기, 쓰기, 실행 등)파일 크기파일 데이터가 저장된 물리적 위치생성, 수정, 접근 시간 등의 타임스탬프링크 수 (해당 아이노드를 참조하는 디렉터리나 다른 아이노드의 수)**
    
    **파일 이름은 아이노드에 직접 저장되지 않습니다. 대신, 디렉터리 엔트리가 이름과 연관된 아이노드 번호를 연결짓습니다.**
    
    </aside>
    

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/d3e2a59a-df1c-4139-89b3-78419333382a/Untitled.png)

- 슈퍼 블록과 그룹 기술자가 중요.
    - 그룹 기술자에 아이노드 비트맵, 아이노드 테이블, 블록 비트맵이 있다.
        - 아이노드 테이블: ls 명령어를 할 때 나타나는 정보들(디렉토리 정보)
        - 블록 비트맵: 블록 사용현황
    - 슈퍼 블록은 어떤 파일 시스템인지, 아이노드 수, 전체 블록 수, 블록 그룹 번호, 크기 등등을 기록
- 간접블록: 추가 데이터를 위한 포인터들을 위해 존재
- 홀: 간접블록이나 아니노드안의 데이터블록의 주소

## XFS

- 고성능의 저널링 파일 시스템 구현
- 로그 최적화, 완전한 64비트
- extent 기반 지연 할당 등등 할당 체계를 사용
- 자료구조는 b-tree
- 4종류 데몬을 이용 xfssyncd xfsbufd xfsdatad xfslogd

### 디스크 구조

- XFS는 할당 그룹이라는 단위로 나뉘어짐
- 독립적, 병렬적
- 크기를 정하지 않으면 기본적으로 8등분
- 0번은 슈퍼블록 → 잘 이해 안됨
- 아이노드 → 가변적 구조로

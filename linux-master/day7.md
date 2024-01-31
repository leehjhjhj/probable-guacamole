# 7회차

# 장치관리

## 모듈

- 리눅스에서 모듈이란: 우주선의 일부를 이루지만 독립적으로 행동할 수 있는 작은 소선(커널 모듈)
- 로드 모듈 = 커널의 일부가 된다, 언로드 = 커널과 별도로 존재한다.
- 모놀리식은 비효율, 그래서 리눅스는 커널 모듈을 사용
- /lib/modules/커널버전/kernel 디렉토리에 존재
- 레드헷은 ko.xz인데 우분투는 아직 .ko 인듯

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/ea54db28-9cd8-44db-b42e-df835d857aad/Untitled.png)

### 명령어

- `lsmod`: 커널 적재 모듈 정보 출력
- `insmod` 모듈 파일명: 커널에 모듈을 적재, but 의존성이 있는 모듈이면 적재 불가능
- `rmmod`
- `modprobe` 옵션 모듈 [기호=값]
    - 의존성이 있는 모듈도 적재, 제거 가능
    - -r을 사용하면 사용하지 않는 의존성 모듈도 모두 제거
    - 매개 변수도 할당 가능
- `modinfo`

### 모듈 관련

- 설정파일 /etc/modprobe.d 및 /lib/modeprobe.d 의 .conf 파일
- modules.dep 모듈 의존성 파일
    - /lib/modules/커널버전 디렉터리 안에 존재
    - `depmod`로 의존성을 관리함

## 커널

- 시스템 자원을 소유하고 관리하는 역할 수행
- 실제 리눅스의 버전은 커널 버전으로 평가한다. ‘`uname -r`’

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/2e0fd0c2-24bd-4aec-b8c4-fb26b44586e3/Untitled.png)

### 컴파일

- C 컴파일 도구 있으면 /usr/src/kernels 에 커널 버전의 소스를 다운로드
- configure 할 때 생기는 오브젝트 파일 및 config 파일을 지우기 위해 `make mrproper`을 사용한다.
- config 만들 때는 거의 `make menuconfig`를 사용한다.

## 주변 장치 설정

- 디스크, 프린터, 사운드 카드 , 스캐너

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/8bd5e5e7-be81-4a43-8dd5-c988830310ae/Untitled.png)

## LVM(논리볼륨관리자)

### 명령어

- pvscan
- vgscan
- pvcreate: fdisk를 이용해서 파티션을 분할시키고 LVM 속성으로 지정한뒤에 해당 파티션을 PV로 만들 때
- vgcreate
- vgdisplay
- lvcreate
    - lvcreate -L 2000M -n backup lvm0

<aside>
💡 장치 파일명은 /dev/VG명/LV명, /dev/mapper/VG명-LV명

</aside>

- lvscan
- lvdisplay
- vgextend: 이미 있는 VG에 PV를 추가
- vgreduce
- lvetend: 기본 단위는 mb, -L로 사이즈를 정해주어야함
    - PE가 뭐였지?
- lvreduce: 파괴된 경우 다시 mkfs해야 된다는 건 무슨소릴까(파일 시스템 다시 생성?)
- lvrename
- lvremove: 사용중인 경우 미리 unmount를 해야한다.
- vgchange: -a로 사용여부, -l로 생성할 수 있는 최대 LV를 제한
- vgremove
- pvmove: pe를 옮긴다.
- fsadm: 파일시스템의 크기를 조정하고 점검
    - check
    - resize

### 절차

1. fsdisk로 파티션 생성하고 LVM 속성으로 변경
    1. t를 누르고 8e 입력
    2. 후에 재부팅 or partprobe
2. pvcreate
3. vgcreate
4. lvcreate
5. 파일 시스템 생성
6. 마운트 디렉터리 생성
7. 마운트 실행
8. /etc/fstab에 등록
- lvm 확장도 같은 맥락. 디스크를 장착하고 pv로 만들고 vg에 추가한 뒤 lv를 확장시킨다. 그 이후에 파일 시스템 용량도 늘려줘야 파일시스템이 해당 용량을 인식한다.
- `fsadm resize lvm명`

## RAID

- mdadm을 통해서 Software RAID을 구성한다
    - 1, 4, 5, 6, 10 레벨 가능
    - 생성 후 정보는 `/proc/mdstat` 에서 확인 가능
- RAID-0
    - 2개의 파티션을 사용
- RAID-1
    - 2개의 파티션을 이용해서 하나의 디스크 오류에 대체 가능한 mirroring 기술
- RAID-5
    - 3개의 파티션 + 1개의 디스크 패리티
- RAID-6
    - 4개의 파티션이 필요. 2개의 디스크를 패리티로 사용
- /proc/mdstat에 RAID 관련 장치 상태 정보가 저장된다.
- /proc/partitions 에서도 장치명과 용량 확인 가능
- 오류가 발생했을 때, 결함이 허용되는 RAID 레벨에서는 오류가 발생한 디스크를 제거하고 디스크를 장착하면 자동 복구

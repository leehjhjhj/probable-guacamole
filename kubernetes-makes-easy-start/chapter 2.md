# Chapter 2

# 2.1 쿠버네티스 아키텍처

## 2.1.1 쿠버네티스 구조

- 쿠버네티스 클러스터: 여러 리소스 관리
- 마스터 노드: 클러스터 전체를 관리하는 시스템
- 워커 노드: 마스터 노드에 의해 명령을 받고 파드를 생성 → 서비스
- 컨테이너 런타임: 파드를 실행하는 엔진. 도커가 대표적
- 영구 스토리지: 파드는 휘발성, DB같은 중요한 데이터는 영구 스토리지에 저장. CSI로 외부 스토리지를 파드에 연결 가능

## 2.1.2 쿠버네티스 컴포넌트

파드 배포 명령어 이후 동작 순서를 서술한다.

```jsx
kubectl create -f deployment.yaml 
```

- 쿠버네티스에서 yaml은 매니페스트라고 한다.
1. API서버
    - 쿠버네티스 클러스터의 API를 사용가능하게 하는 프로세스
    - 요청에 대한 유효성 검사
        
        `kubectl create -f deployment.yaml` 
        
        1. 사용자 인증
        2. 명령어 검증
        3. 파드 생성
2. ectd
    - 클러스터의 상태를 저장, 즉 파드와 같은 리소스들의 상태 정보가 담겨 있음
    - 키-값으로 저장
    - 사용자에게 파드가 생성됨을 알림
3. 스케줄러
    - 파드를 위치시킬 적당한 워커 노드 확인(리소스를 참고)
    - API 서버에 이를 알리고 API서버는 etcd에 해당 정보 저장
4. kublet
    - 파드가 생성될 위치의 워커 노드에 있는 kublet에 파드 생성 정보 전달
    - 그리고 해당 정보를 통해 파드 생성
    - API서버에 생성된 파드 정보 전달 → API서버는 etcd에 저장

그 외. 

1. 컨트롤러 매니저
    - kube-controller-manger
        - 다양한 컴포넌트의 상태를 지속적으로 모니터링, 실행 상태 유지 역할
    - cloud-controller-manger
        - 퍼블릭 클라우드에서 제공하는 쿠버네티스와 연동되는 서비스들
2. 프록시
    - 클러스터 내부와 외부의 통신 담당
    - 모든 노드에서 실행되는 네트워크 프록시
3. 컨테이너 런타임
    - 컨테이너 실행을 담당
    - 도커, 컨테이너디, 크라이오

# 2.2 쿠버네티스 컨트롤러

파드를 관리하는 역할, 용도에 따라 선택적으로 사용

매니패스트 기본 골격

```yaml
apiVersion: # 사용하려는 쿠버네티스 API의 버전
kind: # 어떤 작업으로 할 것이냐
metadata: # 리소스에 대한 메타데이터를 제공. 이름(name), 네임스페이스, 레이블 및 주석 등을 포함
	...
spec: # 리소스에 대한 원하는 상태를 정의
	...
```

## 2.2.1 디플로이먼트

- 상태가 없는 애플리케이션을 배포할 때 사용

<aside>
💡 여기서 말하는 상태가 없다는?
파드가 삭제 되었을 때, 보존하지 않아도 되는 어플리케이션!

</aside>

- 레플리카셋의 상위 개념, 파드를 배포할 때 사용

## 2.2.2 레플리카셋

- 몇 개의 파드를 유지할지 결정하는 컨트롤러
- 레플리케이션도 있는데 잘 쓰이지 않는다.

## 2.2.3 잡

- 하나 이상의 파드를 지정하고 지정된 수의 파드가 성공적으로 실행되도록 함

## 2.2.4 크론잡

- 잡의 일종으로 특정 시간에 특정 파드를 실행시키는 것
- 데이터를 백업하는데 주로 사용

```
*　　　　　　*　　　　　　*　　　　　　*　　　　　　*
분(0-59)　　시간(0-23)　　일(1-31)　　월(1-12)　　　요일(0-7)
```

## 2.2.5 데몬셋

- 디플로이먼트처럼 파드를 생성하고 관리
- 차이점은 특정 노드 또는 모든 노드에 파드를 배포하고 관리
- 따라서 주로 노드마다 배치되어야 하는 성능 수집 및 로그 수집 같은 작업에 사용

<aside>
💡 테인트와 톨러레이션?
- 특정 노드에 특정 성격의 파드만 배포하고 싶을 때 사용
- 테인트가 설정된 노드에 일반적으로 사용되는 파드는 배포 불가능
`kubectl taint nodes [NODE_NAME] [KEY]=[VALUE]:[EFFECT]`
- 이펙트에는 세가지가 있다.
1. NoSchedule: 톨러레이션이 일치하는 파드만 배포
2. NoExecute: 기존에 이미 배포된 파드를 다른 노드에 옮김, 새로운 파드는 배포 못하게 함
3. PreferNoSchedule: 리소스가 부족할 때 배포할 수 있다.

</aside>

## 2.3 쿠버네티스 서비스

동적으로 변하는 파드에 고정된 방법으로 접근하기 위한 것이 서비스 → 고정된 주소

- 클러스터 IP: 클러스터 내부에서 파드들이 통신
- 노드포트: 서비스를 외부로 노출할 때 사용
    - ex) 워커 노드 IP: `192.186.2.3,` 포트: `30010`, `192.186.2.3:30010`로 접속 가능
- 로드밸런서: 퍼블릭 클라우드의 로드밸런서에 연결할 때 사용. 사용자는 로드밸런서의 외부 IP 사용
- 사용자 → 로드밸런서 → 노드포트 → 클러스터IP
- 인그레스: 클러스터 외부에서 내부로 접근하는 요청들을 어떻게 처리할지에 대한 규칙 모음

매니페스트

```yaml
apiVersion: v1
kind: Service
metadata:
	name: service-name
spec:
	type: service-type
	selector:
		app: webserver # 워커 노드의 컨테이너 중 webserver를 노출시킨다.
	ports:
	- protocol: TCP
		port: 80 # 서비스 - 컨테이너 애플리케이션과 매핑 시킬 포트 번호
		targetPort: 8080 # 컨테이너에서 구동되고 있는 애플리케이션 포트 번호
```

# 2.4 쿠버네티스 통신

## 특징들

- 파드의 (가상)네트워크와 노드의 (물리)네트워크는 다르다.
- 걑은 노드의 파드끼리만 통신이 가능하다
- 다른 노드와 통신하려면 CNI 플러그인 필요 → 별도 설치 必

## 2.4.1 같은 파드에 포함된 컨테이너 간 통신

- 직접 통신이 가능하다.
- 같은 가상 네트워크를 사용한다. = 동일 IP 사용
- 컨테이너들은 포트로 구분한다.
- 노드의 네트워크와 파드의 네트워크 사이에는 `docker0`이라는 브리지가 존재한다.

## 2.4.2 단일 노드에서 파드 간 통신

- 단일 노드에 떠있는 파드들은 같은 대역을 사용
- `docker0` 라는 브릿지를 사용해서 통신

## 2.4.3 다수의 노드에서 파드 간 통신

다른 노드의 파드 두개가 같은 IP라면?! → 오버레이 네트워크

- 오버레이 네트워크: 노드의 물리네트워크 위에 가상 네트워크를 구성, 모든 노드의 파드 간 통신 가능
- CNI 규약을 따르는 플러그인 별도 설치 필요, 대표적으로 **`플라넬`**
    - 파드 → 가상네트워크(veth1) → 플라넬 → 물리네트워크(eth1) → 라우터, 게이트웨이 → 물리네트워크 ..
    - 쿠버넷 안에 존재 … ?
- 칼리코, 실리움, 멀터스(다중네트워크) 등등 존재,,

<aside>
💡 **플라넬 CNI를 쓰면 브릿지를 거치지 않아도 단일 노드 내의 파드 간 통신이 가능할까?**

</aside>

## 2.4.4 파드와 서비스 간의 통신

## 서비스의 특성

- 파드처럼 IP를 갖는다.
- 파드와 서비스가 사용하는 IP 대역은 다르다.
- 서비스의 가상 네트워크는 ifconfig나 라우팅테이블에서 확인 불가능

## 그런데 서비스 IP로 특정 파드에 접속 가능 HOW?

### 리눅스 커널의 netfilter와 iptables로 가능!
# 쿠버네티스 사용하기

## 미니쿠베 설치

- `minikube start`
- `minikube dashboard`
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/1c1c3a57-7718-46a8-b4e4-bbd1113efc26/Untitled.png)
    

## yaml 파일 알아보기

- 매니페스트: 쿠버네티스의 오브젝트를 생성하기 위한 메타 정보를 yaml나 json 으로 기술한 파일

## 파드 생성하고 관리하기

- 파드에 여러개의 컨테이너: 사이드카(기본 기능 컨테이너 + 부가 기능 컨테이너 결합)
- 파드 생성 명령어
    - `kubectl create` : 클러스터에 새로운 리소스 생성
    - `kubectl apply` : create와 replace의 혼합 (생성된 오브젝트 삭제 후 새로운 오브젝트 생성)

```bash
> kubectl create deployment my-httpd --image=httpd --replicas=1 --port=80
> deployment.apps/my-httpd created
```

- deployment: stateless 파드 생성
- my-httpd: 디플로이먼트 이름
- — image: 파드를 생성하는데 사용되는 이미지
- —replicas=1 running 상태를 유지할 파드 개수
- —port=80 파드에 접근할 때 포트 번호

## Stateless VS stateful

- 세션을 저장해 둘 필요가 있냐? 없냐?

## kubectl get deployment

```bash
leehyunje@ihyeonje-ui-MacBookAir ~ % kubectl get deployment
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
my-httpd   1/1     1            1           2m59s
```

## kubectl get deployment -o wide

```bash
leehyunje@ihyeonje-ui-MacBookAir ~ % kubectl get deployment -o wide
NAME       READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES   SELECTOR
my-httpd   1/1     1            1           3m37s   httpd        httpd    app=my-httpd
```

- ready: 레플리카 개수
- up-to-date: 최신 상태 레플리카의 개수
- available: 사용 가능한 레플리카 개수
- age: 지속시간
- containers: 파드에 포함된 컨~~테이너 개수~~  → **Deployment에 의해 관리되는 Pod 내에서 실행되는 컨테이너의 이름**
- images: 파드 생성에 사용된 이미지
- SELECTOR: yaml파일의 셀렉터이며, yaml파일의 셀렉터는 라벨이 app=my-httpd 인 파드만 선택해서 서비스(관리) 하겠다는 의미

## kubectl get pod

- 파드 이름 및 상태를 확인

```bash
leehyunje@ihyeonje-ui-MacBookAir ~ % kubectl get pod               
NAME                       READY   STATUS    RESTARTS   AGE
my-httpd-cf79fbb57-gwnbd   1/1     Running   0          9m32s
```

## kubectl get pod -o wide

```bash
leehyunje@ihyeonje-ui-MacBookAir ~ % kubectl get pod -o wide 
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
my-httpd-cf79fbb57-gwnbd   1/1     Running   0          10m   10.244.0.8   minikube   <none>           <none>
```

- NOMINATED NODE: 예약된 노드
- READINESS GATES: 파드 상태 정보, 세부 정보를 확인하기 위해 추가 가능

## curl 10.244.0.8:80

```bash
leehyunje@ihyeonje-ui-MacBookAir ~ % curl 10.244.0.8:80
```

- timeout 발생!

## kubectl delete deployment my-httpd

- 디플로이먼트 삭제 명령
- pod를 삭제하고 싶으면 deployment 대신 `pod`
- 디플로이먼트를 삭제하면 pod도 삭제된다.

## kubectl edit <deployment or pod> <name>

- 디플로이먼트나 파드의 속성을 변경하는 명령어

## kubectl exec -it <pod name> — /bin/bash

```bash
leehyunje@ihyeonje-ui-MacBookAir ~ % kubectl exec -it my-httpd-cf79fbb57-9nmxg -- /bin/bash
root@my-httpd-cf79fbb57-9nmxg:/usr/local/apache2#
```

- —it
    - i: 컨테이너에 대화형 셸 형성
    - t: 대화형 터미널을 도커 컨테이너에 연결
- `exit`로 빠져나옴

## kubectl logs <pod-name>

```bash
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.244.0.9. Set the 'ServerName' directive globally to suppress this message
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.244.0.9. Set the 'ServerName' directive globally to suppress this message
[Fri Sep 22 12:08:01.277245 2023] [mpm_event:notice] [pid 1:tid 281473182855200] AH00489: Apache/2.4.57 (Unix) configured -- resuming normal operations
[Fri Sep 22 12:08:01.277381 2023] [core:notice] [pid 1:tid 281473182855200] AH00094: Command line: 'httpd -D FOREGROUND'
```

- 로그 확인

# 디플로이먼트와 서비스 이용하기

- 디플로이먼트
    - stateless 애플리케이션 배포에 용이
    - 레플리카셋의 상위 개념, 파드의 개수 유지, 배포 작업 세분화 관리

## 디플로이먼트 배포 전략

- 주로 어플리케이션이 변경될 때 사용
- 롤링, 재생, 블루/그린, 카나리

## 롤링 업데이트

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/109520b2-3a90-4432-b540-47fcd69a28e7/Untitled.png)

- 새 파드 배포할 때, 새 버전의 애플리케이션은 하나씩 늘려가고, 기존의 애플리케이션은 하나씩 줄임
- 표준 배포 방식
- 안정적이나 느리다.

## 

```yaml
leehyunje@ihyeonje-ui-MacBookAir ~ % kubectl edit deployment my-httpd
...

strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate

...
```

- replica와 template 중간에 삽입한다.
- maxSurge: 업데이트 중에 만들 수 있는 파드의 최대 개수
- maxUnavailable: 업데이트 중에 사용할 수 없는 파드의 개수

## 재생성 업데이트(recreate)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/2f1fb2b6-a6c6-43a8-94a3-4b3adc990c09/Untitled.png)

- 이전 버전의 파드를 모두 한번에 종료, 새 버전의 파드로 일괄교체
- 빠른 교체 but 장애 대처 곤란

## 블루/그린 업데이트

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/eeb85ee9-0b32-43b0-9d6b-bb801374a3c9/Untitled.png)

- V1과 V2가 동시에 운영
- 그러나 서비스로는 새버전의 파드만 가능하고, 이전 버전은 테스트 목적으로만
- 자원 이슈
- version으로 구분하여 관리. 이전 버전을 삭제하려면 새 버전으로 바꾼다.

## 카나리 업데이트

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/3619f475-2dc8-4e6a-9bf8-4c36291fef2e/Untitled.png)

- 몇몇 새로운 기능을 테스트할 때 사용
- 두 버전을 모두 배포, but 새 버전의 트래픽을 증가시켜서 기능 테스트

## 파드와 디플로이먼트의 차이?

- 파드: 컨테이너의 그룹
- 디플로이먼트
    - 원하는 동작이나 특성을 정의하는 파일
    - 각 파드 상태를 모니터링
    - 개발 운영 환경 사용하기 적합

## 디플로이먼트와 서비스 사용하기

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/3b1946fb-b9b6-49d9-9477-5b7732bb7558/Untitled.png)

- 기본적으로 파드는 같은 노드의 파드끼리만 통신 가능 → CNI 플러그인으로 해결
- BUT 플러스 알파로 쿠버네티스의 서비스도 필요함

## nginx.yaml

```yaml
apiVersion: apps/v1
kind: Deployment              
metadata:              
  name: nginx-deploy    
  labels:
    app: nginx                
spec:    
  replicas: 2    
  selector: # 디플로이먼트가 관리할 파드 선택
    matchLabels:
      app: nginx # 이 둘은 같아야함
  template: # 여기 정의된 내용에 따라 파드 생성
    metadata:
      labels:
        app: nginx # 이 둘은 같아야함
    spec:    
      containers:
      - name: nginx
        image: nginx:latest    
        ports:
        - containerPort: 80
```

- 디플로이먼트 → 파드 → 컨테이너 순으로 설정
- `kubectl apply -f nginx-deploy.yaml` 실행 (-f는 filename이라는 뜻)

```yaml
leehyunje@ihyeonje-ui-MacBookAir minikubetest % kubectl get deployments
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deploy   2/2     2            2           3m46s
```

- 두 개의 파드가 생성되었다.

```yaml
leehyunje@ihyeonje-ui-MacBookAir minikubetest % kubectl get pod        
NAME                            READY   STATUS    RESTARTS   AGE
nginx-deploy-57d84f57dc-6fs5g   1/1     Running   0          4m30s
nginx-deploy-57d84f57dc-6t76l   1/1     Running   0          4m30s
```

## 레이블이란?

- 오브젝트에 키-값 쌍으로 리소스 식별하고 속성을 지정
- 카테고리이다.

## nginx-svc.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc    
  labels:
    app: nginx
spec:
  type: NodePort #노드포트
  ports:
  - port: 8080
    nodePort: 31472
    targetPort: 80 # 컨테이너에서 구동되고 있는 애플리케이션 포트 번호
  selector:
    app: nginx
```

- `kubectl apply -f nginx-svc.yaml`로 서비스 생성
- `kubectl get svc`로 서비스 모아보기

```yaml
leehyunje@ihyeonje-ui-MacBookAir minikubetest % kubectl get svc                
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          2d1h
nginx-svc    NodePort    10.104.14.247   <none>        8080:31472/TCP   9s
```

→ minukube ip + NodePort의 Port로 접속하여도 응답이 없..다?

# 레플리카셋 사용하기

- 일정한 개수의 동일한 파드가 항상 실행되도록 함 → 서비스 지속성을 위해

## replicaset.yaml

```yaml
apiVersion: apps/v1
kind: ReplicaSet    
metadata:
  name: 3-replicaset    
spec:
  template:
    metadata:
      name: 3-replicaset
      labels:
        app: 3-replicaset
    spec:
      containers:
      - name: 3-replicaset    
        image: nginx
        ports:
        - containerPort: 80
  replicas: 3  # 3개 생성
  selector:
    matchLabels:
      app: 3-replicaset
```

- `kubectl apply - f replicaset.yaml`

```yaml
leehyunje@ihyeonje-ui-MacBookAir minikubetest % kubectl get replicasets,pods
NAME                           DESIRED   CURRENT   READY   AGE
replicaset.apps/3-replicaset   3         3         3       92s

NAME                     READY   STATUS    RESTARTS   AGE
pod/3-replicaset-5kjn6   1/1     Running   0          92s # 삭제 대상
pod/3-replicaset-qf2tz   1/1     Running   0          92s
pod/3-replicaset-zlfxb   1/1     Running   0          92s
```

## kubectl delete pod pod/3-replicaset-5kjn6

```yaml
leehyunje@ihyeonje-ui-MacBookAir minikubetest % kubectl get replicasets,pods             
NAME                           DESIRED   CURRENT   READY   AGE
replicaset.apps/3-replicaset   3         3         2       2m36s

NAME                     READY   STATUS              RESTARTS   AGE
pod/3-replicaset-qf2tz   1/1     Running             0          2m36s
pod/3-replicaset-sgrz5   0/1     ContainerCreating   0          4s
pod/3-replicaset-zlfxb   1/1     Running             0          2m36s
```

- 삭제를 하였는데도 파드의 개수는 3개로 유지된다.

## kubectl scale replicaset/3-replicaset —replicas=5

```yaml
NAME                           DESIRED   CURRENT   READY   AGE
replicaset.apps/3-replicaset   5         5         4       4m20s

NAME                     READY   STATUS              RESTARTS   AGE
pod/3-replicaset-f4278   0/1     ContainerCreating   0          3s
pod/3-replicaset-n2msk   1/1     Running             0          3s
pod/3-replicaset-qf2tz   1/1     Running             0          4m20s
pod/3-replicaset-sgrz5   1/1     Running             0          108s
pod/3-replicaset-zlfxb   1/1     Running             0          4m20s
```

- `kubectl scale replicaset/<레플리카셋 이름> —replicas=<개수>`
- 이후에 확인을하면 5개로 나온다.
- 기존의 파드 5개를 유지하고, 레플리카셋만 삭제하고 싶다면 `—cascade=orphan` 을 사용한다.

# 번외

## 롤백

- 롤링 업데이트와 함께 롤백도 지원. → 문제 발생시 버전 다운

## kubectl set image deployment.v1.apps/nginx-deploy nginx=nginx:1.16.1

- nginx 이미지의 버전을 바꾼다.

## kubectl describe deploy nginx-deploy

- `describe deploy`를 통해 배포 상태를 확인할 수 있다.

```yaml
...
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.16.1 # 잘 바뀌었다.
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
...
```

## 만약 없는 이미지 버전으로 업데이트 했다면?

- kubectl set image deployment.v1.apps/nginx-deploy nginx=nginx:1.9999

```yaml
kubectl rollout status deployment/nginx-deploy
Waiting for deployment "nginx-deploy" rollout to finish: 1 out of 2 new replicas have been updated...
```

- `kubectl rollout status deployment/<deployment이름>` 로 조회

```yaml
Waiting for deployment "nginx-deploy" rollout to finish: 1 out of 2 new replicas have been updated...
```

```yaml
leehyunje@ihyeonje-ui-MacBookAir minikubetest % kubectl get pods
NAME                            READY   STATUS             RESTARTS   AGE
nginx-deploy-665fc4dc89-45ctk   1/1     Running            0          5m13s
nginx-deploy-665fc4dc89-mrzr4   1/1     Running            0          5m22s
nginx-deploy-6dcb74f4d7-cm5q5   0/1     ImagePullBackOff   0          89s
```

- `ImagePullBackOff` 라는 오류 발생

## kubectl rollout undo deployment/<이름>

- 롤백 후 버전 확인

```yaml
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.16.1
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
```

## —to-revision=<번호>

- kubectl rollout histroy deployment/<이름>

```yaml
REVISION  CHANGE-CAUSE
1         <none>
3         <none>
4         <none>
```

- kubectl rollout undo deployment/nginx-deploy —to-revision=3 을 통해 특정 revision으로 롤백이 가능하다.

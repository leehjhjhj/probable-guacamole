# chapter4

# 컨피그랩과 비밀값으로 애플리케이션 설정하기

- 쿠버네티스에서 컨테이너에 설정값을 주입할 때 쓰는 것
    - 컨피그맵
    - 비밀값
- 클러스터 속에서 다른 리소스와 독립적인 곳에서 보관

### 환경변수 확인

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/c7e553ac-0397-4c85-8982-824b055c30f0/Untitled.png)

- printenv는 환경변수의 값을 출력하는 리눅스 명령어

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sleep
spec:
  selector:
    matchLabels:
      app: sleep
  template:
    metadata:
      labels:
        app: sleep
    spec:
      containers:
        - name: sleep
          image: kiamol/ch03-sleep
          env:
          - name: KIAMOL_CHAPTER
            value: "04"
```

- env가 추가

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/a7363b5e-eb58-4df9-8f5c-36f8a3c604bc/Untitled.png)

- 그러나 실제 환경 변수는 훨씬 복잡하고, 이 때는 컨피그맵을 이용한다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/fdddb799-1ade-42dd-a6b0-7b811609d606/Untitled.png)

```yaml
spec:
      containers:
        - name: sleep
          image: kiamol/ch03-sleep
          env:
          - name: KIAMOL_CHAPTER
            value: "04"
          - name: KIAMOL_SECTION
            valueFrom:
              configMapKeyRef:              
                name: sleep-config-literal #이놈이 컴피그맵
                key: kiamol.section
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/a876a76c-4639-43e2-9e45-c50a1ec94601/Untitled.png)

- 이렇게 간단하게 만들 수 있다.
- cm은 configMap이 약자이다!

## 컨피그맵에 저장한 설정 파일 사용하기

```yaml
leehyunje@ihyeonje-ui-MacBookAir ch04 % cat sleep/ch04.env
KIAMOL_CHAPTER=ch04
KIAMOL_SECTION=ch04-4.1
KIAMOL_EXERCISE=try it now
```

- 이렇게 파일로 해서 `kubectl create configmap sleep-config-env-file --from-env-file=sleep/ch04.env` 명령으로 env파일의 기반으로 컨피그맵 생성 가능

```yaml

envFrom:
	- configMapRef:
			name: sleep-config-env-file
```

- deploy에서 endFrom에서 환경변수로 만든 컨피그맵을 불러온다.
- 환경 변수의 이름이 같을 경우 envFrom 항목의 값이 우선된다. → 편리!
- json 파일 등, 어플리케이션의 기본 값 설정은 컨테이너 이미지에 포함시키지만 이렇게 우선순위를 활용해서 필요한 설정 값들을 엎어 씌운다.
- 처음에 /config를 접속했지만 실패

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/249c298c-3015-4491-af95-ad59c2c31ec1/Untitled.png)

- 이렇게 된 컨피그맵을 적용시킨 후 다시 파드를 생성해보자.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-web-config-dev
data:
  config.json: |-
    {
      "ConfigController": {
        "Enabled" : true
      }
    }
```

- 필자는 이렇게 컨피그맵 안에 json 내용도 넣는 것을 선호한다고 한다. apply 한방에 가능하기 때문
- 결과

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/9e7f9931-9b62-4802-b8b6-3901ebf8765c/Untitled.png)

## 컨피그맵에 담긴 설정값 데이터 주입하기

- 컨테이너 파일 시스템 속 파일로 설정 값을 주입할 수 있음
- 컨피그맵은 디렉토리, 각 항목은 파일 형태로 컨테이너 파일 시스템에 추가

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/a2b19a12-bb5a-4614-a88c-01089664bad5/Untitled.png)

- 아까 생성한 configMap이 이렇게 파일화 된 것을 보여주는 이미지이다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/f715269b-1f6a-41b3-98bb-32dc1993d599/Untitled.png)

- 이렇게 하면 파일화된 컨피그맵의 볼륨이 생성되고, /app/config에 마운트 된다.
- 이렇게 되면 컨피그맵 속의 config.json의 값이 우선 적용됨
- 도커컴포즈의 마운트 처럼 폴더가 없으면 생성해준다.
- 컨피그맵만 업데이트 되면 수정된 파일을 컨테이너에 전달하나, 파드가 대체될 때까지는 아무런 일이 일어나지 않는다.
- 주의해야 될 점은 디렉토리를 잘 설정해야 된다 /app 으로 하게되면 마운트 될 파일들이 추가되는 것이 아니라 그대로 덮어 씌이게 된다. (제 생각에는 그냥 볼륨으로 연결만 해주는 듯)

```yaml
volumes:
- name: config
	configMap:
		name: todo-web-config-dev
		items:
			- key: config.json
				path: config. json
```

- 이렇게 하면 특정 파일만 전달 할 수 있다.

## 비밀 값을 이용하여 민감한 정보가 담긴 설정값 다루기

- 해당 값을 사용해야 되는 노드에만 전달, 노드에서도 메모리에만 담김

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/47f212e0-91b5-4a21-9410-0e2a686bb0ef/Untitled.png)

- describe에서도 표기되지 않는다.
- | base64 -d로 인코딩 해야지 볼 수 있다. 평문으로 노출되는 것을 막음
- 하지만 이렇게 컨테이너로 전달되면 평문이 출력된다.

```yaml
containers:
- name: sleep
	image: kiamol/ch03-sleep
	env :
		- name: KIAMOL_SECRET
			valueFrom:
				secretKeyRef:
					name: sleep-secret-literal
					key: secret
```

- 이렇게 해당 비밀 값을 컨테이너로 전달한다.
- 리소스 객체의 정보에는 평문이 그대로 저장된댜.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-db
spec:
  selector:
    matchLabels:
      app: todo-db
  template:
    metadata:
      labels:
        app: todo-db
    spec:
      containers:
        - name: db
          image: postgres:11.6-alpine
          env:
          - name: POSTGRES_PASSWORD_FILE
            value: /secrets/postgres_password
          volumeMounts:
            - name: secret
              mountPath: "/secrets"
      volumes:
        - name: secret
          secret:
            secretName: todo-db-secret-test
            defaultMode: 0400
            items:
            - key: POSTGRES_PASSWORD
              path: postgres_password
```

- 채찍비티 해설
    
      **◦ `env`: 컨테이너의 환경 변수를 설정합니다.
                        ▪ `name: POSTGRES_PASSWORD_FILE`: 환경 변수의 이름을 'POSTGRES_PASSWORD_FILE'로 설정합니다.
                        ▪ `value: /secrets/postgres_password`: 'POSTGRES_PASSWORD_FILE' 환경 변수의 값을 '/secrets/postgres_password'로 설정합니다. 이는 비밀번호를 참조하는 데 사용됩니다.
                    ◦ `volumeMounts`: 컨테이너에 마운트할 볼륨을 정의합니다.
                        ▪ `name: secret`: 마운트할 볼륨의 이름을 'secret'으로 설정합니다.
                        ▪ `mountPath: "/secrets"`: 볼륨이 마운트될 컨테이너 내의 경로를 '/secrets'로 설정합니다.
                • `volumes`: 파드에 추가할 볼륨의 목록을 정의합니다.
                    ◦ `name: secret`: 볼륨의 이름을 'secret'으로 설정합니다.
                    ◦ `secret`: 이 볼륨이 시크릿 볼륨임을 나타냅니다.
                        ▪ `secretName: todo-db-secret-test`: 사용할 시크릿의 이름을 'todo-db-secret-test'로 설정합니다.
                        ▪ `defaultMode: 0400`: 시크릿 파일의 기본 권한 모드를 설정합니다. 여기서 '0400'은 소유자만 읽을 수 있음을 나타냅니다.
                        ▪ `items`: 시크릿에서 생성할 항목을 정의합니다.
                            • `key: POSTGRES_PASSWORD`: 시크릿에서 참조할 키를 'POSTGRES_PASSWORD'로 설정합니다.
                            • `path: postgres_password`: 해당 키의 값이 저장될 파일의 경로를 'postgres_password'로 설정합니다.**
    

## 쿠버네티스의 애플리케이션 설정 관리

### 어플리케이션의 중단 없이 설정 변경에 대응이 필요한가?

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/9ae63286-e1e1-4d61-8272-a70ab93a2608/Untitled.png)

- 볼륨을 수정하면 파드를 교체해야 하지만(디플로이 파일을 변경하는 것 같습니다.), 기존의 컨피그맵이나 비밀값을 업데이트 하면 파드를 교체하지 않아도 된다.
- 두번째 방식은 파드 교체가 필요하지만, 이전 설정값들이 남아 있어서 다시 돌아갈 수 있다.

### 민감 정보를 어떻게 관리할 것인가?

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/19f14110-c29c-496f-9b95-062969c86b08/0f1933f3-c865-4020-b4e6-0dcca28aa7f1/Untitled.png)

- 깃헙 시크릿이나 aws configure을 사용하는 것 같다.

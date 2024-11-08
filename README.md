# git clone
    git clone https://github.com/sihogu/deepdrive.git

# Installation
    pip install -r requirements.txt

### 주의 사항
- `requirements.txt`에는 torch, torchvision, CUDA 버전이 명시되지 않습니다.
이유는 일반적인 설치 명령으로는 특정 CUDA 버전을 지정할 수 없기 때문입니다.

# 학습 방법
## 1.merge 없이 학습 
    python -m train

## 2.merge 후 학습 (주의: merge.py 실행 시 원본 데이터가 변경됨)
    python -m merge
    python -m train

or

    python -m train --use_merge

# train 옵션 설정
## 학습 디바이스 설정 (기본값: 자동으로 사용 가능한 CUDA 디바이스 확인)



- 여러 디바이스 사용:

      python -m train --device 0,1,2

- CPU 사용:
  
      python -m train --device cpu
- 하나의 디바이스만 사용:

        python -m train --device 0

## 학습 프로세스 워커 개수 설정 (기본값: 8)

```bash
python -m train --workers 8

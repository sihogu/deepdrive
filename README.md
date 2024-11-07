# git clone
    git clone https://github.com/sihogu/deepdrive.git

# Installation
    pip install -r requirements.txt


# 실행 예시
## 1.merge 없이 학습 
    python -m train

## 2.merge 후 학습 (주의: merge.py 실행 시 원본 데이터가 변경됨)
    python -m merge
    python -m train

or

    python -m train --use_merge

## train 옵션 설정
- 학습 디바이스 설정 (기본값: 자동으로 사용 가능한 CUDA 디바이스 확인)



여러 디바이스 사용:

    python -m train --device 0,1,2

CPU 사용:

    python -m train --device cpu

- 학습 프로세스 워커 개수 설정 (기본값: 8)

```bash
python -m train --workers 8

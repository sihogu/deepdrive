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
학습 device id (default = torch.cuda.device_count() 자동으로 cuda device 확인)


여러개의 디바이스:

    python -m train --device 0,1,2

CPU:

    python -m train --device cpu

학습 process workers 개수 (default = 8)

    python -m train --workers 8
  

## Installation
'pip install -r requirements.txt'


## 실행 예시
# 1.merge 없이 학습 (merge를 한번이라도 하면 merge없이 불가능)
'''python
python -m train

# 2.merge 후 학습
'python -m merge'
'python -m train'

or

'python -m train --use_merge'

# 3.train 옵션 설정
학습 device id (default = 0)

여러개의 디바이스:
'python -m train --device 0,1,2'

CPU:
'python -m train --device cpu'

학습 process workers 개수 (default = 8)
'python -m train --workers 8'

# train.py

import os
import argparse
from ultralytics import YOLO
import torch
import sys
import json
import yaml

torch.cuda.empty_cache()

#next.yaml의 path 수정
def update_yaml_path(current_dir,dir_name):
    yaml_file = os.path.join(current_dir,dir_name,'nextchip.yaml')

    with open (yaml_file, 'r',encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    yaml_data['path'] = 'datasets/nextchip'

    with open(yaml_file, 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)
    
    print(f"Updated path to {current_dir, dir_name} in {yaml_file}")

#욜로 데이터셋 지정경로를 강제로 현재 경로로
def update_datasets_dir():   
    settings_path = os.path.join(os.getenv('APPDATA'), 'Ultralytics', 'settings.json')
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    if os.path.exists(settings_path):
        with open(settings_path, 'r+') as f:
            settings = json.load(f)
            settings['datasets_dir'] = current_dir
            f.seek(0)
            json.dump(settings, f, indent=4)
            f.truncate()
        print(f"Updated datasets_dir to {current_dir}")
    else:
        print("Ultralytics settings.json file not found.")

def parse_device(value):
    if value.lower() == 'cpu':
        return 'cpu'
    
    # 여러 GPU를 사용할 경우
    try:
        devices = [int(x) for x in value.split(',')]
        return devices
    except ValueError:
        return int(value)

def get_available_devices():
    # 사용 가능한 GPU 디바이스가 없으면 CPU 사용
    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        if device_count > 1:
            devices = [str(i) for i in range(device_count)]  # 여러 GPU 사용
            print(f"Using multiple GPUs: {devices}")
            return ','.join(devices)
        else:
            print(f"Using single GPU: {0}")
            return '0'
    else:
        print("CUDA is not available. Using CPU.")
        return 'cpu'

def parse_args():
    parser = argparse.ArgumentParser(description="Train YOLO model with optional dataset merge.")
    parser.add_argument('--dir_name', type=str, default='datasets/nextchip', help="Dataset directory name")
    parser.add_argument('--workers', type=int, default=8, help="Dataset directory name")
    parser.add_argument('--device', type=str, default=get_available_devices(), help="Device id or list of device ids (e.g. 0 or 0,1)")
    parser.add_argument('--use_merge', action='store_true', help="Merge test into train before training")
    return parser.parse_args()

def main():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    update_datasets_dir()

    args = parse_args()

    if 'datasets' not in args.dir_name:
        dir_name = os.path.join('datasets',args.dir_name)
    else:
        dir_name = args.dir_name
        
    device = args.device
    workers = args.workers
    
    update_yaml_path(current_dir,dir_name)

    if args.use_merge:
        print("Merging test set into train set...")
        import merge
        sys.argv = [sys.argv[0], '--dir_name', dir_name]
        merge.main()
    
    model = YOLO(os.path.join(current_dir,'config','deepdrive.yaml'))

    
    data_path = os.path.join(current_dir, dir_name, 'nextchip.yaml')

    results_train = model.train(
        data=data_path,
        epochs=500,
        patience=50,
        batch=15,
        workers=workers,
        device=device,
        auto_augment='autoaugment'
    )

if __name__ == "__main__":
    main()

import yaml
import os
import json

#next.yaml의 path 수정
def update_yaml_path(current_dir, dir_name):
    yaml_file = os.path.join(current_dir, dir_name,'nextchip.yaml')

    try:
        with open (yaml_file, 'r',encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
        yaml_data['path'] = dir_name

        with open(yaml_file, 'w',encoding='utf-8') as file:
            yaml.dump(yaml_data, file, default_flow_style=False)
        
        print(f"Updated path to {dir_name} in {yaml_file}")
    except FileNotFoundError:
        print(f"File not found: {yaml_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

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

def main(dir_name='datasets/nextchip'):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    update_datasets_dir()
    update_yaml_path(current_dir, dir_name)
    

if __name__ == "__main__":
    main()

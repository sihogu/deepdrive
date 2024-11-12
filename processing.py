import yaml
import os
import json
import tarfile

#압축해제
def extract_tgz(tgz_path, extract_to):
    if os.path.exists(extract_to) and os.listdir(extract_to):
        print(f"Directory '{extract_to}' already contains files. Extraction skipped.")
        return
        
    with tarfile.open(tgz_path, 'r:gz') as tar:
        print('Extracting...')
        tar.extractall(path='datasets')
    print(f"Extracted {tgz_path} to datasets")


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

def main(dir_name=os.path.join('datasets','nextchip_shared')):
    current_dir = os.path.abspath(os.path.dirname(__file__))

    update_datasets_dir()
    update_yaml_path(current_dir, dir_name)
    extract_tgz(os.path.join('datasets','merge_source.tgz'), extract_to=os.path.join('datasets','merge_source'))
    extract_tgz(os.path.join('datasets','nextchip.tgz'), extract_to=os.path.join('datasets','nextchip_shared'))
    

if __name__ == "__main__":
    main()

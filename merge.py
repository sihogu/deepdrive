# merge.py

import os
import shutil
import argparse
import tarfile

def extract_tgz(tgz_path, extract_to):
    if os.path.exists(extract_to) and os.listdir(extract_to):
        print(f"Directory '{extract_to}' already contains files. Extraction skipped.")
        return
        
    with tarfile.open(tgz_path, 'r:gz') as tar:
        print('Extracting...')
        tar.extractall(path='datasets')
    print(f"Extracted {tgz_path} to datasets")

def parse_args():
    parser = argparse.ArgumentParser(description="Merge test images and labels into train set.")
    parser.add_argument('--dir_name', type=str, default=os.path.join('datasets','nextchip_shared'), help="Base directory for dataset")
    return parser.parse_args()

def move_files(source_dir, destination_dir, all_files, extension, start_num):

    if not all_files:
        print(f'{extension} file does not exist. Path checked:{source_dir}')

    for i, file in enumerate(all_files):
        new_name = f"{i + start_num}.{extension}"
        old_path = os.path.join(source_dir, file)
        new_path = os.path.join(destination_dir, new_name)

        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            print(f"Moved {extension} file: {file} -> {new_name}")
        else:
            print(f"{extension} file {file} does not exist.")

# def copy_files(source_dir, destination_dir, all_files, extension, start_num):
#     if not all_files:
#         print(f'{extension} file does not exist. Path checked: {source_dir}')

#     for i, file in enumerate(all_files):
#         new_name = f"{i + start_num}.{extension}"
#         old_path = os.path.join(source_dir, file)
#         new_path = os.path.join(destination_dir, new_name)

#         if os.path.exists(old_path):
#             shutil.copy2(old_path, new_path)
#             print(f"Copied {extension} file: {file} -> {new_name}")
#         else:
#             print(f"{extension} file {file} does not exist.")

def replace_txt_file(destination_img_dir, txt_file_path):
    start_img_num = len(os.listdir(destination_img_dir))
    len_size=sorted(list(map(str,list(range(start_img_num)))))
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write("./images/train\n")
        for i in len_size:
            txt_file.write(f"./images/train/{i}.jpg\n")

def main():
    args = parse_args()
    if 'datasets' not in args.dir_name:
        base_dir = os.path.join('datasets',args.dir_name)
    else:
        base_dir = args.dir_name
    
    extract_tgz(os.path.join('datasets','merge_source.tgz'), extract_to=os.path.join('datasets','merge_source'))
    extract_tgz(os.path.join('datasets','nextchip.tgz'), extract_to=os.path.join('datasets','nextchip_shared'))

    source_img_dir = os.path.join(base_dir, 'images', 'test')
    destination_img_dir = os.path.join(base_dir, 'images', 'train')

    source_label_dir = os.path.join('datasets','merge_source', 'test')
    destination_label_dir = os.path.join(base_dir, 'labels', 'train')

    txt_file_path = os.path.join(base_dir, 'train.txt')
    all_imgs = sorted(os.listdir(source_img_dir), key=lambda x: int(os.path.splitext(x)[0]))
    all_labels = sorted(os.listdir(source_label_dir), key=lambda x: int(os.path.splitext(x)[0]))

    start_img_num = len(os.listdir(destination_img_dir))
    start_label_num = len(os.listdir(destination_label_dir))
    
    move_files(source_img_dir, destination_img_dir, all_imgs, 'jpg', start_img_num)
    move_files(source_label_dir, destination_label_dir, all_labels, 'txt', start_label_num)
    replace_txt_file(destination_img_dir, txt_file_path)

if __name__ == "__main__":
    main()

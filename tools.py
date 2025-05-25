import os
import shutil

def create_or_clear_folder(folder_path):
    if os.path.exists(folder_path):
        # 資料夾存在，刪除裡面所有內容
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 刪除檔案或符號連結
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 刪除子資料夾
            except Exception as e:
                print(f'刪除 {file_path} 時發生錯誤: {e}')
    else:
        # 資料夾不存在，建立它
        os.makedirs(folder_path)



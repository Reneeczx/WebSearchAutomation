import requests
import zipfile
import io
import os
import shutil

def download_chromedriver():
    print("开始下载ChromeDriver...")
    # 使用Stable通道的132.0.6834.83版本
    url = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/132.0.6834.83/win64/chromedriver-win64.zip"
    
    try:
        # 下载文件
        print("正在下载...")
        response = requests.get(url)
        response.raise_for_status()
        
        # 解压文件
        print("正在解压...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(".")
            
        # 移动chromedriver到正确位置
        print("正在设置ChromeDriver...")
        if os.path.exists("chromedriver.exe"):
            os.remove("chromedriver.exe")
        os.rename("chromedriver-win64/chromedriver.exe", "chromedriver.exe")
        
        # 清理临时文件
        print("清理临时文件...")
        if os.path.exists("chromedriver-win64"):
            shutil.rmtree("chromedriver-win64")
        
        print("ChromeDriver下载和设置完成！")
        
    except Exception as e:
        print(f"下载失败: {str(e)}")

if __name__ == "__main__":
    download_chromedriver() 
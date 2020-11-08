# @Time : 2020/11/1 15:25 
# @Author : LeeWJ
# @Function  :
# @Version  : 1.0

import os
import time
import requests
import excel


#demo1
def ts_download(path,workbook,worksheet):
    previous_raw_video = ''
    for i in range(1,100):
        try:
            e = excel.Excel(workbook, worksheet)
            name = e.read(i,1)
            url = e.read(i,3)
            key = e.read(i,5)
            raw_video = rf"{path}\raw\{name}.ts"
            video = rf"{path}\{name}.ts"
            print(f'名字：{name},TSURL：{url}，密钥：{key}')
            start_time = time.time()
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
            }
            print('下载中...')
            req = requests.get(url=url,headers=headers, stream=True)
            try:
                total_kb = req.headers.get('Content-Length')
                total_mb = int(total_kb)/1024/1024
                total_mb = f'{str(total_mb)}'
            except:
                total_mb = 'unknown size'
            size = 0
            print(' ')
            with open(raw_video , "wb") as f:
                for chunk in req.iter_content(chunk_size=10240000):  # 每次加载10240000字节
                    f.write(chunk)

                    if size%(1024*3) == 0:
                        print(f'{name}： {str(size/1024)}M / {total_mb}M', end='\n', flush=True)
                    size +=10240


            if not os.path.exists(path):
                os.mkdir(path)

            end_time = time.time()
            print(f"整个文件下载完成,共花费了{end_time - start_time}秒，总大小为{total_mb}MB")
            print(f'开始异步解密文件{video}，同时删除上一个原始ts:{previous_raw_video}...')
            if not previous_raw_video == '':
                try:
                    os.remove(previous_raw_video)
                except Exception as e:
                    print(f'删除失败：{str(e)}')
            try:
                cmd = rf'openssl aes-128-cbc -d -in {raw_video} -out {video} -nosalt -iv 00000000000000000000000000000000 -K {key}'
                print(f'解密命令：{cmd}')
                f = os.popen(cmd)

                #f.readlines() #阻塞
            except Exception as e:
                print(e)
            previous_raw_video = raw_video

        except Exception as e:
            print(f'全局错误：{str(e)}')
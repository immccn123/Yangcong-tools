# 使用方法

## 从二进制文件运行（Windows）
从[这里](https://github.com/mashirozx/sakura/releases/latest)下载最新可执行文件（ych.exe）。

打开 cmd，把 yct.exe 拖入窗口中，此时命令类似于下列格式：
```batch
C:\Users\Imken_Reborn\Desktop\Yangcong-tools\yct.exe
```

若要完成作业，请在最后追加 `hw do`：
```batch
C:\Users\Imken_Reborn\Desktop\Yangcong-tools\yct.exe hw do
```

## 从源码运行

```sh
git clone https://github.com/immccn123/Yangcong-tools.git
cd Yangcong-tools/src
python -m pip install -r requirements.txt   # for linux users run `python3`
python yct.py                               # for linux users run `python3`
```

## 高级使用方法

### 多用户/保存密码

在运行目录下新建 `users.json`，格式参见 `users.sample.json`。例如：
```json
[
    {
        "username": "您的用户名",
        "password": "您的密码"
    },
    {
        "username": "第二个用户的账号",
        "password": "114514"
    }
]
```

请确保最后一个大括号 `}` 之后没有逗号。

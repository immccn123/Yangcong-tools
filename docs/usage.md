# 使用方法

## 克隆项目

```sh
git clone https://github.com/immccn123/Yangcong-tools.git
cd Yangcong-tools
```

## 安装依赖

```sh
python -m pip install -r requirements.txt
```

## 运行程序

```sh
python ./main.py
```

## 精简项目

安装依赖后，可以只保留以下文件。
```
Yangcong-tools
 ├─ main.py
 └─ api.py
```

## 高级使用方法

### 多用户/保存密码

在项目根目录下新建 `users.json`，格式参见 `users.sample.json`。例如：
```json
[
    {
        "username": "您的用户名",
        "password": "您的密码"
    }
]
```

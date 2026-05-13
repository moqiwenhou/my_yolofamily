# Django Web 系统（PyCharm 可直接打开）

## 功能
- 登录/注册
- 上传视频文件
- 点击“开始跟踪”触发 YOLO + DeepSort 跟踪
- 在网页展示输出参数与输出视频

## 快速启动
```bash
cd django_yolo
pip install -r ../requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

访问：`http://127.0.0.1:8000/`

> 说明：`tracker/services.py` 复用仓库中的 `main.py`、`deep_sort` 与 `ultralytics` 实现目标检测跟踪流程。

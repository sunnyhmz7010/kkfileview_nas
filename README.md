# kkfileview_nas
![image](https://github.com/user-attachments/assets/7da484ed-46c8-4263-a2eb-35d11c77abfd)
这是一个专门用于NAS版的文件文档预览项目，基于[kkfileview]([url](https://kkview.cn/zh-cn/index.html))

# 如何部署
## 使用docker Compose
```bash
services:
  kkfileview_nas:
    image: kkfileview_nas:latest
    container_name: kfileview_nas
    restart: always
    environment:
      - FILE_URL_DATA=192.168.10.28:5000 #NAS地址+当前容器映射的宿主端口
      - PREVIEW_URL_DATA=192.168.10.28:8012 #kkfileview服务地址+当前容器映射的宿主端口
    volumes:
      - /vol1/1000/文件:/app/files  # 需要预览的文件夹
    ports:
      - "5000:5000"  #映射的服务地址

  kkfileview:
    image: keking/kkfileview:latest
    container_name: kkfileview-container
    restart: always
    environment:
      - KKFILEVIEW_PORT=8012
    ports:
      - "8012:8012"  # 映射的服务地址
```

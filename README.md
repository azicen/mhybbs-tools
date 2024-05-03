# mhybbs-tools

米游社签到工具


## 功能

- [x] 原神签到
- [x] 星穹铁道签到


## 用户配置

每个`*.toml`文件配置一个需要米游社签到的账号。

配置文件模板位置: `./conf/conf.template.toml`。

```toml
# 账户cookie
cookie = ""

[act]
# 是否进行米游社原神签到
genshin_impact = true
# 是否进行米游社星穹铁道签到
honkai_star_rail = true

[job]
# 预计每日签到的时间
trigger_time = "8:30"
```


## 使用

### 快速启动

```sh
mkdir ./config
cp ./conf/conf.template.toml ./config/user.toml

vim ./config/user.toml
# 在配置文件中设置账户cookie

python main.py
```


### 通过docker部署
```sh
docker run \
  -e TZ="Asia/Shanghai" \
  -e CONFIG_DIR="/app/config" \
  -e JOB_TIME_INTERVAL=30 \
  -e USER_INTERVAL=5 \
  -v "./config:/app/config" \
  ghcr.io/azicen/mhybbs-tools:latest
```


### 通过docker-compose部署
```yaml
version: '3.8'

services:
  mhybbs-tools:
    image: "ghcr.io/azicen/mhybbs-tools:latest"
    container_name: mhybbs-tools
    environment:
      TZ: "Asia/Shanghai"
      CONFIG_DIR: "/app/config"
      JOB_TIME_INTERVAL: 30
      USER_INTERVAL: 5
    volumes:
      - "./config:/app/config"
```


## 环境变量

| 变量名 | 描述 | 默认值 |
| ----- | ----- | ----- |
| CONFIG_DIR | 配置文件目录 | ./config
| JOB_TIME_INTERVAL | JOB每次执行的时间间隔 | 30分钟
| USER_INTERVAL | 两个用户之间的签到时间间隔，用户数量 x USER_INTERVAL 应该小于 JOB_TIME_INTERVAL | 5分钟

# mhybbs-tools

## 使用

每个`.toml`配置文件配置一个需要米游社签到的账号, 配置文件模板在`./conf/conf.template.toml`

### 快速启动

```sh
mkdir ./config
cp ./conf/conf.template.toml ./config/user.toml

vim ./config/user.toml
# 在配置文件中设置账户cookie

python main.py
```

## 环境变量

| 变量名 | 描述 | 默认值 |
| ----- | ----- | ----- |
| CONFIG_DIR | 配置文件目录 | ./config
| JOB_TIME_INTERVAL | JOB每次执行的时间间隔 | 30分钟
| USER_INTERVAL | 两个用户之间的签到时间间隔，用户数量 x USER_INTERVAL 应该小于 JOB_TIME_INTERVAL | 5分钟

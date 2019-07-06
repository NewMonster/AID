### 认证相关

#### 登录

url:  /api-token-auth/

请求方式：POST

请求参数：

| 请求参数 | 参数类型 | 参数说明 |
| :------: | :------: | :------: |
| username |    String   | 用户名 |
| password |    String   | 密码 |

返回：

```json
{
    token: '1234',
    user: {
        id: 1,
        userid: '1234',
        username: '123',
        nickname: '123',
        avatar: '8723y5',
        is_manager: true
    }
}
```

#### I am 接口

url:  /api/user/iam/

请求方式：GET

请求参数：
​    无
返回：

```json
{
    id: 1,
    userid: '1234',
    username: '123',
    nickname: '123',
    avatar: '8723y5',
    is_manager: true
}
```

#### 注销登录

url:  /api/user/logout/

请求方式：POST

请求参数：
​    无
返回：

```json
{
    result: 'info',
    msg: '已注销'
}
```

#### 用户列表

url:  /api/user/

请求方式：GET

请求参数：

| 请求参数 | 参数类型 | 参数说明 |
| :------: | :------: | :------: |
| search |    String   | 模糊搜索（username/nickname） |

返回：

```json
{
    count: 12,
    next: 'https://...',
    results: [
        {
            id: 1,
            username: '123',
            nickname: '123',
        }
    ]
}
```

#### 用户密码修改

url api/password/

请求方式：POST

请求参数：

| 请求参数 | 参数类型 | 参数说明 |
| :------: | :------: | :------: |
| old_password |    String   | 旧密码 |
| new_password |    String   | 新密码 |

返回：

```json
{
    'result': 'info',
     'msg': '修改成功'
}
```

#### 客户简略信息列表

url: /api/simple_clients/

请求方式 ：GET

请求参数：

| 请求参数 | 参数类型 | 参数说明 |
| :------: | :------: | :------: |
|    serach      |    String      |     模糊搜索，模糊匹配客户名称，客户代码|
|     city     |    int      |    客户所属县区id      |

返回：

```json
{
    count: 32,
    next: 'https://...',  // 下一页链接
    previous: 'https://...',  // 上一页链接
    results: [
        {
            id: 1,
            name: '张三',
            code: 'zhangsan',
        },
        {
            
        }
    ]
}
```
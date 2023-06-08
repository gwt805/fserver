# 后端API

### 运行
```bash
    python app.py
```

### 数据库
```bash
    flask db init       # 创建迁移文件夹 migrates , 只需调用一次
    flask db migrate    # 生成迁移文件
    flask db upgrade    # 开始迁移
    flask db downgrade  # 回滚到上次的迁移结果
```

### ORM查询方法及路由参数
```python
'''
<converter:variable_name>
     converter 接收的参数类型
        string 接收任何没有斜杠('/') 的文件(默认)
        int 接收整型
        float 接收浮点型
        path 接收路径, 可接收斜线('/')
        uuid 只接收uuid 字符串, 唯一码, 一种生成规则
        any 可以同时指定多种路径, 进行限定
    eg: /list/<int:id>/

search
    过滤器
        filter()
        filter_by()
        limit()
        offset()
        order_by()
        group_by()
    常用查询
        all()
        first() 没有则返回 None
        first_or_404()
        get() 没有则返回 None
        get_or_404()
        count()
        paginate() # 返回一个 Paginate 对象, 包含指定范围内的结果
    查询属性
        contains
        startswith
        endswith
        in_
        __gt__
        __ge__
        __lt__
        __le__
    逻辑运算
        与 and_
        或 or_
        非 not_
'''
```


#关于数据库app的Q&A

##文件职责

app.py
主程序工厂函数：
    app
内含主路由：
    route("/")
注册Blueprint模块
    search_bp
    api_bp
    auth_bp
    favo_bp
Config注册
    create_app(DevConfig)
关闭函数注册
    teardown.context
生产环境变量app提供：
    create_app(ProdConfig)
name=main运行
    app = create_app(DevConfig)

config.py
内建Config类，数据库、配置独立：
    测试用(TestConfig)
    开发用(DevConfig)
    生产用(ProdConfig)

db.py
与数据库对接，内含：
    数据库连接(get_db)
    关闭连接(close_connection)
    初始化(init_db)
    搜索、注册、验证、收藏功能

exceptions.py
在ValueError下自定义错误子类
    
routes/__init__.py
使routes被识别为包，方便调用内容

routs/search.py
主模块包，包含search_bp蓝图注册与search相关路由

routs/api.py
与search类似，返回json格式

routes/helper.py
包含前端拉取搜索关键词语login_requirement验证器

routes/favorites.py
用户操作：收藏、删除、展示收藏

routes/auth.py
用户操作：登录，登出，注册

tests/conftest.py
由fixture生成测试client

tests/test_api.py
api测试项目

test/test_auth.py
用户操作测试项目

Procfile
运行gunicorn（是个服务器软件），web声明软件类型，运行app.py中的app(Flask)
是远古网站heroku的用户使用习惯遗留，代码可以在render-setting中完成

requirements.txt
环境需求

.gitignore
推库时忽略文件，虚拟环境、缓存文件夹等，以后可能还会有data


##请求链路

用户：填写关键词、搜索

系统：
网络层：submit的buttom通过form标签上传输入的关键词，拼接url发送get请求到render服务器，由gunicorn读取，转交给Flask，Flask找到 /search 路由

代码层：在healper中获取关键词，db中的get_db连接数据库，由search路由引入。调用db中的get_info获取详细资料，给出。

用户：注册页填写账号密码，注册

网络层：submit通过post上传表单数据到gunicorn，再传到Flask

代码层：由 auth 的 form.get 获取post表单数据，db搜索数据库查重，密码由argon2哈希加密后以INTEGER id、username、password_hash、TIMESTAMP 的create_at字段写入数据库

用户：登录页填写账号密码，登录

网络层同上

代码层：由 auth 的 form.get 获取post表单数据，db经过form_name_to_id由用户名搜索唯一id(用户名查重的重要性)，argon2哈希verify后登录

用户：点击收藏列表

网络层：方法为get，登录所需的username从session中提取。

代码层：得到username后，由db的get_favo_list读取数据库返回数据

##三个“为什么”

db.py为了解耦存在，防止蓝图文件与主应用互相调用

blueprint为了模块化

app.run(debug=True)是调试环境而非生产环境：
    为单一线程，无法同时处理多个请求，gunicorn则可以。
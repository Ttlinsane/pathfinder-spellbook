#关于数据库app的Q&A

##文件职责

app.py
主程序，内含主路由、注册Blueprint模块、Config注册、关闭函数注册

config.py
内建Config类，属性包含results per page等默认设置

db.py
使主程序与蓝图包search.py解耦，使打开和关闭连接函数单一来源

routes/__init__.py
使routes被识别为包，方便调用内容

route/search.py
主模块包，包含蓝图注册与search相关路由

Procfile
运行gunicorn（是个服务器软件），web声明软件类型，运行app.py中的app(Flask)
是远古网站heroku的用户使用习惯遗留，代码可以在render-setting中完成

requirements.txt
环境需求

.gitigonre
推库时忽略文件，虚拟环境、缓存文件夹等，以后可能还会有data


##请求链路

用户：填写关键词、搜索

系统：
网络层：submit的buttom通过form标签上传输入的关键词，拼接url发送get请求（form的method，虽然仍然不知道get请求是什么）到render服务器，由gunicorn读取，转交给Flask（这部分完全是复制粘贴细则老妈的，不清楚gunicorn工作原理只能用），Flask找到/search路由

代码层：在search路由中，get_db()，检查g对象，创建g对象（我目前对于g对象的用途似乎只是方便关闭），request.args.get获取关键词，上报sql，cursor.execute执行SELECT搜索，结果列表return render_template，由jinja2处理返回变量入html模板（这大概就是我之前requests.get(url)返回的数据），由css添加样式。


##三个“为什么”

db.py为了解耦存在，防止蓝图文件与主应用互相调用

blueprint为了模块化

app.run(debug=True)是调试环境而非生产环境：
    为单一线程，无法同时处理多个请求，gunicorn则可以。


##概念理解

我仍然不知道哪个是理解了哪个没理解，只是模模糊糊感觉并未全都理解掌握。


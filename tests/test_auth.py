from exceptions import *

def test_register_page_loads(client):
    # 1. 隐形顾客发送 GET 请求访问注册页
    response = client.get("/auth/register")

    # 2. 对状态码放狠话：HTTP状态码必须是 200 (200 代表 OK，页面正常)
    assert response.status_code == 200

    # 3. 对网页内容放狠话：网页的 HTML 源码里，必须包含 "注册" 或者某个特定的词汇
    # (因为 response.data 是字节类型 byte，所以要把字符串转成 byte：b"你的词")
    assert b"username" in response.data


def test_register_empty_username_is_blocked(client):
    # 1. 隐形顾客强行发送 POST 请求，假装点下了注册按钮
    # data 字典里装的就是你要塞进表单里的数据
    response = client.post(
        "/auth/register",
        data={"username": "   ", "password": "123"}
    )
    # 2. 昨天我们设定：如果被拦截，会重新渲染 register.html，并带上错误提示
    # 重新渲染页面的状态码依然是 200
    # 3. 对网页内容放狠话：网页里必须包含你写的错误提示词！
    # 提示：你昨天写的是 "用户名和密码不能为空！" 或者是英文，把下面这行换成你真实的报错词汇
    assert "不能为空".encode('utf-8') in response.data


def test_register_success(client):
    response = client.post("/auth/register",data={"username":"test1","password":"test1"}) 
    assert response.status_code == 302
    assert "auth/login" in response.headers["location"]

def test_login_success(client):
    client.post("/auth/register",data={"username":"test1","password":"test1"}) 
    response2 = client.post("/auth/login",data={"username":"test1","password":"test1"})
    assert response2.status_code == 302

#0322-0323
def test_login_wrong_password(client):
    client.post("/auth/register",data={"username":"test1","password":"test1"})
    response = client.post("/auth/login",data={"username":"test1","password":"wrongpassword"})
    assert response.status_code != 302

def test_register_duplicate_blocked(client):
    client.post("/auth/register",data={"username":"test1","password":"test1"})
    resp = client.post("/auth/register",data={"username":"test1","password":"test1"})
    assert resp.json["http_status"] == 400

def test_logout(client):
    client.post("/auth/register",data={"username":"test1","password":"test1"})
    response = client.post("/auth/login",data={"username":"test1","password":"test1"})
    assert response.status_code == 302
    client.get("/auth/logout")
    response2 = client.get("/user/get")
    assert response2.status_code == 302

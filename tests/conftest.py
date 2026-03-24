import pytest

from app import create_app
from db import init_db,get_db
from config import TestConfig

# @pytest.fixture 告诉 pytest：这是一个战前准备工作
@pytest.fixture
def client(tmp_path):
    # 1. 在临时目录下创建一个测试专用数据库路径
    test_db = tmp_path / "test.db"
    
    app = create_app(TestConfig)
    # 2. 告诉 Flask：别用生产数据库了，用这个临时的
    app.config.update({
        "DATABASE": str(test_db),
    })
    with app.test_client() as client:
        with app.app_context():
            init_db()
            conn = get_db()
            with conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO spells (name, level_str, school, casting_time,
                        components, range_, effect, aiming,
                        duration, saving_throw, resistance, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",("Fireball","3","塑能","A","B","C","D","E","F","G","H","I"))
                cursor.execute(
                    "INSERT INTO levels (name,class,level) VALUES(?,?,?)",
                    ("Fireball","wizard","3"),
                )
        yield client
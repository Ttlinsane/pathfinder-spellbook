from pathlib import Path
import os

BASE_DIR = Path(__file__).parent

class Config:
    """基础配置类"""
    # 网站名称（给 HTML 用的）
    SITE_NAME = "Pathfinder 法术档案馆"
    
    # 数据库路径（原来在 db.py 里的，现在抽到这里）
    DATABASE = BASE_DIR / "data" / "spell_level.db"
    
    # 默认每页显示条数（原来 search.py 里的 25）
    ITEMS_PER_PAGE = 25

    SECRET_KEY = "dev-secret-key-不要用于生产"

class DevConfig(Config):
    """开发环境"""
    DEBUG = True

class TestConfig(Config):
    """测试环境"""
    TESTING = True

class ProdConfig(Config):
    """生产环境"""
    SECRET_KEY = os.environ.get("SECRET_KEY")
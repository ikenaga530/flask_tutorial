from pathlib import Path

basedir = Path(__file__).parent.parent

#BaseConfigクラスを作成
class BaseConfig :
    SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
    WTF_CSRF_SECRET_KEY = "AuwzysU5sugKN7KZs6f"

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'test.sqlite'}"
    SQALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

config = {
    "testing" : TestingConfig,
    "local" : LocalConfig,
}
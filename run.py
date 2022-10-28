from datetime import datetime

from app import cpity

from app.utils.logger import Log
from app import dao
from app.controllers.auth.user import auth
from app.controllers.request.http import req
from app.controllers.project.project import pr
from app.controllers.testcase.testcase import ts

# 注册蓝图
cpity.register_blueprint(auth)
cpity.register_blueprint(req)
cpity.register_blueprint(pr)
cpity.register_blueprint(ts)


@cpity.route('/')
def hello_world():
    log = Log("hello world专用")
    log.info("you have  hello_world")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    return now


if __name__ == '__main__':
    cpity.run("0.0.0.0", threaded=True, debug=True, port=7777)

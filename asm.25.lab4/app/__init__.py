import os
from flask import Flask
from flask import jsonify
from flask import render_template

app = Flask(__name__)


# добавить импорт своего модуля по шаблону

from app.akm2501.st00 import bp as bp0100
from app.akm2501.st14 import bp as bp0114
from app.akm2501.st09 import bp as bp0109
from app.asm2504.st00 import bp as bp0400
from app.asm2504.st10 import bp as bp0410
from app.asm2504.st12 import bp as bp0412
from app.akm2501.st11 import bp as bp0111
from app.akm2501.st08 import bp as bp0108
from app.asm2504.st18 import bp as bp0418
from app.akm2501.st18 import bp as bp0118
from app.akm2501.st03 import bp as bp0103
from app.asm2504.st06 import bp as bp0406
from app.asm2504.st09 import bp as bp0409
from app.asm2504.st24 import bp as bp0424
from app.asm2504.st03 import bp as bp0403
from app.asm2504.st23 import bp as bp0423
from app.asm2504.st29 import bp as bp0613
from app.asm2504.st05 import bp as bp0405
from app.asm2504.st16 import bp as bp0416
from app.akm2501.st20 import bp as bp0120
from app.akm2501.st04 import bp as bp0104
from app.asm2504.st01 import bp as bp0401
from app.asm2504.st26 import bp as bp0426


# добавить пункт меню для вызова своего модуля по шаблону:
bps = [
    ["[2501-00] Образец 2501", bp0100],
    ["[2501-14] Погосян", bp0114],
    ["[2504-00] Образец 2504", bp0400],
    ["[2504-10] Князев", bp0410],
    ["[2504-12] Комаров", bp0412],
    ["[2501-11] Кондакова", bp0111],
    ["[2501-03] Бердичев", bp0103],
    ["[2501-08] Зубков", bp0108],
    ["[2504-18] Нуритдинов", bp0418],
    ["[2504-06] Галимов", bp0406],
    ["[2504-09] Карпова", bp0409],
    ["[2504-24] Столер", bp0424],
    ["[2501-09] Исламов", bp0109],
    ["[2504-03] Батюшкова", bp0403],
    ["[2501-18] Сунагатова", bp0118],
    ["[2504-23] Степура", bp0423],
    ["[2504-29] Яшонков", bp0613],
    ["[2504-05] Брыгина", bp0405],
    ["[2501-20] Цуканова", bp0120],
    ["[2501-04] Долгов", bp0104],
    ["[2504-16] Медведев", bp0416],
    ["[2504-01] Алешко", bp0401],
    ["[2504-26] Шипов", bp0426],
]

for i, (title, bp) in enumerate(sorted(bps), start=1):
    app.register_blueprint(bp, url_prefix=f"/st{i}")


@app.route("/")
def index():
    return render_template("index.tpl", bps=sorted(bps))


@app.route("/api/", methods=['GET'])
def api():
    sts = []
    for i, (title, bp) in enumerate(sorted(bps), start=1):
        sts.append([i, title])
    return jsonify({'sts': sts})

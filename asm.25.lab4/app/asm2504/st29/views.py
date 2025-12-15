from flask import Blueprint, render_template, request, redirect, url_for
from .storage import SQLiteStorage
from .web_io import WebIO
from .stock import Stock
from .bond import Bond

# УНИКАЛЬНОЕ ИМЯ для вашего модуля
bp = Blueprint('asm2504_st29_views', __name__, url_prefix='/st29')
storage = SQLiteStorage()

def create_asset_from_form(asset_type, form_data):
    web_io = WebIO()
    web_io.set_form_data(form_data)

    asset = None
    if asset_type == 'stock':
        asset = Stock()
    elif asset_type == 'bond':
        asset = Bond()

    if asset:
        asset.set_io_handler(web_io)
        asset.input()

    return asset


@bp.route('/')
def main():
    assets = storage.get_all_assets()
    total_value = sum(asset.price for asset in assets)
    return render_template('asm2504/st29/index.html',
                           assets=assets,
                           total_value=total_value,
                           assets_count=len(assets))


@bp.route('/add', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        asset_type = request.form.get('asset_type')
        asset = create_asset_from_form(asset_type, request.form)

        if asset:
            storage.add_asset(asset)
            return redirect(url_for('st29.main'))

    return render_template('asm2504/st29/add.html')


@bp.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_asset(index):
    asset = storage.get_asset(index)

    if not asset:
        return redirect(url_for('st29.main'))

    if request.method == 'POST':
        asset.name = request.form.get('Название актива', '')

        try:
            asset.price = float(request.form.get('Цена', 0))
        except ValueError:
            asset.price = 0.0

        asset.currency = request.form.get('Валюта', 'USD')

        if asset.get_type() == "Акция":
            try:
                asset.dividend_yield = float(request.form.get('Дивидендная доходность (%)', 0))
            except ValueError:
                asset.dividend_yield = 0.0
        elif asset.get_type() == "Облигация":
            try:
                asset.coupon_rate = float(request.form.get('Купонная ставка (%)', 0))
            except ValueError:
                asset.coupon_rate = 0.0

            try:
                asset.maturity_years = int(request.form.get('Срок до погашения (лет)', 1))
            except ValueError:
                asset.maturity_years = 1

            try:
                asset.face_value = float(request.form.get('Номинальная стоимость', 1000))
            except ValueError:
                asset.face_value = 1000.0

        storage.edit_asset(index, asset)
        return redirect(url_for('st29.main'))

    return render_template('asm2504/st29/edit.html', asset=asset, index=index)


@bp.route('/delete/<int:index>')
def delete_asset(index):
    storage.delete_asset(index)
    return redirect(url_for('st29.main'))


@bp.route('/export')
def export_data():
    success = storage.export_to_pickle()
    assets = storage.get_all_assets()

    if success:
        message = f"Успешно экспортировано {len(assets)} активов в файл"
        return render_template('asm2504/st29/index.html',
                               assets=assets,
                               message=message,
                               total_value=sum(a.price for a in assets),
                               assets_count=len(assets))
    else:
        return render_template('asm2504/st29/index.html',
                               assets=assets,
                               error="Ошибка экспорта",
                               total_value=sum(a.price for a in assets),
                               assets_count=len(assets))


@bp.route('/import')
def import_data():
    success = storage.import_from_pickle()
    assets = storage.get_all_assets()

    if success:
        message = f"Успешно импортировано {len(assets)} активов из файла"
        return render_template('asm2504/st29/index.html',
                               assets=assets,
                               message=message,
                               total_value=sum(a.price for a in assets),
                               assets_count=len(assets))
    else:
        return render_template('asm2504/st29/index.html',
                               assets=assets,
                               error="Ошибка загрузки файла",
                               total_value=sum(a.price for a in assets),
                               assets_count=len(assets))


@bp.route('/clear')
def clear_all():
    storage.clear_all()
    assets = storage.get_all_assets()
    return render_template('asm2504/st29/index.html',
                           assets=assets,
                           message="Портфель очищен",
                           total_value=0,
                           assets_count=0)

from . import api
bp.register_blueprint(api.api_bp)

# В самом конце views.py добавьте:
import hashlib

# Генерируем уникальное имя для Blueprint
unique_suffix = hashlib.md5(__file__.encode()).hexdigest()[:6]
bp.name = f"{bp.name}_{unique_suffix}"
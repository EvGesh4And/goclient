from flask import Blueprint, jsonify, request
from .storage import SQLiteStorage
import json

# УНИКАЛЬНОЕ ИМЯ для API
api_bp = Blueprint('asm2504_st29_api', __name__, url_prefix='/api')
storage = SQLiteStorage()



def asset_to_dict(asset):
    """Преобразование объекта Asset в словарь"""
    asset_dict = {
        'id': asset.id,
        'type': asset.get_type(),
        'name': asset.name,
        'price': asset.price,
        'currency': asset.currency
    }

    if asset.get_type() == "Акция":
        asset_dict['dividend_yield'] = asset.dividend_yield
    elif asset.get_type() == "Облигация":
        asset_dict['coupon_rate'] = asset.coupon_rate
        asset_dict['maturity_years'] = asset.maturity_years
        asset_dict['face_value'] = asset.face_value

    return asset_dict


@api_bp.route('/assets', methods=['GET'])
def get_all_assets():
    """Получить все активы"""
    assets = storage.get_all_assets()
    return jsonify([asset_to_dict(asset) for asset in assets])


@api_bp.route('/assets/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Получить актив по ID"""
    # В storage нужно добавить метод get_asset_by_id
    assets = storage.get_all_assets()
    for asset in assets:
        if asset.id == asset_id:
            return jsonify(asset_to_dict(asset))
    return jsonify({'error': 'Asset not found'}), 404


@api_bp.route('/assets', methods=['POST'])
def create_asset():
    """Создать новый актив"""
    data = request.json

    if data['type'] == 'Акция':
        from .stock import Stock
        asset = Stock(data.get('dividend_yield', 0.0))
    elif data['type'] == 'Облигация':
        from .bond import Bond
        asset = Bond(
            data.get('coupon_rate', 0.0),
            data.get('maturity_years', 1),
            data.get('face_value', 1000.0)
        )
    else:
        return jsonify({'error': 'Invalid asset type'}), 400

    asset.name = data['name']
    asset.price = data['price']
    asset.currency = data.get('currency', 'USD')

    storage.add_asset(asset)

    # Получаем ID добавленного актива
    assets = storage.get_all_assets()
    if assets:
        asset.id = assets[-1].id

    return jsonify(asset_to_dict(asset)), 201


@api_bp.route('/assets/<int:index>', methods=['PUT'])
def update_asset(index):
    """Обновить актив"""
    asset = storage.get_asset(index)
    if not asset:
        return jsonify({'error': 'Asset not found'}), 404

    data = request.json
    asset.name = data.get('name', asset.name)
    asset.price = data.get('price', asset.price)
    asset.currency = data.get('currency', asset.currency)

    if asset.get_type() == "Акция":
        asset.dividend_yield = data.get('dividend_yield', asset.dividend_yield)
    elif asset.get_type() == "Облигация":
        asset.coupon_rate = data.get('coupon_rate', asset.coupon_rate)
        asset.maturity_years = data.get('maturity_years', asset.maturity_years)
        asset.face_value = data.get('face_value', asset.face_value)

    storage.edit_asset(index, asset)
    return jsonify(asset_to_dict(asset))


@api_bp.route('/assets/<int:index>', methods=['DELETE'])
def delete_asset(index):
    """Удалить актив"""
    if storage.delete_asset(index):
        return jsonify({'message': 'Asset deleted'})
    return jsonify({'error': 'Asset not found'}), 404


@api_bp.route('/assets/count', methods=['GET'])
def get_assets_count():
    """Получить количество активов"""
    assets = storage.get_all_assets()
    return jsonify({'count': len(assets)})


@api_bp.route('/assets/total', methods=['GET'])
def get_total_value():
    """Получить общую стоимость портфеля"""
    assets = storage.get_all_assets()
    total_value = sum(asset.price for asset in assets)
    return jsonify({'total_value': total_value})


@api_bp.route('/export', methods=['GET'])
def export_data():
    """Экспортировать данные"""
    if storage.export_to_pickle():
        return jsonify({'message': 'Data exported successfully'})
    return jsonify({'error': 'Export failed'}), 500


@api_bp.route('/import', methods=['GET'])
def import_data():
    """Импортировать данные"""
    if storage.import_from_pickle():
        return jsonify({'message': 'Data imported successfully'})
    return jsonify({'error': 'Import failed'}), 500
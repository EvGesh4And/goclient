from flask import jsonify, request, abort, g
from .company import Company
from .employee import Employee
from .manager import Manager
from .director import Director

def register_api(bp):
    @bp.route("/api/employees", methods=["GET"])
    def api_get_all():
        employees = get_company().get_employee_list()
        return jsonify(employees)

    @bp.route("/api/employees/<emp_id>", methods=["GET"])
    def api_get_one(emp_id):
        emp = get_company().storage.get_by_id(emp_id)
        if not emp:
            abort(404, description="Сотрудник не найден")
        return jsonify({
            "id": emp.id,
            "type": emp.__class__.__name__,
            **emp.output_data()
        })
    
    @bp.route("/api/employees/search")
    def api_search():
        name = request.args.get("name", "")
        employees = get_company().get_employee_list()
        found = [e for e in employees if name.lower() in e.get("name", "").lower()]
        return jsonify(found)

    @bp.route("/api/employees", methods=["POST"])
    def api_add():
        data = request.get_json()
        if not data or "type" not in data:
            abort(400, description="Нужно указать type: Employee, Manager или Director")

        emp_type = data["type"]
        if emp_type not in ["Employee", "Manager", "Director"]:
            abort(400, description="Неверный тип")

        company = get_company()
        from .employee import Employee
        from .manager import Manager
        from .director import Director
        classes = {"Employee": Employee, "Manager": Manager, "Director": Director}
        cls = classes[emp_type]
        emp = cls(company.io)
        emp.input_data_from_dict(data.get("data", {}))
        company.storage.add(emp)
        return jsonify({"id": emp.id, "status": "added"}), 201

    @bp.route("/api/employees/<emp_id>", methods=["PUT"])
    def api_update(emp_id):
        payload = request.get_json()
        if not payload:
            abort(400, description="Нет данных")

        emp = get_company().storage.get_by_id(emp_id)
        if not emp:
            abort(404, description="Сотрудник не найден")

        data = payload.get("data", {})
        emp.input_data_from_dict(data) 
        get_company().storage.update_by_id(emp_id, emp)
        return jsonify({"status": "updated", "id": emp_id})

    @bp.route("/api/employees/<emp_id>", methods=["DELETE"])
    def api_delete(emp_id):
        if get_company().delete_employee(emp_id):
            return jsonify({"status": "deleted"})
        abort(404)

    @bp.route("/api/employees/clear", methods=["POST"])
    def api_clear():
        get_company().clear_list()
        return jsonify({"status": "cleared"})

    def get_company():
        if '_company' not in g:
            from . import get_company as gc
            g._company = gc()
        return g._company
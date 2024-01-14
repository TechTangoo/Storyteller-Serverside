from app.users import bp


@bp.route("/new", methods=['GET'])
def new_user():
    return "New user hi"


@bp.route("/data", methods=['GET'])
def user_data():
    return "New data"

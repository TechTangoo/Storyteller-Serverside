from app.users import bp


@bp.route("/register", methods=['POST'])
def new_user():
    return "New user hi"

@bp.route("/login", methods=['POST'])
def new_user():
    return "authorization"

@bp.route("/[userid:string]", methods=['GET'])
def new_user():
    return "get user details"

@bp.route("/[userid:string]", methods=['PUT'])
def new_user():
    return "put user details"

@bp.route("/remove", methods=['PATCH'])
def new_user():
    return "New user hi"
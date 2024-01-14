from app.users import bp


@bp.route("/register", methods=['POST'])
def new_user():
    return "New user hi"


@bp.route("/login", methods=['GET'])
def login_user():
    print("lgon user")
    return "authorization"

# @bp.route("/<string:userid>", methods=['GET'])
# def get_user():
#     return "get user details"

# @bp.route("/<string:userid>", methods=['PUT'])
# def update_user():
#     """Function printing python version."""
#     return "put user details"

# @bp.route("/remove", methods=['PATCH'])
# def delete_user():
#     return "New user hi"

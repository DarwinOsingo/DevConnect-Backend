from flask import Blueprint

users_bp = Blueprint("users", __name__)

@users_bp.route("/users/test", methods=["GET"])
def test_user_route():
    return {"message": "User route works!"}

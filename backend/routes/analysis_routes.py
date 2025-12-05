from flask import Blueprint, jsonify, request
import jwt

from config import Config

from services.analysis_service import get_analysis


analysis_bp = Blueprint("analyze", __name__)

@analysis_bp.get("/analysis/get")
def analyze():
    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)

    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401

    user_id = jwt_payload["user_id"]
    
    result = get_analysis(user_id)
    
    return jsonify(result)
from flask import Blueprint, jsonify, request
import jwt

from config import Config

from services.analysis_service import get_analysis
from services.auth_service import get_curent_user_id


analysis_bp = Blueprint("analyze", __name__)

@analysis_bp.get("/analysis/get")
def analysis_get():
    start_date = request.args.get("start_date")
    
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    result = get_analysis(user_id_response["user_id"], start_date)
    
    return result
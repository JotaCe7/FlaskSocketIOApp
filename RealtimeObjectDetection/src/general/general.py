
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

general_bp = Blueprint("general_bp", __name__, template_folder="templates",static_folder="static",static_url_path='/general/static')

@general_bp.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML template.
    """
    if request.method == "GET":
        return render_template("general/index.html")

@general_bp.route("/display_stream")
def display_stream():
    """
    Display image predicted by the model in our UI.
    """
    return redirect(url_for("static", filename="predictions/output_img.jpeg"))
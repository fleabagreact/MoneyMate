from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from models import Budget, Expense

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    last_budget = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.created_at.desc()).first()

    last_expense = None
    if last_budget:
        last_expense = Expense.query.filter_by(budget_id=last_budget.id).order_by(Expense.created_at.desc()).first()

    return render_template("dashboard.html", last_expense=last_expense)

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import Expense, Budget
from datetime import datetime, timedelta

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/")
@login_required
def reports():
    filter_option = request.args.get("filter", "all")

    query = Expense.query.join(Budget).filter(Budget.user_id == current_user.id)

    today = datetime.today()
    start_date, end_date = None, None

    if filter_option == "day":
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif filter_option == "month":
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + timedelta(days=32)).replace(day=1)
    elif filter_option == "year":
        start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = today.replace(year=today.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    if start_date and end_date:
        query = query.filter(Expense.created_at >= start_date, Expense.created_at < end_date)

    expenses = query.all()
    total = sum(exp.amount for exp in expenses)

    return render_template("reports.html", expenses=expenses, total=total, filter_option=filter_option)

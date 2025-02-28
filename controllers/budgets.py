from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Budget, Expense

budgets_bp = Blueprint("budgets", __name__, url_prefix="/budgets")

@budgets_bp.route("/", methods=["GET", "POST"])
@login_required
def budgets():
    if request.method == "POST":
        month = request.form.get("month")
        year = request.form.get("year")

        if not month or not year:
            flash("Mês e ano são obrigatórios!", "danger")
            return redirect(url_for("budgets.budgets"))

        budget = Budget(user_id=current_user.id, month=month, year=year)
        db.session.add(budget)
        db.session.commit()
        flash("Orçamento criado com sucesso!", "success")

    budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.year.desc(), Budget.month.desc()).all()
    return render_template("budgets.html", budgets=budgets)


@budgets_bp.route("/<int:budget_id>", methods=["GET", "POST"])
@login_required
def budget_detail(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    if budget.user_id != current_user.id:
        flash("Acesso negado!", "danger")
        return redirect(url_for("budgets.budgets"))

    if request.method == "POST":
        category = request.form.get("category")
        amount = request.form.get("amount")

        if not category or not amount:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for("budgets.budget_detail", budget_id=budget_id))

        try:
            amount = float(amount)
        except ValueError:
            flash("O valor deve ser numérico!", "danger")
            return redirect(url_for("budgets.budget_detail", budget_id=budget_id))

        new_expense = Expense(budget_id=budget.id, category=category, amount=amount)
        db.session.add(new_expense)
        db.session.commit()
        flash("Despesa adicionada com sucesso!", "success")

        return redirect(url_for("budgets.budget_detail", budget_id=budget_id))

    expenses = budget.expenses
    return render_template("budget_detail.html", current_budget=budget, expenses=expenses)

@budgets_bp.route("/delete/<int:budget_id>", methods=["POST"])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    if budget.user_id != current_user.id:
        flash("Acesso negado!", "danger")
        return redirect(url_for("budgets.budgets"))

    db.session.delete(budget)
    db.session.commit()
    flash("Orçamento excluído com sucesso!", "success")

    return redirect(url_for("budgets.budgets"))

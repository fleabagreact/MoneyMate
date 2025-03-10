import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Budget, Expense

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@expenses_bp.route("/<int:budget_id>/add", methods=["POST"])
@login_required
def add_expense(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    if budget.user_id != current_user.id:
        flash("Acesso negado!", "danger")
        return redirect(url_for("budgets.budget_detail", budget_id=budget_id))

    category = request.form.get("category")
    amount = request.form.get("amount")
    created_at = request.form.get("created_at")

    if not category or not amount or not created_at:
        flash("Todos os campos são obrigatórios!", "danger")
        return redirect(url_for("budgets.budget_detail", budget_id=budget_id))

    try:
        amount = float(amount)
        created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d")
    except ValueError:
        flash("Formato de valor ou data inválido!", "danger")
        return redirect(url_for("budgets.budget_detail", budget_id=budget_id))

    new_expense = Expense(
        budget_id=budget.id,
        category=category,
        amount=amount,
        created_at=created_at
    )
    db.session.add(new_expense)
    db.session.commit()
    flash("Despesa adicionada com sucesso!", "success")

    return redirect(url_for("budgets.budget_detail", budget_id=budget_id))

@expenses_bp.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    if expense.budget.user_id != current_user.id:
        flash("Você não tem permissão para editar esta despesa.", "danger")
        return redirect(url_for("budgets.budget_detail", budget_id=expense.budget_id))

    if request.method == "POST":
        category = request.form.get("category")
        amount = request.form.get("amount")
        created_at = request.form.get("created_at")

        if not category or not amount or not created_at:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for("expenses.edit_expense", expense_id=expense.id))

        try:
            expense.amount = float(amount)
            expense.created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d")
        except ValueError:
            flash("Formato de valor ou data inválido!", "danger")
            return redirect(url_for("expenses.edit_expense", expense_id=expense.id))

        expense.category = category
        db.session.commit()
        flash("Despesa atualizada com sucesso!", "success")
        return redirect(url_for("budgets.budget_detail", budget_id=expense.budget_id))

    return render_template("edit_expense.html", expense=expense)

@expenses_bp.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if expense.budget.user_id != current_user.id:
        flash("Acesso negado!", "danger")
        return redirect(url_for("budgets.budget_detail", budget_id=expense.budget_id))

    db.session.delete(expense)
    db.session.commit()
    flash("Despesa removida!", "success")

    return redirect(url_for("budgets.budget_detail", budget_id=expense.budget_id))

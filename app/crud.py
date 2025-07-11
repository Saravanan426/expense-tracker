from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func



# ---------- USERS ----------
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        phonenumber=user.phonenumber,
        email=user.email,
        password_hash=user.password,  # hash if needed
        address=user.address,
        profileimage=user.profileimage
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------- INCOMES ----------
# Create income
def create_income(db: Session, income: schemas.IncomeCreate):
    db_income = models.Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

# Get all incomes for user
def get_incomes_by_user(db: Session, user_id: int):
    return db.query(models.Income).filter(models.Income.user_id == user_id).all()

# Update income
def update_income(db: Session, income_id: int, updated: schemas.IncomeBase):
    db_income = db.query(models.Income).filter(models.Income.id == income_id).first()
    if not db_income:
        return None
    for key, value in updated.dict().items():
        setattr(db_income, key, value)
    db.commit()
    db.refresh(db_income)
    return db_income

# Delete income
def delete_income(db: Session, income_id: int):
    db_income = db.query(models.Income).filter(models.Income.id == income_id).first()
    if not db_income:
        return None
    db.delete(db_income)
    db.commit()
    return db_income



# ---------- EXPENSES ----------
def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses_by_user(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()

# ---------- UPDATE EXPENSE ----------
def update_expense(db: Session, expense_id: int, updated_data: schemas.ExpenseCreate):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if db_expense is None:
        return None

    for key, value in updated_data.dict().items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense

# ---------- DELETE EXPENSE ----------
def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if db_expense is None:
        return None

    db.delete(db_expense)
    db.commit()
    return db_expense



# ---------- BILL REMINDERS ----------
def create_bill_reminder(db: Session, reminder: schemas.BillReminderCreate):
    db_reminder = models.BillReminder(**reminder.dict())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

def get_bill_reminders_by_user(db: Session, user_id: int):
    return db.query(models.BillReminder).filter(models.BillReminder.user_id == user_id).all()

def update_bill_reminder(db: Session, reminder_id: int, update_data: schemas.BillReminderBase):
    db_reminder = db.query(models.BillReminder).filter(models.BillReminder.id == reminder_id).first()
    if db_reminder is None:
        return None
    for key, value in update_data.dict().items():
        setattr(db_reminder, key, value)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

def delete_bill_reminder(db: Session, reminder_id: int):
    db_reminder = db.query(models.BillReminder).filter(models.BillReminder.id == reminder_id).first()
    if db_reminder is None:
        return None
    db.delete(db_reminder)
    db.commit()
    return db_reminder



# ---------- CATEGORIES ----------
def create_category(db: Session, category: schemas.CategoryCreate):
    db_cat = models.Category(**category.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_categories_by_user(db: Session, user_id: int):
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()

def get_summary(db: Session, user_id: int):
    total_income = db.query(func.coalesce(func.sum(models.Income.amount), 0)).filter(models.Income.user_id == user_id).scalar()
    total_expense = db.query(func.coalesce(func.sum(models.Expense.amount), 0)).filter(models.Expense.user_id == user_id).scalar()

    remaining = total_income - total_expense
    needed = abs(remaining) if remaining < 0 else 0
    status = "Within Budget" if remaining >= 0 else "Over Budget"

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "remaining_amount": float(remaining),
        "needed_amount": float(needed),
        "status": status
    }

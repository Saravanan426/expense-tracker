from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud, database,models,auth,token
from datetime import timedelta
from .dependencies import get_current_user

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- USERS ----------------
@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.hash_password(user.password)
    user_data = models.User(
        name=user.name,
        phonenumber=user.phonenumber,
        email=user.email,
        password_hash=hashed_password,
        profileimage=user.profileimage,
        address=user.address
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


@router.post("/login", response_model=schemas.Token)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not auth.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = token.create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# ---------------- INCOMES ----------------
# ----------- INCOMES -----------

@router.post("/incomes/", response_model=schemas.IncomeResponse)
def create_income(
    income: schemas.IncomeBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    income_data = schemas.IncomeCreate(**income.dict(), user_id=current_user.id)
    return crud.create_income(db, income_data)


@router.get("/incomes/", response_model=list[schemas.IncomeResponse])
def get_incomes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_incomes_by_user(db, current_user.id)


@router.put("/incomes/{income_id}", response_model=schemas.IncomeResponse)
def update_income(
    income_id: int,
    income: schemas.IncomeBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_income = db.query(models.Income).filter(models.Income.id == income_id, models.Income.user_id == current_user.id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return crud.update_income(db, income_id, income)


@router.delete("/incomes/{income_id}", response_model=schemas.IncomeResponse)
def delete_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_income = db.query(models.Income).filter(models.Income.id == income_id, models.Income.user_id == current_user.id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return crud.delete_income(db, income_id)




# ---------------- EXPENSES ----------------
@router.post("/expenses/", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseBase,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense_data = schemas.ExpenseCreate(**expense.dict(), user_id=current_user.id)
    return crud.create_expense(db, expense_data)


@router.get("/expenses/", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_expenses_by_user(db, current_user.id)


# ---------- UPDATE EXPENSE ----------
@router.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = crud.update_expense(db, expense_id, expense)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

# ---------- DELETE EXPENSE ----------
@router.delete("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = crud.delete_expense(db, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense



# ---------------- BILL REMINDERS ----------------
# ----------- BILL REMINDERS -----------

@router.post("/bill-reminders/", response_model=schemas.BillReminderResponse)
def create_bill_reminder(
    reminder: schemas.BillReminderBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reminder_data = schemas.BillReminderCreate(**reminder.dict(), user_id=current_user.id)
    return crud.create_bill_reminder(db, reminder_data)


@router.get("/bill-reminders/", response_model=list[schemas.BillReminderResponse])
def get_bill_reminders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_bill_reminders_by_user(db, current_user.id)


@router.put("/bill-reminders/{reminder_id}", response_model=schemas.BillReminderResponse)
def update_bill_reminder(
    reminder_id: int,
    reminder: schemas.BillReminderBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_reminder = db.query(models.BillReminder).filter(models.BillReminder.id == reminder_id, models.BillReminder.user_id == current_user.id).first()
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Bill reminder not found")
    return crud.update_bill_reminder(db, reminder_id, reminder)


@router.delete("/bill-reminders/{reminder_id}", response_model=schemas.BillReminderResponse)
def delete_bill_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_reminder = db.query(models.BillReminder).filter(models.BillReminder.id == reminder_id, models.BillReminder.user_id == current_user.id).first()
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Bill reminder not found")
    return crud.delete_bill_reminder(db, reminder_id)



# ---------------- CATEGORIES ----------------
@router.post("/categories/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@router.get("/categories/user/{user_id}", response_model=list[schemas.CategoryResponse])
def get_categories(user_id: int, db: Session = Depends(get_db)):
    return crud.get_categories_by_user(db, user_id)

@router.get("/summary/", response_model=schemas.SummaryResponse)
def get_financial_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_summary(db, current_user.id)

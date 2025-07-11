from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


# ---------- USER ----------
class UserBase(BaseModel):
    name: str
    phonenumber: str
    email: EmailStr
    address: Optional[str] = None
    profileimage: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {
    "from_attributes": True
}



# ---------- INCOME ----------
class IncomeBase(BaseModel):
    amount: float
    source: Optional[str] = None
    received_date: date

class IncomeCreate(IncomeBase):
    user_id: int

class IncomeResponse(IncomeBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
    "from_attributes": True
}



# ---------- EXPENSE ----------
class ExpenseBase(BaseModel):
    title: str
    amount: float
    expense_date: date
    category_id: Optional[int] = None

class ExpenseCreate(ExpenseBase):
    user_id: int

class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
    "from_attributes": True
}

# ---------- BILL REMINDER ----------
class BillReminderBase(BaseModel):
    title: str
    amount: float
    due_date: date
    repeat_cycle: Optional[str] = None
    status: Optional[str] = "pending"
    notes: Optional[str] = None

class BillReminderCreate(BillReminderBase):
    user_id: int

class BillReminderResponse(BillReminderBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
    "from_attributes": True
}



# ---------- CATEGORY ----------
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    user_id: int

class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
    "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    remaining_amount: float
    needed_amount: float
    status: str



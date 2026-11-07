from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

DATE_FORMAT = "%Y-%m-%d"

def calculate_next_due(current_due_str: str, cycle: str) -> str:
    current_due = datetime.strptime(current_due_str, DATE_FORMAT)
    if cycle == "Weekly":
        next_due = current_due + timedelta(days=7)
    elif cycle == "Semi-Monthly":
        next_due = current_due + timedelta(days=15)
    elif cycle == "Monthly":
        next_due = current_due + relativedelta(months=1)
    return next_due.strftime(DATE_FORMAT)

def get_days_left(due_date_str: str) -> int:
    due_date = datetime.strptime(due_date_str, DATE_FORMAT).date()
    today = datetime.now().date()
    return (due_date - today).days

def generate_receipt_text(tenant_name: str, unit: str, amount: float, new_due: str) -> str:
    receipt = f"""
========================================
       LOLA'S HOME RENTALS RECEIPT      
========================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Tenant: {tenant_name}
Unit: {unit}
Amount Paid: Php {amount:.2f}
New Due Date: {new_due}
Status: PAID
========================================
"""
    return receipt
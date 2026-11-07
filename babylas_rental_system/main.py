from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from models import TenantCreate, PaymentRequest
import database
import utils

app = FastAPI(title="Babyla's Home Rentals API")

@app.post("/api/tenants", status_code=status.HTTP_201_CREATED)
def create_tenant(tenant: TenantCreate):
    db = database.load_data()
    new_id = max([t["id"] for t in db], default=0) + 1
    today_str = datetime.now().strftime("%Y-%m-%d")
    next_due = utils.calculate_next_due(today_str, tenant.billing_cycle)

    record = {
        "id": new_id,
        "name": tenant.name,
        "unit": tenant.unit,
        "rate": tenant.rate,
        "billing_cycle": tenant.billing_cycle,
        "next_due": next_due,
        "status": "PAID"
    }
    db.append(record)
    database.save_data(db)
    return {"message": "Tenant registered successfully", "tenant": record}

@app.get("/api/tenants", status_code=status.HTTP_200_OK)
def get_dashboard_summary():
    db = database.load_data()
    for tenant in db:
        days_left = utils.get_days_left(tenant["next_due"])
        tenant["days_left"] = days_left
        if days_left < 0:
            tenant["status"] = "OVERDUE"
        elif days_left <= 5 and tenant["status"] != "PAID":
            tenant["status"] = "PENDING"
    return {"total_tenants": len(db), "tenants": db}

@app.put("/api/tenants/{tenant_id}/pay", status_code=status.HTTP_200_OK)
def process_payment(tenant_id: int, payment: PaymentRequest):
    db = database.load_data()
    tenant = next((t for t in db if t["id"] == tenant_id), None)

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if payment.amount_paid < tenant["rate"]:
        raise HTTPException(status_code=400, detail="Insufficient payment amount")

    tenant["next_due"] = utils.calculate_next_due(tenant["next_due"], tenant["billing_cycle"])
    tenant["status"] = "PAID"
    database.save_data(db)

    receipt = utils.generate_receipt_text(tenant["name"], tenant["unit"], payment.amount_paid, tenant["next_due"])
    return {"message": "Payment recorded successfully", "new_due_date": tenant["next_due"], "receipt": receipt}

@app.delete("/api/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tenant(tenant_id: int):
    db = database.load_data()
    updated_db = [t for t in db if t["id"] != tenant_id]
    if len(db) == len(updated_db):
        raise HTTPException(status_code=404, detail="Tenant not found")
    database.save_data(updated_db)
    return None
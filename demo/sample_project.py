"""Sample project for CacheFlow demo."""
from fastapi import FastAPI, Query
from sqlalchemy.orm import Session

app = FastAPI()

# Anti-pattern: No caching on read-heavy endpoint
@app.get("/api/products")
async def get_products(category: str = Query(None), db: Session = None):
    """This endpoint is called 1000x/min but has no caching."""
    products = db.query(Product).filter_by(category=category).all()
    return {"products": [p.to_dict() for p in products]}

# Anti-pattern: Expensive computation without cache
@app.get("/api/analytics/dashboard")
async def get_dashboard(user_id: int, db: Session = None):
    """Expensive aggregation query runs every request."""
    total_orders = db.query(func.count(Order.id)).filter_by(user_id=user_id).scalar()
    total_spent = db.query(func.sum(Order.total)).filter_by(user_id=user_id).scalar()
    avg_order = db.query(func.avg(Order.total)).filter_by(user_id=user_id).scalar()
    return {
        "total_orders": total_orders,
        "total_spent": total_spent,
        "avg_order": avg_order
    }

# Good: Write-heavy, should NOT be cached
@app.post("/api/orders")
async def create_order(order: OrderCreate, db: Session = None):
    """Write-heavy endpoint, caching not appropriate."""
    return db.create_order(order)

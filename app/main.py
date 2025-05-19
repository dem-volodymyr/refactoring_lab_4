from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import dishes, customers, orders
from app.populate_db import populate_database

# Create the FastAPI app
app = FastAPI(
    title="Restaurant Order Management System",
    description="An API for managing restaurant orders, customers, and menu items",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(dishes.router)
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/")
def read_root():
    """API root endpoint."""
    return {
        "message": "Welcome to the Restaurant Order Management System API",
        "documentation": "/docs",
        "endpoints": [
            "/dishes",
            "/customers",
            "/orders"
        ]
    }


@app.on_event("startup")
def startup_event():
    """Load sample data when the application starts."""
    print("Starting the Restaurant Order Management System...")
    data = populate_database()
    print(f"Loaded {len(data['menu_items'])} menu items")
    print(f"Loaded {len(data['customers'])} customers")
    print(f"Loaded {len(data['orders'])} orders") 
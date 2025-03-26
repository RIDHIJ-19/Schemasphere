from flask import Flask, request, render_template
import re
import pandas as pd
import sqlite3
import requests
import io
import logging

app = Flask(__name__)  # Initialize Flask app

# Enable debugging logs
logging.basicConfig(level=logging.DEBUG)

CSV_FILES = {
    "categories": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/categories.csv",
    "customers": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/customers.csv",
    "employee_territories": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/employee_territories.csv",
    "employees": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/employees.csv",
    "order_details": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/order_details.csv",
    "orders": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/orders.csv",
    "products": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/products.csv",
    "regions": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/regions.csv",
    "shippers": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/shippers.csv",
    "suppliers": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/suppliers.csv",
    "territories": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/territories.csv"
}

def get_table_name(query):
    """Extract table name from SQL query."""
    match = re.search(r'FROM\s+([a-zA-Z_]+)', query, re.IGNORECASE)
    if match:
        table_name = match.group(1).strip().lower()  # Normalize to lowercase
        logging.debug(f"🟢 Extracted Table Name: {table_name}")
        logging.debug(f"📌 Available Tables: {list(CSV_FILES.keys())}")
        return table_name if table_name in CSV_FILES else None
    return None

def load_csv_to_sqlite(table_name):
    """Load CSV into an SQLite database in memory."""
    table_name = table_name.lower()
    csv_url = CSV_FILES.get(table_name)

    if not csv_url:
        logging.error(f"❌ Table `{table_name}` not found in CSV_FILES dictionary!")
        return None

    try:
        logging.info(f"🔗 Downloading CSV from: {csv_url}")
        response = requests.get(csv_url)
        df = pd.read_csv(io.StringIO(response.text))

        conn = sqlite3.connect(":memory:")
        df.to_sql(table_name, conn, index=False, if_exists="replace")

        logging.info(f"✅ Successfully loaded CSV for `{table_name}`, rows: {df.shape[0]}")
        return conn
    except Exception as e:
        logging.error(f"❌ Error loading CSV: {e}")
        return None

@app.route("/", methods=["GET"])
def index():
    """Home page (index.html)"""
    return render_template("index.html")

@app.route("/app", methods=["GET"])
def query_page():
    """Query input page (query.html)"""
    return render_template("query.html", data=[], headers=[], selected_query=None, error=None)

@app.route("/query", methods=["POST"])
def run_query():
    """Process SQL query and display results."""
    sql_query = request.form["query"]
    logging.debug(f"📥 Received Query: {sql_query}")

    table_name = get_table_name(sql_query)
    if not table_name:
        return render_template("query.html", data=[], headers=[], selected_query=sql_query, error="Invalid SQL syntax!")

    conn = load_csv_to_sqlite(table_name)
    if not conn:
        return render_template("query.html", data=[], headers=[], selected_query=sql_query, error="Table not found!")

    try:
        df = pd.read_sql_query(sql_query, conn)
        headers = df.columns.tolist()
        data = df.values.tolist()
        logging.debug(f"✅ Query Executed Successfully: {df.shape[0]} rows returned")
    except Exception as e:
        logging.error(f"❌ SQL Error: {str(e)}")
        return render_template("query.html", data=[], headers=[], selected_query=sql_query, error=str(e))

    return render_template("query.html", data=data, headers=headers, selected_query=sql_query, error=None)

if __name__ == "__main__":
    app.run(debug=True)

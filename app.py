from flask import Flask, request, render_template
import re
import pandas as pd
import sqlite3
import requests
import io
import logging
import time
from io import BytesIO
import gzip

app = Flask(__name__)

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
    "territories": "https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/csv/territories.csv",
    "large": "https://raw.githubusercontent.com/RIDHIJ-19/Schemasphere/main/large.csv"
}

def get_table_name(query):
    """Extract table name from SQL query, handling quotes."""
    match = re.search(r'FROM\s+[\'"]?([a-zA-Z_]+)[\'"]?', query, re.IGNORECASE)
    if match:
        table_name = match.group(1).strip().lower()
        logging.debug(f"🟢 Extracted Table Name: {table_name}")
        return table_name if table_name in CSV_FILES else None
    return None

def load_csv_to_sqlite(table_name):
    """Load large CSV files into SQLite using chunk-based approach."""
    table_name = table_name.lower()
    csv_url = CSV_FILES.get(table_name)

    if not csv_url:
        logging.error(f"❌ Table `{table_name}` not found in CSV_FILES dictionary!")
        return None

    try:
        logging.info(f"🔗 Downloading CSV from: {csv_url}")
        response = requests.get(csv_url, stream=True)
        response.raise_for_status()

        # Handle GZIP compression
        try:
            with gzip.GzipFile(fileobj=BytesIO(response.content), mode="rb") as gz_file:
                csv_data = gz_file.read().decode("utf-8")
        except gzip.BadGzipFile:
            logging.warning("⚠️ File is not GZIP compressed. Trying normal read.")
            csv_data = response.content.decode("utf-8", errors="replace")

        conn = sqlite3.connect(":memory:")
        
        # Chunk-based loading
        chunksize = 10_000  # Read 10,000 rows at a time
        chunk_iter = pd.read_csv(BytesIO(csv_data.encode()), chunksize=chunksize)

        first_chunk = True
        for chunk in chunk_iter:
            chunk.columns = chunk.columns.str.lower().str.replace(" ", "_")  # Normalize column names
            chunk.to_sql(table_name, conn, index=False, if_exists="replace" if first_chunk else "append")
            first_chunk = False  # Append subsequent chunks

        logging.info(f"✅ Successfully loaded `{table_name}` into SQLite using chunk-based processing")
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
    """Process SQL query and display results with execution time."""
    sql_query = request.form["query"]
    logging.debug(f"📥 Received Query: {sql_query}")

    table_name = get_table_name(sql_query)
    if not table_name:
        return render_template("query.html", data=[], headers=[], selected_query=sql_query, error="Invalid SQL syntax!")

    conn = load_csv_to_sqlite(table_name)
    if not conn:
        return render_template("query.html", data=[], headers=[], selected_query=sql_query, error="Table not found!")

    try:
        start_time = time.time()  # Start timing
        df = pd.read_sql_query(sql_query, conn)
        end_time = time.time()  # End timing

        execution_time = end_time - start_time  # Compute execution time
        logging.debug(f"⏳ Query Execution Time: {execution_time:.6f} seconds")
        headers = df.columns.tolist()
        data = df.values.tolist()

    except Exception as e:
        logging.error(f"❌ SQL Error: {str(e)}")
        return render_template("query.html", data=[], headers=[], selected_query=sql_query, error=str(e))

    return render_template("query.html", data=data, headers=headers, selected_query=sql_query, error=None, execution_time=f"{execution_time:.6f} seconds")

if __name__ == "__main__":
    app.run(debug=True)

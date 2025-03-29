# SCHEMASPHERE ✨🌐

## A SQL Playground for Your CSV Files!

🌐 Live Demo : https://schemasphere.onrender.com

---

## 🚀 About the Project

**SCHEMASPHERE** transforms your CSV files into queryable databases—no setup, no hassle! Just add a CSV file, write SQL queries, and get structured results instantly. Whether you're a data enthusiast, analyst, or just SQL-curious, this tool makes exploring CSV data a breeze.

---

## 🌟 Features

- ✅ **Run SQL Queries directly on CSV files**—because spreadsheets deserve more respect!
- ✅ **Instant Schema Detection** for easy reference—no more guessing column names.
- ✅ **Lightning Fast ⚡**—powered by Flask & Pandas for smooth performance.
- ✅ **Zero Setup**—no need for traditional databases or config headaches.
- ✅ **Simple & Interactive UI**—because querying data should be fun, not frustrating.
- ✅ **Supports Large CSV Files**—Efficient handling of CSV files over **100,000 rows**.

---
### 🎡 How It Works 

1️⃣ **Importing Required Libraries**  
The project starts by importing essential Python libraries. These include **Flask** for the web app, **Pandas** for data handling, **SQLite** for query execution, and **Requests** for downloading CSV files.

2️⃣ **Flask App Setup**  
The **Flask** web framework runs the backend. It serves the main webpage and processes SQL queries submitted by users.

3️⃣ **CSV File Sources**  
A dictionary called `CSV_FILES` stores URLs of publicly available **CSV datasets**. Users can query these datasets using **SQL**.

4️⃣ **Extracting the Table Name from SQL Queries**  
Before running a query, we need to determine which **CSV file (table)** the user wants to query.

- The function `get_table_name(query)` extracts the table name from the SQL query.
- If the table exists in our `CSV_FILES` dictionary, we proceed. Otherwise, an **error is returned**.

5️⃣ **Loading CSV Data into SQLite (Handling Large Files Efficiently)**  
This is where **chunk-based processing** is used to handle large **CSV files**.

**Why is chunk processing important?**  
- Reading large CSV files (e.g., **100,000+ rows**) at once can consume too much memory.  
- Instead, we **load data in smaller chunks** (10,000 rows at a time) to improve efficiency.

**How It Works:**  
1. The function `load_csv_to_sqlite(table_name)` downloads the **CSV file** from the given URL.  
2. If the file is **gzip compressed**, it is decompressed before reading.  
3. A **temporary SQLite database (in-memory)** is created to store the data.  
4. The file is read in **chunks of 10,000 rows** using `pd.read_csv(chunksize=10_000)`.  
5. The **first chunk** creates the database table.  
6. **Additional chunks** are appended to avoid memory overload.  
7. Once all chunks are processed, the **SQLite database is ready for querying**.  

> **This approach prevents crashes when dealing with huge files and improves performance.**

6️⃣ **Running SQL Queries & Measuring Execution Time**  
1. When a user submits an **SQL query**, the app identifies the table and loads the **CSV file**.  
2. A timer (`time.time()`) is used to measure **execution time** of the query.  
3. The query runs on the **SQLite database** using Pandas.  
4. The results are displayed on the **webpage**, along with execution time.

7️⃣ **Flask Routes (Connecting the Backend to the Web Interface)**  
- `/` (**Home Page**) → Displays the **main interface**.  
- `/app` (**Query Page**) → Shows the **SQL input area**.  
- `/query` (**Processing SQL Queries**) → Runs the query and returns results.

8️⃣ **Running the Web App**  
Finally, the `app.run(debug=True)` command starts the **Flask server**, making the app **accessible via a browser**.

---

## 🛠 Technologies & Tools Used

### **Backend:**
- Flask (Python) for handling HTTP requests and query processing.

### **Database:**
- SQLite (in-memory) for fast and efficient querying.

### **Frontend:**
- HTML, CSS, and JavaScript for a structured, lightweight UI.

### **Data Handling:**
- Pandas for loading, managing, and querying CSV data.

### **HTTP Requests:**
- Requests library for fetching CSV files dynamically.

### **Compression Handling:**
- Supports **gzip-compressed** CSV files for optimized loading.

---

## ⚡ Performance & Optimizations

### 🕒 **Measuring Execution Time**
- time.time() records the current time in seconds. To measure execution time, the start time is captured before executing a task, and the end time is recorded after the task completes. The difference between these two values gives the total execution duration. This method helps assess   performance and identify bottlenecks in code execution.
 

### 🚀 **Optimizations for Large CSV Files**
- **Streaming Data Loading:** Chunk processing allows handling large CSV files efficiently by loading them in smaller portions instead of reading the entire file at once. Pandas provides a chunksize parameter that divides the file into manageable DataFrame segments.
- Each chunk is processed independently, reducing memory consumption and improving performance, especially for large datasets
 

---

## 🎡 Project Breakdown

- **Flask-based** web app that executes SQL queries on CSV files loaded from URLs.
- Uses **SQLite (in-memory)** for fast and efficient data processing.
- Provides an **interactive UI** to input and run SQL queries.
- **Error handling and execution logs** ensure seamless debugging.
- **Supports Large Datasets** by handling over **100,000+ rows efficiently**.
- **Supports GZIP compressed CSV files** for faster downloads.

---

## 🔍 Why SCHEMASPHERE?

✨ Because **writing SQL queries is way cooler** than endlessly scrolling through spreadsheets! 😎

Want to dive into structured data without setting up a full database? **SCHEMASPHERE** is your SQL playground.

 

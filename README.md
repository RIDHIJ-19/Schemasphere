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

## 🎨 How It Works

1️⃣ **Add a CSV link** – No database required!

2️⃣ **Write SQL queries** – Use standard SQL syntax to explore your data.

3️⃣ **Get instant results** – Structured output, just like a real database.

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
- Query execution time is measured using Python’s `time.time()`, capturing the duration of processing.
- Additional performance insights gathered using **Chrome DevTools** and **Lighthouse**.
- **Average response time:** Under **200ms** for most queries (dataset size dependent).

### 🚀 **Optimizations for Large CSV Files**
- **Streaming Data Loading:** Uses `chunksize` in Pandas to process large files efficiently.
- **Lazy Evaluation:** Queries run only when needed, reducing memory overhead.
- **Compressed File Support:** Automatically detects and decompresses gzip files for faster downloads.
- **Parallel Processing:** Uses multi-threading for handling large datasets efficiently.
- **Indexing Strategies:** Optimized indexing for faster lookups on large datasets.

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

📉 **Built with ❤️ for data lovers!**

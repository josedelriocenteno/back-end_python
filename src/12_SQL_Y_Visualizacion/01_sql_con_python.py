# ===========================================================================
# 01_sql_con_python.py
# ===========================================================================
# MODULO 12: SQL Y VISUALIZACION
# ARCHIVO 01: SQL con Python (sqlite3, SQLAlchemy, Patterns)
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar SQL desde Python: DDL, DML, queries avanzados,
# joins, subqueries, window functions, CTEs, y ORM.
#
# CONTENIDO:
#   1. sqlite3: conexion, cursor, execute.
#   2. DDL: CREATE, ALTER, DROP.
#   3. DML: INSERT, UPDATE, DELETE.
#   4. SELECT: WHERE, ORDER BY, LIMIT.
#   5. Aggregation: GROUP BY, HAVING.
#   6. JOINs: INNER, LEFT, RIGHT, CROSS.
#   7. Subqueries y CTEs.
#   8. Window functions.
#   9. Indices y optimizacion.
#   10. Pandas + SQL interop.
#   11. Patrones de produccion.
#   12. SQL injection y seguridad.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import sqlite3
import pandas as pd
import numpy as np
import time
import os


# =====================================================================
#   PARTE 1: SQLITE3 BASICO
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: SQLITE3 BASICO ===")
print("=" * 80)

"""
sqlite3: modulo built-in de Python para bases de datos SQL.
No requiere servidor. Base de datos en un archivo o en memoria.
Perfecto para prototyping, testing, datasets pequeños/medianos.
"""

print("\n--- Conexion ---")

# In-memory database (rapido, no persiste)
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

print(f"  SQLite version: {sqlite3.sqlite_version}")
print(f"  Connection: {conn}")
print(f"  Cursor: {cursor}")


print("\n--- Context manager ---")

"""
SIEMPRE usar context manager para commits automaticos:
with conn:
    conn.execute(...)
"""


# =====================================================================
#   PARTE 2: DDL (Data Definition Language)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DDL ===")
print("=" * 80)

print("\n--- CREATE TABLE ---")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        department TEXT,
        salary REAL,
        hire_date TEXT,
        is_active INTEGER DEFAULT 1
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        budget REAL,
        manager_id INTEGER,
        FOREIGN KEY (manager_id) REFERENCES employees(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        budget REAL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_projects (
        employee_id INTEGER,
        project_id INTEGER,
        role TEXT,
        hours_worked REAL DEFAULT 0,
        PRIMARY KEY (employee_id, project_id),
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
""")

conn.commit()

# Verificar tablas creadas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"  Tables: {[t[0] for t in tables]}")

# Schema de una tabla
cursor.execute("PRAGMA table_info(employees)")
schema = cursor.fetchall()
print(f"\n  employees schema:")
for col in schema:
    print(f"    {col[1]:15s} {col[2]:10s} {'NOT NULL' if col[3] else 'NULLABLE':>10s}")


# =====================================================================
#   PARTE 3: DML (Data Manipulation Language)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: DML ===")
print("=" * 80)

print("\n--- INSERT ---")

# Single insert con parametros (SIEMPRE usar ? para evitar SQL injection)
cursor.execute("""
    INSERT INTO employees (name, email, department, salary, hire_date)
    VALUES (?, ?, ?, ?, ?)
""", ('Alice Johnson', 'alice@company.com', 'Engineering', 95000, '2020-01-15'))

# executemany para batch insert (mucho mas rapido)
employees_data = [
    ('Bob Smith', 'bob@company.com', 'Marketing', 65000, '2021-03-20'),
    ('Charlie Brown', 'charlie@company.com', 'Engineering', 110000, '2019-06-01'),
    ('Diana Prince', 'diana@company.com', 'Sales', 78000, '2022-01-10'),
    ('Eve Davis', 'eve@company.com', 'Engineering', 88000, '2021-09-15'),
    ('Frank Wilson', 'frank@company.com', 'Marketing', 72000, '2020-11-01'),
    ('Grace Lee', 'grace@company.com', 'Sales', 82000, '2021-07-20'),
    ('Henry Taylor', 'henry@company.com', 'Engineering', 105000, '2018-04-15'),
    ('Iris Chen', 'iris@company.com', 'Sales', 91000, '2020-08-01'),
    ('Jack Brown', 'jack@company.com', 'Marketing', 68000, '2022-05-10'),
]

cursor.executemany("""
    INSERT INTO employees (name, email, department, salary, hire_date)
    VALUES (?, ?, ?, ?, ?)
""", employees_data)

conn.commit()
print(f"  Inserted {cursor.rowcount + 1} employees")

# Insert departments
dept_data = [
    ('Engineering', 500000, 3),
    ('Marketing', 200000, 2),
    ('Sales', 300000, 4),
]
cursor.executemany("""
    INSERT INTO departments (name, budget, manager_id)
    VALUES (?, ?, ?)
""", dept_data)

# Insert projects
project_data = [
    ('ML Pipeline', 1, '2024-01-01', '2024-06-30', 100000),
    ('Brand Campaign', 2, '2024-02-01', '2024-08-31', 50000),
    ('CRM System', 3, '2024-03-01', '2024-12-31', 150000),
    ('Data Lake', 1, '2024-04-01', '2024-10-31', 200000),
]
cursor.executemany("""
    INSERT INTO projects (name, department_id, start_date, end_date, budget)
    VALUES (?, ?, ?, ?, ?)
""", project_data)

# Insert employee_projects
ep_data = [
    (1, 1, 'Lead', 200), (3, 1, 'Developer', 300), (5, 1, 'Developer', 250),
    (8, 1, 'Architect', 150), (2, 2, 'Manager', 100), (6, 2, 'Designer', 180),
    (4, 3, 'Lead', 220), (7, 3, 'Sales Rep', 160), (9, 3, 'Analyst', 140),
    (1, 4, 'Architect', 180), (3, 4, 'Lead', 250), (5, 4, 'Developer', 200),
]
cursor.executemany("""
    INSERT INTO employee_projects (employee_id, project_id, role, hours_worked)
    VALUES (?, ?, ?, ?)
""", ep_data)

conn.commit()


print("\n--- UPDATE ---")

cursor.execute("""
    UPDATE employees SET salary = salary * 1.10
    WHERE department = 'Engineering' AND salary < 100000
""")
print(f"  Updated {cursor.rowcount} rows (10% raise for Engineers < 100k)")
conn.commit()


print("\n--- DELETE ---")

cursor.execute("SELECT COUNT(*) FROM employees WHERE is_active = 1")
print(f"  Active employees: {cursor.fetchone()[0]}")


# =====================================================================
#   PARTE 4: SELECT BASICO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: SELECT ===")
print("=" * 80)

print("\n--- SELECT basico ---")

cursor.execute("SELECT id, name, department, salary FROM employees ORDER BY salary DESC")
rows = cursor.fetchall()
print(f"  {'ID':>3s} {'Name':<18s} {'Department':<15s} {'Salary':>10s}")
for row in rows:
    print(f"  {row[0]:3d} {row[1]:<18s} {row[2]:<15s} {row[3]:>10,.0f}")


print("\n--- WHERE con operadores ---")

cursor.execute("""
    SELECT name, salary FROM employees
    WHERE salary BETWEEN 70000 AND 100000
    AND department IN ('Engineering', 'Sales')
    ORDER BY salary
""")
for row in cursor.fetchall():
    print(f"  {row[0]:<18s} {row[1]:>10,.0f}")


print("\n--- LIKE pattern matching ---")

cursor.execute("SELECT name FROM employees WHERE name LIKE '%son%' OR name LIKE 'E%'")
print(f"  LIKE matches: {[r[0] for r in cursor.fetchall()]}")


# =====================================================================
#   PARTE 5: AGGREGATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: AGGREGATION ===")
print("=" * 80)

print("\n--- GROUP BY ---")

cursor.execute("""
    SELECT department,
           COUNT(*) as count,
           ROUND(AVG(salary), 0) as avg_salary,
           MIN(salary) as min_salary,
           MAX(salary) as max_salary,
           ROUND(SUM(salary), 0) as total_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""")

print(f"  {'Dept':<15s} {'Count':>5s} {'Avg':>10s} {'Min':>10s} {'Max':>10s} {'Total':>12s}")
for row in cursor.fetchall():
    print(f"  {row[0]:<15s} {row[1]:>5d} {row[2]:>10,.0f} {row[3]:>10,.0f} {row[4]:>10,.0f} {row[5]:>12,.0f}")


print("\n--- HAVING ---")

cursor.execute("""
    SELECT department, COUNT(*) as cnt, ROUND(AVG(salary), 0) as avg_sal
    FROM employees
    GROUP BY department
    HAVING cnt >= 3 AND avg_sal > 70000
""")
print(f"  HAVING (count >= 3 AND avg > 70k):")
for row in cursor.fetchall():
    print(f"    {row[0]}: count={row[1]}, avg={row[2]:,.0f}")


# =====================================================================
#   PARTE 6: JOINS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: JOINS ===")
print("=" * 80)

print("\n--- INNER JOIN ---")

cursor.execute("""
    SELECT e.name, d.name as dept_name, d.budget
    FROM employees e
    INNER JOIN departments d ON e.department = d.name
    ORDER BY d.budget DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"  {row[0]:<18s} {row[1]:<15s} {row[2]:>12,.0f}")


print("\n--- LEFT JOIN ---")

cursor.execute("""
    SELECT e.name, ep.project_id, ep.role, ep.hours_worked
    FROM employees e
    LEFT JOIN employee_projects ep ON e.id = ep.employee_id
    ORDER BY e.name
""")
print(f"\n  LEFT JOIN (employees + projects):")
for row in cursor.fetchall():
    proj = row[1] if row[1] else 'None'
    role = row[2] if row[2] else '-'
    hours = row[3] if row[3] else 0
    print(f"    {row[0]:<18s} proj={str(proj):>4s} role={role:<12s} hours={hours:>5.0f}")


print("\n--- Multi-table JOIN ---")

cursor.execute("""
    SELECT e.name, p.name as project, ep.role, ep.hours_worked
    FROM employee_projects ep
    JOIN employees e ON ep.employee_id = e.id
    JOIN projects p ON ep.project_id = p.id
    ORDER BY p.name, ep.hours_worked DESC
""")
print(f"\n  Multi-table JOIN:")
for row in cursor.fetchall():
    print(f"    {row[0]:<18s} {row[1]:<18s} {row[2]:<12s} {row[3]:>5.0f}h")


# =====================================================================
#   PARTE 7: SUBQUERIES Y CTEs
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: SUBQUERIES Y CTEs ===")
print("=" * 80)

print("\n--- Subquery en WHERE ---")

cursor.execute("""
    SELECT name, salary FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees)
    ORDER BY salary DESC
""")
print(f"  Above average salary:")
for row in cursor.fetchall():
    print(f"    {row[0]:<18s} {row[1]:>10,.0f}")


print("\n--- Subquery correlacionada ---")

cursor.execute("""
    SELECT e.name, e.department, e.salary
    FROM employees e
    WHERE e.salary = (
        SELECT MAX(e2.salary) FROM employees e2
        WHERE e2.department = e.department
    )
""")
print(f"\n  Top earner per department:")
for row in cursor.fetchall():
    print(f"    {row[0]:<18s} {row[1]:<15s} {row[2]:>10,.0f}")


print("\n--- CTE (Common Table Expression) ---")

cursor.execute("""
    WITH dept_stats AS (
        SELECT department,
               AVG(salary) as avg_sal,
               COUNT(*) as cnt
        FROM employees
        GROUP BY department
    ),
    above_avg AS (
        SELECT e.name, e.department, e.salary, ds.avg_sal
        FROM employees e
        JOIN dept_stats ds ON e.department = ds.department
        WHERE e.salary > ds.avg_sal
    )
    SELECT name, department, salary, ROUND(avg_sal, 0) as dept_avg
    FROM above_avg
    ORDER BY salary DESC
""")
print(f"\n  CTE - Above dept average:")
for row in cursor.fetchall():
    print(f"    {row[0]:<18s} {row[1]:<15s} sal={row[2]:>10,.0f} avg={row[3]:>10,.0f}")


# =====================================================================
#   PARTE 8: WINDOW FUNCTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: WINDOW FUNCTIONS ===")
print("=" * 80)

"""
Window functions: calculos sobre un "window" de filas.
No colapsan filas como GROUP BY.
"""

print("\n--- ROW_NUMBER, RANK, DENSE_RANK ---")

cursor.execute("""
    SELECT name, department, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as row_num,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank,
           DENSE_RANK() OVER (ORDER BY salary DESC) as global_dense_rank
    FROM employees
    ORDER BY department, salary DESC
""")
print(f"  {'Name':<18s} {'Dept':<12s} {'Salary':>8s} {'Row#':>4s} {'Rank':>4s} {'GDR':>4s}")
for row in cursor.fetchall():
    print(f"  {row[0]:<18s} {row[1]:<12s} {row[2]:>8,.0f} {row[3]:>4d} {row[4]:>4d} {row[5]:>4d}")


print("\n--- Running totals (SUM OVER) ---")

cursor.execute("""
    SELECT name, salary,
           SUM(salary) OVER (ORDER BY hire_date) as running_total,
           AVG(salary) OVER (ORDER BY hire_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as ma_3
    FROM employees
    ORDER BY hire_date
""")
print(f"\n  Running totals:")
for row in cursor.fetchall():
    print(f"    {row[0]:<18s} sal={row[1]:>8,.0f} run_total={row[2]:>10,.0f} MA3={row[3]:>8,.0f}")


print("\n--- LAG / LEAD ---")

cursor.execute("""
    SELECT name, salary,
           LAG(salary, 1) OVER (ORDER BY salary) as prev_salary,
           LEAD(salary, 1) OVER (ORDER BY salary) as next_salary,
           salary - LAG(salary, 1) OVER (ORDER BY salary) as diff
    FROM employees
    ORDER BY salary
""")
print(f"\n  LAG/LEAD:")
for row in cursor.fetchall():
    prev = f"{row[2]:>8,.0f}" if row[2] else "    NULL"
    diff = f"{row[4]:>+8,.0f}" if row[4] else "    NULL"
    print(f"    {row[0]:<18s} {row[1]:>8,.0f} prev={prev} diff={diff}")


# =====================================================================
#   PARTE 9: INDICES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: INDICES ===")
print("=" * 80)

"""
Indices aceleran SELECTs pero ralentizan INSERTs/UPDATEs.
Crear en columnas usadas en WHERE, JOIN, ORDER BY.
"""

print("\n--- Create index ---")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_dept ON employees(department)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_salary ON employees(salary)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_hire ON employees(hire_date)")

# Composite index
cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_dept_sal ON employees(department, salary)")

cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
indices = [r[0] for r in cursor.fetchall()]
print(f"  Indices: {indices}")


print("\n--- EXPLAIN QUERY PLAN ---")

cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM employees WHERE department = 'Engineering'")
plan = cursor.fetchall()
print(f"  Query plan (with index):")
for step in plan:
    print(f"    {step}")


# =====================================================================
#   PARTE 10: PANDAS + SQL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: PANDAS + SQL ===")
print("=" * 80)

"""
pd.read_sql(): leer SQL query en DataFrame.
df.to_sql(): escribir DataFrame a tabla SQL.
"""

print("\n--- read_sql ---")

df_emp = pd.read_sql("SELECT * FROM employees", conn)
print(f"  DataFrame from SQL:\n{df_emp[['name','department','salary']].head()}")

# Query parametrizada
df_eng = pd.read_sql(
    "SELECT name, salary FROM employees WHERE department = ?",
    conn,
    params=['Engineering'],
)
print(f"\n  Parametrized:\n{df_eng}")


print("\n--- to_sql ---")

# Crear DataFrame y guardarlo en SQL
df_metrics = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'revenue': np.random.randint(1000, 5000, 30),
    'users': np.random.randint(100, 500, 30),
})

df_metrics.to_sql('daily_metrics', conn, if_exists='replace', index=False)

# Verificar
cursor.execute("SELECT COUNT(*) FROM daily_metrics")
print(f"  Saved {cursor.fetchone()[0]} rows to daily_metrics")


print("\n--- SQL analysis con Pandas ---")

df_analysis = pd.read_sql("""
    SELECT department,
           COUNT(*) as headcount,
           ROUND(AVG(salary), 0) as avg_salary
    FROM employees
    GROUP BY department
""", conn)
print(f"\n  SQL -> Pandas analysis:\n{df_analysis}")


# =====================================================================
#   PARTE 11: SQL INJECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: SQL INJECTION ===")
print("=" * 80)

"""
NUNCA interpolar strings en queries SQL.
SIEMPRE usar parametros (? o :name).
"""

print("\n--- MAL (vulnerable) ---")

user_input = "Engineering"
# PELIGROSO: f"SELECT * FROM employees WHERE department = '{user_input}'"
print(f"  BAD: f-string interpolation -> SQL injection risk!")


print("\n--- BIEN (seguro) ---")

# Positional parameters
cursor.execute("SELECT name FROM employees WHERE department = ?", (user_input,))
print(f"  GOOD (?): {[r[0] for r in cursor.fetchall()]}")

# Named parameters
cursor.execute(
    "SELECT name FROM employees WHERE department = :dept AND salary > :min_sal",
    {'dept': 'Engineering', 'min_sal': 90000}
)
print(f"  GOOD (:name): {[r[0] for r in cursor.fetchall()]}")


# =====================================================================
#   PARTE 12: TRANSACTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: TRANSACTIONS ===")
print("=" * 80)

"""
ACID: Atomicity, Consistency, Isolation, Durability.
En sqlite3: conn funciona como context manager para transacciones.
"""

print("\n--- Transaction con rollback ---")

try:
    with conn:
        conn.execute("UPDATE employees SET salary = 999999 WHERE name = 'Alice Johnson'")
        # Simular error
        raise ValueError("Simulated error!")
except ValueError:
    print("  Transaction rolled back (salary not changed)")

cursor.execute("SELECT salary FROM employees WHERE name = 'Alice Johnson'")
print(f"  Alice salary after rollback: {cursor.fetchone()[0]:,.0f}")


print("\n--- Batch insert performance ---")

# Without transaction (implicit auto-commit) vs with transaction
n = 5000

cursor.execute("CREATE TABLE IF NOT EXISTS bench (id INTEGER, val REAL)")

# With explicit transaction (fast)
start = time.perf_counter()
with conn:
    conn.executemany(
        "INSERT INTO bench VALUES (?, ?)",
        [(i, np.random.random()) for i in range(n)]
    )
t_batch = time.perf_counter() - start
print(f"\n  Batch insert ({n} rows): {t_batch:.3f}s")

cursor.execute("DROP TABLE bench")
conn.commit()


# =====================================================================
#   PARTE 13: PATRONES DE PRODUCCION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: PATRONES PRODUCCION ===")
print("=" * 80)

print("\n--- Connection factory ---")

class DatabaseManager:
    """Context manager para conexiones SQL."""
    
    def __init__(self, db_path=':memory:'):
        self.db_path = db_path
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Dict-like rows
        self.conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        self.conn.execute("PRAGMA foreign_keys=ON")
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

with DatabaseManager() as db:
    db.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    db.execute("INSERT INTO test VALUES (1, 'hello')")
    row = db.execute("SELECT * FROM test").fetchone()
    print(f"  Row factory: id={row['id']}, name={row['name']}")


print("\n--- UPSERT (INSERT OR REPLACE) ---")

cursor.execute("""
    INSERT OR REPLACE INTO employees (id, name, email, department, salary, hire_date)
    VALUES (1, 'Alice Johnson', 'alice_new@company.com', 'Engineering', 100000, '2020-01-15')
""")
conn.commit()

cursor.execute("SELECT email, salary FROM employees WHERE id = 1")
row = cursor.fetchone()
print(f"  After UPSERT: email={row[0]}, salary={row[1]:,.0f}")


# Reopen for more demos
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Recreate tables for remaining demos
cursor.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary REAL, hire_date TEXT)")
cursor.executemany("INSERT INTO employees VALUES (?,?,?,?,?)", [
    (1,'Alice','Engineering',100000,'2020-01-15'), (2,'Bob','Marketing',65000,'2021-03-20'),
    (3,'Charlie','Engineering',110000,'2019-06-01'), (4,'Diana','Sales',78000,'2022-01-10'),
    (5,'Eve','Engineering',96800,'2021-09-15'), (6,'Frank','Marketing',72000,'2020-11-01'),
    (7,'Grace','Sales',82000,'2021-07-20'), (8,'Henry','Engineering',105000,'2018-04-15'),
    (9,'Iris','Sales',91000,'2020-08-01'), (10,'Jack','Marketing',68000,'2022-05-10'),
])
conn.commit()


# =====================================================================
#   PARTE 14: CASE WHEN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: CASE WHEN ===")
print("=" * 80)

cursor.execute("""
    SELECT name, salary,
           CASE
               WHEN salary >= 100000 THEN 'Senior'
               WHEN salary >= 80000 THEN 'Mid'
               ELSE 'Junior'
           END as tier,
           CASE department
               WHEN 'Engineering' THEN 'Tech'
               WHEN 'Marketing' THEN 'Business'
               ELSE 'Revenue'
           END as division
    FROM employees
    ORDER BY salary DESC
""")

print(f"  {'Name':<15s} {'Salary':>10s} {'Tier':<8s} {'Division':<10s}")
for row in cursor.fetchall():
    print(f"  {row[0]:<15s} {row[1]:>10,.0f} {row[2]:<8s} {row[3]:<10s}")


# =====================================================================
#   PARTE 15: UNION, INTERSECT, EXCEPT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: SET OPERATIONS ===")
print("=" * 80)

print("\n--- UNION ---")

cursor.execute("""
    SELECT name, 'high_salary' as reason FROM employees WHERE salary > 90000
    UNION
    SELECT name, 'engineering' as reason FROM employees WHERE department = 'Engineering'
    ORDER BY name
""")
print(f"  UNION (high salary OR engineering):")
for row in cursor.fetchall():
    print(f"    {row[0]:<15s} {row[1]}")


print("\n--- EXCEPT ---")

cursor.execute("""
    SELECT name FROM employees WHERE department = 'Engineering'
    EXCEPT
    SELECT name FROM employees WHERE salary > 100000
""")
print(f"  EXCEPT (engineering but NOT > 100k): {[r[0] for r in cursor.fetchall()]}")


# =====================================================================
#   PARTE 16: VIEWS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: VIEWS ===")
print("=" * 80)

"""
Views: queries guardados como tablas virtuales.
No almacenan datos, se recalculan cada vez.
"""

cursor.execute("""
    CREATE VIEW IF NOT EXISTS dept_summary AS
    SELECT department,
           COUNT(*) as headcount,
           ROUND(AVG(salary), 0) as avg_salary,
           MIN(salary) as min_salary,
           MAX(salary) as max_salary
    FROM employees
    GROUP BY department
""")
conn.commit()

cursor.execute("SELECT * FROM dept_summary ORDER BY avg_salary DESC")
print(f"  View dept_summary:")
for row in cursor.fetchall():
    print(f"    {row[0]:<15s} count={row[1]} avg={row[2]:,.0f}")


# =====================================================================
#   PARTE 17: TRIGGERS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: TRIGGERS ===")
print("=" * 80)

"""
Triggers: acciones automaticas en INSERT/UPDATE/DELETE.
"""

cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT,
        action TEXT,
        old_value TEXT,
        new_value TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS log_salary_change
    AFTER UPDATE OF salary ON employees
    BEGIN
        INSERT INTO audit_log (table_name, action, old_value, new_value)
        VALUES ('employees', 'UPDATE_SALARY',
                OLD.name || ': ' || OLD.salary,
                NEW.name || ': ' || NEW.salary);
    END
""")
conn.commit()

# Trigger a salary update
cursor.execute("UPDATE employees SET salary = 115000 WHERE name = 'Charlie'")
conn.commit()

cursor.execute("SELECT * FROM audit_log")
for row in cursor.fetchall():
    print(f"  Audit: {row[2]} | old={row[3]} | new={row[4]}")


# =====================================================================
#   PARTE 18: RECURSIVE CTE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: RECURSIVE CTE ===")
print("=" * 80)

"""
Recursive CTEs: para datos jerarquicos (org charts, trees).
"""

cursor.execute("""
    CREATE TABLE IF NOT EXISTS org (
        id INTEGER PRIMARY KEY,
        name TEXT,
        manager_id INTEGER
    )
""")
cursor.executemany("INSERT INTO org VALUES (?,?,?)", [
    (1, 'CEO', None), (2, 'VP_Eng', 1), (3, 'VP_Sales', 1),
    (4, 'Lead_1', 2), (5, 'Lead_2', 2), (6, 'Dev_1', 4), (7, 'Dev_2', 4),
])
conn.commit()

cursor.execute("""
    WITH RECURSIVE org_tree AS (
        SELECT id, name, manager_id, 0 as level, name as path
        FROM org WHERE manager_id IS NULL
        UNION ALL
        SELECT o.id, o.name, o.manager_id, ot.level + 1,
               ot.path || ' > ' || o.name
        FROM org o
        JOIN org_tree ot ON o.manager_id = ot.id
    )
    SELECT level, name, path FROM org_tree ORDER BY path
""")
print(f"  Org hierarchy:")
for row in cursor.fetchall():
    indent = "  " * row[0]
    print(f"    {indent}{row[1]} (level {row[0]})")


# =====================================================================
#   PARTE 19: QUERY BUILDER PATTERN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: QUERY BUILDER ===")
print("=" * 80)

class QueryBuilder:
    """Builder pattern para SQL queries."""
    
    def __init__(self, table):
        self._table = table
        self._columns = ['*']
        self._wheres = []
        self._params = []
        self._order = None
        self._limit = None
    
    def select(self, *columns):
        self._columns = list(columns)
        return self
    
    def where(self, condition, *params):
        self._wheres.append(condition)
        self._params.extend(params)
        return self
    
    def order_by(self, column, desc=False):
        self._order = f"{column} {'DESC' if desc else 'ASC'}"
        return self
    
    def limit(self, n):
        self._limit = n
        return self
    
    def build(self):
        sql = f"SELECT {', '.join(self._columns)} FROM {self._table}"
        if self._wheres:
            sql += " WHERE " + " AND ".join(self._wheres)
        if self._order:
            sql += f" ORDER BY {self._order}"
        if self._limit:
            sql += f" LIMIT {self._limit}"
        return sql, self._params

# Usage
query, params = (
    QueryBuilder('employees')
    .select('name', 'salary', 'department')
    .where('salary > ?', 80000)
    .where('department = ?', 'Engineering')
    .order_by('salary', desc=True)
    .limit(5)
    .build()
)

print(f"  Built query: {query}")
print(f"  Params: {params}")

cursor.execute(query, params)
for row in cursor.fetchall():
    print(f"    {row[0]:<15s} {row[1]:>10,.0f} {row[2]}")


# =====================================================================
#   PARTE 20: MIGRATION PATTERN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: MIGRATIONS ===")
print("=" * 80)

"""
Schema migrations: versionado de schema.
"""

def migrate(conn, migrations):
    """Aplicar migraciones pendientes."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY,
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    current = conn.execute("SELECT MAX(version) FROM schema_version").fetchone()[0] or 0
    
    for version, sql in migrations.items():
        if version > current:
            conn.execute(sql)
            conn.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))
            print(f"  Applied migration v{version}")
    
    conn.commit()

migrations = {
    1: "ALTER TABLE employees ADD COLUMN bonus REAL DEFAULT 0",
    2: "CREATE INDEX IF NOT EXISTS idx_emp_bonus ON employees(bonus)",
}

migrate(conn, migrations)
cursor.execute("SELECT version FROM schema_version ORDER BY version")
print(f"  Schema versions: {[r[0] for r in cursor.fetchall()]}")


# =====================================================================
#   PARTE 21: AGGREGATE FUNCTIONS CUSTOM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: CUSTOM AGGREGATES ===")
print("=" * 80)

"""
sqlite3 permite crear funciones aggregate custom.
"""

class MedianAggregate:
    def __init__(self):
        self.values = []
    
    def step(self, value):
        if value is not None:
            self.values.append(value)
    
    def finalize(self):
        if not self.values:
            return None
        self.values.sort()
        n = len(self.values)
        if n % 2 == 0:
            return (self.values[n//2 - 1] + self.values[n//2]) / 2
        return self.values[n//2]

conn.create_aggregate("MEDIAN", 1, MedianAggregate)

cursor.execute("SELECT department, MEDIAN(salary) as median_sal FROM employees GROUP BY department")
print(f"  Custom MEDIAN aggregate:")
for row in cursor.fetchall():
    print(f"    {row[0]:<15s} median={row[1]:,.0f}")


conn.close()


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE SQL CON PYTHON:

1. sqlite3: built-in, sin servidor, ideal para prototyping.
2. SIEMPRE usar parametros (?) - NUNCA string interpolation.
3. executemany para batch operations.
4. CTEs para queries legibles y mantenibles.
5. Window functions para analytics sin GROUP BY.
6. Indices en columnas de WHERE/JOIN/ORDER BY.
7. pd.read_sql/to_sql para interop Pandas.
8. ACID transactions con context manager.
9. row_factory=sqlite3.Row para acceso por nombre.
10. PRAGMA WAL para concurrencia.

Siguiente archivo: Matplotlib Deep Dive.
"""

print("\n FIN DE ARCHIVO 01_sql_con_python.")
print(" SQL con Python ha sido dominado.")

import sqlite3


DATABASE_NAME = "database.db"


# --------------------------------
# Connect to Database
# --------------------------------

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)

    # Enable SQLite foreign-key support
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# --------------------------------
# Create or Update Users Table
# --------------------------------

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT DEFAULT 'N/A',
            age INTEGER NOT NULL
        )
    """)

    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()

    column_names = [
        column[1]
        for column in columns
    ]

    if "gender" not in column_names:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN gender TEXT DEFAULT 'N/A'
        """)

    conn.commit()
    conn.close()


# --------------------------------
# Create Charges Table
# --------------------------------

def create_charges_table():
    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS charges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            charge REAL NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------
# Add User
# --------------------------------

def add_to_database(name, gender, age):
    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (
            name,
            gender,
            age
        )
        VALUES (?, ?, ?)
        """,
        (
            name,
            gender,
            age
        )
    )

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


# --------------------------------
# Get All Users
# --------------------------------

def getData():
    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, gender, age
        FROM users
        ORDER BY name
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# --------------------------------
# Get One User
# --------------------------------

def get_user(user_id):
    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, gender, age
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# --------------------------------
# Update User
# --------------------------------

def update_user(user_id, name, gender, age):
    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET name = ?,
            gender = ?,
            age = ?
        WHERE id = ?
        """,
        (
            name,
            gender,
            age,
            user_id
        )
    )

    conn.commit()
    conn.close()


# --------------------------------
# Delete One User
# --------------------------------

def delete_user(user_id):
    create_table()
    create_charges_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()


# --------------------------------
# Delete Multiple Users
# --------------------------------

def deleteDataRows(ids):
    create_table()
    create_charges_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        [
            (user_id,)
            for user_id in ids
        ]
    )

    conn.commit()
    conn.close()


# --------------------------------
# Delete From Starting ID to End
# --------------------------------

def delete_from_id(start_id):
    create_table()
    create_charges_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id >= ?
        """,
        (start_id,)
    )

    conn.commit()
    conn.close()


# --------------------------------
# Add Charge
# --------------------------------

def add_charge(user_id, charge, description):
    create_charges_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO charges (
            user_id,
            charge,
            description
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            charge,
            description
        )
    )

    charge_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return charge_id


# --------------------------------
# Get Charges for One User
# --------------------------------

def get_charges(user_id):
    create_charges_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, charge, description
        FROM charges
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    charges = cursor.fetchall()

    conn.close()

    return charges


# --------------------------------
# Delete One Charge
# --------------------------------

def delete_charge(charge_id):
    create_charges_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM charges
        WHERE id = ?
        """,
        (charge_id,)
    )

    conn.commit()
    conn.close()


# --------------------------------
# Start Database
# --------------------------------
# --------------------------------
# Get Total Charges
# --------------------------------

def get_total_charges(user_id):
    create_charges_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(charge), 0)
        FROM charges
        WHERE user_id = ?
        """,
        (user_id,)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return float(total)

create_table()
create_charges_table()
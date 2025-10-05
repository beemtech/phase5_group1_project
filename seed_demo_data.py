
import psycopg2

conn = psycopg2.connect(
    dbname="homematch_db",
    user="homematch",
    password="homematch",
    host="db",
    port="5432"
)
cur = conn.cursor()

# Create tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS landlords (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS renters (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        price NUMERIC,
        landlord_id INT REFERENCES landlords(id)
    );
""")

# Clear existing
cur.execute("DELETE FROM listings;")
cur.execute("DELETE FROM landlords;")
cur.execute("DELETE FROM renters;")

# Insert demo landlords
landlords = [
    ("Antony", "antony@example.com"),
    ("Kelvin", "kelvin@example.com"),
    ("Mercy", "mercy@example.com")
]
cur.executemany("INSERT INTO landlords (name, email) VALUES (%s, %s);", landlords)

# Insert demo renters
renters = [
    ("Beth", "beth@example.com"),
    ("Edwin", "edwin@example.com"),
    ("Mirriam", "mirriam@example.com")
]
cur.executemany("INSERT INTO renters (name, email) VALUES (%s, %s);", renters)

# Insert demo listings
listings = [
    ("2-Bedroom Apartment in Nairobi", 50000, 1),
    ("1-Bedroom in Westlands", 30000, 2),
    ("Studio in Kisumu", 15000, 3)
]
cur.executemany("INSERT INTO listings (title, price, landlord_id) VALUES (%s, %s, %s);", listings)

conn.commit()
cur.close()
conn.close()

print("✅ Demo data seeded successfully!")

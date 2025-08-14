from __init__ import CURSOR, CONN


class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Department instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Department instances"""
        sql = """
            DROP TABLE IF EXISTS departments
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Save this Department instance to the database"""
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, location):
        """Create a new Department instance and save it to the database"""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the database row corresponding to this Department instance"""
        if self.id is None:
            raise ValueError("Department instance must be saved before updating")
        
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the database row corresponding to this Department instance"""
        if self.id is None:
            raise ValueError("Department instance must be saved before deleting")
        
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Department instance having the attribute values from the table row"""
        return cls(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        """Return a list of all Department instances from the database"""
        sql = """
            SELECT * FROM departments
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Find a department by its ID and return a Department instance"""
        sql = """
            SELECT * FROM departments
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Find a department by its name and return a Department instance"""
        sql = """
            SELECT * FROM departments
            WHERE name = ?
            LIMIT 1
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

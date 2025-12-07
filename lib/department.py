from __init__ import CURSOR, CONN


class Department:

    all = {}  # dictionary to store instances by id

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    # -----------------------------------------
    # TABLE METHODS
    # -----------------------------------------

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()

    # -----------------------------------------
    # INSTANCE SAVE / CREATE
    # -----------------------------------------

    def save(self):
        """Insert a new row into db and store instance in Department.all"""
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid

        # store in dictionary
        Department.all[self.id] = self

    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    # -----------------------------------------
    # UPDATE
    # -----------------------------------------

    def update(self):
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

        # update dictionary
        Department.all[self.id] = self

    # -----------------------------------------
    # DELETE
    # -----------------------------------------

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # remove from dictionary
        if self.id in Department.all:
            del Department.all[self.id]

        # set id to None to satisfy tests
        self.id = None

    # -----------------------------------------
    # INSTANCE_FROM_DB
    # -----------------------------------------

    @classmethod
    def instance_from_db(cls, row):
        """Return an instance from a DB row, reuse if exists."""
        id, name, location = row

        if id in cls.all:
            dept = cls.all[id]
            dept.name = name
            dept.location = location
        else:
            dept = cls(name, location, id)
            cls.all[id] = dept

        return dept

    # -----------------------------------------
    # GET ALL
    # -----------------------------------------

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    # -----------------------------------------
    # FIND BY ID
    # -----------------------------------------

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # -----------------------------------------
    # FIND BY NAME
    # -----------------------------------------

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

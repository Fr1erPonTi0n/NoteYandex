import sqlite3

from datetime import datetime
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLabel, QAbstractItemView
from PyQt6.QtGui import QIcon


class OutputBase(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о базе")
        self.setWindowIcon(QIcon("assets/note.png"))
        self.layout = QVBoxLayout()
        self.resize(700, 400)
        self.table_widget_one = QTableWidget()
        self.table_widget_two = QTableWidget()
        self.layout.addWidget(QLabel('Таблица заметок'))
        self.layout.addWidget(self.table_widget_one)
        self.layout.addWidget(QLabel('Таблица каталогов'))
        self.layout.addWidget(self.table_widget_two)
        self.setLayout(self.layout)
        self.load_data()
        self.table_widget_one.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget_two.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def load_data(self):
        con = sqlite3.connect("database.sqlite")
        cur = con.cursor()

        cur.execute("SELECT * FROM catalogs")
        catalogs = cur.fetchall()

        cur.execute("SELECT * FROM notes")
        notes = cur.fetchall()

        self.table_widget_one.setRowCount(len(notes))
        self.table_widget_one.setColumnCount(8)

        self.table_widget_one.setHorizontalHeaderLabels([
            "NOTE_ID", "ID_CATALOG", "NOTE_NAME", "TEXT", "COUNT_LINES",
            "CREATE_DATE_NOTE", "PLANNED_DATE", "LAST_DATE_CHANGE"
        ])

        for row_index, note in enumerate(notes):
            self.table_widget_one.setItem(row_index, 0, QTableWidgetItem(str(note[0])))
            self.table_widget_one.setItem(row_index, 1, QTableWidgetItem(str(note[1])))
            self.table_widget_one.setItem(row_index, 2, QTableWidgetItem(note[2]))
            self.table_widget_one.setItem(row_index, 3, QTableWidgetItem(note[3]))
            self.table_widget_one.setItem(row_index, 4, QTableWidgetItem(str(note[4])))
            self.table_widget_one.setItem(row_index, 5, QTableWidgetItem(note[5]))
            self.table_widget_one.setItem(row_index, 6, QTableWidgetItem(note[6]))
            self.table_widget_one.setItem(row_index, 7, QTableWidgetItem(note[7]))

        self.table_widget_two.setRowCount(len(catalogs))
        self.table_widget_two.setColumnCount(3)
        self.table_widget_two.setHorizontalHeaderLabels(["ID", "NAME_CATALOG", "CREATE_DATE_CATALOG"])

        for row_index, catalog in enumerate(catalogs):
            self.table_widget_two.setItem(row_index, 0, QTableWidgetItem(str(catalog[0])))
            self.table_widget_two.setItem(row_index, 1, QTableWidgetItem(catalog[1]))
            self.table_widget_two.setItem(row_index, 2, QTableWidgetItem(catalog[2]))

        con.close()


class Base:
    def __init__(self):
        self.con = sqlite3.connect("database.sqlite")

    def get_all_notes(self):
        cur = self.con.cursor()
        notes = cur.execute("SELECT note_name FROM notes ORDER BY note_name").fetchall()
        return [note[0] for note in notes]

    def create_note(self, notename, catalog):
        cur = self.con.cursor()
        existing_note = cur.execute("SELECT * FROM notes WHERE note_name = ?", (notename,)).fetchone()
        if existing_note:
            self.con.close()
            return Exception
        create_date = datetime.now().strftime('%d.%m.%Y')
        if catalog is None or catalog == '' or catalog == 'Основная категория':
            id_catalog = 1
        else:
            existing_catalog = cur.execute("SELECT * FROM catalogs WHERE name_catalog = ?",
                                           (catalog,)).fetchone()
            if existing_catalog:
                id_catalog = existing_catalog[0]
            else:
                cur.execute("INSERT INTO catalogs (name_catalog, create_date_catalog) VALUES (?, ?)",
                            (catalog, create_date))
                id_catalog = cur.lastrowid
        cur.execute("INSERT INTO notes (note_name, create_date_note, id_catalog) VALUES (?, ?, ?)",
                    (notename, create_date, id_catalog))
        self.con.commit()

    def load_catalogs(self):
        cur = self.con.cursor()
        rows = cur.execute("SELECT id, name_catalog FROM catalogs").fetchall()
        return rows

    def list_notes_by_catalog(self, catalog_id):
        cur = self.con.cursor()
        if catalog_id is not None:
            notes = cur.execute("SELECT note_name FROM notes WHERE id_catalog = ?",
                                (catalog_id,)).fetchall()
        else:
            notes = cur.execute("SELECT NOTE_NAME FROM notes").fetchall()
        return [note[0] for note in notes]

    def get_note_text(self, note_name):
        cur = self.con.cursor()
        note_text_row = cur.execute("SELECT text FROM notes WHERE note_name = ?",
                                    (note_name,)).fetchone()
        return note_text_row[0] if note_text_row else ""

    def info_notes(self, note_name):
        cur = self.con.cursor()
        query = """
            SELECT 
                notes.note_id, 
                notes.note_name,
                notes.count_lines,
                notes.create_date_note,
                notes.planned_date,
                notes.last_date_change,
                catalogs.id,
                catalogs.name_catalog,
                catalogs.create_date_catalog
                
            FROM 
                notes 
            JOIN 
                catalogs
            ON 
                notes.id_catalog = catalogs.id
            WHERE 
                notes.note_name = ?;
            """
        result = cur.execute(query, (note_name,)).fetchone()
        return result

    def rename_note(self, last_name, new_name):
        cur = self.con.cursor()
        existing_note = cur.execute('SELECT * FROM notes WHERE note_name = ?', (last_name,)).fetchone()
        if existing_note:
            cur.execute("UPDATE notes SET note_name = ? WHERE note_name = ?", (new_name, last_name))
            self.con.commit()
        else:
            raise Exception

    def delete_note(self, notename):
        cur = self.con.cursor()
        if notename is None or notename == '':
            raise Exception
        cur.execute("DELETE FROM notes WHERE note_name = ?", (notename,))
        self.con.commit()

    def save_note(self, notename, text, planned_date, count_lens, id_catalog):
        cur = self.con.cursor()
        last_date_change = datetime.now().strftime('%d.%m.%Y')

        existing_note = cur.execute('SELECT * FROM notes WHERE note_name = ?', (notename,)).fetchone()
        if id_catalog is None:
            id_catalog = 1
        if existing_note:
            if planned_date is None:
                cur.execute('''
                            UPDATE notes 
                            SET text = ?, count_lines = ?, last_date_change = ?
                            WHERE note_name = ?
                        ''', (text, count_lens, last_date_change, notename))
            else:
                cur.execute('''
                            UPDATE notes 
                            SET text = ?, planned_date = ?, count_lines = ?, last_date_change = ?
                            WHERE note_name = ?
                        ''', (text, planned_date, count_lens, last_date_change, notename))
        else:
            if planned_date is None:
                cur.execute('''
                            INSERT INTO notes (note_name, text, count_lines, last_date_change, id_catalog) 
                            VALUES (?, ?, ?, ?, ?)
                        ''', (notename, text, count_lens, last_date_change, id_catalog))
            else:
                cur.execute('''
                            INSERT INTO notes (note_name, text, planned_date, count_lines, last_date_change, id_catalog) 
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (notename, text, planned_date, count_lens, last_date_change, id_catalog))
        self.con.commit()

    def create_catalog(self, catalogname):
        cur = self.con.cursor()
        existing_catalog = cur.execute(
            'SELECT * FROM catalogs WHERE name_catalog = ?',
            (catalogname,)
        ).fetchone()
        create_date = datetime.now().strftime('%d.%m.%Y')

        if existing_catalog:
            raise Exception
        else:
            cur.execute('''INSERT INTO catalogs (name_catalog, create_date_catalog) VALUES (?, ?)''',
                        (catalogname, create_date))

        self.con.commit()

    def delete_catalog(self, catalogname, namenote):
        cur = self.con.cursor()
        existing_catalog = cur.execute('SELECT * FROM catalogs WHERE name_catalog = ?',
                                       (catalogname,)).fetchone()

        if existing_catalog:
            id_catalog = existing_catalog[0]

            existing_note = cur.execute('SELECT * FROM notes WHERE id_catalog = ? AND note_name = ?',
                                        (id_catalog, namenote)).fetchone()

            cur.execute('DELETE FROM notes WHERE id_catalog = ?', (id_catalog,))
            cur.execute('DELETE FROM catalogs WHERE name_catalog = ?', (catalogname,))
        else:
            raise Exception

        self.con.commit()

        if existing_note:
            return True

    def close_base(self):
        self.con.close()

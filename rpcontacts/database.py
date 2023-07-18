from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def _createContactsTable():
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                plant VARCHAR(50) NOT NULL,
                description VARCHAR(50) NOT NULL,
                watering_time VARCHAR(50)
            )
        """
    )


def createConnection(dbName):
    conn = QSqlDatabase.addDatabase("QSQLITE")
    conn.setDatabaseName(dbName)

    if not conn.open():
        QMessageBox.warning(
            None,
            'Contacts',
            f"Database Error: {conn.lastError().text()}",
        )
        return False

    _createContactsTable()
    return True
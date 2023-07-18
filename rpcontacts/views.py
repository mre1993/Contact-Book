from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from model import ContactsModel


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Contacts Book')
        self.resize(650, 350)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.contactsModel = ContactsModel()
        self.setupUI()


    def setupUI(self):
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()

        self.addButton = QPushButton('Add...')
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton('Delete')
        self.deleteButton.clicked.connect(self.deleteContact)
        self.clearAllButton = QPushButton('Clear All')
        self.clearAllButton.clicked.connect(self.clearContact)

        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)


    def openAddDialog(self):
        dialog = AddDialog(self)
        dialog.resize(275, 150)
        if (dialog.exec() == QDialog.Accepted):
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()


    def deleteContact(self):
        row = self.table.currentIndex().row()
        if (row < 0):
            return
        
        msgBox = QMessageBox.warning(
            self,
            'Warning!',
            "ایا از حذف این سطر مطمئنی؟",
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if (msgBox == QMessageBox.Ok):
            self.contactsModel.deleteContact(row)


    def clearContact(self):
        msgBox = QMessageBox.warning(
            self,
            'WARNING!',
            "?ایا از حذف تمام سطرها مطمئنی",
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if (msgBox == QMessageBox.Ok):
            self.contactsModel.clearContact()


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('Add Contact')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()


    def setupUI(self):
        self.nameField = QLineEdit()
        self.nameField.setObjectName('Name')
        self.emailField = QLineEdit()
        self.emailField.setObjectName('Phone')
        self.statusField = QLineEdit()
        self.statusField.setObjectName('Email')

        layout = QFormLayout()
        layout.addRow('Name:', self.nameField)
        layout.addRow('Phone:', self.emailField)
        layout.addRow('Email:', self.statusField)
        self.layout.addLayout(layout)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)


    def accept(self):
        self.data = []
        for field in (self.nameField, self.emailField, self.statusField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    'Error!',
                    f"!باید داده وارد شود {field.objectName()}",
                )
                self.data = None
                return
            else:
                self.data.append(field.text())
        super().accept()
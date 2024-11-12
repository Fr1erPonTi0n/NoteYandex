import sys, os, re
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QListWidget,
                             QMenu, QApplication, QHBoxLayout, QDialog, QLabel, QDialogButtonBox, QLineEdit)
from PyQt6.QtGui import QAction, QIcon
from base import Base


def is_valid_filename(filename):
    pattern_without_extension = r'^[^<>:;,?"*|/\\]+$'
    pattern_with_extension = r'^[^<>:;,?"*|/\\]+\.[tT][xX][tT]$'
    return re.match(pattern_without_extension, filename) or re.match(pattern_with_extension, filename)


class InfoFile(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/info.png"))
        self.resize(400, 300)
        self.setWindowTitle("Информация о файле")

        self.layout = QVBoxLayout()
        self.text = QLabel('!!!!')
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        self.exec()


class RenameFile(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/info.png"))
        self.resize(400, 300)
        self.setWindowTitle("Изменение имени")
        self.setFixedHeight(100)

        QBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setFixedHeight(30)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_input(self):
        return self.text_input.text().strip()


class ChoiceOpenFile(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/info.png"))
        self.resize(400, 300)
        self.setWindowTitle('Открыть файл')
        self.setFixedHeight(100)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel("Вы точно хотите открыть файл, не сохранив этот вариант?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class CreateFile(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/info.png"))
        self.resize(400, 300)
        self.setWindowTitle('Создание файла')
        self.setFixedHeight(160)

        QBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.name_file = QLabel("Имя файла:")
        self.input_name = QTextEdit()
        self.name_category = QLabel("Имя категории:")
        self.input_category = QTextEdit()

        self.layout.addWidget(self.name_file)
        self.layout.addWidget(self.input_name)
        self.layout.addWidget(self.name_category)
        self.layout.addWidget(self.input_category)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_input(self):
        return self.input_name.toPlainText().strip(), self.input_category.toPlainText().strip()


class DeleteFile(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/info.png"))
        self.resize(400, 300)
        self.setWindowTitle('Открыть файл')
        self.setFixedHeight(100)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel("Вы точно хотите удалить файл?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        '''ОБЪЕКТЫ В КОДЕ
                central_widget (QWidget) = {
                createCategory - Создает категорию (QPushButton);
                deleteCategory - Удаляет категорию (QPushButton);
                editFile - Изменяет тект в файле (QTextEdit);
                filterFiles - Фильтрация файлов по категориям (QComboBox);
                foundFile - Находит файл по набранному тексту (QTextEdit);
                listFiles - Список всех файлов по определенным критериям указанных выше (QListWidget);
                nameEdit - Название файла, возможность изменять название файла (QTextEdit)
                }

                menubar - (QMenuBar) = {
                menuMenu - (QMenu) = {actionOpen_File - Открывает файл (QAction);
                actionSave_File - Сохраняет файл (QAction);
                actionCreate_File - Создает новый файл (QAction);
                actionDelete_Fire - Удаляет файл (QAction);
                actionFile_info - Вывод информации о файле (QAction)}
                }'''
        self.setWindowTitle("Блокнот")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/main.png"))
        self.later = ""

        # Элементы управления
        self.createCategory = QPushButton("Создать категорию")
        self.createCategory.setFixedHeight(30)
        self.deleteCategory = QPushButton("Удалить категорию")
        self.deleteCategory.setFixedHeight(30)
        self.editFile = QTextEdit()
        self.filterFiles = QComboBox()
        self.filterFiles.setFixedHeight(30)
        self.foundFile = QTextEdit()
        self.foundFile.setFixedHeight(30)
        self.listFiles = QListWidget()
        self.nameEdit = QTextEdit()
        self.nameEdit.setFixedHeight(30)

        # Центральный виджет
        wid = QWidget()
        self.setCentralWidget(wid)

        # Основной макет
        hl_1 = QHBoxLayout()
        hl_2 = QHBoxLayout()
        hl_3 = QHBoxLayout()
        main_v = QVBoxLayout()

        hl_1.addWidget(self.filterFiles, 2)
        hl_1.addWidget(self.createCategory, 2)
        hl_1.addWidget(self.deleteCategory, 2)

        hl_2.addWidget(self.foundFile, 2)
        hl_2.addWidget(self.nameEdit, 4)

        hl_3.addWidget(self.listFiles, 2)
        hl_3.addWidget(self.editFile, 4)

        # Добавление элементов в макет
        main_v.addLayout(hl_1)
        main_v.addLayout(hl_2)
        main_v.addLayout(hl_3)

        # Создание меню
        self.menubar = self.menuBar()

        # Меню "Файл"
        self.menuMenu = QMenu("Файл", self)
        self.menubar.addMenu(self.menuMenu)

        # Действия для меню "Файл"
        self.actionOpen_File = QAction("Открыть файл", self)
        self.actionSave_File = QAction("Сохранить файл", self)
        self.actionCreate_File = QAction("Создать новый файл", self)
        self.actionDelete_File = QAction("Удалить файл", self)
        self.actionFile_info = QAction("Информация о файле", self)
        self.actionRename_file = QAction("Изменить имя файла", self)

        # Добавление действий в меню "Файл"
        self.menuMenu.addAction(self.actionFile_info)
        self.menuMenu.addAction(self.actionRename_file)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionOpen_File)
        self.menuMenu.addAction(self.actionSave_File)
        self.menuMenu.addAction(self.actionCreate_File)
        self.menuMenu.addAction(self.actionDelete_File)

        wid.setLayout(main_v)

        # Подключение всех кнопок и т.д.
        self.actionFile_info.triggered.connect(self.fileinfo_clicked)
        self.actionRename_file.triggered.connect(self.rename_file)
        self.actionSave_File.triggered.connect(self.save_file)
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionCreate_File.triggered.connect(self.create_file)
        self.actionDelete_File.triggered.connect(self.delete_file)

    def fileinfo_clicked(self):
        if self.sender() == self.actionFile_info:
            print("Вывод информации о файле")
            InfoFile()

    def rename_file(self):
        print("Изменение имени файла")
        if self.sender() == self.actionRename_file:
            rename_dialog = RenameFile()
            if rename_dialog.exec():
                new_name = rename_dialog.get_input()
                current_file_path = f'notes/{self.nameEdit.toPlainText()}'
                if not new_name:
                    print("Новое имя файла не может быть пустым.")
                if not is_valid_filename(new_name):
                    print("Имя файла должно соответствовать шаблонам 'text' или 'text.txt'.")
                if not new_name.lower().endswith('.txt'):
                    new_name += '.txt'
                new_file_path = f'notes/{new_name}'
                if os.path.exists(new_file_path):
                    print(f'Файл с именем "{new_file_path}" уже существует.')
                try:
                    os.rename(current_file_path, new_file_path)
                    self.nameEdit.setText(new_name)
                except:
                    print('Ошибка замены файла')

    def save_file(self):
        if self.nameEdit != "" and self.sender() == self.actionSave_File:
            try:
                with open(f'notes/{self.nameEdit.toPlainText()}', "w", encoding="utf-8") as file:
                    plain_text = self.editFile.toPlainText()
                    file.write(plain_text)
            except:
                print('Что-то не то с сохранением')

    def open_file(self):
        if self.sender() == self.actionOpen_File:
            try:
                filename = self.nameEdit.toPlainText()
                if not is_valid_filename(filename):
                    print("Имя файла должно соответствовать шаблонам 'text' или 'text.txt'.")
                if not filename.lower().endswith('.txt'):
                    filename += '.txt'
                with (open(f'notes/{filename}', "r", encoding="utf-8") as file):
                    data = file.read()
                    if (data != self.editFile.toPlainText() and '' != self.editFile.toPlainText() and
                            self.later != self.editFile.toPlainText()):
                        if not ChoiceOpenFile().exec():
                            raise print('Отказ')
                    self.editFile.setPlainText(data)
                    self.later = self.editFile.toPlainText()
                    self.nameEdit.setText(filename)
            except:
                print('Не найден файл')

    def create_file(self):
        if self.sender() == self.actionCreate_File:
            create_file = CreateFile()
            if create_file.exec() == QDialog.DialogCode.Accepted:
                filename, category = create_file.get_input()
                if filename and category:
                    if not is_valid_filename(filename):
                        print("Имя файла должно соответствовать шаблонам 'text' или 'text.txt'.")
                    if not filename.lower().endswith('.txt'):
                        filename += '.txt'
                    print(f"Создан '{filename}' в категории '{category}'.")
                    self.nameEdit.setText(filename)
                    try:
                        with open(f'notes/{filename}', "w", encoding="utf-8"):
                            pass
                    except:
                        print('Что-то не то с сохранением')
                else:
                    print("Имя файла и категория не могут быть пустыми.")

    def delete_file(self):
        if self.sender() == self.actionDelete_File:
            file_name = self.nameEdit.toPlainText()
            file_path = f'notes/{file_name}'
            if not os.path.exists(file_path):
                print(f'Ошибка: Файл "{file_path}" не найден.')
            delete_file = DeleteFile()
            try:
                if delete_file.exec() == QDialog.DialogCode.Accepted:
                    os.remove(file_path)
                    self.nameEdit.setText('')
                    self.editFile.setText('')
                else:
                    print('Файл не удалён')
            except:
                print('Ошибка при удалении')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotepadApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
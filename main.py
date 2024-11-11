import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QListWidget,
                             QMenu, QApplication, QHBoxLayout, QDialog, QSizePolicy)
from PyQt6.QtGui import QAction, QIcon


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
                actionExit_File - Выходит из файла (QAction);
                actionSave_File - Сохраняет файл (QAction);
                actionCreate_File - Создает новый файл (QAction);
                actionDelete_Fire - Удаляет файл (QAction);
                actionFile_info - Вывод информации о файле (QAction)}

                menuView - (QMenu) : 
                menuScale - (QMenu) = {actionDecrease = Уменьшение текста в editFile (QAction);
                actionIncrease = Увеличение текста в editFile (QAction)}
                }'''
        self.setWindowTitle("Блокнот")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/main.png"))

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
        hl_1.addWidget(self.deleteCategory, 2)
        hl_1.addWidget(self.createCategory, 2)

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

        # Добавление действий в меню "Файл"
        self.menuMenu.addAction(self.actionFile_info)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionOpen_File)
        self.menuMenu.addAction(self.actionSave_File)
        self.menuMenu.addAction(self.actionCreate_File)
        self.menuMenu.addAction(self.actionDelete_File)

        wid.setLayout(main_v)

        # Подключение всех кнопок и т.д.
        self.actionFile_info.triggered.connect(self.fileinfo_clicked)

    def fileinfo_clicked(self):
        print("вывод информации о файле")
        dlg = QDialog(self)
        dlg.setWindowIcon(QIcon("assets/info.png"))
        dlg.resize(400, 300)
        dlg.setWindowTitle("Информация о файле")
        dlg.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotepadApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
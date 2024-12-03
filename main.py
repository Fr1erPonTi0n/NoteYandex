import sys

from PyQt6.QtGui import QAction, QPixmap, QIcon
from PyQt6.QtWidgets import (QMainWindow, QWidget, QPushButton, QTextEdit, QComboBox, QListWidget, QMenu,
                             QApplication, QHBoxLayout, QDialogButtonBox, QLineEdit, QDialog, QVBoxLayout, QLabel)
from datetime import datetime
from db_work import Base, OutputBase


class CreateCatalog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.resize(400, 300)
        self.setWindowTitle("Создание категории")
        self.setFixedHeight(100)

        self.qBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(self.qBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.text_input = QLineEdit()
        self.text = QLabel('Введите имя категории')
        self.text_input.setFixedHeight(30)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_input(self):
        return self.text_input.text().strip()


class DeleteCatalog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.resize(400, 300)
        self.setWindowTitle("Удаление категории")
        self.setFixedHeight(100)

        self.qBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(self.qBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.text = QLabel('Вы точно хотите удалить данную категорию и связанные с ней заметки?')
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Error(QDialog):
    def __init__(self, error):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.resize(400, 150)
        self.setWindowTitle("Ошибка")

        self.layout = QVBoxLayout()

        self.error_layout = QHBoxLayout()

        # Add the error image
        self.error_image = QLabel()
        self.error_image.setPixmap(QPixmap("assets/error.png"))
        self.error_image.setFixedSize(64, 64)
        self.error_layout.addSpacing(10)
        self.error_layout.addWidget(self.error_image, 1)

        self.error_layout.addSpacing(20)

        self.message = QLabel(f"Ошибка: {error}")
        self.error_layout.addWidget(self.message, 2)

        self.layout.addLayout(self.error_layout)

        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.accept)
        self.close_button.setFixedHeight(30)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)


class InfoNote(QDialog):
    def __init__(self, notename):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.setFixedSize(400, 300)
        self.setWindowTitle("Информация о заметке")

        note_data = Base().info_notes(notename)
        self.layout = QVBoxLayout()
        self.text1 = QLabel(f'ID Заметки: {note_data[0] if note_data[0] is not None else "неизвестно"}')
        self.text3 = QLabel(f'Имя заметки: {note_data[1] if note_data[1] is not None else "неизвестно"}')
        self.text4 = QLabel(f'Количество строк: {note_data[2] if note_data[2] is not None else "неизвестно"}')
        self.text5 = QLabel(f'Дата создания заметки: {note_data[3] if note_data[3] is not None else "неизвестно"}')
        self.text6 = QLabel(
            F"Запланированный день заметки: {note_data[4] if note_data[4] is not None else 'неизвестно'}")
        self.text7 = QLabel(
            F'Дата последнего изменения заметки: {note_data[5] if note_data[5] is not None else "неизвестно"}')
        self.line = QLabel("<hr>")
        self.text8 = QLabel(F'ID Каталога: {note_data[6] if note_data[6] is not None else "неизвестно"}')
        self.text9 = QLabel(F'Имя каталога: {note_data[7] if note_data[7] is not None else "неизвестно"}')
        self.text10 = QLabel(F'Дата создания каталога: {note_data[8] if note_data[8] is not None else "неизвестно"}')

        self.layout.addWidget(self.text1)
        self.layout.addWidget(self.text3)
        self.layout.addWidget(self.text4)
        self.layout.addWidget(self.text5)
        self.layout.addWidget(self.text6)
        self.layout.addWidget(self.text7)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.text8)
        self.layout.addWidget(self.text9)
        self.layout.addWidget(self.text10)
        self.setLayout(self.layout)


class RenameNote(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.resize(400, 300)
        self.setWindowTitle("Изменение имени заметки")
        self.setFixedHeight(100)

        self.qBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(self.qBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("📝 Введите имя заметки")
        self.text_input.setFixedHeight(30)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_input(self):
        return self.text_input.text().strip()


class SaveNote(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.resize(400, 300)
        self.setWindowTitle('Сохранить заметку')
        self.setFixedHeight(100)

        self.qBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(self.qBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.message = QLabel("Напишите дату реализации вашей заметки, если надо:")
        self.planned_date = QLineEdit()
        self.planned_date.setPlaceholderText("📝 Пример: 12.12.4242")
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.planned_date)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_input(self):
        return self.planned_date.text().strip()


class CreateNote(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.resize(460, 300)
        self.setWindowTitle('Создание заметки')
        self.setFixedHeight(160)

        self.qBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(self.qBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.name_note = QLabel("Имя заметки:")
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('📝 Например: Work Note')
        self.name_catalog = QLabel("Имя категории:")
        self.input_catalog = QLineEdit()
        self.input_catalog.setPlaceholderText("📝 Если тут пусто, то ваша заметка будет привязана к основной категории")

        self.layout.addWidget(self.name_note)
        self.layout.addWidget(self.input_name)
        self.layout.addWidget(self.name_catalog)
        self.layout.addWidget(self.input_catalog)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_input(self):
        return self.input_name.text().strip(), self.input_catalog.text().strip()


class DeleteNote(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/note.png"))
        self.resize(400, 300)
        self.setWindowTitle('Удалить заметку')
        self.setFixedHeight(100)

        self.qBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(self.qBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.message = QLabel("Вы точно хотите удалить заметку?")
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        '''ОБЪЕКТЫ В КОДЕ
                central_widget (QWidget) = {
                createCatalog - Создает категорию (QPushButton);
                deleteCatalog - Удаляет категорию (QPushButton);
                editNote - Изменяет тект в файле (QTextEdit);
                filterNotes - Фильтрация файлов по категориям (QComboBox);
                foundNotes - Находит файл по набранному тексту (QTextEdit);
                listNotes - Список всех файлов по определенным критериям указанных выше (QListWidget);
                nameEdit - Название файла, возможность изменять название файла (QTextEdit)
                }

                menubar - (QMenuBar) = {
                menuMenu - (QMenu) = {actionOpen_Note - Открывает файл (QAction);
                actionSave_Note - Сохраняет файл (QAction);
                actionCreate_Note - Создает новый файл (QAction);
                actionDelete_Fire - Удаляет файл (QAction);
                actionNote_info - Вывод информации о файле (QAction)}
                }'''
        self.setWindowTitle("Блокнот")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/note.png"))
        self.later = ""

        # Элементы управления
        self.createCatalog = QPushButton("Создать категорию")
        self.createCatalog.setFixedHeight(30)
        self.deleteCatalog = QPushButton("Удалить категорию")
        self.deleteCatalog.setFixedHeight(30)
        self.editNote = QTextEdit()
        self.editNote.setPlaceholderText("📝 Здесь текст заметки, если тут пусто, то заметка является пустой")
        self.filterNotes = QComboBox()
        self.filterNotes.setFixedHeight(30)
        self.foundNotes = QLineEdit()
        self.foundNotes.setFixedHeight(30)
        self.foundNotes.setPlaceholderText("📝 Введите имя для поиска заметки")
        self.listNotes = QListWidget()
        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText("📝 Здесь имя заметки")
        self.nameEdit.setFixedHeight(30)

        # Центральный виджет
        wid = QWidget()
        self.setCentralWidget(wid)

        # Основной макет
        hl_1 = QHBoxLayout()
        hl_2 = QHBoxLayout()
        hl_3 = QHBoxLayout()
        main_v = QVBoxLayout()

        hl_1.addWidget(self.filterNotes, 2)
        hl_1.addWidget(self.createCatalog, 2)
        hl_1.addWidget(self.deleteCatalog, 2)

        hl_2.addWidget(self.foundNotes, 2)
        hl_2.addWidget(self.nameEdit, 4)

        hl_3.addWidget(self.listNotes, 2)
        hl_3.addWidget(self.editNote, 4)

        # Добавление элементов в макет
        main_v.addLayout(hl_1)
        main_v.addLayout(hl_2)
        main_v.addLayout(hl_3)

        # Создание меню
        self.menubar = self.menuBar()

        # Меню "Файл"
        self.menuMenu = QMenu("Работа с заметкой", self)
        self.menubar.addMenu(self.menuMenu)

        # Действия для меню "Файл"
        self.actionOpen_Note = QAction("Открыть заметку", self)
        self.actionSave_Note = QAction("Сохранить заметку", self)
        self.actionCreate_Note = QAction("Создать новую заметку", self)
        self.actionDelete_Note = QAction("Удалить заметку", self)
        self.actionNote_info = QAction("Информация о заметке", self)
        self.actionRename_Note = QAction("Изменить имя заметки", self)
        self.actionBase_info = QAction("Информация о базе", self)

        # Добавление действий в меню "Файл"
        self.menuMenu.addAction(self.actionNote_info)
        self.menuMenu.addAction(self.actionRename_Note)
        self.menuMenu.addAction(self.actionBase_info)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionOpen_Note)
        self.menuMenu.addAction(self.actionSave_Note)
        self.menuMenu.addAction(self.actionCreate_Note)
        self.menuMenu.addAction(self.actionDelete_Note)

        wid.setLayout(main_v)

        # Подключение всех кнопок и т.д.
        self.actionNote_info.triggered.connect(self.noteinfo)
        self.actionRename_Note.triggered.connect(self.rename_note)
        self.actionSave_Note.triggered.connect(self.save_note)
        self.actionOpen_Note.triggered.connect(self.open_note)
        self.actionCreate_Note.triggered.connect(self.create_note)
        self.actionDelete_Note.triggered.connect(self.delete_note)
        self.actionBase_info.triggered.connect(self.output_base)

        self.filterNotes.currentIndexChanged.connect(self.update_list_notes)
        self.listNotes.currentItemChanged.connect(self.update_edit_and_name_note)
        self.listNotes.itemDoubleClicked.connect(self.update_edit_and_name_note)
        self.foundNotes.textChanged.connect(self.filter_notes)
        self.createCatalog.clicked.connect(self.create_and_delete_catalog)
        self.deleteCatalog.clicked.connect(self.create_and_delete_catalog)

        self.update_catalogs()

    def noteinfo(self):
        """Здесь осуществляется вывод всей информации по поводу заметки. Вся эта информация выводиться в отдельном окне.
        """
        if self.sender() == self.actionNote_info:
            try:
                print("Вывод информации о заметке")
                notename = self.nameEdit.text()
                if notename is None:
                    raise Exception
                InfoNote(notename).exec()
            except Exception:
                Error(f'При открытии информации о заметке').exec()
        Base().close_base()
        print("Вывод информации о заметки")

    def rename_note(self):
        """Здесь осуществляется изменение имени заметки.
        Выводится окно в котором, надо написать новое имя заметки и нужно после этого подвердить изменение.
        """
        if self.sender() == self.actionRename_Note:
            try:
                if self.nameEdit.text() == '':
                    raise Exception
                rename = RenameNote()
                if rename.exec():
                    last_name = self.nameEdit.text()
                    new_name = rename.get_input()
                    if last_name is not None:
                        Base().rename_note(last_name, new_name)
                        self.nameEdit.setText(new_name)
                    else:
                        raise Exception
            except Exception:
                Error('При изменении имени заметки').exec()
            self.update_list_notes()
        Base().close_base()
        print("Изменение имени заметки")

    def save_note(self):
        """Здесь осуществляется сохранение заметки. Выводитья специальное окно в котором можно указать дату
        реализации для этой заметки."""
        if self.nameEdit.text() != "" and self.sender() == self.actionSave_Note:
            notename = self.nameEdit.text()
            text = self.editNote.toPlainText()
            count_line = len(self.editNote.toPlainText().splitlines())
            id_catalog = self.filterNotes.currentData()
            savenote = SaveNote()
            if savenote.exec() == QDialog.DialogCode.Accepted:
                planned_date = savenote.get_input()
                is_valid_date = True
                if planned_date:
                    try:
                        datetime.strptime(planned_date, "%d.%m.%Y")
                    except Exception:
                        is_valid_date = False
                if is_valid_date:
                    Base().save_note(notename, text, planned_date, count_line, id_catalog)
                else:
                    Error('Неверна указана дата').exec()
        Base().close_base()
        self.update_catalogs()
        print('Сохранение заметки')

    def open_note(self):
        """Здесь осуществляется открытие заметки по имени заметки."""
        if self.sender() == self.actionOpen_Note:
            try:
                namenote = self.nameEdit.text().strip()
                note_text = Base().get_note_text(namenote)
                self.editNote.setPlainText(note_text)
            except Exception:
                Error('Не введено имя заметки').exec()
        Base().close_base()

    def create_note(self):
        """Здесь осуществляется создание заметки с указанием имени и каталога. Специальное окно выводиться для этого."""
        if self.sender() == self.actionCreate_Note:
            createnote = CreateNote()
            if createnote.exec() == QDialog.DialogCode.Accepted:
                notename, catalog = createnote.get_input()
                if notename == '' or notename is None:
                    Error("Произошёл сбой при создания заметки.").exec()
                    return
                base = Base().create_note(notename, catalog)
                if base is Exception:
                    Error("Произошёл сбой при создания заметки.").exec()
                    return
                print(f"Создана заметка '{notename}' в категории '{catalog}'.")
                self.nameEdit.setText(notename)
                self.editNote.setText('')
                self.update_catalogs()
        Base().close_base()

    def delete_note(self):
        """Здесь осуществляется удаление заметки. Выводиться специальное диалоговое окно для подтверждение удаления."""
        if self.sender() == self.actionDelete_Note:
            note_name = self.nameEdit.text()
            deletenote = DeleteNote()
            try:
                if deletenote.exec() == QDialog.DialogCode.Accepted:
                    Base().delete_note(note_name)
                    self.nameEdit.setText('')
                    self.editNote.setText('')
                    self.update_catalogs()
            except Exception:
                Error('При удалении заметки').exec()
        Base().close_base()
        print('Удаление заметки')

    @staticmethod
    def output_base():
        """Здесь осуществляется вывод двух таблиц из базы данных."""
        OutputBase().exec()

    def update_catalogs(self):
        """Здесь осуществляется обновление всех категории, довабляя функцию "все категории". """
        self.filterNotes.clear()
        self.filterNotes.addItem('Все категории')
        catalogs = Base().load_catalogs()
        for catalog in catalogs:
            self.filterNotes.addItem(catalog[1], catalog[0])
        Base().close_base()

    def update_list_notes(self):
        """Здесь осуществляется обновление списка заметок."""
        self.listNotes.clear()
        catalog_id = self.filterNotes.currentData()
        if catalog_id != 'Все категорий':
            notes_names = Base().list_notes_by_catalog(catalog_id)
        else:
            notes_names = Base().list_notes_by_catalog(None)
        for name in notes_names:
            self.listNotes.addItem(name)
        Base().close_base()

    def update_edit_and_name_note(self, current_item):
        """Здесь обрабатывают нажатие на заметку в списке файлов. При нажатии на объект: поле для ввода текста
        присваивает значение текста этой заметки, а также имя заметки присваивает значение имени этой заметки."""
        try:
            note_name = current_item.text()
            self.nameEdit.setText(note_name)
            note_text = Base().get_note_text(note_name)
            self.editNote.setPlainText(note_text)
        except Exception:
            self.nameEdit.setText('')
            self.editNote.setPlainText('')
        Base().close_base()

    def filter_notes(self):
        """Здесь идет поиск всех заметок похожих на текст, введеный в поиске заметок. Обновляет список заметок."""
        search_text = self.foundNotes.text().lower()
        self.listNotes.clear()
        all_notes = Base().get_all_notes()
        filtered_notes = [note for note in all_notes if search_text in note.lower()]
        for note in filtered_notes:
            self.listNotes.addItem(note)
        Base().close_base()

    def create_and_delete_catalog(self):
        """Здесь осуществляется удаление и создание категории. Специальное окно выводиться для этого."""
        if self.sender() == self.deleteCatalog:
            try:
                deletecatalog = DeleteCatalog()
                namenote = self.nameEdit.text()
                if deletecatalog.exec() == QDialog.DialogCode.Accepted:
                    namecatalog = self.filterNotes.currentText().strip()
                    if namecatalog is None or self.filterNotes.currentData() == 1:
                        raise Exception
                    n = Base().delete_catalog(namecatalog, namenote)
                    if n:
                        self.nameEdit.setText('')
                        self.editNote.setText('')
                    self.update_catalogs()
            except Exception:
                Error('При удалении категорий').exec()
            print('Удаление категории')
        elif self.sender() == self.createCatalog:
            try:
                createcatalog = CreateCatalog()
                if createcatalog.exec() == QDialog.DialogCode.Accepted:
                    namecatalog = createcatalog.get_input().strip()
                    if not namecatalog:
                        raise Exception
                    Base().create_catalog(namecatalog)
                    self.update_catalogs()
            except Exception:
                Error('При создания категорий').exec()
            print('Создание категории')
        Base().close_base()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotepadApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

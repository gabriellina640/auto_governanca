from __future__ import annotations

import platform
import subprocess
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.config_service import ConfigService
from app.services.excel_service import ExcelService, ExcelServiceError


class MainWindow(QMainWindow):
    def __init__(self, config_service: ConfigService) -> None:
        super().__init__()
        self.config_service = config_service
        self.excel = ExcelService(self.config_service.config)
        self.form_inputs: dict[str, QLineEdit] = {}

        self.setWindowTitle(self.config_service.get("app_name", "Cadastro Inteligente Excel"))
        self.resize(1360, 800)

        self._build_ui()
        self._load_last_file_if_exists()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(10)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        self.title = QLabel("Cadastro Inteligente Excel")
        self.title.setObjectName("TitleLabel")
        self.subtitle = QLabel("Cadastre, consulte e mantenha seus registros atualizados")
        self.subtitle.setObjectName("SubtitleLabel")
        title_box.addWidget(self.title)
        title_box.addWidget(self.subtitle)
        header.addLayout(title_box)
        header.addStretch()

        self.status_label = QLabel("Nenhuma planilha carregada")
        self.status_label.setObjectName("StatusWarn")
        header.addWidget(self.status_label)
        root_layout.addLayout(header)

        actions_card = QFrame()
        actions_card.setObjectName("Card")
        actions_layout = QHBoxLayout(actions_card)
        actions_layout.setContentsMargins(14, 12, 14, 12)

        self.select_btn = QPushButton("Selecionar planilha")
        self.refresh_btn = QPushButton("Atualizar")
        self.save_btn = QPushButton("Salvar")
        self.open_folder_btn = QPushButton("Abrir pasta")
        for btn in [self.refresh_btn, self.save_btn, self.open_folder_btn]:
            btn.setObjectName("SecondaryButton")

        self.select_btn.clicked.connect(self.select_file)
        self.refresh_btn.clicked.connect(self.refresh_file)
        self.save_btn.clicked.connect(self.save_file)
        self.open_folder_btn.clicked.connect(self.open_folder)

        actions_layout.addWidget(self.select_btn)
        actions_layout.addWidget(self.refresh_btn)
        actions_layout.addWidget(self.save_btn)
        actions_layout.addWidget(self.open_folder_btn)
        actions_layout.addStretch()

        self.file_label = QLabel("Arquivo: —")
        self.file_label.setObjectName("SubtitleLabel")
        actions_layout.addWidget(self.file_label)
        root_layout.addWidget(actions_card)

        splitter = QSplitter(Qt.Horizontal)

        table_card = QFrame()
        table_card.setObjectName("Card")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(12, 12, 12, 12)
        table_title = QLabel("Registros")
        table_title.setObjectName("SectionTitle")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar na tabela...")
        self.search_input.textChanged.connect(self.apply_filter)
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setDefaultSectionSize(150)
        self.table.horizontalHeader().setStretchLastSection(True)
        table_layout.addWidget(table_title)
        table_layout.addWidget(self.search_input)
        table_layout.addWidget(self.table)

        form_card = QFrame()
        form_card.setObjectName("FormCard")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_title = QLabel("Novo registro")
        form_title.setObjectName("SectionTitle")
        form_layout.addWidget(form_title)

        self.form_scroll = QScrollArea()
        self.form_scroll.setObjectName("FormScroll")
        self.form_scroll.setWidgetResizable(True)
        self.form_widget = QWidget()
        self.form_widget.setObjectName("FormBody")
        self.form_grid = QGridLayout(self.form_widget)
        self.form_grid.setContentsMargins(0, 8, 0, 8)
        self.form_grid.setHorizontalSpacing(10)
        self.form_grid.setVerticalSpacing(12)
        self.form_scroll.setWidget(self.form_widget)
        form_layout.addWidget(self.form_scroll)

        self.add_btn = QPushButton("Incluir registro")
        self.add_btn.clicked.connect(self.add_record)
        form_layout.addWidget(self.add_btn)

        splitter.addWidget(table_card)
        splitter.addWidget(form_card)
        splitter.setSizes([1040, 320])
        root_layout.addWidget(splitter)

        self.footer = QLabel("Selecione uma planilha .xlsx para começar.")
        self.footer.setObjectName("SubtitleLabel")
        root_layout.addWidget(self.footer)

        self.setCentralWidget(root)
        self._set_enabled(False)

    def _set_enabled(self, enabled: bool) -> None:
        self.refresh_btn.setEnabled(enabled)
        self.save_btn.setEnabled(enabled)
        self.open_folder_btn.setEnabled(enabled)
        self.add_btn.setEnabled(enabled)
        self.search_input.setEnabled(enabled)

    def _load_last_file_if_exists(self) -> None:
        path = self.config_service.get("excel_path", "")
        if path and Path(path).exists():
            self.load_file(path)

    def select_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar planilha",
            str(Path.home()),
            "Excel (*.xlsx)",
        )
        if path:
            self.config_service.set("excel_path", path)
            self.load_file(path)

    def load_file(self, path: str) -> None:
        try:
            self.excel = ExcelService(self.config_service.config)
            self.excel.load(path)
            self.populate_table()
            self.build_form()
            self._set_enabled(True)
            self.status_label.setText("Planilha carregada")
            self.status_label.setObjectName("StatusOk")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)
            self.file_label.setText(f"Arquivo: {Path(path).name}")
            self.footer.setText(str(Path(path)))
        except ExcelServiceError as exc:
            self.show_error(str(exc))

    def refresh_file(self) -> None:
        path = self.config_service.get("excel_path", "")
        if path:
            self.load_file(path)
            self.show_info("Planilha atualizada.")

    def populate_table(self) -> None:
        rows = self.excel.get_visible_rows()
        headers = self.excel.get_visible_headers()
        self.table.setSortingEnabled(False)
        self.table.clear()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem("" if value is None else str(value))
                self.table.setItem(r, c, item)

        self.table.resizeColumnsToContents()
        for col in range(self.table.columnCount()):
            width = self.table.columnWidth(col)
            self.table.setColumnWidth(col, min(max(width, 120), 240))
        self.table.setSortingEnabled(True)

    def build_form(self) -> None:
        while self.form_grid.count():
            item = self.form_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.form_inputs = {}
        required = set(self.config_service.get("required_fields", []))
        headers = self.excel.get_form_headers()
        for row, header in enumerate(headers):
            label_text = f"{header} *" if header in required else header
            label = QLabel(label_text)
            label.setObjectName("FieldLabel")
            field = QLineEdit()
            field.setPlaceholderText(f"Digite {header}")
            field.setMinimumHeight(40)
            self.form_grid.addWidget(label, row, 0)
            self.form_grid.addWidget(field, row, 1)
            self.form_inputs[header] = field
        self.form_grid.setRowStretch(len(headers), 1)

    def add_record(self) -> None:
        if self.excel.has_external_change():
            answer = self.ask_question(
                "Arquivo alterado",
                "A planilha foi alterada desde a última leitura. Deseja atualizar antes de incluir?",
            )
            if answer == QMessageBox.Yes:
                self.refresh_file()
                return

        values = {header: field.text().strip() for header, field in self.form_inputs.items()}
        visible_required = [h for h in self.config_service.get("required_fields", []) if h in self.form_inputs]
        missing = [h for h in visible_required if not values.get(h)]
        if missing:
            self.show_error("Preencha os campos obrigatórios: " + ", ".join(missing))
            return

        try:
            self.excel.add_record(values)
            self.excel.save()
            self.populate_table()
            for field in self.form_inputs.values():
                field.clear()
            self.show_info("Registro incluído e arquivo salvo.")
        except ExcelServiceError as exc:
            self.show_error(str(exc))

    def save_file(self) -> None:
        if self.excel.has_external_change():
            answer = self.ask_question(
                "Arquivo alterado",
                "Existe uma versão mais recente no disco. Salvar agora pode sobrescrever mudanças. Deseja continuar?",
            )
            if answer != QMessageBox.Yes:
                return
        try:
            self.excel.save()
            self.show_info("Arquivo salvo com sucesso.")
        except ExcelServiceError as exc:
            self.show_error(str(exc))

    def apply_filter(self, text: str) -> None:
        text = text.strip().lower()
        for row in range(self.table.rowCount()):
            visible = not text
            if text:
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item and text in item.text().lower():
                        visible = True
                        break
            self.table.setRowHidden(row, not visible)

    def open_folder(self) -> None:
        path = self.config_service.get("excel_path", "")
        if not path:
            return
        folder = Path(path).parent
        system = platform.system()
        if system == "Windows":
            subprocess.Popen(["explorer", str(folder)])
        elif system == "Darwin":
            subprocess.Popen(["open", str(folder)])
        else:
            subprocess.Popen(["xdg-open", str(folder)])

    def show_error(self, message: str) -> None:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle("Erro")
        box.setText(message)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()

    def show_info(self, message: str) -> None:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle("Tudo certo")
        box.setText(message)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()

    def ask_question(self, title: str, message: str) -> QMessageBox.StandardButton:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle(title)
        box.setText(message)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        return box.exec()

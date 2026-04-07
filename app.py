import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit,
    QPushButton, QMessageBox, QHBoxLayout, QFrame, QSizePolicy
)
from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtCore import Qt


eng_to_th = {
    '`': '_', '~': '%',
    '1': 'ๅ', '!': '+',
    '2': '/', '@': '๑',
    '3': '-', '#': '๒',
    '4': 'ภ', '$': '๓',
    '5': 'ถ', '%': '๔',
    '6': 'ุ', '^': 'ู',
    '7': 'ึ', '&': '฿',
    '8': 'ค', '*': '๕',
    '9': 'ต', '(': '๖',
    '0': 'จ', ')': '๗',
    '-': 'ข', '_': '๘',
    '=': 'ช', '+': '๙',

    'q': 'ๆ', 'Q': '๐',
    'w': 'ไ', 'W': '"',
    'e': 'ำ', 'E': 'ฎ',
    'r': 'พ', 'R': 'ฑ',
    't': 'ะ', 'T': 'ธ',
    'y': 'ั', 'Y': 'ํ',
    'u': 'ี', 'U': '๊',
    'i': 'ร', 'I': 'ณ',
    'o': 'น', 'O': 'ฯ',
    'p': 'ย', 'P': 'ญ',
    '[': 'บ', '{': 'ฐ',
    ']': 'ล', '}': ',',
    '\\': 'ฃ', '|': 'ฅ',

    'a': 'ฟ', 'A': 'ฤ',
    's': 'ห', 'S': 'ฆ',
    'd': 'ก', 'D': 'ฏ',
    'f': 'ด', 'F': 'โ',
    'g': 'เ', 'G': 'ฌ',
    'h': '้', 'H': '็',
    'j': '่', 'J': '๋',
    'k': 'า', 'K': 'ษ',
    'l': 'ส', 'L': 'ศ',
    ';': 'ว', ':': 'ซ',
    "'": 'ง', '"': '.',

    'z': 'ผ', 'Z': '(',
    'x': 'ป', 'X': ')',
    'c': 'แ', 'C': 'ฉ',
    'v': 'อ', 'V': 'ฮ',
    'b': 'ิ', 'B': 'ฺ',
    'n': 'ื', 'N': '์',
    'm': 'ท', 'M': '?',
    ',': 'ม', '<': 'ฒ',
    '.': 'ใ', '>': 'ฬ',
    '/': 'ฝ', '?': 'ฦ',
}

th_to_eng = {v: k for k, v in eng_to_th.items()}


def count_english_chars(text):
    return sum(1 for ch in text if ch in eng_to_th)


def count_thai_chars(text):
    return sum(1 for ch in text if ch in th_to_eng)


def convert_eng_to_th(text):
    return ''.join(eng_to_th.get(ch, ch) for ch in text)


def convert_th_to_eng(text):
    return ''.join(th_to_eng.get(ch, ch) for ch in text)


def detect_direction(text):
    eng_count = count_english_chars(text)
    thai_count = count_thai_chars(text)

    if eng_count == 0 and thai_count == 0:
        return "eng_to_th"
    if eng_count >= thai_count:
        return "eng_to_th"
    return "th_to_eng"


class InputTextEdit(QTextEdit):
    def __init__(self, convert_callback, parent=None):
        super().__init__(parent)
        self.convert_callback = convert_callback

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and (
            event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier
        ):
            self.convert_callback()
            return
        super().keyPressEvent(event)


class LanguageConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.force_mode = "auto"   # auto / eng_to_th / th_to_eng
        self.setWindowTitle("Right Language")
        self.resize(920, 680)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(16)

        title = QLabel("Right Language")
        title.setObjectName("Title")

        subtitle = QLabel("แปลงข้อความที่พิมพ์ผิดภาษาให้กลับมาเป็น layout ที่ถูกต้อง")
        subtitle.setObjectName("Subtitle")

        self.mode_badge = QLabel("Auto Detect")
        self.mode_badge.setObjectName("ModeBadge")
        self.mode_badge.setAlignment(Qt.AlignCenter)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(6)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addWidget(self.mode_badge, alignment=Qt.AlignLeft)

        main_layout.addLayout(header_layout)

        self.input_box = InputTextEdit(self.convert_text)
        self.input_box.setPlaceholderText("พิมพ์หรือวางข้อความที่นี่...")
        self.input_box.setObjectName("Editor")
        self.input_box.setMinimumHeight(190)

        self.output_box = QTextEdit()
        self.output_box.setPlaceholderText("ผลลัพธ์จะแสดงที่นี่...")
        self.output_box.setReadOnly(True)
        self.output_box.setObjectName("Editor")
        self.output_box.setMinimumHeight(190)

        self.input_card = self.make_card("Input", self.input_box)
        self.output_card = self.make_card("Output", self.output_box)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        self.convert_btn = self.make_button("Convert", primary=True)
        self.convert_btn.clicked.connect(self.convert_text)

        self.switch_btn = self.make_button("Switch Mode")
        self.switch_btn.clicked.connect(self.toggle_mode)

        self.paste_btn = self.make_button("Paste")
        self.paste_btn.clicked.connect(self.paste_text)

        self.copy_btn = self.make_button("Copy")
        self.copy_btn.clicked.connect(self.copy_result)

        self.clear_btn = self.make_button("Clear")
        self.clear_btn.clicked.connect(self.clear_text)

        button_row.addWidget(self.convert_btn)
        button_row.addWidget(self.switch_btn)
        button_row.addWidget(self.paste_btn)
        button_row.addWidget(self.copy_btn)
        button_row.addWidget(self.clear_btn)

        hint = QLabel("Tip: ใช้ Cmd + Enter หรือ Ctrl + Enter เพื่อแปลงทันที")
        hint.setObjectName("Hint")

        main_layout.addWidget(self.input_card)
        main_layout.addLayout(button_row)
        main_layout.addWidget(self.output_card)
        main_layout.addWidget(hint)

        self.setLayout(main_layout)
        self.input_box.textChanged.connect(self.auto_convert)
        self.apply_styles()
        self.update_mode_badge()

    def make_card(self, title_text, widget):
        card = QFrame()
        card.setObjectName("Card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("CardTitle")

        card_layout.addWidget(title)
        card_layout.addWidget(widget)
        card.setLayout(card_layout)
        return card

    def make_button(self, text, primary=False):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setProperty("primary", primary)
        return btn

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                color: #1e293b;
                font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
                font-size: 14px;
            }

            QLabel#Title {
                font-size: 30px;
                font-weight: 700;
                color: #0f172a;
            }

            QLabel#Subtitle {
                font-size: 14px;
                color: #64748b;
            }

            QLabel#ModeBadge {
                background-color: #eff6ff;
                color: #2563eb;
                border: 1px solid #bfdbfe;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 600;
                min-width: 120px;
                max-width: 220px;
            }

            QLabel#CardTitle {
                font-size: 13px;
                font-weight: 700;
                color: #475569;
                padding-bottom: 2px;
            }

            QLabel#Hint {
                color: #94a3b8;
                font-size: 12px;
                padding-left: 2px;
            }

            QFrame#Card {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
            }

            QTextEdit#Editor {
                background-color: transparent;
                border: none;
                color: #0f172a;
                font-size: 16px;
                padding: 4px 2px 4px 2px;
                selection-background-color: #bfdbfe;
            }

            QPushButton {
                background-color: #ffffff;
                color: #334155;
                border: 1px solid #dbe3ee;
                border-radius: 14px;
                padding: 12px 18px;
                font-size: 13px;
                font-weight: 600;
                min-width: 100px;
            }

            QPushButton:hover {
                background-color: #f8fbff;
                border: 1px solid #cbd5e1;
            }

            QPushButton[primary="true"] {
                background-color: #4da3ff;
                color: white;
                border: 1px solid #4da3ff;
            }

            QPushButton[primary="true"]:hover {
                background-color: #3696fb;
                border: 1px solid #3696fb;
            }

            QPushButton[primary="true"]:pressed {
                background-color: #2388f5;
                border: 1px solid #2388f5;
            }
        """)

    def update_mode_badge(self):
        if self.force_mode == "auto":
            self.mode_badge.setText("Auto Detect")
        elif self.force_mode == "eng_to_th":
            self.mode_badge.setText("English → Thai")
        else:
            self.mode_badge.setText("Thai → English")

    def toggle_mode(self):
        if self.force_mode == "auto":
            self.force_mode = "eng_to_th"
        elif self.force_mode == "eng_to_th":
            self.force_mode = "th_to_eng"
        else:
            self.force_mode = "auto"

        self.update_mode_badge()
        self.convert_text()

    def paste_text(self):
        clipboard = QApplication.clipboard()
        self.input_box.setPlainText(clipboard.text())

    def copy_result(self):
        result = self.output_box.toPlainText().strip()
        if not result:
            QMessageBox.information(self, "แจ้งเตือน", "ยังไม่มีผลลัพธ์ให้คัดลอก")
            return
        QApplication.clipboard().setText(result)
        QMessageBox.information(self, "สำเร็จ", "คัดลอกผลลัพธ์แล้ว")

    def clear_text(self):
        self.input_box.blockSignals(True)
        self.output_box.blockSignals(True)
        self.input_box.clear()
        self.output_box.clear()
        self.input_box.blockSignals(False)
        self.output_box.blockSignals(False)
        self.update_mode_badge()

    def auto_convert(self):
        self.convert_text(silent=True)

    def convert_text(self, silent=False):
        text = self.input_box.toPlainText()

        if not text.strip():
            self.output_box.clear()
            self.update_mode_badge()
            return

        if self.force_mode == "auto":
            direction = detect_direction(text)
        else:
            direction = self.force_mode

        if direction == "eng_to_th":
            result = convert_eng_to_th(text)
            if self.force_mode == "auto":
                self.mode_badge.setText("Auto • English → Thai")
        else:
            result = convert_th_to_eng(text)
            if self.force_mode == "auto":
                self.mode_badge.setText("Auto • Thai → English")

        self.output_box.setPlainText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 13))
    window = LanguageConverterApp()
    window.show()
    sys.exit(app.exec())
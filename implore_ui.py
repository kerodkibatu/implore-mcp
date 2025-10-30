"""
Implore UI - Clean, intuitive quiz interface for collecting user input.
"""

import sys
import json
import argparse
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup, QTextEdit, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class QuizWidget(QWidget):
    def __init__(self, questions, title):
        super().__init__()
        self.questions = questions
        self.title = title
        self.answers = {}
        self.question_widgets = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(self.title)
        self.setMinimumSize(700, 550)
        self.resize(900, 700)
        
        # Apply theme
        self.setStyleSheet("""
            QWidget {
                background-color: #09090b;
                color: #fafafa;
                font-family: "Segoe UI", sans-serif;
            }
            
            QLabel#title {
                font-size: 26px;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 4px;
            }
            
            QLabel#subtitle {
                font-size: 15px;
                color: #a1a1aa;
                margin-bottom: 32px;
            }
            
            QLabel#question_number {
                font-size: 13px;
                font-weight: 600;
                color: #71717a;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            QLabel#question_text {
                font-size: 15px;
                font-weight: 500;
                color: #fafafa;
                line-height: 1.5;
            }
            
            QFrame#questionCard {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 12px;
            }
            
            QRadioButton {
                spacing: 12px;
                padding: 14px 16px;
                margin: 4px 0px;
                background-color: transparent;
                border: 1px solid #27272a;
                border-radius: 8px;
                color: #fafafa;
                font-size: 14px;
            }
            
            QRadioButton:hover {
                background-color: #27272a;
                border-color: #3f3f46;
            }
            
            QRadioButton:checked {
                background-color: #18181b;
                border-color: #52525b;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #52525b;
                background-color: transparent;
            }
            
            QRadioButton::indicator:checked {
                background-color: #fafafa;
                border-color: #fafafa;
            }
            
            QTextEdit {
                background-color: #09090b;
                border: 1px solid #27272a;
                border-radius: 8px;
                padding: 14px;
                font-size: 14px;
                color: #fafafa;
                min-height: 100px;
            }
            
            QTextEdit:focus {
                border-color: #52525b;
                background-color: #0c0c0e;
            }
            
            QPushButton {
                padding: 11px 20px;
                border-radius: 8px;
                font-weight: 500;
                font-size: 14px;
                border: none;
            }
            
            QPushButton#submit {
                background-color: #fafafa;
                color: #09090b;
                min-width: 110px;
                font-weight: 600;
            }
            
            QPushButton#submit:hover {
                background-color: #e4e4e7;
            }
            
            QPushButton#cancel {
                background-color: #18181b;
                color: #fafafa;
                border: 1px solid #27272a;
            }
            
            QPushButton#cancel:hover {
                background-color: #27272a;
            }
            
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QScrollBar:vertical {
                background: transparent;
                width: 10px;
            }
            
            QScrollBar::handle:vertical {
                background: #27272a;
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #3f3f46;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)
        
        # Header section
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        title_label = QLabel(self.title)
        title_label.setObjectName("title")
        header_layout.addWidget(title_label)
        
        question_count = len(self.questions)
        subtitle_text = f"{question_count} question" + ("s" if question_count != 1 else "")
        subtitle_label = QLabel(subtitle_text)
        subtitle_label.setObjectName("subtitle")
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_widget)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)
        
        # Add all questions
        for i, question in enumerate(self.questions):
            question_widget = self.create_question_card(i + 1, question)
            content_layout.addWidget(question_widget)
            self.question_widgets.append(question_widget)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)
        
        # Footer with action buttons
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 20, 0, 0)
        footer_layout.setSpacing(10)
        footer_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancel")
        cancel_button.clicked.connect(self.on_cancel)
        cancel_button.setCursor(Qt.PointingHandCursor)
        footer_layout.addWidget(cancel_button)
        
        submit_button = QPushButton("Submit")
        submit_button.setObjectName("submit")
        submit_button.setDefault(True)
        submit_button.clicked.connect(self.on_submit)
        submit_button.setCursor(Qt.PointingHandCursor)
        footer_layout.addWidget(submit_button)
        
        main_layout.addLayout(footer_layout)
        self.setLayout(main_layout)
    
    def create_question_card(self, number, question):
        """Create a card widget for a single question."""
        q_id = question['id']
        q_type = question['type']
        q_text = question['text']
        
        # Card container
        card = QFrame()
        card.setObjectName("questionCard")
        card.question_id = q_id
        card.question_type = q_type
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)
        
        # Question number
        number_label = QLabel(f"Question {number}")
        number_label.setObjectName("question_number")
        card_layout.addWidget(number_label)
        
        # Question text
        text_label = QLabel(q_text)
        text_label.setObjectName("question_text")
        text_label.setWordWrap(True)
        card_layout.addWidget(text_label)
        
        # Input area based on question type
        if q_type == "multiple_choice":
            options = question.get('options', [])
            button_group = QButtonGroup(card)
            button_group.setExclusive(True)
            
            options_layout = QVBoxLayout()
            options_layout.setSpacing(8)
            options_layout.setContentsMargins(0, 8, 0, 0)
            
            for option in options:
                radio = QRadioButton(option)
                radio.setCursor(Qt.PointingHandCursor)
                button_group.addButton(radio)
                options_layout.addWidget(radio)
            
            card_layout.addLayout(options_layout)
            card.button_group = button_group
            
        elif q_type == "free_form":
            text_input = QTextEdit()
            text_input.setPlaceholderText("Type your answer here...")
            card_layout.addWidget(text_input)
            card.text_widget = text_input
        
        return card
    
    def collect_answers(self):
        """Collect all answers from question widgets."""
        answers = {}
        
        for widget in self.question_widgets:
            q_id = widget.question_id
            q_type = widget.question_type
            
            if q_type == "multiple_choice":
                checked_button = widget.button_group.checkedButton()
                answers[q_id] = checked_button.text() if checked_button else None
            elif q_type == "free_form":
                text = widget.text_widget.toPlainText().strip()
                answers[q_id] = text if text else ""
        
        return answers
    
    def on_submit(self):
        """Handle submit button click."""
        self.answers = self.collect_answers()
        self.accept_result = True
        self.close()
    
    def on_cancel(self):
        """Handle cancel button click."""
        self.accept_result = False
        self.close()


def main():
    parser = argparse.ArgumentParser(description="Quiz interface for user input")
    parser.add_argument("--questions", required=True, help="JSON string of questions")
    parser.add_argument("--title", required=True, help="Window title")
    parser.add_argument("--output-file", required=True, help="Output JSON file")
    
    args = parser.parse_args()
    
    try:
        questions = json.loads(args.questions)
    except json.JSONDecodeError as e:
        result = {"success": False, "error": f"Invalid JSON: {e}"}
        with open(args.output_file, 'w') as f:
            json.dump(result, f)
        sys.exit(1)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    quiz = QuizWidget(questions, args.title)
    quiz.accept_result = False
    quiz.show()
    
    app.exec()
    
    result = {
        "success": quiz.accept_result,
        "answers": quiz.answers if quiz.accept_result else {}
    }
    
    with open(args.output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    sys.exit(0 if quiz.accept_result else 1)


if __name__ == "__main__":
    main()

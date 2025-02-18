import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit,
                            QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
from qt_material import apply_stylesheet
from input_simulator import InputSimulator
import time

class InputSimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulator = InputSimulator()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('输入模拟器')
        self.setMinimumSize(600, 400)
        
        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 文本输入区域
        text_group = QGroupBox("文本输入设置")
        text_layout = QVBoxLayout()
        
        # 输入文本
        input_layout = QHBoxLayout()
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("请输入要模拟的文本...")
        input_layout.addWidget(self.text_input)
        text_layout.addLayout(input_layout)
        
        # 输入模式选择
        mode_layout = QHBoxLayout()
        mode_label = QLabel("输入模式:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["固定间隔", "随机间隔"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        
        # 间隔设置
        interval_label = QLabel("间隔(秒):")
        self.interval_spin = QDoubleSpinBox()
        self.interval_spin.setRange(0.01, 10.0)
        self.interval_spin.setValue(0.1)
        self.interval_spin.setSingleStep(0.1)
        mode_layout.addWidget(interval_label)
        mode_layout.addWidget(self.interval_spin)
        
        # 随机间隔范围
        self.random_min_label = QLabel("最小间隔:")
        self.random_min_spin = QDoubleSpinBox()
        self.random_min_spin.setRange(0.01, 10.0)
        self.random_min_spin.setValue(0.1)
        self.random_min_spin.setSingleStep(0.1)
        self.random_max_label = QLabel("最大间隔:")
        self.random_max_spin = QDoubleSpinBox()
        self.random_max_spin.setRange(0.01, 10.0)
        self.random_max_spin.setValue(0.3)
        self.random_max_spin.setSingleStep(0.1)
        
        self.random_min_label.hide()
        self.random_min_spin.hide()
        self.random_max_label.hide()
        self.random_max_spin.hide()
        
        mode_layout.addWidget(self.random_min_label)
        mode_layout.addWidget(self.random_min_spin)
        mode_layout.addWidget(self.random_max_label)
        mode_layout.addWidget(self.random_max_spin)
        mode_layout.addStretch()
        
        text_layout.addLayout(mode_layout)
        text_group.setLayout(text_layout)
        main_layout.addWidget(text_group)
        
        # 控制按钮区域
        control_group = QGroupBox("控制面板")
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("开始输入")
        self.start_btn.clicked.connect(self.start_input)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_input)
        self.stop_btn.setEnabled(False)
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # 状态栏
        self.statusBar().showMessage('就绪')
        
        # 设置样式
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton {
                min-width: 100px;
                min-height: 30px;
            }
        """)
        
    def on_mode_changed(self, text):
        if text == "固定间隔":
            self.interval_spin.show()
            self.random_min_label.hide()
            self.random_min_spin.hide()
            self.random_max_label.hide()
            self.random_max_spin.hide()
        else:
            self.interval_spin.hide()
            self.random_min_label.show()
            self.random_min_spin.show()
            self.random_max_label.show()
            self.random_max_spin.show()
            
    def start_input(self):
        text = self.text_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "警告", "请输入要模拟的文本！")
            return
            
        # 准备开始倒计时
        self.start_btn.setEnabled(False)
        self.text_input.setEnabled(False)
        self.mode_combo.setEnabled(False)
        self.statusBar().showMessage('3秒后开始输入...')
        
        QTimer.singleShot(3000, lambda: self.perform_input(text))
        
    def perform_input(self, text):
        self.stop_btn.setEnabled(True)
        self.statusBar().showMessage('正在输入...')
        
        try:
            if self.mode_combo.currentText() == "固定间隔":
                interval = self.interval_spin.value()
                self.simulator.start_continuous_input(text, interval)
            else:
                min_interval = self.random_min_spin.value()
                max_interval = self.random_max_spin.value()
                self.simulator.start_continuous_input(text, (min_interval, max_interval))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"输入过程出错: {str(e)}")
            self.stop_input()
            
    def stop_input(self):
        self.simulator.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.text_input.setEnabled(True)
        self.mode_combo.setEnabled(True)
        self.statusBar().showMessage('已停止')
        
    def closeEvent(self, event):
        self.simulator.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    
    window = InputSimulatorGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
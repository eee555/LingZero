import sys, os
import pytesseract
# 判断是开发环境还是生产环境
if os.path.exists("./.github"):
    pytesseract.pytesseract.tesseract_cmd = r'D:/Tesseract-OCR/tesseract.exe'
    os.environ["TESSDATA_PREFIX"] = r'D:/Tesseract-OCR/tessdata'
else:
    pytesseract.pytesseract.tesseract_cmd = r'./tesseract/tesseract.exe'
    os.environ["TESSDATA_PREFIX"] = r'./tesseract/tessdata'
from PySide6.QtCore import Qt, QRect, QPoint, Signal, QEvent
from PySide6.QtGui import (QGuiApplication, QPainter, QColor, QCursor, QMouseEvent)
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QDialog,
                                QSystemTrayIcon, QMenu, QLabel, QStyle, QVBoxLayout)
from pynput import mouse
import keyboard
from PIL import Image
import ctypes
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

import logging
logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    filename='debug.log',
                    filemode='a')

# import argostranslate.translate
from argostranslate import translate
# translated_text = argostranslate.translate.translate("why.", "en", "zh")

langs = translate.get_installed_languages()
if not langs:
    from argostranslate import package
    model_path = './translate-en_zh-1_9.argosmodel'  # 替换为你的模型文件路径
    package.install_from_path(model_path)
    langs = translate.get_installed_languages()
    
source_lang = next(filter(lambda x: x.code == 'en', langs))
target_lang = next(filter(lambda x: x.code == 'zh', langs))
translator = source_lang.get_translation(target_lang)

# 太长或太短，或英文占比没有达到60%，都不翻译
def is_more_than_60_percent_english(text):
    total_chars = len(text)
    if not text or total_chars > 10000:
        return False
    # 复制了文件
    if r"///" in text:
        return False
    english_chars = sum(1 for char in text if char.isalpha() and ('a' <= char.lower() <= 'z'))
    percentage = english_chars / total_chars
    return percentage >= 0.6

class TextWindow(QWidget):
    def __init__(self, raw_text, trans_text, position: QRect = None, parent=None):
        super(TextWindow, self).__init__(parent=parent)
        logging.debug(f'TextWindow: {raw_text} -> {trans_text}')
        self.trans_text = trans_text
        self.raw_text = raw_text
        self.position = position
        self.setup_ui()
        QApplication.instance().installEventFilter(self)
        screen = QApplication.primaryScreen()
        self.scale_factor = screen.devicePixelRatio()
        

    def setup_ui(self):
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.content = QLabel(self)
        if self.position:
            pad = min(self.position.width(), self.position.height())
            pad = int(pad / 10)
            pad = min(pad, 10)
        else:
            self.content.setMaximumWidth(300)
            pad = 3
        self.content.setStyleSheet(f"background: #fef9e7; border-radius: 4px; padding: {pad}px;")
        
        if len(self.trans_text) > 30:
            self.content.setAlignment(Qt.AlignLeft)
        else:
            self.content.setAlignment(Qt.AlignCenter)
        self.content.setWordWrap(True)
        self.content.setText(self.trans_text)
        self.trans_flag = True
        layout.addWidget(self.content)
        self.setLayout(layout)

        self.drag_pos = None

        
        if self.position:
            self.setGeometry(self.position)
        else:
            mouse_pos = QCursor.pos()
            self.setFixedWidth(300)
            # label_size_hint = self.content.sizeHint()
            # height = label_size_hint.height() + layout.contentsMargins().top() + layout.contentsMargins().bottom()
            # rect = QRect(mouse_pos.x(), mouse_pos.y(), 300, height)
            # self.setGeometry(rect)
            self.move(mouse_pos)

        self.update()
        # 处理未处理的事件
        QApplication.processEvents()

    # 切换原文/翻译
    def switch(self):
        if self.trans_flag:
            self.content.setText(self.raw_text)
        else:
            self.content.setText(self.trans_text)
        if not self.position:
            self.adjustSize()
        self.trans_flag = not self.trans_flag

    # 窗口拖动逻辑（保持不变）
    def mousePressEvent(self, event: QMouseEvent):
        # 按下且拖动过
        self.drag_flag = False
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            self.drag_flag = True

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_pos = None
        if not self.drag_flag:
            self.switch()
    
    def mouseClick(self, x, y, name, flag):
        frame_rect = self.frameGeometry()
        # 修正缩放后的真实像素范围
        real_left = frame_rect.x() * self.scale_factor
        real_top = frame_rect.y() * self.scale_factor
        real_width = frame_rect.width() * self.scale_factor
        real_height = frame_rect.height() * self.scale_factor
        client_rect = QRect(real_left, real_top, real_width, real_height)
        if not client_rect.contains(x, y):
            self.close()

    # 全局事件过滤器
    def eventFilter(self, obj, event: QEvent):
        # print(event)
        if event.type() == QEvent.WindowDeactivate:
            self.close()

        # ESC键关闭
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
            self.close()
            
        return super().eventFilter(obj, event)

class ScreenShotWindow(QDialog):
    esc_triggered = Signal()
    click_triggered = Signal(int, int, str, bool)
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.dragging = False
        keyboard.add_hotkey('esc',  self.on_hotkey_close)
        self.esc_triggered.connect(self.close)

    def init_ui(self):
        # 设置窗口属性
        self.setWindowFlags(Qt.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.screen = QGuiApplication.primaryScreen()

        # 获取主屏幕尺寸并全屏显示
        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.show()

    def on_hotkey_close(self):
        self.esc_triggered.emit()

    def paintEvent(self, event):
        # 绘制半透明蒙层和选择框
        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0, 100))  # 半透明黑色背景
        painter.drawRect(self.rect())

        if self.dragging:
            # 绘制选择框
            rect = QRect(self.start_point, self.end_point).normalized()
            painter.setPen(Qt.GlobalColor.white)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.globalPosition().toPoint()
            self.end_point = self.start_point
            self.dragging = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.end_point = event.globalPosition().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.close()
            self.capture_selected_area()

    def capture_selected_area(self):
        # 获取选中的矩形区域
        rect = QRect(self.start_point, self.end_point).normalized()
        # 截取屏幕图像
        screen = QGuiApplication.primaryScreen()
        if rect.width() < 5 or rect.height() < 5:
            return
        screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
        qimage = screenshot.toImage()
        byte_data = qimage.constBits().tobytes()
        pil_image = Image.frombytes(
            "RGB", 
            (qimage.width(), qimage.height()),
            byte_data,
            'raw', 'BGRX'  # 处理Qt的32-bit颜色格式
        )
        try:
            text = pytesseract.image_to_string(pil_image, lang='eng').strip()
        except Exception as e:
            logging.error(f"OCR识别失败: {e}")
            import traceback
            traceback_text = traceback.format_exc()
            logging.debug(f'traceback_text：{traceback_text}')
        if not is_more_than_60_percent_english(text):
            logging.debug(f'is_more_than_60_percent_english')
            return
        texts = text.split("\n\n")
        translated_texts = []
        try:
            for t in texts:
                t = t.replace("\n", " ")
                translated_texts.append(translator.translate(t))
            translated_text = "\n\n".join(translated_texts)
        except Exception as e:
            import traceback
            translated_text = "报错：" + translated_text + ", " + traceback.format_exc()
        logging.debug(f'999')
        self.textWindow = TextWindow(text, translated_text, rect)
        self.textWindow.show()
        self.esc_triggered.connect(self.textWindow.close)
        logging.debug(f'111')
        self.click_triggered.connect(self.textWindow.mouseClick)

class TrayApp(QMainWindow):
    capture_triggered = Signal()
    clipboard_changed_triggered = Signal()
    esc_triggered = Signal()
    click_triggered = Signal(int, int, str, bool)
    def __init__(self):
        super().__init__()
        self.tray = QSystemTrayIcon(self)
        # self.tray.setIcon(QIcon("icon.png"))
        default_icon = QApplication.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray.setIcon(default_icon)

        
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu::item {
                padding: 5px 10px 5px 10px;
                icon: none;
            }
        """)
        capture_action = menu.addAction("截屏翻译（ctrl+space）")
        capture_action.triggered.connect(self.capture)
        capture_action = menu.addAction("禁用/启用复制翻译（ctrl+1）")
        capture_action.triggered.connect(self.on_hotkey_stoptrans)
        exit_action = menu.addAction("退出")
        exit_action.triggered.connect(QApplication.quit)
        
        self.tray.setContextMenu(menu)
        self.tray.show()

        self.capture_triggered.connect(self.capture)
        self.clipboard_changed_triggered.connect(self.clipboard_changed_trans)

        keyboard.add_hotkey('ctrl+space', self.capture_triggered.emit)
        self.stop_trans = False
        keyboard.add_hotkey('ctrl+1', self.on_hotkey_stoptrans)
        keyboard.add_hotkey('esc', self.esc_triggered.emit)

        self.clipboard = QApplication.clipboard()
        # 连接剪贴板的 dataChanged 信号到槽函数
        self.clipboard.dataChanged.connect(self.clipboard_changed_triggered.emit)


        def on_click_wrapper(x, y, button, pressed):
            self.click_triggered.emit(x, y, button.name, pressed)
        # 创建鼠标监听器
        self.listener = mouse.Listener(
            on_click=on_click_wrapper,
        )
        self.listener.start()

    def clipboard_changed_trans(self):
        if self.stop_trans:
            return
        clipboard_text = self.clipboard.text().strip()
        texts = clipboard_text.split("\n\n")
        translated_texts = []
        for t in texts:
            t = t.replace("\n", " ")
            translated_texts.append(translator.translate(t))
        translated_text = "\n\n".join(translated_texts)

        if not is_more_than_60_percent_english(clipboard_text):
            return
        self.textWindow = TextWindow(clipboard_text, translated_text)
        self.textWindow.show()
        self.esc_triggered.connect(self.textWindow.close)
        self.click_triggered.connect(self.textWindow.mouseClick)
        
    def on_hotkey_stoptrans(self):
        self.stop_trans = not self.stop_trans

    def capture(self):
        self.shot_window = ScreenShotWindow()
        self.shot_window.show()
        self.click_triggered.connect(self.shot_window.click_triggered)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    # Windows任务栏图标设置
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('myapp.ocr.v1')
    main = TrayApp()
    sys.exit(app.exec())


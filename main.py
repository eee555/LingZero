import sys, os, time
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")
secret_config = configparser.ConfigParser()
secret_config.read('secret.ini', encoding="utf-8")
import pytesseract
# 判断是开发环境还是生产环境
if os.path.exists("./.github"):
    pytesseract.pytesseract.tesseract_cmd = r'D:/Tesseract-OCR/tesseract.exe'
    os.environ["TESSDATA_PREFIX"] = r'D:/Tesseract-OCR/tessdata'
else:
    pytesseract.pytesseract.tesseract_cmd = r'./tesseract/tesseract.exe'
    os.environ["TESSDATA_PREFIX"] = r'./tesseract/tessdata'
from PySide6.QtCore import Qt, QRect, QPoint, Signal, QEvent
from PySide6.QtGui import (QGuiApplication, QPainter, QColor, QCursor, QMouseEvent, QIcon)
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QDialog,
                                QSystemTrayIcon, QMenu, QLabel, QStyle, QVBoxLayout, 
                                QGraphicsDropShadowEffect)

from pynput import mouse as pynput_mouse
from pynput import keyboard as pynput_keyboard
import keyboard
import pyperclip
from PIL import Image
import ctypes
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

from translator import Translator
trans = Translator()

from translator import tencent, data_cleaning
tencent_trans = tencent.Trans(secret_config)

def wait_for_all_keys_up(timeout=2.0, interval=0.1):
    """等待所有物理按键抬起（超时时间内）"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not any(keyboard.is_pressed(key) for key in keyboard.all_modifiers | set("abcdefghijklmnopqrstuvwxyz1234567890")):
            return True
        time.sleep(interval)
    return False

def copy_selected_text():
    """模拟 Ctrl+C 并返回复制的文本"""
    if not wait_for_all_keys_up():
        return None
    # 模拟 Ctrl+C
    keyboard.press('ctrl')
    keyboard.press('c')
    time.sleep(0.1)  # 等待复制完成
    keyboard.release('c')
    keyboard.release('ctrl')
    # 获取剪贴板内容
    return pyperclip.paste()

class RightClickIgnoreLabel(QLabel):
    # 不处理右键鼠标事件的Qlabel
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # 忽略右键事件，让其传递给父控件
            event.ignore()
        else:
            # 其他按钮（如左键）使用默认处理方式
            super().mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            event.ignore()
        else:
            super().mouseReleaseEvent(event)
    def contextMenuEvent(self, event):
        # 忽略上下文菜单事件，让其传递给父控件
        event.ignore()

# 翻译弹窗，用于展示翻译结果
class TextWindow(QWidget):
    open_or_close_triggered = Signal()
    def __init__(self, raw_text, position: QRect = None, parent=None):
        super(TextWindow, self).__init__(parent=parent)
        self.trans_text = ""
        self.raw_text = raw_text
        self.position = position
        self.setup_ui()
        QApplication.instance().installEventFilter(self)
        screen = QApplication.primaryScreen()
        self.scale_factor = screen.devicePixelRatio()
        trans.set_ui(self)
        # 初始化标志变量，用于记录当前文本是否可复制
        self.text_selectable = False
        self.priority_level = 5

    def setup_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.content = RightClickIgnoreLabel(self)
        self.content.setContextMenuPolicy(Qt.NoContextMenu)
        if self.position:
            pad = min(self.position.width(), self.position.height())
            pad = int(pad / 10)
            pad = min(pad, 10)
        else:
            self.content.setFixedWidth(config.getint('DEFAULT', 'copy_trans_fixed_width'))
            pad = 3

        # QLabel样式：白色背景 + 圆角
        self.content.setStyleSheet(f"""
            QLabel {"{"}
                {config.get('DEFAULT', 'background_style').strip("' ()[]" + '"')}
                margin: 8px;
                padding: {pad}px;
            {"}"}
        """)

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)  # 阴影模糊程度
        shadow.setOffset(0, 0)     # 阴影不偏移
        shadow.setColor(QColor(30, 144, 255, 180))  # 淡蓝色，透明度约70%
        self.content.setGraphicsEffect(shadow)

        self.trans_flag = True
        layout.addWidget(self.content)
        self.setLayout(layout)
        self.drag_pos = None
        # 移动窗口位置、调整窗口尺寸
        if self.position:
            self.position.adjust(-8, -8, 8, 8)
            self.setGeometry(self.position)
        else:
            mouse_pos = QCursor.pos()
            self.setFixedWidth(config.getint('DEFAULT', 'copy_trans_fixed_width'))
            self.move(mouse_pos + QPoint(-8, -8))
        self.update()

    def update_result(self, trans_result, priority_level = 3):
        # 离线翻译的优先度为3，腾讯翻译为2，词典翻译为1，优先度越低越优先采用
        if self.priority_level > priority_level:
            self.priority_level = priority_level
        else:
            return
        self.trans_text = trans_result
        if len(self.trans_text) > 30:
            self.content.setAlignment(Qt.AlignLeft)
        else:
            self.content.setAlignment(Qt.AlignCenter)
        self.content.setWordWrap(True)
        if self.trans_flag:
            self.content.setText(self.trans_text)
        if not self.position:
            hint_size = self.content.sizeHint()
            self.setFixedHeight(hint_size.height())
            self.setMinimumHeight(0)
        self.layout().update()
        self.update()

    # 切换原文/翻译
    def switch(self):
        if self.trans_flag:
            self.content.setText(self.raw_text)
        else:
            self.content.setText(self.trans_text)
        if not self.position:
            hint_size = self.content.sizeHint()
            # 和self.content.setFixedHeight(hint_size.height())、self.content.setMinimumHeight(0)
            # 相比，前者会向中间收缩，而窗口高度不变
            # 首先设置固定尺寸，再设置最小尺寸，也就是取消固定尺寸，方便下次尺寸修改
            self.setFixedHeight(hint_size.height())
            self.setMinimumHeight(0)
        else:
            hint_size = self.content.sizeHint()
            max_height = max(self.position.height(), hint_size.height())
            self.setFixedHeight(max_height)
            self.setMinimumHeight(0)

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
        if event.button() == Qt.LeftButton:
            if not self.drag_flag:
                self.switch()
        if event.button() == Qt.RightButton:
            if not self.text_selectable:
                self.content.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            else:
                self.content.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            self.text_selectable = not self.text_selectable
    
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

    def showEvent(self, event):
        self.open_or_close_triggered.emit()
        super().showEvent(event)

    def closeEvent(self, event):
        self.open_or_close_triggered.emit()
        return super().closeEvent(event)


# 全屏的截屏窗口，半透明，鼠标拖动框选截屏区域
class ScreenShotWindow(QDialog):
    esc_triggered = Signal()
    click_triggered = Signal(int, int, str, bool)
    text_window_open_or_close_triggered = Signal()
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
        text = pytesseract.image_to_string(pil_image, lang='eng')
        text_show = "\n\n".join(data_cleaning(text)).strip()
        self.textWindow = TextWindow(text_show, rect)
        self.textWindow.open_or_close_triggered.connect(self.text_window_open_or_close_triggered.emit)
        self.textWindow.show()
        if not trans.translate(text):
            return
        self.esc_triggered.connect(self.textWindow.close)
        self.click_triggered.connect(self.textWindow.mouseClick)

# 主程序，启动后直接缩小到托盘
class TrayApp(QMainWindow):
    capture_triggered = Signal()
    clipboard_changed_triggered = Signal()
    esc_triggered = Signal()
    click_triggered = Signal(int, int, str, bool)
    copy_into_english_triggered = Signal()
    def __init__(self):
        super().__init__()
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("a.ico"))
        self.menu = QMenu()
        self.menu.setStyleSheet("""
            QMenu::item {
                padding: 5px 10px 5px 10px;
                icon: none;
            }
        """)
        a = self.menu.addAction(f"截屏翻译（{config.get('DEFAULT', 'capture_triggered_hotkey')}）")
        a.triggered.connect(self.capture)
        self.action_stoptrans = self.menu.addAction(f"禁用复制翻译（{config.get('DEFAULT', 'stoptrans_triggered_hotkey')}）")
        self.action_stoptrans.triggered.connect(self.on_hotkey_stoptrans)
        exit_action = self.menu.addAction("退出")
        exit_action.triggered.connect(QApplication.quit)
        
        self.tray.setContextMenu(self.menu)
        self.tray.show()

        # 连接截屏翻译
        self.capture_triggered.connect(self.capture)
        capture_triggered_hotkeys = config.get('DEFAULT', 'capture_triggered_hotkey').split(",")
        self.capture_handle_hotkeys = []
        for hotkey in capture_triggered_hotkeys:
            self.capture_handle_hotkeys.append(
                keyboard.add_hotkey(hotkey, self.capture_triggered.emit))
        self.stop_trans = False

        # 连接停止翻译
        stoptrans_triggered_hotkeys = config.get('DEFAULT', 'stoptrans_triggered_hotkey').split(",")
        for hotkey in stoptrans_triggered_hotkeys:
            keyboard.add_hotkey(hotkey, self.on_hotkey_stoptrans)

        # 连接停止截屏
        keyboard.add_hotkey('esc', self.esc_triggered.emit)

        # 连接将选中的中文转为英文
        copy_into_english_triggered_hotkeys =\
            config.get('DEFAULT', 'copy_into_english_triggered_hotkey').split(",")
        for hotkey in copy_into_english_triggered_hotkeys:
            keyboard.add_hotkey(hotkey, self.on_hotkey_copy_into_english)

        self.clipboard = QApplication.clipboard()
        self.on_hotkey_stoptrans()

        # 创建鼠标监听器
        def on_click_wrapper(x, y, button, pressed):
            self.click_triggered.emit(x, y, button.name, pressed)
        self.mouse_listener = pynput_mouse.Listener(
            on_click=on_click_wrapper,
        )
        self.mouse_listener.start()

    def clipboard_changed_trans(self):
        clipboard_text = self.clipboard.text().strip()
        self.textWindow = TextWindow(clipboard_text)
        if not trans.translate(clipboard_text):
            return
        self.textWindow.open_or_close_triggered.connect(self.on_hotkey_stoptrans)
        self.textWindow.show()
        self.esc_triggered.connect(self.textWindow.close)
        self.click_triggered.connect(self.textWindow.mouseClick)
        
    # 启用/停用复制翻译
    def on_hotkey_stoptrans(self):
        if self.stop_trans:
            self.clipboard.dataChanged.disconnect(self.clipboard_changed_triggered.emit)
            self.clipboard_changed_triggered.disconnect(self.clipboard_changed_trans)
            self.action_stoptrans.setText(f"启用复制翻译（{config.get('DEFAULT', 'stoptrans_triggered_hotkey')}）")
        else:
            self.clipboard.dataChanged.connect(self.clipboard_changed_triggered.emit)
            self.clipboard_changed_triggered.connect(self.clipboard_changed_trans)
            self.action_stoptrans.setText(f"禁用复制翻译（{config.get('DEFAULT', 'stoptrans_triggered_hotkey')}）")
        self.stop_trans = not self.stop_trans

    # 将选中的中文转为英文快捷键，并原地粘贴，并修改剪切板
    def on_hotkey_copy_into_english(self):
        self.on_hotkey_stoptrans()
        clipboard_text = copy_selected_text()
        if trans_result := tencent_trans.translate(clipboard_text, target="en"):
            pyperclip.copy(trans_result)
            keyboard.press_and_release('ctrl+v')
        self.on_hotkey_stoptrans()
        
    def capture(self):
        self.shot_window = ScreenShotWindow()
        self.shot_window.text_window_open_or_close_triggered.connect(self.on_hotkey_stoptrans)
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


from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QGraphicsPixmapItem, QStackedWidget, QGraphicsScene,
    QGraphicsView, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton,
    QFileDialog
)
from gui_elements import Camera, ResultPopup, DataCarousel, OrderPopup
import constants
from utils.get_data import get_data_from_pdf

PAGE_INFO, PAGE_DYES, PAGE_CAMERA, PAGE_RESULTS = range(4)

# temp method before i build out other pages
def make_label_page(text):
    page = QWidget()
    QVBoxLayout(page).addWidget(QLabel(text, alignment=Qt.AlignTop | Qt.AlignHCenter))
    return page

class CameraPage(QWidget):
    def __init__(self, index = 0):
        super().__init__()
        
        self.index = index
        self.camera_thread = None
        self.camera = None
        self.scenePixmapItem = None
        self.order_info = None
        self.order_window = None

        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        QVBoxLayout(self).addWidget(self.graphicsView)
        
    def start_cam(self):
        if self.camera_thread is not None: return
        
        self.camera_thread = QThread()
        self.camera = Camera(self.index)
        self.camera.moveToThread(self.camera_thread)
        self.camera.frame_captured.connect(self.process_frame)
        self.camera_thread.started.connect(self.camera.run)
        self.camera.dye_found.connect(self.show_result)
        self.camera_thread.start()
        self.show_order()
        
    def stop_cam(self):
        if self.camera_thread is None: return
        
        self.camera.stop()
        self.camera_thread.quit()
        self.camera_thread.wait()
        self.camera.deleteLater()
        self.camera_thread.deleteLater()
        self.camera = None
        self.camera_thread = None
        
        self.scene.clear()
        self.scenePixmapItem = None
        
        if self.order_window is not None:
            self.order_window.close()
            self.order_window = None
        
    def process_frame(self, frame):
        if self.camera is None: return
        
        h, w, ch = frame.shape
        image = QImage(
            frame.data, 
            w,
            h,
            ch * w,
            QImage.Format.Format_BGR888
        ).copy()
        pixmap = QPixmap.fromImage(image)
            
        if self.scenePixmapItem is None:
            self.scenePixmapItem = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.scenePixmapItem)
            self.scene.setSceneRect(self.scenePixmapItem.boundingRect())
        else:
            self.scenePixmapItem.setPixmap(pixmap)

    def fit(self):
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.scenePixmapItem is not None: self.fit()
        
    def show_result(self, dye_info):
        popup = ResultPopup(dye_info, parent=self)
        popup.show()
        if self.order_window is not None:
            self.order_window.check_dye(dye_info)
    
    def show_order(self):
        if self.order_info is None: return

        if self.order_window is not None:
            self.order_window.close()
            self.order_window.deleteLater()

        self.order_window = OrderPopup(self.order_info, parent=self)
        self.order_window.show()

class InputPage(QWidget):
    confirmed = Signal(dict)
    def __init__(self):
        super().__init__()
        self.file_data = None
        self.data_carousel = None
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout = QVBoxLayout(self)
        
        self.upload_widget = QWidget()
        self.upload_widget.setObjectName("uploadWidget")
        self.upload_layout = QHBoxLayout(self.upload_widget)
        self.upload_text = QLabel("Upload PDF")
        
        self.upload_button = QPushButton("Upload file")
        self.upload_button.setObjectName("uploadButton")
        self.upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_button.clicked.connect(self.upload_file)
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setObjectName("confirmButton")
        self.confirm_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_button.clicked.connect(self.confirm_upload)
        
        self.upload_layout.addWidget(self.upload_text)
        self.upload_layout.addWidget(self.upload_button)
        self.upload_layout.addWidget(self.confirm_button)
        
        self.main_layout.addWidget(self.upload_widget)
        
        self.setStyleSheet(f"""
            QPushButton#uploadButton, QPushButton#confirmButton {{
                border: 2px solid {constants.primary_accent};
                border-radius: 10px;
                min-height: 50px;
                background: {constants.secondary_bg};
                font-size: 18px;
                font-weight: bold;
            }}
        """)
         
    def upload_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Select Worksheet to Upload",
            dir="",
            filter="PDF Files (*.pdf)"
        )
        
        if not path: return
        
        self.file_data = get_data_from_pdf(path)
        self.show_carousel()
    
    def confirm_upload(self):
        if self.file_data is None: return
        # set to camera page index
        self.confirmed.emit(self.file_data)
    
    def show_carousel(self):
        if self.data_carousel is not None:
            self.main_layout.removeWidget(self.data_carousel)
            self.data_carousel.deleteLater()
        self.data_carousel = DataCarousel(self.file_data)
        self.main_layout.addWidget(self.data_carousel)
            
class PageStack(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.camera_page = CameraPage(0)
        self.input_page = InputPage()
        self.input_page.confirmed.connect(self.on_confirmed)
        
        self.addWidget(make_label_page("INFO"))
        self.addWidget(self.input_page)
        self.addWidget(self.camera_page)
        self.addWidget(make_label_page("Results"))
        
    def on_confirmed(self, file_data):
        self.camera_page.order_info = file_data
        self.show_page(PAGE_CAMERA)
        
    def show_page(self, index):
        if index != PAGE_CAMERA:
            self.camera_page.stop_cam()
        
        self.setCurrentIndex(index)
        
        if index == PAGE_CAMERA:
            self.camera_page.start_cam()
        
    def shutdown(self):
        self.camera_page.stop_cam()
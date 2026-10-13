from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QGraphicsPixmapItem, QStackedWidget, QGraphicsScene,
    QGraphicsView, QLabel, QVBoxLayout, QWidget
)
from gui_elements import Camera

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
        self.camera_thread.start()
    
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
        
class PageStack(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.camera_page = CameraPage(0)
        
        self.addWidget(make_label_page("Info"))
        self.addWidget(make_label_page("Input Dyes"))
        self.addWidget(self.camera_page)
        self.addWidget(make_label_page("Results"))
        
    def show_page(self, index):
        if index != PAGE_CAMERA:
            self.camera_page.stop_cam()
        
        self.setCurrentIndex(index)
        
        if index == PAGE_CAMERA:
            self.camera_page.start_cam()
        
    def shutdown(self):
        self.camera_page.stop_cam()
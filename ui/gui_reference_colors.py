from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
from sklearn.cluster import KMeans


class GUIReferenceColors(QWidget):
    # Signal emitted when color is selected
    update_color_signal = pyqtSignal(np.ndarray)
    
    def __init__(self, win_size=512):
        QWidget.__init__(self)
        self.win_size = win_size
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)
        self.setLayout(main_layout)
        
        # Load reference image button
        self.load_btn = QPushButton("Load Reference Image")
        self.load_btn.setToolTip("Load a reference image to pick colors from")
        self.load_btn.clicked.connect(self.load_reference_image)
        main_layout.addWidget(self.load_btn)
        
        # Interactive reference image display
        self.ref_image_widget = ReferenceImageDisplay(win_size)
        self.ref_image_widget.color_picked.connect(self.on_color_picked)
        main_layout.addWidget(self.ref_image_widget)
        
        # Info label
        self.info_label = QLabel("Load a reference image and click on it to pick colors")
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("QLabel { font-size: 9pt; padding: 4px; color: #aaa; }")
        main_layout.addWidget(self.info_label)
        
        # Store reference image
        self.reference_image = None
        
    def load_reference_image(self):
        """Load a reference image and extract colors"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Reference Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        
        if file_path:
            try:
                # Load image
                img = cv2.imread(file_path)
                if img is None:
                    self.info_label.setText("Error: Could not load image")
                    return
                
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Resize to match window size
                h, w = img_rgb.shape[:2]
                max_dim = max(h, w)
                scale = self.win_size / max_dim
                new_w = int(w * scale / 4) * 4  # Make divisible by 4
                new_h = int(h * scale / 4) * 4
                
                self.reference_image = cv2.resize(img_rgb, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
                
                # Update display
                self.ref_image_widget.set_image(self.reference_image)
                
                self.info_label.setText(f"Loaded: {file_path.split('/')[-1]} - Click on image to pick colors")
                
            except Exception as e:
                self.info_label.setText(f"Error: {str(e)}")
    
    def on_color_picked(self, color_rgb):
        """Handle color picked from reference image"""
        self.info_label.setText(f"Picked: RGB({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})")
        self.update_color_signal.emit(color_rgb)
    
    def sizeHint(self):
        return QSize(self.win_size, self.win_size + 60)


class ReferenceImageDisplay(QWidget):
    # Signal emitted when color is picked from image
    color_picked = pyqtSignal(np.ndarray)
    
    def __init__(self, win_size=512):
        QWidget.__init__(self)
        self.win_size = win_size
        self.setMinimumSize(256, 256)
        self.setMaximumSize(win_size, win_size)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image = None
        self.image_rgb = None
        self.dw = 0
        self.dh = 0
        self.img_w = 0
        self.img_h = 0
        self.setMouseTracking(True)
        
    def set_image(self, img_rgb):
        """Set the reference image to display"""
        self.image_rgb = img_rgb
        h, w = img_rgb.shape[:2]
        
        # Calculate padding to center image
        self.img_h = h
        self.img_w = w
        self.dw = (self.win_size - w) // 2
        self.dh = (self.win_size - h) // 2
        
        # Convert to QImage
        bytes_per_line = 3 * w
        q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image = QPixmap.fromImage(q_img)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QColor(49, 54, 49))
        
        if self.image is not None:
            # Draw image centered
            painter.drawPixmap(self.dw, self.dh, self.image)
            
            # Draw border
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawRect(self.dw, self.dh, self.img_w, self.img_h)
        else:
            # Draw placeholder text
            painter.setPen(Qt.white)
            painter.drawText(event.rect(), Qt.AlignCenter, "No reference image\nClick 'Load Image' to start")
        
        painter.end()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.image_rgb is not None:
            pos = event.pos()
            x = pos.x() - self.dw
            y = pos.y() - self.dh
            
            # Check if click is within image bounds
            if 0 <= x < self.img_w and 0 <= y < self.img_h:
                # Get color at clicked position
                color = self.image_rgb[y, x]
                self.color_picked.emit(color)
    
    def sizeHint(self):
        return QSize(self.win_size, self.win_size)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import cv2
from sklearn.cluster import KMeans
import sys
sys.path.append('.')
from auto_colorize_from_reference import AutoColorizeFromReference


class GUIReferenceColors(QWidget):
    # Signal emitted when color is selected
    update_color_signal = pyqtSignal(np.ndarray)
    # Signal emitted when auto-colorization is requested
    auto_colorize_signal = pyqtSignal(list)  # List of (x, y, r, g, b) tuples
    
    def __init__(self, win_size=512):
        QWidget.__init__(self)
        self.win_size = win_size
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)
        self.setLayout(main_layout)
        
        # Buttons layout
        btn_layout = QHBoxLayout()
        
        # Load reference image button
        self.load_btn = QPushButton("Load Reference")
        self.load_btn.setToolTip("Load a reference image to pick colors from")
        self.load_btn.clicked.connect(self.load_reference_image)
        btn_layout.addWidget(self.load_btn)
        
        # Auto-colorize button
        self.auto_btn = QPushButton("Auto-Colorize")
        self.auto_btn.setToolTip("Automatically extract and apply colors from reference image")
        self.auto_btn.clicked.connect(self.auto_colorize)
        self.auto_btn.setEnabled(False)
        btn_layout.addWidget(self.auto_btn)
        
        main_layout.addLayout(btn_layout)
        
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
        
        # Store reference image and grayscale image
        self.reference_image = None
        self.grayscale_image = None
        
        # Auto-colorizer
        self.auto_colorizer = None
        
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
                
                # Enable auto-colorize button if we have both images
                if self.grayscale_image is not None:
                    self.auto_btn.setEnabled(True)
                
                self.info_label.setText(f"Loaded: {file_path.split('/')[-1]} - Click to pick colors or use Auto-Colorize")
                
            except Exception as e:
                self.info_label.setText(f"Error: {str(e)}")
    
    def set_grayscale_image(self, gray_image):
        """Set the grayscale image for auto-colorization"""
        self.grayscale_image = gray_image
        
        # Enable auto-colorize button if we have both images
        if self.reference_image is not None:
            self.auto_btn.setEnabled(True)
    
    def auto_colorize(self):
        """Automatically extract colors from reference and apply to grayscale image"""
        if self.reference_image is None:
            self.info_label.setText("Please load a reference image first")
            return
        
        if self.grayscale_image is None:
            self.info_label.setText("Please load a grayscale image first")
            return
        
        try:
            self.info_label.setText("Detecting features and matching colors...")
            QApplication.processEvents()
            
            # Initialize auto-colorizer if needed
            if self.auto_colorizer is None:
                self.auto_colorizer = AutoColorizeFromReference(
                    method='orb',
                    num_points=30,  # Start with 30 points
                    match_threshold=0.75
                )
            
            # Resize reference image to match grayscale if needed
            ref_img = self.reference_image
            if ref_img.shape[:2] != self.grayscale_image.shape[:2]:
                ref_img = cv2.resize(ref_img, 
                                    (self.grayscale_image.shape[1], self.grayscale_image.shape[0]))
            
            # Extract color points
            color_points, _ = self.auto_colorizer.extract_color_points(
                self.grayscale_image, ref_img, visualize=False
            )
            
            if len(color_points) == 0:
                self.info_label.setText("No matching features found. Try a different reference image.")
                return
            
            # Emit signal with color points
            self.auto_colorize_signal.emit(color_points)
            
            self.info_label.setText(f"Applied {len(color_points)} color points automatically!")
            
        except Exception as e:
            self.info_label.setText(f"Auto-colorize error: {str(e)}")
            print(f"Auto-colorize error: {e}")
            import traceback
            traceback.print_exc()
    
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

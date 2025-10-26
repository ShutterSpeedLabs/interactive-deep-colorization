from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
from . import color_presets


class GUIPresetPalette(QWidget):
    # Define signals
    update_color_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        QWidget.__init__(self)
        self.color_width = 20
        self.border = 4
        self.colors_per_row = 6
        self.visible_rows = 8
        
        # Calculate dimensions
        self.palette_width = self.colors_per_row * self.color_width + (self.colors_per_row + 1) * self.border
        self.palette_height = self.visible_rows * self.color_width + (self.visible_rows + 1) * self.border
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)
        self.setLayout(main_layout)
        
        # Category dropdown
        self.category_combo = QComboBox()
        self.category_combo.addItems(color_presets.get_all_categories())
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        main_layout.addWidget(self.category_combo)
        
        # Scroll area for colors
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFixedWidth(self.palette_width + 20)  # +20 for scrollbar
        scroll_area.setMinimumHeight(self.palette_height)
        
        # Color display widget
        self.color_widget = ColorDisplayWidget(
            self.color_width, 
            self.border, 
            self.colors_per_row
        )
        self.color_widget.color_selected.connect(self.on_color_selected)
        scroll_area.setWidget(self.color_widget)
        
        main_layout.addWidget(scroll_area)
        
        # Color name label
        self.color_name_label = QLabel("Select a color")
        self.color_name_label.setWordWrap(True)
        self.color_name_label.setFixedWidth(self.palette_width)
        self.color_name_label.setStyleSheet("QLabel { font-size: 9pt; padding: 2px; }")
        main_layout.addWidget(self.color_name_label)
        
        # Initialize with first category
        self.on_category_changed(self.category_combo.currentText())
        
    def on_category_changed(self, category_name):
        """Update colors when category changes"""
        colors = color_presets.get_category_colors_array(category_name)
        color_names = color_presets.get_category_color_names(category_name)
        self.color_widget.set_colors(colors, color_names)
        self.color_name_label.setText(f"{category_name} - Select a color")
        
    def on_color_selected(self, color_rgb, color_name):
        """Handle color selection"""
        self.color_name_label.setText(color_name)
        self.update_color_signal.emit(color_rgb)
    
    def sizeHint(self):
        return QSize(self.palette_width + 20, self.palette_height + 80)


class ColorDisplayWidget(QWidget):
    # Signal emitted when color is selected
    color_selected = pyqtSignal(np.ndarray, str)
    
    def __init__(self, color_width, border, colors_per_row):
        QWidget.__init__(self)
        self.color_width = color_width
        self.border = border
        self.colors_per_row = colors_per_row
        self.colors = None
        self.color_names = None
        self.selected_id = -1
        self.setMouseTracking(True)
        
    def set_colors(self, colors, color_names):
        """Set colors to display"""
        self.colors = colors
        self.color_names = color_names
        self.selected_id = -1
        
        if colors is not None:
            num_colors = len(colors)
            num_rows = (num_colors + self.colors_per_row - 1) // self.colors_per_row
            height = num_rows * self.color_width + (num_rows + 1) * self.border
            width = self.colors_per_row * self.color_width + (self.colors_per_row + 1) * self.border
            self.setFixedSize(width, height)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QColor(49, 54, 49))
        
        if self.colors is not None:
            for n, c in enumerate(self.colors):
                ca = QColor(int(c[0]), int(c[1]), int(c[2]), 255)
                
                # Draw border for selected color
                if n == self.selected_id:
                    painter.setPen(QPen(Qt.white, 2))
                else:
                    painter.setPen(QPen(Qt.black, 1))
                
                painter.setBrush(ca)
                
                grid_x = n % self.colors_per_row
                grid_y = n // self.colors_per_row
                x = grid_x * (self.color_width + self.border) + self.border
                y = grid_y * (self.color_width + self.border) + self.border
                
                painter.drawRoundedRect(x, y, self.color_width, self.color_width, 2, 2)
        
        painter.end()
    
    def get_color_id_at_pos(self, pos):
        """Get color ID at mouse position"""
        if self.colors is None:
            return -1
        
        width = self.color_width + self.border
        x_grid = pos.x() // width
        y_grid = pos.y() // width
        
        # Check if click is within color square (not in border)
        dx = pos.x() % width
        dy = pos.y() % width
        
        if dx < self.border or dy < self.border:
            return -1
        
        if x_grid >= self.colors_per_row:
            return -1
        
        color_id = y_grid * self.colors_per_row + x_grid
        
        if color_id >= len(self.colors):
            return -1
        
        return color_id
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            color_id = self.get_color_id_at_pos(event.pos())
            if color_id >= 0:
                self.selected_id = color_id
                color = self.colors[color_id]
                color_name = self.color_names[color_id] if self.color_names else f"Color {color_id}"
                self.color_selected.emit(color, color_name)
                self.update()
    
    def sizeHint(self):
        if self.colors is not None:
            num_colors = len(self.colors)
            num_rows = (num_colors + self.colors_per_row - 1) // self.colors_per_row
            height = num_rows * self.color_width + (num_rows + 1) * self.border
            width = self.colors_per_row * self.color_width + (self.colors_per_row + 1) * self.border
            return QSize(width, height)
        return QSize(200, 200)

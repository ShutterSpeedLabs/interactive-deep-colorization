from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from . import gui_draw
from . import gui_vis
from . import gui_gamut
from . import gui_palette
from . import gui_preset_palette
from . import gui_reference_colors
import time


class GUIDesign(QWidget):
    def __init__(self, color_model, dist_model=None, img_file=None, load_size=256,
                 win_size=256, save_all=True):
        # draw the layout
        QWidget.__init__(self)
        
        # Set size policy to allow resizing
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # main layout
        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)
        
        # Left panel with scroll area for color selection tools
        leftScrollArea = QScrollArea()
        leftScrollArea.setWidgetResizable(True)
        leftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        leftScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        leftScrollArea.setMinimumWidth(280)
        leftScrollArea.setMaximumWidth(400)
        
        leftWidget = QWidget()
        colorLayout = QVBoxLayout()
        leftWidget.setLayout(colorLayout)
        leftScrollArea.setWidget(leftWidget)
        mainLayout.addWidget(leftScrollArea)
        
        # gamut layout
        self.gamutWidget = gui_gamut.GUIGamut(gamut_size=160)
        gamutLayout = self.AddWidget(self.gamutWidget, 'ab Color Gamut')
        colorLayout.addLayout(gamutLayout)

        # palette
        self.customPalette = gui_palette.GUIPalette(grid_sz=(10, 1))
        self.usedPalette = gui_palette.GUIPalette(grid_sz=(10, 1))
        cpLayout = self.AddWidget(self.customPalette, 'Suggested colors')
        colorLayout.addLayout(cpLayout)
        upLayout = self.AddWidget(self.usedPalette, 'Recently used colors')
        colorLayout.addLayout(upLayout)

        # Add preset color palette
        self.presetPalette = gui_preset_palette.GUIPresetPalette()
        presetLayout = self.AddWidget(self.presetPalette, 'Preset Colors')
        colorLayout.addLayout(presetLayout)

        self.colorPush = QPushButton()  # to visualize the selected color
        self.colorPush.setFixedWidth(self.customPalette.width())
        self.colorPush.setFixedHeight(25)
        self.colorPush.setStyleSheet("background-color: grey")
        colorPushLayout = self.AddWidget(self.colorPush, 'Color')
        colorLayout.addLayout(colorPushLayout)
        colorLayout.setAlignment(Qt.AlignTop)

        # drawPad layout - center panel
        drawPadLayout = QVBoxLayout()
        self.drawWidget = gui_draw.GUIDraw(color_model, dist_model, load_size=load_size, win_size=win_size)
        drawPadWidget = self.AddWidget(self.drawWidget, 'Drawing Pad')
        drawPadLayout.addLayout(drawPadWidget)
        
        # Add to main layout with stretch factor
        mainLayout.addLayout(drawPadLayout, 1)

        drawPadMenu = QHBoxLayout()

        self.bGray = QCheckBox("&Gray")
        self.bGray.setToolTip('show gray-scale image')

        self.bLoad = QPushButton('&Load')
        self.bLoad.setToolTip('load an input image')
        self.bSave = QPushButton("&Save")
        self.bSave.setToolTip('Save the current result.')
        
        self.bUndo = QPushButton("&Undo")
        self.bUndo.setToolTip('Undo last action (Ctrl+Z)')
        self.bUndo.setEnabled(False)
        
        self.bRedo = QPushButton("Re&do")
        self.bRedo.setToolTip('Redo last undone action (Ctrl+Y)')
        self.bRedo.setEnabled(False)

        drawPadMenu.addWidget(self.bGray)
        drawPadMenu.addWidget(self.bLoad)
        drawPadMenu.addWidget(self.bSave)
        drawPadMenu.addWidget(self.bUndo)
        drawPadMenu.addWidget(self.bRedo)

        drawPadLayout.addLayout(drawPadMenu)
        
        # Add instruction label
        self.instructionLabel = QLabel("Left-click: Add/Move point | Right-click: Remove point | Mouse wheel: Change brush size")
        self.instructionLabel.setWordWrap(True)
        self.instructionLabel.setStyleSheet("QLabel { font-size: 9pt; padding: 4px; color: #aaa; }")
        drawPadLayout.addWidget(self.instructionLabel)
        
        # Right side layout for result and reference with scroll
        rightScrollArea = QScrollArea()
        rightScrollArea.setWidgetResizable(True)
        rightScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        rightScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        rightScrollArea.setMinimumWidth(win_size + 40)
        
        rightWidget = QWidget()
        rightLayout = QVBoxLayout()
        rightWidget.setLayout(rightLayout)
        rightScrollArea.setWidget(rightWidget)
        mainLayout.addWidget(rightScrollArea, 1)
        
        # Result widget
        self.visWidget = gui_vis.GUI_VIS(win_size=win_size, scale=win_size / float(load_size))
        visWidgetLayout = self.AddWidget(self.visWidget, 'Result')
        rightLayout.addLayout(visWidgetLayout)

        self.bRestart = QPushButton("&Restart")
        self.bRestart.setToolTip('Restart the system')

        self.bQuit = QPushButton("&Quit")
        self.bQuit.setToolTip('Quit the system.')
        visWidgetMenu = QHBoxLayout()
        visWidgetMenu.addWidget(self.bRestart)
        visWidgetMenu.addWidget(self.bQuit)
        visWidgetLayout.addLayout(visWidgetMenu)
        
        # Add reference image below result
        self.referencePalette = gui_reference_colors.GUIReferenceColors(win_size=win_size)
        referenceLayout = self.AddWidget(self.referencePalette, 'Reference Image (Click to pick colors)')
        rightLayout.addLayout(referenceLayout)

        self.drawWidget.update()
        self.visWidget.update()
        # Connect button click
        self.colorPush.clicked.connect(self.drawWidget.change_color)
        
        # Connect color indicator signals
        self.drawWidget.update_color_signal.connect(self.colorPush.setStyleSheet)
        
        # Connect result update signals
        self.drawWidget.update_result_signal.connect(self.visWidget.update_result)
        self.visWidget.update_color_signal.connect(self.gamutWidget.set_ab)
        self.visWidget.update_color_signal.connect(self.drawWidget.set_color)
        
        # Connect gamut update signals
        self.drawWidget.update_gamut_signal.connect(self.gamutWidget.set_gamut)
        self.drawWidget.update_ab_signal.connect(self.gamutWidget.set_ab)
        self.gamutWidget.update_color_signal.connect(self.drawWidget.set_color)
        
        # Connect palette signals
        self.drawWidget.suggest_colors_signal.connect(self.customPalette.set_colors)
        self.customPalette.update_color_signal.connect(self.drawWidget.set_color)
        self.customPalette.update_color_signal.connect(self.gamutWidget.set_ab)
        
        self.drawWidget.used_colors_signal.connect(self.usedPalette.set_colors)
        self.usedPalette.update_color_signal.connect(self.drawWidget.set_color)
        self.usedPalette.update_color_signal.connect(self.gamutWidget.set_ab)
        
        # Connect preset palette signals
        self.presetPalette.update_color_signal.connect(self.drawWidget.set_color)
        self.presetPalette.update_color_signal.connect(self.gamutWidget.set_ab)
        
        # Connect reference palette signals
        self.referencePalette.update_color_signal.connect(self.drawWidget.set_color)
        self.referencePalette.update_color_signal.connect(self.gamutWidget.set_ab)
        self.referencePalette.auto_colorize_signal.connect(self.drawWidget.apply_color_points)
        self.drawWidget.grayscale_loaded_signal.connect(self.referencePalette.set_grayscale_image)
        # menu events
        self.bGray.setChecked(True)
        self.bRestart.clicked.connect(self.reset)
        self.bQuit.clicked.connect(self.quit)
        self.bGray.toggled.connect(self.enable_gray)
        self.bSave.clicked.connect(self.save)
        self.bLoad.clicked.connect(self.load)
        self.bUndo.clicked.connect(self.undo)
        self.bRedo.clicked.connect(self.redo)
        
        # Connect to update undo/redo button states
        self.drawWidget.update_result_signal.connect(self.update_undo_redo_buttons)

        self.start_t = time.time()

        if img_file is not None:
            self.drawWidget.init_result(img_file)

    def AddWidget(self, widget, title):
        widgetLayout = QVBoxLayout()
        widgetBox = QGroupBox()
        widgetBox.setTitle(title)
        vbox_t = QVBoxLayout()
        vbox_t.addWidget(widget)
        widgetBox.setLayout(vbox_t)
        widgetLayout.addWidget(widgetBox)

        return widgetLayout

    def nextImage(self):
        self.drawWidget.nextImage()

    def reset(self):
        # self.start_t = time.time()
        print('============================reset all=========================================')
        self.visWidget.reset()
        self.gamutWidget.reset()
        self.customPalette.reset()
        self.usedPalette.reset()
        self.drawWidget.reset()
        self.update()
        self.colorPush.setStyleSheet("background-color: grey")

    def enable_gray(self):
        self.drawWidget.enable_gray()

    def quit(self):
        print('time spent = %3.3f' % (time.time() - self.start_t))
        self.close()

    def save(self):
        print('time spent = %3.3f' % (time.time() - self.start_t))
        self.drawWidget.save_result()

    def load(self):
        self.drawWidget.load_image()

    def change_color(self):
        print('change color')
        self.drawWidget.change_color(use_suggest=True)
    
    def undo(self):
        """Undo last action"""
        if self.drawWidget.undo():
            self.update_undo_redo_buttons()
    
    def redo(self):
        """Redo last undone action"""
        if self.drawWidget.redo():
            self.update_undo_redo_buttons()
    
    def update_undo_redo_buttons(self):
        """Update undo/redo button states"""
        self.bUndo.setEnabled(self.drawWidget.can_undo())
        self.bRedo.setEnabled(self.drawWidget.can_redo())

    def keyPressEvent(self, event):
        # Check for Ctrl modifier
        ctrl_pressed = event.modifiers() & Qt.ControlModifier
        
        if ctrl_pressed and event.key() == Qt.Key_Z:
            # Ctrl+Z: Undo
            self.undo()
        elif ctrl_pressed and event.key() == Qt.Key_Y:
            # Ctrl+Y: Redo
            self.redo()
        elif ctrl_pressed and (event.key() == Qt.Key_R or event.key() == Qt.Key_Shift):
            # Ctrl+Shift+Z: Also redo
            if event.modifiers() & Qt.ShiftModifier:
                self.redo()
        elif event.key() == Qt.Key_R:
            self.reset()
        elif event.key() == Qt.Key_Q:
            self.save()
            self.quit()
        elif event.key() == Qt.Key_S:
            self.save()
        elif event.key() == Qt.Key_G:
            self.bGray.toggle()
        elif event.key() == Qt.Key_L:
            self.load()
        elif event.key() == Qt.Key_F11:
            # Toggle fullscreen
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
    
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # Update widgets if needed
        self.update()

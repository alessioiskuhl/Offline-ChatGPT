from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QDesktopWidget, QDialog, QCheckBox, QSpinBox
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QRect
import sys
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

#-----Create the Main window-----
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)
        self.setModal(True)  # Make the dialog modal (blocks interaction with other windows)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # Remove the title bar for the settings menu

        layout = QVBoxLayout()

        # Add a checkbox for enabling or disabling a setting
        self.checkbox = QCheckBox("Enable Some Feature", self)
        layout.addWidget(self.checkbox)

        # Add a spin box for numeric input (e.g., a volume setting)
        self.spinbox = QSpinBox(self)
        self.spinbox.setRange(0, 100)  # Example: range from 0 to 100
        self.spinbox.setValue(0)  # Default value
        layout.addWidget(QLabel("Volume Setting:"))
        layout.addWidget(self.spinbox)

        # Add more settings as needed (you can add more widgets)
        self.setLayout(layout)

    def get_settings(self):
        # Return the current settings when the dialog is closed
        return self.checkbox.isChecked(), self.spinbox.value()
    
class ResizableWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set initial window properties
        self.setWindowTitle("OffGPT") # Set the Window title
        self.setGeometry(100, 100, 269, 50)  # x, y, width, height
        self.setMinimumSize(269, 50)  # Optional: Set a minimum size
        self.setMaximumSize(400, 50)

        # Internal resolution (fixed)
        self.internal_width = 2550
        self.internal_height = 1440

        # Create a label for displaying content (e.g., game screen or UI)
        self.content_label = QLabel(self)
        self.content_label.setGeometry(0, 0, self.internal_width, self.internal_height)

        # Create a central widget and layout
        central_widget = QWidget(self)
        layout = QHBoxLayout(central_widget)

        # Create buttons
        self.button1 = QPushButton("Start Coaching", self)
        self.button2 = QPushButton("Stop Coaching", self)
        self.button3 = QPushButton("Settings", self)
        self.button4 = QPushButton("Close", self)

        # Apply a style using QSS (Qt Style Sheets)
        self.apply_tinytask_style(self.button1)
        self.apply_tinytask_style(self.button2)
        self.apply_tinytask_style(self.button3)
        self.apply_tinytask_style(self.button4)

        self.button3.clicked.connect(self.toggle_settings_dialog)  # Connect the button to the settings dialog

        # Add buttons to layout
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)

        self.setCentralWidget(central_widget)

        # Initialize settings_dialog as None to avoid uninitialized error
        self.settings_dialog = None

        def apply_style(self, button):
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;   /* Light gray background */
                    border: 1px solid #333;      /* Dark border for the button */
                    color: #333;                 /* Text color (dark gray) */
                    font-size: 9px;              /* Smaller font size */
                    padding: 5px 0px;            /* Padding for button size */
                    border-radius: 4px;          /* Rounded corners */
                }
                QPushButton:hover {
                    background-color: #e0e0e0;  /* Darken background on hover */
                }
                QPushButton:pressed {
                    background-color: #ccc;     /* Darken background further when pressed */
                }
            """)

            # set the background to be white
            self.setStyleSheet("background-color: white;")

        def resizeEvent(self, a0):
            # Get new window dimensions
            window_width = self.width()
            window_height = self.height()

            # Calculate aspect ratio to maintain resolution
            aspect_ratio = self.internal_width / self.internal_height

            # Adjust content size to fit the window while keeping the aspect ratio
            if window_width / window_height > aspect_ratio:
                # Window is wider than the content
                new_width = int(window_height * aspect_ratio)
                new_height = window_height
            else:
                # Window is taller than the content
                new_width = window_width
                new_height = int(window_width / aspect_ratio)

            # Center the content in the window
            x_offset = (window_width - new_width) // 2
            y_offset = (window_height - new_height) // 2

            self.content_label.setGeometry(x_offset, y_offset, new_width, new_height)

            # Call the parent class resizeEvent to ensure default behavior
            super().resizeEvent(a0)

        def paintEvent(self, a0):
            # Paint the background
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(255, 255, 255))
            super().paintEvent(a0)

        def toggle_settings_dialog(self):
            # Check if the settings dialog is already open
            if self.settings_dialog and self.settings_dialog.isVisible():
                self.settings_dialog.close()  # Close the dialog if it's already open
            else:
                # Create and show the settings dialog
                self.settings_dialog = SettingsDialog()

                # Set the dialog as non-modal
                self.settings_dialog.setModal(False)

                # Position the dialog relative to the button
                button_position = self.button3.mapToGlobal(self.button3.rect().topLeft())
                self.settings_dialog.move(button_position.x(), button_position.y() + self.button3.height())

                self.settings_dialog.show()

        def moveEvent(self, a0):
            # If the window is moved, close the settings dialog
            if self.settings_dialog and self.settings_dialog.isVisible():
                self.settings_dialog.close()

            # Call the parent class moveEvent to ensure default behavior
            super().moveEvent(a0)

        def closeEvent(self, a0):
            # Close the settings menu if its open
            if self.settings_dialog and self.settings_dialog.isVisible():
                self.settings_dialog.close()
            
            #Close the Main window
            super().closeEvent(a0)
        
        # Create a button inside the window
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close_window)  # Use a custom function
        close_button.resize(close_button.sizeHint())
        close_button.move(100, 50)  # Position the close button
    
        def close(self):
            return super().close()  # Close the window

# Main function
def main():
    app = QApplication(sys.argv)
    app.platformName()
    window = ResizableWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

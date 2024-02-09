import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateTimeEdit, QMessageBox
from PyQt5.QtCore import QTimer, QDateTime, QSize
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ClickerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set initial window size
        self.resize(500, 600)

        # Create layout
        layout = QVBoxLayout()

        # Time input
        self.time_label = QLabel("Target Time (with milliseconds):")
        self.time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss.zzz")
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_edit)

        # City Name input
        self.city_name_label = QLabel("City Name:")
        self.city_name_edit = QLineEdit("nursultan")
        layout.addWidget(self.city_name_label)
        layout.addWidget(self.city_name_edit)

        # School Name input
        self.school_name_label = QLabel("School Name:")
        self.school_name_edit = QLineEdit()
        layout.addWidget(self.school_name_label)
        layout.addWidget(self.school_name_edit)
        
        # Initial URL input
        self.url_label = QLabel("Initial Website URL:")
        self.url_edit = QLineEdit()
        default_city_name = "nursultan"
        default_url = f"https://indigo-{default_city_name}.e-orda.kz/ru/cabinet/request/list"
        self.url_edit.setText(default_url)  # Set default URL here
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)

        # Button Class Names (CSS Selectors)
        self.button_selectors = []
        default_classes = [
           ".btn.btn-success",
           ".btn.btn-indigo.btn-block.btn-need-disable",
           ".btn.btn-outline-indigo.mt-3.fp-select-place",
           ".btn.btn-indigo.ml-auto.link-to-disable"
        ]

        for i, default_class in enumerate(default_classes, start=1):
            selector_label = QLabel(f"Button {i} Class (CSS):")
            selector_edit = QLineEdit()
            selector_edit.setText(default_class)  # Set default class here
            layout.addWidget(selector_label)
            layout.addWidget(selector_edit)
            self.button_selectors.append(selector_edit)

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.on_start_clicked)
        layout.addWidget(self.start_button)

        # Set layout for the window
        self.setLayout(layout)

    def on_start_clicked(self):
        target_time = self.time_edit.dateTime().toPyDateTime()
        city_name = self.city_name_edit.text().strip().lower()  # Get the city name from the input and format it
        # Construct the URL using the city name with the 'indigo-' prefix
        initial_url = f"https://indigo-{city_name}.e-orda.kz/ru/cabinet/request/list"
        self.url_edit.setText(initial_url)  # Set the constructed URL in the URL input field

        # Initialize Selenium WebDriver and open the initial URL
        self.driver = webdriver.Chrome()  # or use webdriver.Firefox() if you prefer
        self.driver.get(initial_url)

        # Calculate the delay
        now = datetime.now()
        delay_ms = int((target_time - now).total_seconds() * 1000)

        # Set a timer to start the process at the specified time
        if delay_ms > 0:
            QTimer.singleShot(delay_ms, self.start_process)
        else:
            self.start_process()

    def start_process(self):
        print("Start Process")
        school_name = self.school_name_edit.text()  # Get the school name from the input
        search_text = f'Детский сад "{school_name}"'  # Construct the search text

        for i, selector in enumerate(self.button_selectors, start=1):
            css_selector = selector.text()
            try:
                # Wait for the button to be clickable
                WebDriverWait(self.driver, 70).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
                )
                
                # Click the button
                button = self.driver.find_element(By.CSS_SELECTOR, css_selector)
                button.click()
                print(f"Clicked button at {self.driver.current_url}")

                # After reaching the first screen
                if i == 1:  # Assuming you want to check after the first button click
                    # Check if the school name is in the page source
                    if search_text not in self.driver.page_source:
                        # School name not found
                        print("School name not found")
                        QMessageBox.warning(self, "Warning", "School name not found. Restarting...")
                        self.restart_program()
                        return

                # After reaching the third screen
                if i == 3:  # Assuming the third screen is after the third button click
                    # Find the section with the specific school name
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{search_text}')]")
                    # ... (Add actions to interact with the element or related elements as needed)

            except TimeoutException:
                # Handle the timeout exception by showing an error dialog
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle("Error")
                error_dialog.setText(f"Timeout occurred waiting for button {i} to be clickable.")
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.exec_()
                break  # Break the loop if a timeout occurs

            except Exception as e:
                # Handle other exceptions
                print(f"An error occurred on button {i}: {e}")
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle("Error")
                error_dialog.setText(f"An error occurred: {e}")
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.exec_()
        
    def restart_program(self):
        """Restarts the current program, with file objects and descriptors cleanup"""
        try:
            # Attempt to close the Selenium browser if open
            self.driver.quit()
        except Exception as e:
            print(f"Error closing the driver: {e}")

        # Restart the application
        python = sys.executable
        os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClickerApp()
    window.show()
    sys.exit(app.exec_())

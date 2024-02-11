
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


'packages': ['sys', 'os', 'PyQt5', 'selenium', 'datetime'],
}
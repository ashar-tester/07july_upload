from playwright.sync_api import sync_playwright, expect
import os, time

def test_keyboard_upload_download():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # -------------------------------
        # PART 1: KEYBOARD ACTIONS
        # -------------------------------
        page.goto("https://demoqa.com/text-box/")
        time.sleep(3)

        # Fill Full Name
        full_name = page.locator("#userName")
        full_name.fill("Ashar Zia")

        # Select all and copy
        full_name.press("Control+A")
        full_name.press("Control+C")

        # Move to Email field using Tab
        full_name.press("Tab")

        email = page.locator("#userEmail")

        # Paste into Email field
        email.press("Control+V")

        # Validation: Check copied text
        expect(email).to_have_value("Ashar Zia")

        # Press Tab to move forward
        email.press("Tab")

        # Press Enter to submit form
        page.keyboard.press("Enter")

        # -------------------------------
        # PART 2: FILE UPLOAD
        # -------------------------------
        page.goto("https://demoqa.com/upload-download")

        # Create a sample file dynamically
        file_path = os.path.abspath("sample.txt")
        with open(file_path, "w") as f:
            f.write("This is a test file")

        # Upload file
        upload_input = page.locator("#uploadFile")
        upload_input.set_input_files(file_path)

        # Validation: Check uploaded file name
        uploaded_text = page.locator("#uploadedFilePath")
        expect(uploaded_text).to_contain_text("sample.txt")

        # -------------------------------
        # PART 3: FILE DOWNLOAD
        # -------------------------------
        with page.expect_download() as download_info:
            page.click("#downloadButton")

        download = download_info.value

        # Save file locally
        download_path = os.path.join(os.getcwd(), download.suggested_filename)
        download.save_as(download_path)

        # Validation: File exists
        assert os.path.exists(download_path), "Download failed!"

        print("Download successful:", download_path)

        browser.close()


if __name__ == "__main__":
    test_keyboard_upload_download()
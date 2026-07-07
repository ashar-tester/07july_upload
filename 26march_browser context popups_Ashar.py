from playwright.sync_api import sync_playwright, expect


def test_browser_context(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])

    # Create two separate contexts (like 2 users)
    context1 = browser.new_context(no_viewport=True)
    context2 = browser.new_context(no_viewport=True)

    page1 = context1.new_page()
    page2 = context2.new_page()

    # Open same website
    url = "https://demoqa.com/text-box"
    page1.goto(url)
    page2.goto(url)

    # Perform different actions
    page1.fill("#userName", "User One")
    page2.fill("#userName", "User Two")

    # Validation → Data should not be shared
    expect(page1.locator("#userName")).to_have_value("User One")
    expect(page2.locator("#userName")).to_have_value("User Two")

    context1.close()
    context2.close()
    browser.close()


def test_popup_handling(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    page.goto("https://demoqa.com/browser-windows")

    # Handle popup (new window)
    with context.expect_page() as new_page_info:
        page.click("#windowButton")

    new_page = new_page_info.value
    new_page.wait_for_load_state()

    # Validation
    heading = new_page.locator("#sampleHeading")
    expect(heading).to_have_text("This is a sample page")

    browser.close()


def test_multiple_tabs(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context()

    # First tab
    page1 = context.new_page()
    page1.goto("https://the-internet.herokuapp.com/windows")

    # Open new tab
    page2 = context.new_page()
    page2.goto("https://demoqa.com")

    # Validation → correct URLs
    expect(page1).to_have_url("https://the-internet.herokuapp.com/windows")
    expect(page2).to_have_url("https://demoqa.com/")

    # Perform actions in both tabs
    page1.bring_to_front()
    expect(page1.locator("h3")).to_have_text("Opening a new window")

    page2.bring_to_front()
    expect(page2.locator(".home-banner")).to_be_visible()

    # Print all tabs
    print("\nOpened Tabs:")
    for p in context.pages:
        print(p.url)

    browser.close()


def main():
    with sync_playwright() as playwright:
        print("Running Browser Context Test...")
        test_browser_context(playwright)

        print("Running Popup Test...")
        test_popup_handling(playwright)

        print("Running Multiple Tabs Test...")
        test_multiple_tabs(playwright)


if __name__ == "__main__":
    main()
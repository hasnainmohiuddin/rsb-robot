from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF

from dotenv import load_dotenv
import os
import logging

# Load environment variables at the start
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='log.txt')

@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""
    try:
        browser.configure(
            slowmo=100,
        )
        logging.info("Browser configured successfully.")
        open_the_intranet_website()
        logging.info("Intranet website opened successfully.")
        log_in()
        logging.info("Logged in successfully.")
        download_excel_file()
        logging.info("Excel file downloaded successfully.")
        fill_form_with_excel_data()
        logging.info("Form filled with excel data successfully.")
        collect_results()
        logging.info("Results collected successfully.")
        export_as_pdf()
        logging.info("Data exported to PDF successfully.")
        log_out()
        logging.info("Logged out successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def open_the_intranet_website():
    """Navigates to the given URL"""
    try:
        browser.goto(os.getenv("WEBSITE_URL"))
    except Exception as e:
        logging.error(f"Failed to open the intranet website: {e}")

def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    try:
        page = browser.page()
        page.fill("#username", os.getenv("USERNAME"))
        page.fill("#password", os.getenv("PASSWORD"))
        page.click("button:text('Log in')")
    except Exception as e:
        logging.error(f"Login failed: {e}")

def fill_and_submit_sales_form(sales_rep):
    """Fills in the sales data and click the 'Submit' button"""
    try:
        page = browser.page()

        page.fill("#firstname", sales_rep["First Name"])
        page.fill("#lastname", sales_rep["Last Name"])
        page.select_option("#salestarget", str(sales_rep["Sales Target"]))
        page.fill("#salesresult", str(sales_rep["Sales"]))
        page.click("text=Submit")
    except Exception as e:
        logging.error(f"Failed to submit sales form: {e}")

def download_excel_file():
    """Downloads excel file from the given URL"""
    try:
        http = HTTP()
        http.download(url="https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True)
    except Exception as e:
        logging.error(f"Failed to download excel file: {e}")

def fill_form_with_excel_data():
    """Read data from excel and fill in the sales form"""
    try:
        excel = Files()
        excel.open_workbook("SalesData.xlsx")
        worksheet = excel.read_worksheet_as_table("data", header=True)
        excel.close_workbook()

        for row in worksheet:
            fill_and_submit_sales_form(row)
    except Exception as e:
        logging.error(f"Failed to fill form with excel data: {e}")

def collect_results():
    """Take a screenshot of the page"""
    try:
        page = browser.page()
        page.screenshot(path="output/sales_summary.png")
    except Exception as e:
        logging.error(f"Failed to collect results: {e}")

def export_as_pdf():
    """Export the data to a pdf file"""
    try:
        page = browser.page()
        sales_results_html = page.locator("#sales-results").inner_html()

        pdf = PDF()
        pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")
    except Exception as e:
        logging.error(f"Failed to export as PDF: {e}")

def log_out():
    """Presses the 'Log out' button"""
    try:
        page = browser.page()
        page.click("text=Log out")
    except Exception as e:
        logging.error(f"Failed to log out: {e}")
import argparse
import os
import logging
import requests

from scraper import scrape_products, scrape_url,  read_csv
from processor import process_products
from exporter import export_to_excel


# Configure logging
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(
        description="Python Data Automation & Reporting Tool"
    )

    parser.add_argument(
        "input_file",
        help="Path to a CSV, HTML file, or HTTP/HTTPS URL"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Data Automation Engine v1.0"
    )
    parser.add_argument(
        "--output",
        default="product-report.xlsx",
        help="Name of the Excel output file"
    )

    args = parser.parse_args()

    file_path = args.input_file
    output_file = args.output

    print("\n======================================")
    print("   PYTHON DATA AUTOMATION ENGINE")
    print("======================================")

    logger.info("Automation started")
    logger.info(f"Input file: {file_path}")
    logger.info(f"Output file: {output_file}")

    # -----------------------------------
    # CHECK FILE
    # -----------------------------------

    if not os.path.isfile(file_path):

        print("\n❌ ERROR: File not found.")
        print(f"File: {file_path}")
        print("Please check the file path.")

        logger.error(f"File not found: {file_path}")
        return

    # -----------------------------------
    # READ INPUT
    # -----------------------------------

    print("\n📂 Reading input file...")

    if file_path.lower().startswith(("http://", "https://")):

        try:
            products = scrape_url(file_path)

            logger.info("Web URL processed successfully")

        except requests.exceptions.RequestException as e:

            print("\n❌ ERROR: Could not access the webpage.")
            print(f"Reason: {e}")

            logger.error(f"URL request failed: {e}")
            return

    elif file_path.lower().endswith(".csv"):

        try:
            products = read_csv(file_path)

            logger.info("CSV file read successfully")

        except Exception as e:

            print("\n❌ ERROR: Could not read CSV file.")
            print(f"Reason: {e}")

            logger.error(f"CSV reading failed: {e}")
            return

    elif file_path.lower().endswith(".html"):

        try:
            products = scrape_products(file_path)

            logger.info("HTML file processed successfully")

        except Exception as e:

            print("\n❌ ERROR: Could not process HTML file.")
            print(f"Reason: {e}")

            logger.error(f"HTML processing failed: {e}")
            return

    else:

        print("\n❌ ERROR: Unsupported input.")
        print("Use a CSV file, HTML file, or HTTP/HTTPS URL.")

        logger.error("Unsupported input type")
        return

    # -----------------------------------
    # CHECK DATA
    # -----------------------------------

    if not products:

        print("\n❌ ERROR: No data found in input file.")

        logger.warning("No product data found")
        return

    print(f"✅ {len(products)} records collected.")

    logger.info(f"Records collected: {len(products)}")

    # -----------------------------------
    # PROCESS DATA
    # -----------------------------------

    print("\n⚙️ Cleaning and processing data...")

    try:

        (
            df,
            average_price,
            highest_price,
            lowest_price,
            total_records,
            valid_records,
            invalid_records
        ) = process_products(products)

        logger.info(
            f"Processing successful: "
            f"{valid_records} valid, "
            f"{invalid_records} invalid"
        )

    except Exception as e:

        print("\n❌ ERROR: Data processing failed.")
        print(f"Reason: {e}")

        logger.error(f"Data processing failed: {e}")
        return

    # -----------------------------------
    # DISPLAY RESULTS
    # -----------------------------------

    print("\n✅ DATA PROCESSING COMPLETED")

    print("\nProcessed Product Data:")
    print("-----------------------")
    print(df)

    print("\nStatistics:")
    print("-----------------------")
    print(f"Average Price : {average_price:.2f}")
    print(f"Highest Price : {highest_price:.2f}")
    print(f"Lowest Price  : {lowest_price:.2f}")

    print("\nData Cleaning Summary:")
    print("-----------------------")
    print(f"Total Records          : {total_records}")
    print(f"Valid Records          : {valid_records}")
    print(f"Invalid Records Removed: {invalid_records}")

    # -----------------------------------
    # EXPORT EXCEL
    # -----------------------------------

    print("\n📊 Generating Excel report...")

    try:

        export_to_excel(
            df,
            average_price,
            highest_price,
            lowest_price,
            total_records,
            valid_records,
            invalid_records,
            output_file
        )

        logger.info(f"Excel report created: {output_file}")

    except Exception as e:

        print("\n❌ ERROR: Could not create Excel report.")
        print(f"Reason: {e}")

        logger.error(f"Excel export failed: {e}")
        return

    # -----------------------------------
    # COMPLETED
    # -----------------------------------

    print("\n======================================")
    print("       AUTOMATION COMPLETED ✅")
    print("======================================")

    print(f"\n📄 Report: {output_file}")
    print("📝 Log: automation.log")

    logger.info("Automation completed successfully")


if __name__ == "__main__":
    main()
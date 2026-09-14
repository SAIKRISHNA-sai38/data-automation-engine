import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_products(file_path):
    """Read products from a local HTML file."""

    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()

    return extract_products(html)


def scrape_url(url):
    """Download a webpage and extract product information."""

    headers = {
        "User-Agent": "DataAutomationEngine/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return extract_products(response.text)


def extract_products(html):
    """Extract products from HTML content."""

    soup = BeautifulSoup(html, "html.parser")

    products = []

    for item in soup.select(".product"):

        name = item.select_one(".name")
        price = item.select_one(".price")

        if not name or not price:
            continue

        product_name = name.get_text(" ", strip=True)
        product_price = price.get_text(" ", strip=True)

        if not product_name:
            continue

        products.append({
            "name": product_name,
            "price": product_price
        })

    return products


def read_csv(file_path):
    """Read products from a CSV file."""

    df = pd.read_csv(file_path)

    return df.to_dict("records")
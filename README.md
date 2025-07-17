# Amazon_products_scraper
Overview
In this project, I created a web scraper to collect product information from Amazon. Since Amazon uses strong protection against bots—like IP blocking, user-agent checks, CAPTCHAs, JavaScript rendering, and behavior tracking—traditional tools like requests don’t work well.

Tools Used
To solve this, I used Playwright, a powerful browser automation tool that can fully load JavaScript-heavy pages, just like a real user. Once the page content was loaded, I used BeautifulSoup to extract product details from the HTML.

What It Extracts
The scraper collects the following product information:

Product Name

Price

Description

Product URL

Image URL

Output
All the scraped data is saved directly to a Google Sheet using the Google Sheets API and a service account. This makes the data easy to access, share, or use for further analysis.

Why This Approach
Using Playwright makes the scraper more reliable when dealing with websites like Amazon that use advanced anti-scraping methods. It ensures the content is loaded properly and helps avoid detection.

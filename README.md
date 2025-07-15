# Amazon_products
In this project, I built a scraper to extract product information from Amazon. Since Amazon uses advanced techniques to block bots like IP blocking, user-agent checks, CAPTCHA, JavaScript rendering, and behavioral detection using basic tools like requests doesn’t work.

To handle this, I used Playwright, a modern and powerful alternative to Selenium, which can load JavaScript-heavy pages just like a real browser. Once the page was fully loaded, I used BeautifulSoup to parse the HTML and extract the product details such as name, price, description, image URL, and product URL.

Finally, I saved all the scraped data into a Google Sheet using the Google Sheets API, making it easy to access and share.

This approach ensures reliable scraping even from a heavily protected site like Amazon.

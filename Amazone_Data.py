# imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
import time


num_count = 0
num_count1 = 0
print('..............scraping amazon product list in progress .............')
# Extract html data using playwright
def extract_data(url):
    storage_file = "amazon_storage.json"
    my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        if os.path.exists(storage_file):
            context = browser.new_context(
                storage_state=storage_file,
                user_agent = my_user_agent,      #user agent
                locale="fr-FR"
            )
        else:
            context = browser.new_context(
                user_agent = my_user_agent,    #user agent
                locale="fr-FR"
            )
        page = context.new_page()
        try:
            page.goto(url, timeout=6000000, wait_until="domcontentloaded")
        except Exception as e:
            print("Failed to load the page  ", str(e))
            return None
        page.wait_for_timeout(20000)
        html = page.content()
        if not html or "captcha" in html.lower():
            print("html content not found.it would be bocked or CAPTCHA encountered")
            return None

        if not os.path.exists(storage_file):
            context.storage_state(path=storage_file)

        context.close()
        browser.close()
    if html :
        return html
    else:
         print ('html is empty ! ')

# Extract product links
def extract_product_links(html):
    print("extracting product links ........")
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find_all('div', {'role': 'listitem'})
    for l in link:
        href = l.find('a').get('href')
        if href:
            base_link = 'https://www.amazon.fr'
            relative_link = href
            full_link = base_link + relative_link
            links.append(full_link)
        else:
            print('href not found')
    return links

# Extract product info
def extract_info(p_links):
        print(' wait until the info parsed and passed to google sheets,in progress...')
        global num_count1
        data_ = []
        total = len(p_links)
        if not p_links:
            print('data is empty')
        else:
            for link in p_links:
                time.sleep(2)
                html = extract_data(link)
                if not html:
                    print('empty html')

                else:
                    soup = BeautifulSoup(html, 'html.parser')
                    try:
                        name = soup.find('span', id='productTitle').get_text(strip = True)
                    except:
                        name = 'none'

                    product_url = link

                    try:
                        desc = soup.find('ul',class_='a-unordered-list a-vertical a-spacing-small').get_text(strip=True)
                    except:
                        desc = 'none'
                    try:
                        image_url = soup.find('div',id='imgTagWrapperId').find('img').get('src')
                    except:
                        image_url = 'none'
                    try:
                     price = soup.find('span',class_='a-price-whole').get_text(strip=True)
                    except:
                        price = 'price not found'


                    data = {'name' : name,
                            'product_url' : product_url,
                            'desc' : desc,
                            'image_url' : image_url,
                            'price' : price}
                    data_.append(data)
                    num_count1 += 1
                    print(f'watch {num_count1} data extracted (total {len(p_links)}.....')
            return data_

# this function run once it clear the sheets previous data and save headers to sheets.
def google_sheets():
    print('erasing google sheets previous data.............. ')
    print('adding  headers to google sheets............')
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    sheet_name = 'amazon-csv'

    creds = ServiceAccountCredentials.from_json_keyfile_name("keys.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    sheet.clear()
    headers = ["name", "description ", "price", "product_url", "image_url"]
    sheet.append_row(headers)
    return sheet


# Saving data like (name,price,description,product_url,image_url,) to google sheets
def add_sheet_data(data_set):
    print('data extracted successfully')
    print('adding product data to google sheets.............')

    global num_count
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    sheet_name = 'amazon-csv'
    if data_set :
        creds = ServiceAccountCredentials.from_json_keyfile_name("keys.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        for item in data_set:
            row = [
                item.get("name", ""),
                item.get("desc", ""),
                item.get("price", ""),
                item.get("product_url", ""),
                item.get("image_url", "")
            ]
            sheet.append_row(row)
            num_count += 1
            print(f"product {num_count} data saved successfully to google sheets! ")
    else:
        print('data set is empty ')


# INFO  to amazon s3
def amazon_s3():
    # needs credit card info to use service
    pass

def main():
    url = "https://www.amazon.fr/s?k=watches&rh=n%3A22623610031%2Cp_n_feature_thirty-two_browse-bin%3A96332143031%2Cp_36%3A20000-31000&dc&language=en&qid=1752346562&rnid=2492331031&ref=sr_nr_p_36_0_0"
    google_sheets()
    while url:
        html = extract_data(url)
        links = extract_product_links(html)
        data_set = extract_info(links)
        add_sheet_data(data_set)

        # use Pagination if needed...
        try:
            soup = BeautifulSoup(html,'html.parser')
            next_link = soup.find('ul',class_='a-unordered-list a-horizontal s-unordered-list-accessibility').find('a').get('href')
            if  next_link :
                url = 'https://www.amazon.fr' +  next_link
            else:
                print('No next link found!')
                break
        except Exception as e:
            print('pagination error',e)
            break


if __name__ == "__main__":
    main()

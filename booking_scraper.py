from playwright.sync_api import sync_playwright
import pandas as pd

def safe_inner_text(locator):
    try:
        return locator.inner_text(timeout=5000)
    except:
        return ""

def main():
    with sync_playwright() as p:
        checkin_date = '2025-06-23'
        checkout_date = '2025-06-24'
        adults = 2
        rooms = 1
        children = 0

        page_url = (
            f'https://www.booking.com/searchresults.en-gb.html?ss=New+Delhi%2C+India&lang=en-gb'
            f'&dest_id=-2106102&dest_type=city&checkin={checkin_date}&checkout={checkout_date}'
            f'&group_adults={adults}&no_rooms={rooms}&group_children={children}'
        )

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = safe_inner_text(hotel.locator('xpath=.//div[@data-testid="title"]'))
            hotel_dict['price'] = safe_inner_text(hotel.locator('xpath=.//span[@data-testid="price-and-discounted-price"]'))
            hotel_dict['score'] = safe_inner_text(hotel.locator('xpath=.//div[@data-testid="review-score"]/div[1]'))
            hotel_dict['avg review'] = safe_inner_text(hotel.locator('xpath=.//div[@data-testid="review-score"]/div[2]/div[1]'))
            
            reviews_count_text = safe_inner_text(hotel.locator('xpath=.//div[@data-testid="review-score"]/div[2]/div[2]'))
            hotel_dict['reviews count'] = reviews_count_text.split()[0] if reviews_count_text else ""

            hotels_list.append(hotel_dict)

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False)

        browser.close()

if __name__ == '__main__':
    main()

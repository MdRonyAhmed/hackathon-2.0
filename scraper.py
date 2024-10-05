import asyncio
from playwright.async_api import async_playwright
from time import sleep
from db import is_table_exist, execute_query, insert_data
import re

# Number of thread
CONCURRENT_LIMIT = 2

async def collect_post_details(context, keyword):
    all_info = []
    page = await context.new_page()
    await page.goto('https://www.tiktok.com/search/video')
    await page.wait_for_load_state('domcontentloaded')
    await page.type('input[type="search"]', keyword)
    await page.click('button[aria-label="Search"]')
    await page.wait_for_load_state('domcontentloaded')
    input("Captcha done?")
    for i in range(5):
        await page.mouse.wheel(0, 17000)
        sleep(3)

    video_elements = await page.locator('div[data-e2e="search_video-item-list"] >div').all()
    for element in video_elements:
        video_url = await element.locator('div[data-e2e="search_video-item"] a').get_attribute("href")
        caption = await element.locator('div[data-e2e="search-card-desc"] h1').inner_text()
        username = await element.locator('div[data-e2e="search-card-desc"] p[data-e2e="search-card-user-unique-id"]').inner_text()

        video_info = {
            "video_url": video_url,
            "video_caption": caption,
            "author_username": username
        }
        all_info.append(video_info)
        
    await page.close()
    # unique_video_urls = list(set(video_urls))
    return all_info

async def collect_auther_details(context, username, all_author_details, semaphore):
    async with semaphore:     
        page = await context.new_page()
        # page.on("response", intercept_response)
        await page.goto(f"https://www.tiktok.com/@{username}")        
        following_count = await page.locator('strong[data-e2e="following-count"]').inner_text()
        followers_count = await page.locator('strong[data-e2e="followers-count"]').inner_text()
        like_count = await page.locator('strong[data-e2e="likes-count"]').inner_text()

        author_info = {
            "username": username,
            "following_count": following_count,
            "follower_count": followers_count,
            "like_count": like_count
        }
        all_author_details.append(author_info)
        await page.close()

async def save_data(table_name, all_info=[]):
    is_exist = is_table_exist(table_name)
    if not is_exist:
        if table_name == "tiktok_post_details":
            sql_query = ''' CREATE TABLE tiktok_post_details (
                video_url VARCHAR, 
                video_caption VARCHAR,
                author_username VARCHAR
            )'''
            execute_query(sql_query)
        elif table_name == "author_info":
            sql_query = ''' CREATE TABLE author_info (
                username VARCHAR, 
                follower_count VARCHAR,
                following_count VARCHAR,
                like_count VARCHAR
            )'''
            execute_query(sql_query)

        elif table_name == "top_influencers_info":
            sql_query = ''' CREATE TABLE top_influencers_info (
                username VARCHAR, 
                follower_count VARCHAR,
                following_count VARCHAR,
                like_count VARCHAR
            )'''
            execute_query(sql_query)
    
    insert_data(table_name, all_info)             

def convert_to_number(value):
    if "k" in value.lower():
        value_from_string = re.findall(r'\d+',value)[-1]
        new_value = float(value_from_string) * 10000
    elif "m" in value.lower():
        value_from_string = re.findall(r'\d+',value)[-1]
        new_value = float(value_from_string) * 1000000
    else:
        new_value = float(value)
    
    return new_value
    

async def scrape_tiktok(search_input = []):
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)   # Limit the concurrency
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        )
        for keyword in search_input:
            videos_details = await collect_post_details(context= context, keyword= keyword)
            await save_data("tiktok_post_details", videos_details)
            all_author_details = []
            tasks = [collect_auther_details(context, video_detail["author_username"], all_author_details, semaphore) for video_detail in videos_details]
            await asyncio.gather(*tasks)
            if len(all_author_details) != 0:
                await save_data("author_info", all_author_details)

            top_influencers = []
            for author_info in all_author_details:
                follower = author_info["follower_count"]
                follower_number = convert_to_number(follower)
                like = author_info["like_count"]
                like_number = convert_to_number(like)

                if follower_number >= 1000000 and like_number >= 1000000:
                    top_influencers.append(author_info)

            print(len(top_influencers))
            if len(top_influencers) != 0:
                await save_data("top_influencers_info", top_influencers)
            

async def main():
    keywords_list = ["beautiful destinations", "places to visit", "places to travel", "places that don't feel real", "travel hacks"]
    await scrape_tiktok(keywords_list)

    hashtag_list = ["#traveltok", "#wanderlust", "#backpackingadventures", "#luxurytravel", "#hiddengems", "#solotravel", "#roadtripvibes", "#travelhacks", "#foodietravel", "#sustainabletravel"]
    await scrape_tiktok(hashtag_list)


if __name__ == '__main__':
    asyncio.run(main())
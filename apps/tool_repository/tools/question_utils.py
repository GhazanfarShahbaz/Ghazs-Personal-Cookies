from typing import List
from repository.model import CodingQuestion
from repository.coding_questions import CodingQuestionRepository
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import time


def setup_browser() -> Chrome:
    chrome_options: ChromeOptions = ChromeOptions()
    chrome_options.add_argument("'--disable-setuid-sandbox'")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = Chrome(
        executable_path="/home/dev_tools/chromedriver", options=chrome_options
    )
    return driver


def update_question_database() -> None:
    question_list: List[CodingQuestion] = CodingQuestionRepository().get(
        {}
    )  # get all current questions
    question_count: int = len(question_list)

    driver: Chrome = setup_browser()
    try:
        page_source: str = "https://leetcode.com/problemset/all/"
        driver.get(page_source)
        # time.sleep(5)
        soup: BeautifulSoup = BeautifulSoup(driver.page_source, features="html.parser")
        page_count: int = 1

        for page_count_button in soup.find_all(
            "button",
            class_="flex items-center justify-center w-8 h-8 rounded select-none focus:outline-none bg-fill-3 dark:bg-dark-fill-3 text-label-2 dark:text-dark-label-2 hover:bg-fill-2 dark:hover:bg-dark-fill-2",
        ):
            try:
                current_page_count: int = int(page_count_button.text.strip())
                page_count = max(page_count, current_page_count)
            except:
                pass

        page_source_w_count: str = "https://leetcode.com/problemset/all/?page="

        # for page in range(1, page_count+1):
        #     driver.get(f"{page_source_w_count}{page}")

        #     for row in soup.find_all("div", class_="odd:bg-overlay-3 dark:odd:bg-dark-overlay-1 even:bg-overlay-1 dark:even:bg-dark-overlay-3"):
        #         children = row.find_all_next(class_="mx-2 py-[11px]")
        #         # print(children[0][1].find_all_next("a"))
        #         print(children[10].find_all_next("a"))
        #         break
        #         # print(len(children))

        #     break

        # select = Select(driver.find_element_by_xpath('//select[@class = "fflex items-center rounded px-3 py-1.5 text-left cursor-pointer focus:outline-none whitespace-nowrap bg-fill-3 dark:bg-dark-fill-3 text-label-2 dark:text-dark-label-2 hover:bg-fill-2 dark:hover:bg-dark-fill-2 active:bg-fill-3 dark:active:bg-dark-fill-3'))
        # select.select_by_visible_text('100 / page')

    except Exception as e:
        driver.close()
        print(e)
    driver.close()

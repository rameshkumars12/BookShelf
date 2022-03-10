# importing the necessary libraries
import sys
import pandas as pd #For dataframe
from time import sleep #to sleep screen
from selenium import webdriver #for using selenium by webdriver
from selenium.webdriver.common.by import By #for using By commands ex:By.XPATH
from selenium.webdriver.common.keys import Keys #for sending keys
from Detect_Text import Book_Image


def book_scrapper(bookname):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    driver = webdriver.Chrome("chromedriver", options=options)

    #Getting the url
    url = "https://books.google.com/"
    driver.get(url)

    book = bookname

    #sending the search key using send_keys
    search = driver.find_element(By.XPATH, '//input[@title="Search Books"]')
    search_book = search.send_keys(book)
    search.send_keys(Keys.RETURN)

    try:
      link = driver.find_element(By.XPATH,'//*[@id="rso"]/div[1]/div[2]/a')
      link.send_keys(Keys.RETURN)
    except:
      return "No Book Found"

    try:
      close_pop = driver.find_element(By.XPATH, '//*[@id="cIFTzb"]/div/span').click()
    except:
      pass


    contents = driver.find_elements(By.XPATH, '//div[@class="zloOqf PZPZlf"]//span[2]')



    book_data = {}
    book_title = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[1]').text
    book_data["Title: "] = book_title
    for index,content in enumerate(contents):
        content = content.text
        #print(index, content)
        if index == 1:
            numbofpages = content
            book_data["Number of Pages"] = numbofpages
        elif index == 5:
            language = content
            book_data["Language"] = language

        elif index == 6:
            author = content
            book_data["Author"] = author
        elif index == 7:
            publishedin = content
            book_data["Published in"] = publishedin

        elif index == 8:
            genre = content
            book_data["Genre"] = genre

    df = pd.DataFrame([book_data])
    df = df.to_html(justify="center")
    return df
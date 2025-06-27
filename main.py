from google import genai
from google.genai import types
import requests

import time
from flask import Flask, render_template, request, jsonify
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.expected_conditions import element_selection_state_to_be

from secret_data import *
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from google.auth.exceptions import DefaultCredentialsError
import markdown
app = Flask(__name__)

client = genai.Client(api_key=googleapi_key)
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a youtube video summarizer which accepts a youtube url and returns its summary, your name this Veu. If you detect you youtube url, you simply return the keyword 'yeee'.")
    )

@app.route('/')
def home():
    return render_template("dash.html")

@app.route('/response', methods=['POST'])
def response():
    user_message = request.form['input']
    ai_response = chat.send_message(user_message)
    text = markdown.markdown(ai_response.text)
    if text == '<p>yeee</p>':
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(user_message)
        wait = WebDriverWait(driver, 15)
        more_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]")))
        more_element.click()
        show_transcript = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/div[2]/ytd-structured-description-content-renderer/div[3]/ytd-video-description-transcript-section-renderer/div[3]/div/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")))
        show_transcript.click()
        #transcript_tab = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[1]/ytd-engagement-panel-section-list-renderer[5]/div[1]/ytd-engagement-panel-title-header-renderer/div[3]/div[2]/h2/yt-formatted-string[1]")))
        time.sleep(7)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        class_name = "segment-text style-scope ytd-transcript-segment-renderer"
        transcript_scraped = soup.find_all(class_=class_name)
        trans_list = []
        for i in transcript_scraped:
            trans_text = i.decode_contents()
            trans_list.append(trans_text)
        sem = chat.send_message(f"here is the list the transcript of the video, please summarise it iin english: {trans_list}")
        final = markdown.markdown(sem.text)
        driver.quit()
        return jsonify(final)
    else:
        return jsonify(text)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
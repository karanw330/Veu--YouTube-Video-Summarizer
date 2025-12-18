from urllib.parse import uses_query
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
import threading
import time
from flask import Flask, render_template, request, jsonify
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from secret_data import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import markdown

import asyncio
from websockets.asyncio.server import serve

app = Flask(__name__)

ws_loop = None

ytt_api = YouTubeTranscriptApi()
client = genai.Client(api_key=googleapi_key1)
chat = client.chats.create(
            model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a youtube video summarizer which accepts a youtube url and returns its summary, your name this Veu. If you detect you youtube url, you simply return the keyword 'yeee'.")
)

clients = set()

async def hello(ws):
    clients.add(ws)
    try:
        await ws.wait_closed()
    finally:
        clients.remove(ws)

async def func_stream(trans_list):
    for ws in clients:
        sem = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=f"here is the list the transcript of the video, please summarise it in english {trans_list}, respond in html only, do not use markdown, Use <p>, <ul>, <li>, <strong>, <em> where appropriate.",
        )
        for chunk in sem:
            final = markdown.markdown(chunk.text)
            print(final)
            await ws.send(final)
            # print(chunk.text, end="")

def run_ws_server():
    global ws_loop
    ws_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(ws_loop)

    async def main():
        async with serve(hello, "localhost", 8765):
            await asyncio.Future()

    ws_loop.run_until_complete(main())

def trans_api(url):
    lis = url.split("v=")
    trans_list = []
    trans = ytt_api.fetch(lis[1])
    for snippet in trans:
        trans_list.append(snippet.text)
    return trans_list

def scrapeTranscript(user_message):
    options = Options()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(user_message)
    wait = WebDriverWait(driver, 15)
    try:
        more_element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                  "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]")))
        more_element.click()
        print("more clicked")
    except Exception as e:
        print("more failed")

    try:
        show_transcript = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/div[3]/ytd-structured-description-content-renderer/div[4]/ytd-video-description-transcript-section-renderer/div[3]/div/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div[2]")))
        show_transcript.click()
        print("show clicked")
    except Exception as e:
        print("show transcript failed")
    # transcript_tab = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[1]/ytd-engagement-panel-section-list-renderer[5]/div[1]/ytd-engagement-panel-title-header-renderer/div[3]/div[2]/h2/yt-formatted-string[1]")))
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ytd-transcript-segment-renderer")
        )
    )
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    class_name = "segment-text style-scope ytd-transcript-segment-renderer"
    transcript_scraped = soup.find_all(class_=class_name)
    print(transcript_scraped)
    trans_list = []
    for i in transcript_scraped:
        trans_text = i.decode_contents()
        trans_list.append(trans_text)
    driver.quit()
    return trans_list
@app.route('/')
def home():
    return render_template("dash.html")

@app.route('/response', methods=['POST'])
def response():
    user_message = request.form['input']
    ai_response = chat.send_message(user_message)
    print(user_message)
    text = markdown.markdown(ai_response.text)
    if text == '<p>yeee</p>':
        li = trans_api(user_message)
        asyncio.run_coroutine_threadsafe(
            func_stream(li),
            ws_loop
        )
        return jsonify("")
    else:
        return jsonify(text)


if __name__ == "__main__":
    _thread = threading.Thread(target=run_ws_server, daemon=True)
    _thread.start()
    app.run(port=5003)

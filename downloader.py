import asyncio
from pyppeteer import launch
import time
import pyautogui
from screeninfo import get_monitors
from pydub import AudioSegment
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import os

async def downloadMp3(url, directory):
    print("--------------------------------------------------")
    print(f"Downloading: {url}")
    browser = await launch(headless=False)  # Launch Chromium in non-headless mode
    page = await browser.newPage()
    print("Browser is opened")

    await page.goto(url)
    monitors = get_monitors()
    await page.setViewport({'width':  monitors[0].width, 'height': monitors[0].height})
    
    await asyncio.sleep(2)
    pyautogui.hotkey('win', 'up')   
    

    duration_element = await page.querySelector('.ytp-time-duration')
    video_title_element = await page.querySelector('.title.style-scope.ytd-video-primary-info-renderer')
    if video_title_element:
        video_title = await page.evaluate('(element) => element.textContent', video_title_element)

    if duration_element:
        video_duration = await page.evaluate('(element) => element.textContent', duration_element)
        vd_split = video_duration.split(':')
        video_seconds = int(vd_split[1]) + (int(vd_split[0]) * 60)

    btnAcceptCookies = await page.xpath("//button[contains(., 'Accept all')]")
    if btnAcceptCookies:
        await btnAcceptCookies[0].click()
    

    ad_button_element = await page.querySelector('.ytp-ad-btn')
    while ad_button_element:
        ad_button_element = await page.querySelector('.ytp-ad-btn')
        await asyncio.sleep(1)
        print("Skippping ad ...")

    print("Starting recording")
    fs = 44100
    input_device = 3
    recording = sd.rec(int((video_seconds+2) * fs), samplerate=fs, channels=2, device=input_device)

    sd.wait()

    samples_to_keep = int(fs * 2)
    recording = recording[samples_to_keep:]

    desired_gain_dB = 10
    desired_gain = 10 ** (desired_gain_dB / 20.0)
    recording *= desired_gain

    print(f"Succesfully recorded mp3 file in {video_duration}")
    await browser.close()
    print("Closeing browser")
    print("Downloading...")
    # Export the audio to an MP3 file
    output_filename = f"{directory}{video_title}.wav"
    finalName = f"{directory}{video_title}.mp3"

    write(output_filename, fs, recording)
    wav_file = AudioSegment.from_wav(output_filename)
    wav_file.export(finalName, format="mp3")
    os.remove(output_filename)

    print(f"Audio exported to '{finalName}'")
    print("Process finished")
import speech_recognition as sr  # for recognising the voice

import pyttsx3  # for text to speech conversion

import webbrowser  # for opening the site
import datetime
import wikipedia  # for searching article on wikipedia
import pywhatkit  # for searching in YouTube using voice command
import os  # for making some directories
import openai  # for AI capabilities

from my_key import apikey

listener = sr.Recognizer()  # let's create a recognizer that will recognize our voice

engine = pyttsx3.init()  # to initialize pytts let's create a variable that will change voice into text


def say(text):  # this function will help us in speaking the text that we provided in it
    engine.say(text)
    engine.runAndWait()


def take_command():
    with sr.Microphone() as source:  # it uses microphone as a source for voice command
        print("listening...")
        voice = listener.listen(source)  # voice variable store the input audio in it
        # listener.pause_threshold = 1
    try:
        print("Recognizing...")
        query = listener.recognize_google(voice, language='en-in')  # query store texts of input audio
        query = query.lower()
        print('recognized..!')
        print(f'user said: {query}')
        return query  # returning texts of input audio

    except:
        return 'Sorry ! Some Error Occurred.'  # In-case of failure of voice recognition


def ai(prompt):  # it uses OpenAi gpt-3 model for generating response to prompt
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt}\n***********\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        print(response['choices'][0]['text'])
        text += response['choices'][0]['text']  # result
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        # creating new text file in Openai directory and named it according to the provided prompt
        with open(f"Openai/{''.join(query.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)  # saving information in text file
    except:
        print("Something went wrong in fetching the data from response")


# this is all about the function that we defined
# let's come to the main part and run it one by one

if __name__ == "__main__":
    say("Hello I am your A.I. Assistant, What can i do for you...")  # for greet
    query = take_command()
    # say(query)

    sites = [['youtube', "https://www.youtube.com"], ['wikipedia', "https://www.wikipedia.com"],
             ['google', "https://www.google.com"], ['techno', 'https://www.techno-dexterous.com']]

    for site in sites:  # let's open site
        if f'open {site[0]}'.lower() in query.lower():
            say(f'opening {site[0]} ...')
            print(f'opening {site[0]} ...')
            webbrowser.open(site[1])

    if 'time' in query:  # know current time
        time = datetime.datetime.now().strftime("%I:%M %p")  # for 12hr format
        print(f"Sir the current time is {time}")
        say(f"Sir the current time is {time}")

    elif 'search' in query:  # search for any person or thing in wikipedia
        query = query.replace('search', '')
        info = wikipedia.summary(query, 1)  # 1 for get summary in one line
        print(info)
        say(info)

    elif 'play' in query:  # play any song in YouTube
        song = query.replace('play', '')
        say('playing' + song)
        print(song)
        pywhatkit.playonyt(song)

    elif "artificial intelligence".lower() in query.lower():  # let's command A.I. to do some work
        query1 = query.replace('use artificial intelligence','')
        print(query1)
        ai(prompt=query1)

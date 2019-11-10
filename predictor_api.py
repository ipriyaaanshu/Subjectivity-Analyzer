import pickle
import numpy as np
from sklearn.externals import joblib
import re

model_dict = joblib.load('./static/models/log_models.p')
word_vectorizer = joblib.load('static/models/log_word_vectorizer.p')

cl_path = 'static/cleaning/clean_letters.txt'

clean_word_dict = {}
with open(cl_path, 'r', encoding='utf-8') as cl:
    for line in cl:
        line = line.strip('\n')
        typo, correct = line.split(',')
        clean_word_dict[typo] = correct


def clean_word(text):
    replace_numbers = re.compile(r'\d+', re.IGNORECASE)
    special_character_removal = re.compile(r'[^a-z\d ]', re.IGNORECASE)

    text = text.lower()

    for typo, correct in clean_word_dict.items():
        text = re.sub(typo, " " + correct + " ", text)

    return text


def raw_chat_to_model_input(raw_input_string):
    from django import forms
    import newspaper
    try:
        f = forms.URLField()
        html = f.clean(raw_input_string)
        a = newspaper.Article(html)
        a.download()
        a.parse()
        raw_input_string = a.text
    except:
        raw_input_string = raw_input_string

    cleaned_text = []
    for text in [raw_input_string]:
        cleaned_text.append(clean_word(text))
    return word_vectorizer.transform(cleaned_text), raw_input_string


def predict_toxicity(raw_input_string):
    ''' Given any input string, predict the toxicity levels'''
    model_input, raw_input_string_ = raw_chat_to_model_input(raw_input_string)

    import requests
    subscription_key = '17fb8beb23724ed1a3c0a7e2af52abdf'
    sentiment_url = 'https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/sentiment'
    sentiment = 0
    try:
        documents = {"documents": [
            {"id": 1, "language": "en",
             "text": raw_input_string_}]}
        if len(raw_input_string_) != 0:
            headers = {"Ocp-Apim-Subscription-Key": subscription_key}
            response = requests.post(sentiment_url, headers=headers, json=documents)
            sentiments = response.json()
            sentiment = sentiments['documents'][0]['score']
    except:
        print(' ')

    results = []
    for key, model in model_dict.items():
        results.append(round(model.predict_proba(model_input)[0, 1], 3))
    return results, sentiment


def make_prediction(input_chat):
    if not input_chat:
        input_chat = ' '

    pred_probs, sentiment = predict_toxicity(input_chat)

    probs = [{'name': list(model_dict.keys())[index], 'prob': pred_probs[index]}
             for index in np.argsort(pred_probs)[::-1]]

    if sentiment < 0.50:
        probs.append({'name': 'sentiment', 'prob': sentiment})
    else:
        probs.append({'name': 'sentiment', 'prob': sentiment})

    return (input_chat, probs)

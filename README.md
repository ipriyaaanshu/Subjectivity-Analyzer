# Subjectivity

### MORE DATA AT https://drive.google.com/open?id=1ckAQ7s5hLe1_ElUK3m26e_91Z9_gsL5I

## Inspiration
Surfing Web is never safe, there is so much that we can read, watch, and learn but still there are scenarios where hateful and fake articles spread hate and disturb the peace. We wanted to build something that is easy and can act as a defense or warning for such content.

## What it does
This project aims at providing a way to score web pages, people can simply enter any text or URL and our Analyzer will easily analyze the text for any **toxic or hateful** content.

## How we built it
We used a combination of Azure's Text Analytics API and our custom-built Spacy Named Entity Recognition model to identify the core entities and topics mentioned in that web-page or text.
It runs on a Flask Server and can easily be scaled with services like AWS Lambda

## Accomplishments that we're proud of
It was really hard to train a Named Entity Recognition model in such a short time but GCP helped us achieve that goal. We are not very proficient with front-end and UI stuff but it was an awesome experience learning how to integrate our backend functionalities with UI and improve user experience.

## What's next for Subjectivity Analyzer
This is definitely not a finished product, we would like to create a background service that automatically analyzes the content you browse for toxicity and obscene content and warn you if certain thresholds are exceeded.

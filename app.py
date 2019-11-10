from flask import Flask,render_template,url_for,request
import re
import pandas as pd
import spacy

from predictor_api import make_prediction
nlp = spacy.load('model')

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		#choice = request.form['taskoption']
		rawtext = request.form['rawtext']
		doc = nlp(rawtext)
		subjectivity = make_prediction(rawtext)
		if subjectivity[1][-1]['prob'] >0.6:
			subjectivity[1][-1]['prob'] = 'POSITIVE'
		if subjectivity[1][-1]['prob'] <0.6 and subjectivity[1][-1]['prob'] >0.35:
			subjectivity[1][-1]['prob'] = 'NEUTRAL'
		else:
			subjectivity[1][-1]['prob'] = 'NEGATIVE'
		
		res = []
		subj = []
		for item in subjectivity[1]:
			if item['name'] == 'sentiment':
				subj.append({item['name']: item['prob']})
			else:
				subj.append({item['name']: str(round(item['prob']*10000,2))+'%'})
		d = []
		for ent in doc.ents:
			d.append({"Text": ent.text , "Entity": ent.label_})

	return render_template("index.html",text = subjectivity[0], subjectivity=subj, entities=d,num_of_results = len(d))


if __name__ == '__main__':
	app.run(host='127.0.0.1', debug=False,port=5000)

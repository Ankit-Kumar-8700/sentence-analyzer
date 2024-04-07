from flask import Flask, render_template, request
import language_tool_python
import spacy
from spacy.lang.en.stop_words import STOP_WORDS


app = Flask(__name__)

nlp=spacy.load("en_core_web_sm")

def preprocess(text):
    doc=nlp(text)
    ners=[]
    pos=[]
    for token in doc.ents:
      ners.append([token,token.label_,spacy.explain(token.label_)])
    for token in doc:
      if token.pos_:
        pos.append([token,token.pos_,spacy.explain(token.tag_)])
    no_stop_words=[token.text for token in doc if not token.is_stop and not token.is_punct]
    return no_stop_words,ners,pos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    text_to_check = request.form['text']
    # Use the language-tool-python library to check grammar and spelling
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text_to_check)

    ans=tool.correct(text_to_check)

    tokens,NER,POS=preprocess(ans)

    # print(tokens)

    return render_template('results.html', text=text_to_check, final_output=ans, matches=matches, tokens=tokens, ner=NER, pos=POS)

if __name__ == '__main__':
    app.run(debug=True)

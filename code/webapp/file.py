from flask import Flask, redirect, url_for, render_template, request
import difflib
from gector.model import load_model
from gector.predict import predict_for_string
import spacy
from nltk.tokenize.treebank import TreebankWordDetokenizer

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict")
def predict():
    model = load_model(vocab_path='./gector/data/output_vocabulary/',
                   model_paths=['./static/nn_models/xlnet_0_gector.th'],
                   model_name="xlnet")
    user_input = request.args.get('jsdata')
    print("'user input'", user_input)
    tokenized_string = tokenize(user_input)
    print("'model input'", tokenized_string)
    corrected_text = predict_for_string(tokenized_string, model)
    print("'model output'", corrected_text)
    output_text = untokenize(corrected_text)
    print("'user output'", output_text)
    return show_diff(user_input, output_text)


def tokenize(text):
    """
    input plain text string,
    outputs tokenized string with spaces
    """
    doc = nlp(text)
    return " ".join([token.text for token in doc])


def untokenize(tokens):
    """
    input tokenized string with spaces
    outputs plain text string
    """
    return TreebankWordDetokenizer().detokenize(tokens.split(" "))


def show_diff(text, n_text):
    """
    compares two strings
    gives the correct css classes accordingly
    """
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append('<span class="delta-insert">' + seqm.b[b0:b1] + '</span>')
        elif opcode == 'delete':
            output.append('<span class="delta-delete">' + seqm.a[a0:a1] + '</span>')
        elif opcode == 'replace':
            output.append('<span class="delta-replace">' + seqm.b[b0:b1] + "</span>")
        else:
            raise RuntimeError("unexpected opcode")
    return ''.join(output)


if __name__ == "__main__":
    app.run(debug = True)
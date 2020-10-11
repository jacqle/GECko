from flask import Flask, redirect, url_for, render_template
from gector.model import load_model
from gector.predict import predict_for_string
# model dl link: https://grammarly-nlp-data-public.s3.amazonaws.com/gector/bert_0_gector.th

app = Flask(__name__) 
model = load_model(vocab_path='./gector/data/output_vocabulary/',
                   model_paths=['/home/leo/nlp/software_project/bert_0_gector.th'])

s = """It 's difficult answer at the question " what are you going to do in the future ? "
         if the only one who has to know it is in two minds ."""
print(predict_for_string(s, model))


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
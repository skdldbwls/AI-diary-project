from flask import Flask, render_template, request
import pickle
import numpy as np

model = pickle.load(open('mbti.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    #데이터 받기
    data1 = request.form['content']

    #데이터 전처리
    titles = ["Extraversion (E) - Introversion (I)",
              "Sensation (S) - INtuition (N)",
              "Thinking (T) - Feeling (F)",
              "Judgement (J) - Perception (P)"
              ]
    b_Pers = {'E': 0, 'I': 1, 'S': 0, 'N': 1, 'T': 0, 'F': 1, 'J': 0, 'P': 1}
    b_Pers_list = [{0: 'E', 1: 'I'}, {0: 'S', 1: 'N'}, {0: 'T', 1: 'F'}, {0: 'J', 1: 'P'}]

    # transform mbti to binary vector
    def translate_personality(personality):
        return [b_Pers[l] for l in personality]

    # transform binary vector to mbti personality
    def translate_back(personality):
        s = ""
        for i, l in enumerate(personality):
            s += b_Pers_list[i][l]
        return s

    list_personality_bin = np.array([translate_personality(p) for p in mydata.type])

    #예측
    pred = model.predict(data1)

    #예측결과 보내기
    return render_template('after.html', data=pred)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
popular_books=pickle.load(open('models/popular.pkl','rb'))
pt = pickle.load(open('models/pt.pkl','rb'))
books = pickle.load(open('models/books.pkl','rb'))
similarity_scores = pickle.load(open('models/similarity_scores.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_books['Book-Title'].values),
                           author = list(popular_books['Book-Author'].values),
                           image = list(popular_books['Image-URL-M'].values),
                           votes = list(popular_books['num_ratings'].values),
                           rating = list(popular_books['avg_rating'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)
    return render_template('recommend.html',data=data)
print(pd.__version__)
if __name__=='__main__':
    app. run(debug=True)
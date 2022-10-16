from flask import Flask, render_template, request, jsonify, json, redirect, url_for
import pandas as pd
import sqlite3
import requests
import logging


app = Flask(__name__)
logging.basicConfig(filename='logs/tool_requests.log', level=logging.DEBUG)


# data for reccomendations
movies_data = pd.read_csv(
    "/home/ghaz/flask_gateway/apps/projects/the_mouseion/static/csv/DataforMovies.csv")
books_data = pd.read_csv(
    "/home/ghaz/flask_gateway/apps/projects/the_mouseion/static/csv/Data_for_Books.csv")
games_data = pd.read_csv(
    "/home/ghaz/flask_gateway/apps/projects/the_mouseion/static/csv/DataForGames.csv")

movies_key = '29774b2346f22d1b825fb697d82d2874'

game_headers = {
    'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
    'x-rapidapi-key': "88069e2e70msh00617b3e7f93fc3p10dbd7jsnca441d3f8cd8"
}

# opens up the userPage when the app starts


@app.route('/')
def index():
    return render_template('userPage.html')


@app.route('/home')
def home():
    return render_template('userPage.html')

# Leads to the book reccomendation page


@app.route('/bookReccomendation')
def bookPage():
    return render_template('bookReccomendation.html')

# leads to movie reccomendation page


@app.route('/movieReccomendation')
def moviePage():
    return render_template("movieReccomendation.html")

# Leads to the game reccomendation page


@app.route('/gameReccomendation')
def gamePage():
    return render_template("videoGameReccomendation.html")

# leads to login page


@app.route('/login')
def loginPage():
    return render_template("index.html")

# reccomends books to user based on what they searched and clicked


@app.route('/recc', methods=['GET', 'POST'])
def get_divinfo():
    bookName = request.args.get("book_name")
    data = pd.read_csv("static/csv/Data_for_Books.csv")

    thisBookData = data[data.Book_Title == bookName]

    rating = float(thisBookData.Average_Rating.values[0])
    averageAge = float(thisBookData.Average_Age.values[0])
    yearpublished = int(thisBookData.Year_Published.values[0])
    totalRating = int(thisBookData.Total_Rating.values[0])

    # Finds closest books to the book picked
    ReccomendedBook = data[(abs(data['Average_Rating']-rating) <= .5)
                           & (abs(data['Year_Published']-yearpublished) <= 5)
                           & (abs(data['Year_Published']-yearpublished) <= 5)
                           & (abs(data['Total_Rating']-totalRating) <= 400)]

    bestBook = ReccomendedBook.iloc[:3]
    book_names = []
    book_url = []
    book_authors = []
    for books in range(3):
        bookName = str(bestBook.iloc[[books]].Book_Title)
        bookUrl = str(bestBook.iloc[[books]].Link_To_Image)
        bookAuthor = str(bestBook.iloc[[books]].Book_Author)

        bookName = bookName[2:bookName.find("Name")]
        bookUrl = bookUrl[2:bookUrl.find("Name")]
        bookAuthor = bookAuthor[2:bookAuthor.find("Name")]

        book_names.append(bookName)
        book_url.append(bookUrl)
        book_authors.append(bookAuthor)

    bestBookName = (str(bestBook.Book_Title))
    bestBookName = bestBookName[2:bestBookName.find("Name")]

    bestBookUrl = str(bestBook.Link_To_Image)
    bestBookUrl = bestBookUrl[2:bestBookUrl.find("Name")]

    bookInfo = {'Book_Name': book_names,
                "Url": book_url, "Book_Author": book_authors}
    return bookInfo

# reccomends movies to user based on whats searched


@app.route('/movieRecc')
def getMovieReccomendation():
    movie_name = request.args.get('movie_name')
    this_movie_data = movies_data[movies_data.title == movie_name]

    bestRecc = movies_data[(movies_data['genres'] == this_movie_data.genres.values[0]) &
                           (abs(movies_data['year'] - float(this_movie_data.year.values[0])))]
    bestRecc['Comparison'] = abs(
        bestRecc['Average_Rating'] - float(this_movie_data.Average_Rating.values[0]))
    bestRecc = bestRecc[bestRecc['Comparison'] < 1.5]
    bestRecc.drop(bestRecc[bestRecc['title'] ==
                  movie_name].index, inplace=True)
    bestRecc.sort_values(by='Comparison', ascending=True, inplace=True)

    bestRecc = bestRecc.iloc[:3]
    movie_names = []
    movies_imdb = []
    for x in range(3):
        movie_names.append(str(bestRecc.iloc[[x]].title.values))
        movies_imdb.append(str(bestRecc.iloc[[x]].imdbId.values))

    moviesInfo = {
        "movie_name": movie_names,
        "movie_id": movies_imdb
    }
    # This doesn't work well, maybe use cosine_similarity in the future
    # For the future, imdb has its own data set online

    return moviesInfo


@app.route('/gameSearch')
def gameSearch():
    # turns response to json
    responseDict = requests.request(
        "GET", f"https://rawg-video-games-database.p.rapidapi.com/games?search={request.args.get('search')}", headers=game_headers).json()

    info = {}
    info['game_info'] = []

    # parses data and adds to dictionary list
    for data in responseDict['results']:
        specific_information = requests.request(
            "GET", f"https://rawg-video-games-database.p.rapidapi.com/games/{data['slug']}", headers=game_headers).json()

        platforms = []

        for x in data['platforms']:
            platforms.append(x['platform']['name'])

        publisher = ""
        try:
            publisher = specific_information['publishers'][0]['name']
        except:
            continue
        else:
            publisher = specific_information['publishers'][0]['name']

        info['game_info'].append({
            "game_name": data['name'],
            "game_rating": data['rating'],
            "game_ratings_count": data['ratings_count'],
            "game_platforms": platforms,
            "game_image": data['background_image'],
            "game_description": specific_information['description_raw'],
            "game_publisher": publisher
        })

    return info

# reccomends games based on what users clicks on


@app.route('/gameRecc')
def gameRecc():

    game_name = request.args.get('game_name')

    game_data = games_data[games_data['Name'] == game_name]

    find_match = games_data[(games_data['Genre'] == game_data.Genre.values[0]) &
                            (games_data['Rating'] == game_data.Rating.values[0]) &
                            (abs(games_data['Year_of_Release'] - game_data['Year_of_Release'].values[0]) <= 5.0) &
                            (abs(games_data['Global_Sales'] - game_data['Global_Sales'].values[0]) <= 60) &
                            (abs(games_data['Critic_Score'] - game_data['Critic_Score'].values[0]) <= 5) &
                            (abs(games_data['User_Score'] - game_data['User_Score'].values[0]) <= 5) &
                            (abs(games_data['Critic_Count'] - game_data['Critic_Count'].values[0]) <= 200) &
                            (abs(games_data['User_Count'] - game_data['User_Count'].values[0]) <= 10000)]

    find_match.drop(find_match[find_match['Name'] ==
                    game_data.Name.values[0]].index, inplace=True)

    # find_match = find_match.iloc[:3]

    # implement function to add links to csv from the api
    info = {}
    info['game_info'] = []

    for x in range(3):
        games_list = requests.request(
            "GET", f"https://rawg-video-games-database.p.rapidapi.com/games?search={find_match.iloc[[x]]['Name'].values[0]}", headers=game_headers).json()

        imageLink = ""

        for data in games_list['results']:
            if data['name'] == find_match.iloc[[x]]['Name'].values[0]:
                imageLink = data['background_image']

        info['game_info'].append({
            "game_name": find_match.iloc[[x]]['Name'].values[0],
            "game_image_links": imageLink
        })

    return info


# calls a function that takes in data from js and places it into a csv
@app.route('/addToData', methods=['GET', 'POST'])
def add_data_to_csv():
    existingData = pd.read_csv("static/csv/googleBooksData.csv")
    # checks if book is already in dataframe or not
    if (request.args.get('book_name') in existingData.Book_Name.values):
        return "Data exists"
    else:
        # instantiatees a data data frame for the new book
        bookData = DataFrame({'Book_Name': request.args.get('book_name'), 'author': request.args.get('author'), "Url": request.args.get('url'),
                              "Average_Rating": request.args.get('rating'), "Ratings_Count": request.args.get('ratings_count'), "Categories": request.args.get('categories'), "Year_Published": request.args.get('year_published')}, index=[0])

        # realigns columns
        bookData = bookData[['Book_Name', 'author', 'Url', 'Average_Rating',
                             'Ratings_Count', 'Categories', 'Year_Published']]
        # adds data into the existing csv
        bookData.to_csv("static/csv/googleBooksData.csv",
                        mode='a', header=False, index=False)
    return "Data was added"

# Used to check if login of a user exists in the database


@app.route('/loginInput')
def tryLogin(methods=['POST']):
    connection = sqlite3.connect("sqlServer/Users.db")
    c = connection.cursor()
    c.execute('Select * from UserLogins Where "Username" = ? and "Password" = ? ',
              (request.args.get('username'), request.args.get('password'),))
    if (c.fetchone()):
        # app.location = "/";
        # NOT WORKING BIG SADDDDDDD
        return "EXISTS"

    return "NOT EXISTS"

# Sends movies key back to js


@app.route('/movieKey')
def sendKey():
    return movies_key


if __name__ == '__main__':
    app.run(debug=True)

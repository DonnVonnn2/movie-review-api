import sqlite3
from sqlite3 import Error
from flask import Flask, abort
from flask import request


app = Flask(__name__)

#list:
# init database
# add movie
# add actor 
# add studio
# add platform 
# login user
# logout user
# add user
# add review
# delete user
# delete review
# edit review
# add castingList
# edit casting list
# retrieve rating
# Studio: movies released
#

#practical: add these later



#get
@app.route("/show-movie")  #non specific showing of movies
def showMovie(): #returns all movies
    conn = None
    movies = []
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT *\nFROM movies"
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            film = {"title": row["title"], "genre": row["genre"], "type": row["release_type"], "year": row["release_year"]}
            movies.append(film)
    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return movies


@app.route("/search-movie")  #does a specific search of a movie
def searchMovie(): #returns a movie. takes in json
    conn = None
    movies = []
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        title = postData["movieTitle"]
        title = "%" + title + "%"

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """SELECT title, release_year\nFROM movies\nWHERE title LIKE ?"""
        cursor.execute(query, (title, ))
        results = cursor.fetchall()
        if not results:
            return "No Results"
        for row in results:
            film = {"id": row["movie_id"],"title": row["title"], "release year": row["release_year"]}
            movies.append(film)
    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return movies

@app.route("/search-actor")
def searchActor(): #returns an actor. takes in json
    conn = None
    actors = []
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        name = postData["actorName"]
        name = "%" + name + "%"

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        queryActor = """SELECT name\nFROM actor\nWHERE name LIKE ?"""
        cursor.execute(queryActor, (name, ))
        results = cursor.fetchall()
        if not results:
            return "No Results"
        for row in results:
            actors.append(row["name"])
    except Error as e:
        print("Error: ", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return actors


@app.route("/review/<int:review_id>")
def showReview(review_id): #shows specfic review
    conn = None
    review = {}
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        query = "SELECT *\nFROM movie_review\nWHERE review_id == ?"
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query,(review_id, ))
        result = cursor.fetchone()
        review = {"movie":result["movie"], "user": result["user"], "review": result["review"], "stars": result["stars"]}
    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return review

@app.route("/display-reviews")
def showReviews():  #shows general reviews
    conn = None
    reviews = []
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        query = "SELECT *\nFROM movie_review"
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            film = {"id": row["review_id"],"movie":row["movie"], "user": row["user"], "review": row["review"], "stars": row["stars"]}
            reviews.append(film)

    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return reviews


@app.route("/get-cast/<int:movie_id>")
def getCast(movie_id): #returns array of actor IDs to be used in search actor
    conn = None
    cast = []
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        query = "SELECT actor\nFROM actor_in_movie\nWHERE movie = ?"
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (movie_id, ))
        data = cursor.fetchall()
        if not data:
            return "No cast"
        for row in data:
            actorr = {"actor_id": row["actor"]}
            cast.append(actorr)
    except Error as e:
        print("Error: ", e)
        abort(500)
    finally:
        if conn:
            conn.close()
        return cast


@app.route("/edit-movie", methods = ["POST"])
def editMovie():#updaes movie. takes in json. returns movie
    conn = None
    movie = {}
    try:
        postData = request.get_json()
        m_id = postData["id"]
        title = postData["title"]
        genre = postData["genre"]
        release_year = postData["release_year"]
        release_type = postData["release_type"]

        conn = sqlite3.connect("./movieReviewDatabase.db")
        update = "UPDATE movies\nSET title = ?, genre = ?, release_year = ?, release_type = ?\nWHERE movie_id == ?"
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(update, (title, genre, release_year, release_type, m_id))
        conn.commit()

        cursor.execute("SELECT *\nFROM movies\nWHERE movie_id == ?", (m_id, ))
        film = cursor.fetchone()
        movie = {"id": film["movie_id"],"title": film["title"], "genre": film["genre"], "release_year": film["release_year"], "release_type": film["release_type"]}
    except Error as e:
        print("Error: ", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return movie


# edit
@app.route("/delete-movie", methods = ["DELETE"])
def deleteMovie(): # takes in movie_id in json. Delets movie
    conn = None
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        deleteData = request.get_json()
        movie = deleteData["movie_id"]
        #first we delete the cast
        delete = "DELETE FROM actor_in_movie\nWHERE movie == ?"
        cursor = conn.cursor()
        cursor.execute(delete, (movie, ))
        conn.commit()
        #then we delete the movie
        delete = "DELETE FROM movies\nWHERE movie_id == ?"
        cursor.execute(delete, (movie, ))
        conn.commit()
    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return "Movie Deleted from Database"

@app.route("/delete-review", methods = ["DELETE"])
def deleteReview(): #Delets a review
    conn = None
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        deleteData = request.get_json()
        review = deleteData["review_id"]
        delete = "DELETE FROM movie_review\nWHERE review_id == ?"
        cursor = conn.cursor()
        cursor.execute(delete, (review, ))
        conn.commit()
    except Error as e:
        print("Error: ", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return "review deleted"


@app.route("/edit-review", methods = ["POST"])
def editReview(): #updates a review
    conn = None
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        review = postData["text"]
        ID = postData["review_id"]
        rate = postData["rating"]
        cursor = conn.cursor()
        cursor.execute("UPDATE movie_review\nSET review = ?, stars = ?\nWHERE review_id == ?", (review, rate ,ID))
        conn.commit()
    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return "Successfully Updated"

@app.route("/add-review", methods = ["POST"])
def newReview(): # adds in a review. returns review aferwards
    conn = None
    revi = {}
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        movie = postData["movie"]
        user = postData["user"]
        review = postData["text"]
        rating = postData["rating"]
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movie_review(movie, user, review, stars)\nVALUES(?,?,?,?)", (movie, user, review, rating))
        conn.commit()
        reviewID = cursor.lastrowid
        cursor.execute("SELECT *\nFROM movie_review\nWHERE review_id == ?", (reviewID, ))
        result = cursor.fetchone()
        revi = {"movie": result["movie"], "user": result["user"], "review": result["review"], "stars": result["stars"]}

    except Error as e:
        print("Error: ", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return revi

#user

@app.route("/add-user", methods = ["POST"])
def newUser(): # adds in a new user. returns user after wards
    conn = None
    user = {}
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        name = postData["username"]
        password = postData["password"]
        insert = """INSERT INTO user(username, password)\nVALUES(?,?)
        """
        conn.row_factory = sqlite3.Row
        curser = conn.cursor()
        curser.execute(insert, (name, password))
        conn.commit()
        query = """SELECT *\nFROM user\nWHERE username == ?"""
        curser.execute(query,(name,))
        userData = curser.fetchone()
        user["ID"] = userData["user_id"]
        user["username"] = userData["username"]
        
    except Error as e:
        print("Error: ", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return user

@app.route("/delete-user", methods = ["DELETE"])
def deleteUser(): #deletes user
    conn = None
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        acc = request.get_json()
        accountID = acc["user_id"]

        delete = """DELETE FROM user\nWHERE user_id == ?"""
        cursor = conn.cursor()
        cursor.execute(delete, (accountID,))
        conn.commit()

    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return "Account Successfully removed!"

@app.route("/login", methods = ["GET"])
def login(): #confirms username and password, and returns username and ID
    conn = None
    login = {}
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        username = postData["username"]
        password = postData["password"]

        conn.row_factory = sqlite3.Row
        curser = conn.cursor()
        query = """SELECT *\nFROM user\nWHERE username == ?\nAND password == ?"""
        curser.execute(query,(username, password))
        userData = curser.fetchone()
        if not userData:
            conn.close()
            return "Incorrect username or password"
        login["ID"] = userData["user_id"]
        login["username"] = userData["username"]
    except Error as e:
        print("Error: ",e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return login



@app.route("/change-password", methods = ["POST"])
def passwordChange(): #changes password
    conn = None
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        password = postData["new_password"]
        userID = postData["user_id"]

        insert = """UPDATE user\nSET password == ?\nWHERE user_id == ?"""
        cursor = conn.cursor()
        cursor.execute(insert,(password, userID))
        conn.commit()
        #will pass in username and possibly user_id, use that to insert or query
    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()

    return "Password update succesfully!"

# i dont know how to do log out

## adding
@app.route("/add-movie", methods=["POST"])
def addMovie(): #adds a movie. returns said movie after wards
    conn = None
    newMovie = {}
    try:
        postData = request.get_json()
        title = postData["title"]
        genre = postData["genre"]
        release_year = postData["release_year"]
        release_type = postData["release_type"]

        conn = sqlite3.connect("./movieReviewDatabase.db")

        if not title:
            title = "n/a"
        if not genre:
            genre == "n/a"
        if not release_year:
            release_year = "n/a"
        if not release_type:
            release_type = "n/a"

        insert = """INSERT INTO movies(title, genre, release_type, release_year)\nVALUES(?, ?, ?, ?)
        """

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(insert,(title, genre, release_type, release_year))
        conn.commit()
        check = """SELECT *
        FROM movies
        WHERE title = ?
        AND genre = ?
        AND release_type = ?
        AND release_year = ?
        """
        cursor.execute(check, (title, genre, release_type, release_year))
        row = cursor.fetchone()
        newMovie["title"] = row["title"]
        #newMovie["studio"] = row["studio"]
        newMovie["genre"] = row["genre"]
        newMovie["release_year"] = row["release_year"]
        newMovie["release_type"] = row["release_type"]

        print("Movie added succesfully!\n")
    except Error as e:
        print(e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return newMovie

@app.route("/add-actor", methods = ["POST"])
def addActor(): # adds an actor. Returns said actor
    conn = None
    actor = None
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        name = postData["name"]

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("INSERT INTO actor(name)\nVALUES(?)", (name,))
        conn.commit()
        actor = name
    except Error as e:
        print("Error: ", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    retval = actor + " has been added!"
    return retval


@app.route("/add-cast", methods = ["POST"])
def addCasting(): # adds a cast to a movie. casting
    conn = None
    cast = {}
    try:
        conn = sqlite3.connect("./movieReviewDatabase.db")
        postData = request.get_json()
        name = postData["actorName"]
        title = postData["movieTitle"]
        name = "%" + name + "%"
        title = "%" + title + "%"

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        queryActor = """SELECT actor_id\nFROM actor\nWHERE name LIKE ?"""
        queryMovie = """SELECT movie_id\nFROM movies\nWHERE title LIKE ?"""
        cursor.execute(queryActor, (name, ))
        act = cursor.fetchone()
        cursor.execute(queryMovie, (title, ))
        mov = cursor.fetchone()

        cursor.execute("INSERT INTO actor_in_movie(movie, actor)\nVALUES(?, ?)", (mov["movie_id"], act["actor_id"]))
        conn.commit()
        castID = cursor.lastrowid
        cursor.execute("SELECT *\nFROM actor_in_movie\nWHERE casting_id == ?", (castID, ))
        data = cursor.fetchone()
        cast = {"movie": data["movie"], "actor": data["actor"]}

    except Error as e:
        print("Error:", e)
        abort(500)
    finally:
        if conn:
            conn.close()
    return cast

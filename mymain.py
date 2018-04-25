from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import cgi

###
#	Prototype of redirect() function is as below −
#	Flask.redirect(location, statuscode, response)
#	In the above function −
#	location parameter is the URL where response should be redirected.
#	statuscode sent to browser’s header, defaults to 302.
#	response parameter is used to instantiate response.
###
app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ablog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_body = db.Column(db.String(300))
    posted = db.Column(db.Boolean)

    def __init__(self, blog_title, blog_body, posted):
        self.blog_title = blog_title
        self.blog_body = blog_body
        self.posted = False


def valid_title(title):
	title_message = []
	if len(title) > 0:
		return True
	else:
		title_error = "The title can not be empty.Enter a title for your new-post"
		return False


def valid_body(body):
	if len(body) > 0:
		return True
	return False


allpost = []
errtitle_message = []
errbody_message = []
ids = []


@app.route('/blog', methods=['GET'])
def index():
	# variable blog_id for requesting id from database
	blog_id = request.args.get('id')
	# If request is true grab blog using id and render template that returns single blog post
	if blog_id:
		blogs = Blog.query.get(blog_id)

		#Then, copy the file .travis/database.json to pymysql/tests/databases.json and edit the new file to match your MySQL configuration

		return render_template('displayentry.html', blogs=blogs)
		#Render page that holds all blogs
	return render_template('showall.html', blogs=Blog.query.all().order_by(Blog.id.desc())

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template("blog.html", title_error="", body_error="")
    elif request.method == 'POST':
        blog_title=request.form['blog_title']
        blog_body=request.form['blog_body']
        if len(blog_title) > 0:  # if valid _title(blog_title):
            title_error=""
            errtitle_message.append(title_error)
        else:
            title_error="The title can not be empty.Enter a title for your new-post"
            errtitle_message.append(title_error)
        if len(blog_body) > 0:  # valid_body(blog_body):
            body_error=""
            errbody_message.append(body_error)
        else:
            body_error="The body of your blog cannot be empty. Enter something!"
            errbody_message.append(body_error)

        if len(blog_title) < 0 or len(blog_body) < 0:
            return render_template("blog.html", title_error=errtitle_message[0], body_error=errbody_message[0])
        else:
                            # Create an object of the class Blog
                            # composants of the blog
            new_blog=Blog(blog_title, blog_body, posted=True)
                            # add new blog to the database
            db.session.add(new_blog)
            db.session.commit()     # confirmation of adding the new post to the database
                                    # adding the new blog to the list
            allpost.append(new_blog)
                                    # Redirect to individual blog post using current blog's information, id is automatically
            return redirect('/blog?id={1}'.format(new_blog.id))
                            # If request is a get request, render page that holds a newpost form with all variables being set to empty strings("")
    return render_template('newpost.html', title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()
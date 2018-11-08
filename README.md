# SimpleBlog

This is an exercise about blog.In this Blog,we can learn how to use [Flask](http://flask.pocoo.org/)--
a microframework for Python based on Werkzeug and [MongoDB](https://www.mongodb.com/cn) rather than Django and sql Database.  

This is my first project about flask,and I use Bootstrap as Frontend to decorate my blog succinctly,this is why it named SimpleBlog.

### Verion
- v1.0 --USER LOGIN
- v2.0 --POST and COMMENTS 
- v3.0 --RESTful API

### Feature
- Multiple user
- Role：admin,editor,writer,reader
- Admin models
- Email comfirm
- MTV design model
- Markdown support
- Multiple comment plugin
- Blog features: posts, tags, categories, comments

# Dependency
### Backend
- Flask  
1.[Flask-WTF](https://flask-wtf.readthedocs.io/en/latest/)  
2.[Flask-Login](https://flask-login.readthedocs.io/en/latest/)  
3.[Flask-Admin](https://flask-admin.readthedocs.io/en/latest/)  
4.[Flask_Mail](https://pythonhosted.org/Flask-Mail/)  
5.[Flask-Principal](https://pythonhosted.org/Flask-Principal/)  
6.[flask_mongoengine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/)  
7.[WTForms](https://wtforms.readthedocs.io/en/stable/)
- MongoDB  
[mongoengine](http://docs.mongoengine.org/tutorial.html)
- Markdown2
- bleach  
### Frontend
- Bootstrap  
1.Clean Blog theme  
2.bootbox.js  
3.bootstrap-markdown.js  
4.bootbox.js
- JQuery  
- Ajax
### Restful API
route:`/SimpleBlog/app/api/v1/`￼￼  
Including `Users` `Posts` `Comments` `Errors`  
Take `Users` as example:  

|URL|Method|Description|  
|--|--|--|  
|/api/v1/users/|GET|Get all users list|
|/api/v1/new-user/|POST|Add a new user|
|/api/v1/users/<user_id>/|GET|Get a user information|
|/api/v1/users/<user_id>/|PUT|Modify a user information|
|/api/v1/users/<user_id>/|PATCH|Update a user information|
|/api/v1/users/<user_id>/|DELETE|Delete a user|  

This is HTTP method.Anthor is [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/quickstart.html),you can find it in view function of this blog.  
## How to Run
### First Step  
Install your [MongoDB](http://www.runoob.com/mongodb/mongodb-osx-install.html)  
Install virtual environment `virtualenv`
```
$ sudo apt-get install python-virtualenv
```
Install requirements:  
```
(sudo) pip install -r requirements.txt
```
### Second Step
going to directory`SimpleBlog/app/config.py` to set you database name.

### Third Step
Run SimpleBlog with this command:
```
python manage.py runserver
```
Then you can visit the blog with url: http://127.0.0.1:5052

If you want to customize manage.py, checkout [Flask-Script](https://flask-script.readthedocs.io/en/latest/)

Get started with OctBlog
1. Create a superuser to administrate OctBlog
Visit the following url and create a superuser

http://127.0.0.1:5052/useraccounts/register/admin

If the url is forbidden, you need to go `SimpleBlog/app/config.py` to modify your configurations to allow the creation.

2. Administrator interface
The admin home is: http://127.0.0.1:5052/admin

3. Modify the default configurations
You either change settings in `SimpleBlog/app/config.py` file, or set the environment variables defined in this file.

Setting environment variables is recommended, and once the configuration is changed, you need to restart the service.


## License
This project is licensed under the [MIT license](https://opensource.org/licenses/MIT), see LICENSE for more details.

Finally,enjoy it!

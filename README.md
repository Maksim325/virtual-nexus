# Social media
It's only beck-end part so I took all the front-end from ChatGPT

## Futures
Posts:
- View all posts
- Adding your post with tags
- Commenting posts
- Like post
- Searching for an article
- Markdown is supported
- Edit post
- Pagination of posts on one page
- Deleting posts

Users:
- Change your username.
- Adding a profile photo
- Adding a description to your profile

API:
- Get all posts
- Creating your own
- Like post and get like counter
- Commenting posts and get list of comments
## To run it on your machine
Clone the ropository: `git clone https://github.com/Maksim325/virtual-nexus.git`

Go to directory: `cd "virtual nexus"`

Create virtual environment and activate it: `python -m venv venv`, `venv\Scripts\activate` 

Or if you in Linux: `source venv\bin\activate`

Install requariments: `pip install -r requariments.txt`

Go to project directory and run server: `cd virual_nexus_project`, `python manage.py runserver`

## Envsroment
Setup all this enviroment
```
#django
SECRET_KEY=
DEBUG=
PRODUCT=

#postgree
NAME=
USER=
PASSWORD=
HOST=
PORT=

#email
DEFAULT_FROM_EMAIL=

#pagination
API_PAGINATION=
POST_PAGINATION=
```

## If you find a bug
Contact me: garvatmaksim@gmail.com
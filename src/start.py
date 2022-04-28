from app.app import app
from config import config
from crawler import crawler

if __name__=='__main__':
    app.run(debug=True) 
    #crawler.crawler()
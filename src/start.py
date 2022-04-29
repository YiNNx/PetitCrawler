from app.app import app
from crawler.crawler import crawler

if __name__=='__main__':
    crawler()
    app.run(debug=True)
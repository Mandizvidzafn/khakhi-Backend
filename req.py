import requests
from project.admin import Categorytype, Category


admin_urls = ["http://127.0.0.1:5000/admin", 
        "http://127.0.0.1:5000/admin/product",
        "http://127.0.0.1:5000/admin/category",
        "http://127.0.0.1:5000/admin/order",
        "http://127.0.0.1:5000/admin/stock"]

for url in admin_urls:
    r = requests.get(url) 
    print(url + ": ", r)
    #print(url)

customer_urls = ["http://127.0.0.1:5000"]

for url in customer_urls:
    r = requests.get(url)
    print(url + ": ", r)



from app import app
with app.app_context():
    categories = Categorytype.query.all()
    for category in categories:
        print(category.type)
    print()
    category = Category.query.all()
    for cat in category:
        print(cat)

from project import db

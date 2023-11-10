import requests

# URL = "https://realpython.github.io/fake-jobs/"
URL = "https://booksmart-app-bd32a8932ff0.herokuapp.com/booksmartapp/booksmart-app/all_authors/"
page = requests.get(URL)
print()
print(page.text)
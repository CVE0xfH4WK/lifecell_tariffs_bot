# lifecell_tariffs_bot-test_repo
### The road of developing the lifecell_bot
To launch the book you need
* to install the dependencies from the `requirements.txt` using `pip install -r requirements.txt`
* create and populate with data `config/dev.json` in a similar way to `config/example.json`, you will need a bot token and a mongodb connection string
* first you need to pupulate the database with parsed data `python -m data.parser` it will parse the data from lifecell's website and add all of the needed intries into the db
* to run the bot using `python -m bot` and enjoy!

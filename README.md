# TODO_RestfulAPI
RESTful API for a simple TODO application.

## Deployment
1. Install python packages
```shell
sudo pip install -r requirements.txt
```
2. Start Flask web server, default ip and port are used: 127.0.0.1:5000/
```shell
python app.py
```
3. Open swagger UI
>Browser visit: 127.0.0.1:5000/apidocs
## Project Structure
| File Name          | Description                                                                 |
|:-------------------|:----------------------------------------------------------------------------|
| app.py             | A Flask web server that handles HTTP requests and conducts data persistence |
| data.db            | A SQLite database. Around 10 records are pre-inserted for test              |
| unit_tests.py      | Test case scripts                                                           |
| Design_Document.md | Design document. Include system architecture and test cases                 |
| apidocs/*.yml      | Config files for swagger                                                    |

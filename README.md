# BIP-Webscraper
# Table of content
- [General info](#General-info)
- [Setup](#Setup)
- [Technologies](#Technologies)
- [Future improvements](#Future-improvements)
- [Status](#Status)

## General info
The project main goal is to create microservices application to webscrap data from BIP (Biuletyn Informacji Publicznej), then find difference (between now and early version) and summarize this with LLM. The final step is to present summarized data to the user. Each services has its own queue (exepect GUI - it doesn't need, fetch data from DB). This appp consist of four microservices: GUI (present data), webscraper (scrape data), differ module (find differentions), LLM (summarize data).

## Setup
To run this project you have to install docker and docker-compose. Go to this page for more informations - [link](https://www.docker.com/products/docker-desktop/). In the next step just run in your terminal docker-compose up. All services will build and run automatically. but if you want to use the same model (Qwen/Qwen3-1.7B), you have to increase your resources in Docker Desktop. On linux or Mac you will have option to do this in application (i think). Otherwise paste below file into your user/user_name folder on your computer and restart Docker.
```
[wsl2]
memory=12GB
processors=16
swap=16GB
```

## Technologies
* Python 
* Fastapi
* Transfomers
* Redis
* RQ
* Celery
* Flask
* Tailwind CSS
* Pandas
* Pytesseract
* Beautifulsoup

## Future improvements
* amend GUI for better UX/UI experience
* enhance robustness of scraping
* deploy app to cloud
* extend CI workflow
* implement CD workflow

## Status
The project is in progress.

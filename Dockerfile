FROM python:3.8

RUN mkdir /scraping_test_task

WORKDIR /scraping_test_task

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python main.py
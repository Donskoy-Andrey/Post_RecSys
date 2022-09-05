FROM python

WORKDIR /recsys

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8899

CMD ["uvicorn", "src.service.service:app","--host", "0.0.0.0", "--reload", "--port", "8899"]
FROM python:3

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

# RUN npx tailwindcss -i ./website/static/src/input.css -o ./website/static/dist/output.css --watch

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
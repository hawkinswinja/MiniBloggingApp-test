FROM python:3.11.4-alpine
# RUN useradd -m -s /bin/bash user
RUN adduser -D -g '' user
WORKDIR /blog
ENV MONGODB_URI='mongodb://db:27017'
ENV MONGODB_DB='blog'
EXPOSE 5000
COPY requirements.txt /blog/
RUN pip install -r requirements.txt
USER user
COPY . /blog/
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]

FROM python:3.11.4-alpine
# RUN useradd -m -s /bin/bash user
RUN adduser -D -g '' user
WORKDIR /blog
EXPOSE 5000
COPY requirements.txt /blog/
RUN pip install -r requirements.txt
USER user
ENV MONGODB_URI=''
ENV MONGODB_DB=''
COPY . /blog/
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]

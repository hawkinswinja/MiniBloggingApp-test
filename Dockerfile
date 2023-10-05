FROM python:2.7.10-slim 
RUN useradd -m -s /bin/bash user
USER user
WORKDIR /blog
ENV MONGODB_URI=''
ENV MONGODB_DB=''
ENV URL=''
COPY requirements.txt /blog/
RUN pip install -r requirements.txt
COPY . /blog/
CMD ["flask", "run"]
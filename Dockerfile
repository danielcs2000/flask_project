FROM python:3.10-alpine AS ui-build

RUN mkdir -p /home/app

COPY . /home/app

# install dependencies

WORKDIR /home/app/
RUN pip3 install -r requirements.txt

EXPOSE 8060


WORKDIR /home/app/
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

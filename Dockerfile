# create the Linux Distro OS
FROM python:3.8.7-slim

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# open port
EXPOSE 5000

# install the dependencies and packages in the requirements file
RUN pip install --upgrade setuptools
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]



CMD ["main.py" ]


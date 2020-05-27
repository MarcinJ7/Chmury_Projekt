FROM tensorflow/tensorflow:2.2.0
EXPOSE 5000
COPY . /flask
ENV ACCEPT_EULA=Y
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev unixodbc-dev libodb-dev curl gnupg apt-transport-https apt-utils
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && apt-get install -y msodbcsql17
RUN pip install flask numpy requests opencv-python pyodbc
CMD FLASK_APP=/flask/server.py flask run --host=0.0.0.0
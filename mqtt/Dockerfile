FROM python:3.12-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y gnupg2 curl
RUN apt-get install -y cron \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get -y install g++ \
    && apt-get -y install unixodbc unixodbc-dev \
    && apt-get clean 
# Edit OpenSSL configuration to enable TLS 1.0
RUN sed -i 's/^\(MinProtocol =\).*/\1 TLSv1.0/' /etc/ssl/openssl.cnf

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
# EXPOSE 1883

# Command to run the application
CMD ["python", "main.py"]
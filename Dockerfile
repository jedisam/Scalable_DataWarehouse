# FROM python:3.7
# RUN pip install markupsafe==2.0.1 && \
#     pip install wtforms==2.3.3 && \
#     pip install 'apache-airflow[postgres]==1.10.14' && \
#     pip install dbt==0.15 && \
#     pip install SQLAlchemy==1.3.23

# RUN mkdir /project
# COPY scripts_airflow/ /project/scripts/

# RUN chmod +x /project/scripts/init.sh
# ENTRYPOINT [ "/project/scripts/init.sh" ]


FROM python:3.8.1-slim-buster

LABEL maintainer="Yididiya"

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -qq -y \
    git gcc build-essential libpq-dev --fix-missing --no-install-recommends \ 
    && apt-get clean

# latest version of pip
RUN pip install --upgrade pip

# Create directory for dbt config
RUN mkdir -p /root/.dbt

# Copy requirements.txt
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy dbt profile
COPY profiles.yml /root/.dbt/profiles.yml

# Copy source code
COPY ./scalable_dwh_dbt /app

# Export environement variables for dbt

# Start the dbt
CMD ["dbt-rpc", "serve"]
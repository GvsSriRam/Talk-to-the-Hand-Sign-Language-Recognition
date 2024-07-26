# Python image to use.

FROM python:3.9.6

# RUN apt-get update \
#   && apt-get install -y --no-install-recommends graphviz \
#   && rm -rf /var/lib/apt/lists/* \
#   && pip install --no-cache-dir pyparsing pydot

# Set the working directory to /app.
#ARG USER_HOME=/app
#ENV API_HOME=$USER_HOME

ENV PYTHONUNBUFFERED True

# RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y

#RUN apt install graphviz
# RUN apt install graphviz

# Copy the rest of the working directory contents into the container at /app

# WORKDIR 

COPY ./ .

# copy the requirements file used for dependencies
#COPY requirement.txt /app/requirement.txt

RUN pip3 install --upgrade pip
# RUN pip3 install -q pydot
# RUN pip3 install -q graphviz
# RUN pip3 install -q  pydotplus

# Install any needed packages specified in requirements.txt
RUN pip install  -r requirements.txt
# RUN apt-get update && apt-get install -y libgl1-mesa-glx
# RUN apt-get update && apt-get install -y tesseract-ocr
# ENV PATH="/opt/homebrew/bin:${PATH}"

#WORKDIR /app/segment_new


#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

#CMD exec gunicorn -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:8080" --workers 2 --threads 8  --timeout 0 --log-level debug app:app --reload 
ENTRYPOINT [ "python", "app.py" ]
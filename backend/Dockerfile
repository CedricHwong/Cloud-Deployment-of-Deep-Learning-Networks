# start by pulling the python image
FROM python:3.8.13

# copy the requirements file into the image
COPY ./requirements.txt /deploy/

# switch working directory
WORKDIR /deploy/

# install the dependencies and packages in the requirements file
# RUN pip install -r requirements.txt
RUN python3 -m pip install numpy
RUN python3 -m pip install pillow
RUN python3 -m pip install tensorflow==2.7.0 -f https://tf.kmtea.eu/whl/stable.html
RUN python3 -m pip install 'protobuf~=3.19.0' 
RUN python3 -m pip install Flask
RUN python3 -m pip install flask_cors
RUN python3 -m pip install scikit-image

# copy every content from the local file to the image
COPY  . /deploy/


EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT ["python", "App.py"]



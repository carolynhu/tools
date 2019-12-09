# We use an official Python runtime as a parent image
FROM python:3.7

# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Create root directory for our project in the container
RUN mkdir /perf_dashboard

# Set the working directory to /perf_dashboard
WORKDIR /perf_dashboard

# Copy the current directory contents into the container at /perf_dashboard
ADD . /perf_dashboard/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

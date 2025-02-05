# syntax=docker/dockerfile:1
# See https://docs.docker.com/language/python/build-images/

FROM registry.access.redhat.com/ubi9-minimal:latest
WORKDIR /app
COPY . .

# findutils provides xargs
RUN microdnf install -y findutils python3 python3-pip gem
# Install Python dependencies
RUN pip3 install -r requirements.txt
# Install Ruby dependencies
RUN gem install bundler
RUN bundle install --gemfile=Gemfile

# Create a simple executable file for enki
RUN echo '#!/bin/sh' > /usr/local/bin/enki
RUN echo 'python3 /app/src/enki.py "$@"' >> /usr/local/bin/enki
RUN chmod +x /usr/local/bin/enki

# When running this container interactively, use `-v .:/mnt/enki:Z`
# to mount the current directory in the host to the container working dir.
VOLUME ["/mnt/enki"]
WORKDIR "/mnt/enki"
CMD ["enki"]

FROM buildpack-deps:jessie

# remove several traces of debian python
RUN apt-get purge -y python.*

# RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
# RUN echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -y ca-certificates \
                          nginx \
                          build-essential \
                          python \
                          python-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN curl -SL 'https://bootstrap.pypa.io/get-pip.py' | python2 && \
    pip install --no-cache-dir --upgrade pip

ADD requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt \
  && rm ./requirements.txt

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

VOLUME ["/var/cache/nginx"]

ADD nginx/bennytize.conf /etc/nginx/sites-available/
ADD nginx/bennytize_uwsgi.ini ./

RUN rm -f /etc/nginx/sites-enabled/default \
  && mkdir -p /var/www/bennytize

WORKDIR /var/www/bennytize

ADD bennytize ./bennytize/
ADD run.py ./

RUN chown -R www-data:www-data /var/www/bennytize

EXPOSE 80 5000
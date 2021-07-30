FROM nginx

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./stream_conf.d /etc/nginx/stream_conf.d


COPY ./lemunter.conf /etc/nginx/conf.d/default.conf

COPY ./includes/ /etc/nginx/includes/

COPY ./ssl/ /etc/ssl/nginx/
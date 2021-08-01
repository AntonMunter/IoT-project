FROM nginx

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./default.conf /etc/nginx/templates/default.conf.template

COPY ./includes/ /etc/nginx/includes/

COPY ./ssl/ /etc/ssl/nginx/
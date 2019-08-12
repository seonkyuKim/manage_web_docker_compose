FROM nginx:latest

COPY manage_web.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/manage_web.conf /etc/nginx/conf.d/

CMD ["nginx", "-g", "daemon off;"]
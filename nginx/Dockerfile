FROM nginx:latest

COPY manage_web.conf /etc/nginx/sites-available/

# Move private key and crt to the container
RUN mkdir /etc/nginx/ssl
# ADD ./private.key /etc/nginx/ssl/
# ADD ./cutypenguin.crt /etc/nginx/ssl/
ADD /home/ec2-user/.ssh/private.key /etc/nginx/ssl/
ADD /home/ec2-user/.ssh/cutypenguin.crt /etc/nginx/ssl/
RUN chmod 600 /etc/nginx/ssl/private.key

# remove default.conf
RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/manage_web.conf /etc/nginx/conf.d/

WORKDIR /etc/nginx

EXPOSE 80 433

CMD ["nginx", "-g", "daemon off;"]
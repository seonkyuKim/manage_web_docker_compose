FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY sites-enabled/ /etc/nginx/sites-enabled

# Move private key and crt to the container
RUN mkdir /etc/nginx/ssl
# ADD ./private.key /etc/nginx/ssl/
# ADD ./cutypenguin.crt /etc/nginx/ssl/
ADD /home/ec2-user/.ssh/private.key /etc/nginx/ssl/
ADD /home/ec2-user/.ssh/cutypenguin.crt /etc/nginx/ssl/
RUN chmod 600 /etc/nginx/ssl/private.key


RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/manage_web.conf /etc/nginx/conf.d/


CMD ["nginx", "-g", "daemon off;"]
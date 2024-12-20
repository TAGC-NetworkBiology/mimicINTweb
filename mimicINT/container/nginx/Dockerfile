FROM nginx:1.25

## modification of the nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf
COPY ./container/nginx/conf.d/nginx.conf /etc/nginx/conf.d/default.conf


## comment to ha-proxy
WORKDIR ./container/nginx/ssl/


## create certificate with openssl for SSL request (port 443)
#RUN openssl req -new -newkey rsa:2048 -nodes -out mimicINT_tagc_luminy.csr -keyout mimicINT_tagc_luminy.key -subj "/C=FR/L=Marseille/O=TAGC/OU=IT/CN=mimicINT.tagc.luminy"

## comment to ha-proxy
RUN openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout key_mimicINT.pem -out cert_mimicINT.pem -days 365 -subj "/C=FR/L=Marseille/O=TAGC/OU=IT/CN=mimicINT.localhost"

## Note : when the website will be on a server, we must increase the security by using let's encrypt certificate
## replace 443 to 80 to ha-proxy
EXPOSE 443
EXPOSE 80
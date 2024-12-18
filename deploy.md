    sudo apt update
    sudo apt install nginx

    sudo mkdir -p /etc/nginx/ssl

<br>

    cd ~
    mkdir ssl_cert
    cd ssl_cert
    openssl req -new -newkey rsa:2048 -nodes -keyout imontero.me.key -out imontero.me.csr

<br>
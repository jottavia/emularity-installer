from utils import log, run_command

def configure_apache():
    log("Configuring Apache...")
    apache_config = """
    <VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html/emularity
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /var/www/html/emularity>
            Options Indexes FollowSymLinks
            AllowOverride None
            Require all granted
        </Directory>
    </VirtualHost>
    """

    with open("/etc/apache2/sites-available/emularity.conf", "w") as file:
        file.write(apache_config)

    run_command("a2ensite emularity.conf")
    run_command("a2dissite 000-default.conf")
    run_command("systemctl reload apache2")

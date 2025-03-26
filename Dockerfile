# Utiliser une image de base officielle Python
FROM php:apache

# Définir le répertoire de travail dans le conteneur
WORKDIR /var/www/html

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances Python
#RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers du projet dans le répertoire de travail
COPY UI/ /var/www/html

RUN echo '<Directory "/var/www/html">' >> /etc/apache2/apache2.conf && \
    echo '    AllowOverride All' >> /etc/apache2/apache2.conf && \
    echo '    Require all granted' >> /etc/apache2/apache2.conf && \
    echo '</Directory>' >> /etc/apache2/apache2.conf


RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# Ajouter le ServerName pour éviter l'erreur
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Exposer le port sur lequel l'application va tourner
EXPOSE 80

# Commande pour exécuter l'application
CMD ["apache2-foreground"]

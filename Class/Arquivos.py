import shutil
import re


class Arquivos:
    def __init__(self, log):
        self.log = log


    def copy_file(self, source, distinction):
        try:
            shutil.copyfile(source, distinction)

        except:
            self.log.append(f"- error copying file {source}")


    def change_file(self, file, regex, new):
        try:
            with open(file, "rt", -1, "utf-8") as robots:
                date = robots.read()
                date = re.sub(regex, new, date)

            with open(f"{file}", "wt", -1, "utf-8") as robots:
                robots.write(date)

        except:
            self.log.append(f"- error when changing the file {file}")


    def htaccess(self, file):
        try:
            self.change_file(
                file=f"{file}", 
                regex="#RewriteCond %{HTTPS} !=on", 
                new="RewriteCond %{HTTPS} !=on"
                )

            self.change_file(
                file=f"{file}", 
                regex="#RewriteRule \^\.\*\$ https:\/\/%{SERVER_NAME}%{REQUEST_URI} \[R,L\]", 
                new="RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [R,L]"
                )
            
            with open(f"{file}", "rt", -1, "utf-8") as htaccess:
                date = htaccess.read()
                rewrite = re.search('RewriteCond %{HTTPS} !=on', date)
                rewrite_www = re.search('RewriteCond %{HTTP_HOST} !\^www\\\. \[NC]', date)

            if not rewrite:
                self.change_file(
                    file=f"{file}", 
                    regex="RewriteEngine On", 
                    new="RewriteEngine On \n\
        RewriteCond %{HTTPS} !=on \n\
        RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [R,L]"
                )
            
            if not rewrite_www:
                self.change_file(
                    file=f"{file}", 
                    regex="RewriteRule \^\.\*\$ https:\/\/%{SERVER_NAME}%{REQUEST_URI} \[R,L\]", 
                    new="RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [R,L] \n\n\
        RewriteCond %{HTTP_HOST} !^www\. [NC] \n\
        RewriteRule ^ https://www.%{HTTP_HOST}%{REQUEST_URI} [R=301,L]"
                )

        except:
            self.log.append(f"- error when changing the file .htaccess")


    def log_error(self, name, message):
        with open(f"{name}.txt", "a", -1, "utf-8") as arquivo:
            arquivo.write(f"{message}\n")



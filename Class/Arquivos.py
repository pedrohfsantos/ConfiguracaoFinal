import shutil
import re
from os import listdir
from difflib import SequenceMatcher as similar
from pprint import pprint


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
            with open(file, "rt", -1, encoding="utf-8") as robots:
                date = robots.read()
                date = re.sub(regex, new, date)

            with open(f"{file}", "wt", -1, encoding="utf-8") as robots:
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
            
            with open(f"{file}", "rt", -1, encoding="utf-8") as htaccess:
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


    def redirect(self, file, root, new_links):
        try:
            all_files =  listdir(root)
            r = re.compile("links?.txt", re.IGNORECASE)
            file_name = list(filter(r.match, all_files))[0]

            with open(f"{root}/{file_name}", "r", encoding="utf-8") as links:
                line = links.readlines()
                old_links = [url.strip("\n").strip(" ") for url in line]
                old_links = list(filter(None, [re.sub("https?://.*?/", "", url) for url in old_links]))
                new_links = list(filter(None, [re.sub("https?://.*?/", "", url) for url in new_links]))
                redirects = []
                
                for old_link in old_links:
                    if old_link not in new_links:
                        highest_score = 0
                        winner = ""
                        for new_link in new_links:
                            score = similar(None, old_link, new_link).ratio()
                            if score > highest_score:
                                highest_score = score
                                winner = "{RAIZ}/"+new_link if highest_score >= 0.6 else "{RAIZ}"

                        redirects.append(f"redirect 301 /{old_link} {winner}")
        except:
            self.log.append(f"- It was not possible to perform the redirects")


        redirects = "\n        ".join(redirects)
        
        self.change_file(
                file=f"{file}", 
                regex="#redirects", 
                new=f"#redirects\n {redirects}"
                )


    def log_error(self, name, message):
        with open(f"{name}.txt", "w", -1, encoding="utf-8") as arquivo:
            arquivo.write(f"{message}\n")

from Class import *
from tqdm.auto import tqdm
import os

log = []
localhost = "C:/xampp/htdocs/Git/"

links = Links(log)
sitemap = Sitemap(log)
arquivos = Arquivos(log)

#key recaptcha
siteKey = ""
secretKey = ""

# "https://www.site.com.br/, idAnalytics or false, idCliente or false, true or false",
# with the value false does not change the item

projetos = [
    "https://www.site.com.br/, idAnalytics, idCliente, true",
]

for projeto in tqdm(projetos):
    try:
        projeto = [x.strip() for x in projeto.split(',')]

        url = projeto[0]
        idAnalytics = projeto[1]
        idCliente = projeto[2]
        key = projeto[3]
        path = f"{localhost}{links.url_base(url)}"
        
        if not os.path.isdir(path):
            os.system(f"git clone git@bitbucket.org:USER/{links.url_base(url)}.git {path}")
        else:
            os.system(f"cd {path} & git add .")
            os.system(f"cd {path} & git stash")
            os.system(f"cd {path} & git pull")

        sig = False if not os.path.isdir(f"{path}/doutor") else True

        site = links.links_site(url)

        if len(site) > 20 and len([x for x in site if 'localhost' in x or 'mpitemporario' in x]) == 0:
            sitemap.generator_sitemap_xml(site, path)
            arquivos.copy_file("Modelos/FILE", f"{path}/FILE")
            arquivos.copy_file("Modelos/FILE", f"{path}/FILE")
            arquivos.copy_file("Modelos/FILE", f"{path}/FILE")

            arquivos.change_file(
                file=f"{path}/robots.txt", 
                regex='Sitemap.*?$', 
                new=f"Sitemap: {url}sitemap.xml"
                )

            arquivos.change_file(
                file=f"{path}/inc/LAB.php", 
                regex="\(function\(i,s,o,g,r,a,m\){i\['GoogleAnalyticsObject.*?([\n|\n\r].*)*pageview['|\"]\);", 
                new='var s=document.createElement("script");function gtag(){dataLayer.push(arguments)}s.type="text/javascript",s.src="//www.googletagmanager.com/gtag/js?id=<?=$idAnalytics?>",document.head.appendChild(s),window.dataLayer=window.dataLayer||[],gtag("js",new Date),gtag("config","<?=$idAnalytics?>");'
                )

            arquivos.change_file(
                file=f"{path}/inc/LAB.php", 
                regex="(\$LAB([\n|\n\r].*)*initMyPage\(\);[\n|\n\r].*?}\);)", 
                new=r"\1 \n\n      <? include('js/btn-whatsapp.js'); ?> \n      <? include('inc/goal_conversion.php'); ?>"
                )

            if idAnalytics.lower() != "false":
                arquivos.change_file(
                    file=f"{path}/inc/geral.php", 
                    regex="\$idAnalytics.*?;", 
                    new=f"$idAnalytics		= '{idAnalytics}';"
                    )

            if idCliente.lower() != "false":
                arquivos.change_file(
                    file=f"{path}/inc/geral.php", 
                    regex="\$idCliente.*?;", 
                    new=f"$idCliente			= '{idCliente}';"
                    )

            if key.lower() != "false":
                arquivos.change_file(
                    file=f"{path}/inc/geral.php", 
                    regex="\$siteKey.*?;", 
                    new=f"$siteKey = '{siteKey}';"
                    )

                arquivos.change_file(
                    file=f"{path}/inc/geral.php", 
                    regex="\$secretKey.*?;", 
                    new=f"$secretKey = '{secretKey}';"
                    )

            if sig:
                arquivos.htaccess(file=f'{path}/index.php')
                arquivos.redirect(file=f'{path}/index.php', root=path, new_links=site)
            else:
                arquivos.htaccess(file=f'{path}/inc/gerador-htaccess.php')
                arquivos.redirect(file=f'{path}/inc/gerador-htaccess.php', root=path, new_links=site)


            if len(log) > 0:
                arquivos.log_error("error", f"{url} - " + ' '.join(log))

            log.clear()

            os.system(f"cd {path} & git add .")
            os.system(f"cd {path} & git commit -m Configuração")
            os.system(f"cd {path} & git push")

        else:
            arquivos.log_error("error", f"{url} - link numbers below expectations")

    except Exception as erro:
        arquivos.log_error("error", f"{url} - It was not possible to complete the script")
        # print(erro)
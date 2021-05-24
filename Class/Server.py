
import paramiko

class Server():
    def __init__(self, host, user_name, password):
        self.host = host
        self.user_name = user_name
        self.password = password
        self.port = 22


    def git_pull(self, project, htaccess=False):
        try:
            if htaccess:
                command = f"cd web/{project}/public_html; rm .htaccess; git pull"
            else:
                command = f"cd web/{project}/public_html; git pull"

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, self.user_name, self.password )

            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()

            [print(x) for x in lines]

            ssh.close()

        except Exception as erro:
            print(f"\n {erro} \n")

    def commit_htaccess(self, project):
        try:
            command = f"cd web/{project}/public_html; git add .htaccess; git commit -m \"htaccess\"; git push"

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, self.user_name, self.password )

            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()

            [print(x) for x in lines]

            ssh.close()

        except Exception as erro:
            print(f"\n {erro} \n")
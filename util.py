import json
import paramiko
import base64
import threading


def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


class Controller(threading.Thread):

    def __init__(self, server_config):
        super(Controller, self).__init__()
        self.name = server_config['name']
        self.hostname = server_config['hostname']
        self.username = server_config['username']
        self.key_file = server_config['private-key']
        self.connect()
        self.cpu_usage = self.hostname
        self.gpu_usage = self.hostname
        self.stop = False

    def connect(self):
        print('Connect to: ', self.hostname, end='')
        k = paramiko.RSAKey.from_private_key_file(self.key_file)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, username=self.username, pkey=k)
        print('  DONE')

    def run(self):
        while True:
            try:
                if self.stop:
                    break
                self.cpu_usage = self.get_cpu_usage()
            except:
                pass
            try:
                if self.stop:
                    break
                self.gpu_usage = self.get_gpu_usage()
            except:
                pass

    def get_gpu_usage(self):
        stdin, stdout, stderr = self.client.exec_command("nvidia-smi")
        output = [x for x in stdout.readlines()[:40]]
        output = ''.join(output)
        return output

    def get_cpu_usage(self):
        stdin, stdout, stderr = self.client.exec_command("top -bn 1")
        output = [x for x in stdout.readlines()[:20]]
        output = ''.join(output)
        return output

    def close(self):
        self.client.close()


def test():
    config = load_config()
    c = Controller(config['server'][0])
    c.close()


if __name__ == '__main__':
    test()

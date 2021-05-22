import subprocess

def update():
    results = subprocess.run(['git','pull','origin','master'], capture_output=True, cwd='/usr/share/exploitdb')
    print(results)

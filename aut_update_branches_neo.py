import subprocess
from os import chdir, getcwd
import tkinter

def run_command(command):
    result = subprocess.run(command.split(), capture_output=True, text=True)
    return result.stderr.strip(), result.stdout.strip()
    
if __name__ == "__main__": 
    chdir(r"C:\Users\ebotelho\Automatizados\AutomatizadoNeo\Codigo")
    
    branches = ['2.54', '2.56']
    
    for branch in branches:
        print(f'\nmain -> {branch} .---------------------------------------------------')
        err, out = run_command(f'git checkout {branch}')
        print(f'1: {err}')
        err, out = run_command(f'git merge main')
        print(f'2: {out}')
        err, out = run_command(f'git push origin {branch}')
        print(f'3: {err}')
        print(f'------------------------------------------------------------------')
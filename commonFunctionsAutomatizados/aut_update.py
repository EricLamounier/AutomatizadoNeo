import subprocess
from os import chdir, getcwd
import tkinter


def run_command(command):
    result = subprocess.run(command.split(), capture_output=True, text=True)
    return result.stderr.strip(), result.stdout.strip()


if __name__ == "__main__":

    projects = [
        {
            "path": r"C:\Users\ebotelho\Desktop\Automatizado\AutomatizadoNFCe",
            "branches": ["3.47"],
        },
    ]

    for project in projects:
        chdir(project["path"])

        err, out = run_command("git checkout main")
        print(f"1 {err}")

        err, out = run_command("git submodule update --remote --merge")
        print(f"2 {err}")

        err, out = run_command("git add .\\commonFunctionsAutomatizados")

        err, out = run_command(
            "git commit -m  Atualiza submódulo python-utils para a versão mais recente"
        )
        print(err, out)

        err, out = run_command("git push origin main")

        err, out = run_command("git push origin main")
        print(err, out)

        for branch in project["branches"]:
            print(
                f"\nmain -> {branch} ---------------------------------------------------"
            )
            err, out = run_command(f"git checkout {branch} --force")
            print(f"1: {err}")
            err, out = run_command(f"git merge main")
            print(f"2: {out}")
            err, out = run_command(f"git push origin {branch} --force")
            print(f"3: {err}")
            print(f"------------------------------------------------------------------")

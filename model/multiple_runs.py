import sys
import subprocess
import argparse
from pathlib import Path 

def main(n_processes, param_path):
    run_path = get_run_path()
    if n_processes != len(param_path) and len(param_path) != 1:
        print(
            f'Required {n_processes} or 1 parameter file(s) but {len(param_path)} '
            f'provided...'
        )
        return 
    # If just one paramter file passed, all processes will use it
    if len(param_path) == 1:
        for _ in range(n_processes-1):
            param_path.append(param_path[0])

    # From https://stackoverflow.com/questions/19156467/
    procs = []
    print(f'Running {n_processes} processes of BeRCM in parallel...')
    for i in range(n_processes):
        if sys.platform.startswith('win32'):
            proc = subprocess.Popen([sys.executable, run_path, param_path[i]], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            proc = subprocess.Popen([sys.executable, run_path, param_path[i]])
        procs.append(proc)
        print(f'Process [{proc.pid}] using {param_path[i]}')

    for proc in procs:
        proc.wait()
    print(f'All processes complete.')
    return 

def get_run_path():
    run_path = Path(__file__).parent / "run.py"
    return run_path

def parse_arguments():
    parser = argparse.ArgumentParser(description='A test')
    parser.add_argument("pcount", help="Number of processes to run")
    parser.add_argument("param", default='param.yaml', nargs='*', help="Test variable")
    args = parser.parse_args()
    return int(args.pcount), args.param

if __name__ == '__main__':
    n_processes, param_path = parse_arguments()
    main(n_processes, param_path)




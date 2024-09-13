import subprocess
from datetime import datetime

def inject_version(notebook, resources):

    version_string = datetime.today().strftime('v.%Y-%m-%d_') + \
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip().decode('utf-8')
    resources['metadata']['version_string'] = version_string
    
    return(notebook, resources)

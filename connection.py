#############################
# Author: Gary Loayza       #
# Date: 2020-04-26          #
#############################
import sqlalchemy
import ibm_db_sa
import os

def create(arg):
    """
    Jupyter Notebook env variable set in:
        /opt/tljh/config/jupyterhub_config.d/environment.py
    Runtime env vars set in systemd unit program.service:
        /etc/systemd/system/program.service
    """
    if arg == 'LIVE':
        LIVE = os.environ.get(arg)
        live = sqlalchemy.create_engine(LIVE)
        return live
    elif arg == 'TEST':
        TEST = os.environ.get(arg)
        t00 = sqlalchemy.create_engine(TEST)
        return t00
    elif arg == 'QUART':
        QUART = os.environ.get(arg)
        qtend = sqlalchemy.create_engine(QUART)
        return qtend
    else:
        print("No Valid DB connection was passed to main")

if __name__ == "__main__":
    create(arg)

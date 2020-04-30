import datetime as dt
from ftplib import FTP
import os

today = dt.date.today()
stamp =  today.strftime("%Y-%m-%d")

def transfer():
    RDRIVE = os.environ.get('RDRIVE')
    BRAD = os.environ.get('BRAD')
    BERRY = os.environ.get('BERRY')

    ftp = FTP(RDRIVE)
    ftp.login(BRAD,BERRY)
    ftp.cwd('/MARKETING/MEMBER_MONTHLY_ANALYSIS/' + today.strftime("%Y"))

    file = open('/opt/program/output/Monthly_Member_Analysis_' + stamp + '.xlsx', 'rb')

    ftp.storbinary('STOR Monthly_Member_Analysis_'+stamp+'.xlsx', file)

    file.close()
    ftp.quit()

if __name__ == "__main__":
    print('To run this program, execute \'$ python main.py\'')

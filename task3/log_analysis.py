import re
import time
import csv
import sys
from datetime import datetime


class Barrel:
    def __init__(self, full_vol=None, vol=None) -> None:
        self.full_vol = float(full_vol)
        self.vol = float(vol)

        # succesful volume that changes in barrel
        self.vol_topup = 0
        self.vol_scoop = 0
        # volume loss for barrel
        self.vol_topup_loss = 0
        self.vol_scoop_loss = 0

        # succesful (top up / scoop) count in barrel
        self.try_topUp = 0
        self.try_scoop = 0
        # all counts for barrel
        self.all_try_topUp = 0
        self.all_try_scoop = 0

    def top_up(self, l: float):
        if self.full_vol - self.vol >= l:
            self.vol += l
            self.vol_topup += l
            self.try_topUp += 1
        else:
            self.vol_topup_loss += l
        self.all_try_topUp += 1

    def scoop(self, l: float):
        if self.vol >= l:
            self.vol -= l
            self.vol_scoop += l
            self.try_scoop += 1
        else:
            self.vol_scoop_loss += l
        self.all_try_scoop += 1
    
    def mistake_topUp(self) -> float:
        """
        return mistake percent of all top up attempts (not all actions with barrel)
        """
        if self.all_try_topUp == 0:
            return 0.0
        return 100*(self.all_try_topUp - self.try_topUp) / self.all_try_topUp

    def mistake_scoop(self) -> float:
        """
        return mistake percent of scoop attempts (not all actions with barrel)
        """
        if self.all_try_scoop == 0:
            return 0.0
        return 100*(self.all_try_scoop - self.try_scoop) / self.all_try_scoop


if len(sys.argv) != 4:
    print('\n\tПример строки запуска: "python3 log_analysis.py log.log 2020-01-01T12:00:00 2020-01-01T13:00:00"\n')
    raise Exception('Ошибка в строке запуска')
t_start = datetime.strptime(sys.argv[2], "%Y-%m-%dT%H:%M:%S")
t_end = datetime.strptime(sys.argv[3], "%Y-%m-%dT%H:%M:%S")

with open(sys.argv[1]) as f:
    data = list(f)

log_barrel = Barrel(float(data[1]), float(data[2]))
vol_init = log_barrel.vol
for i in range(3, len(data)):
    curr_time = datetime.strptime(data[i][:24], "%Y-%m-%dТ%H:%M:%S.%fZ")
    if t_start<=curr_time<=t_end:
        vol = float(re.search(r'.*?(\d+)l', data[i]).group(1))
        if 'top up' in data[i]:
            log_barrel.top_up(vol)
        elif 'scoop' in data[i]:
            log_barrel.scoop(vol)


with open('log_analysis.csv', 'w') as analysis:
    analysis_write = csv.writer(analysis, delimiter=',', quotechar='"')

    analysis_write.writerow(['Объем воды:', 'в начале периода', 'в конце периода'])
    analysis_write.writerow([None, vol_init, log_barrel.vol])
    analysis_write.writerow(['Действие:', 'Наполнение', 'Забор'])
    analysis_write.writerow(['Количество попыток', log_barrel.all_try_topUp, log_barrel.all_try_scoop])
    analysis_write.writerow(['Процент ошибок, %', log_barrel.mistake_topUp(), log_barrel.mistake_scoop()])
    analysis_write.writerow(['Объем воды налит/забран', log_barrel.vol_topup, log_barrel.vol_scoop])
    analysis_write.writerow(['Объем воды не налит/забран', log_barrel.vol_topup_loss, log_barrel.vol_scoop_loss])

import numpy as np
import pandas as pd
from predictor.models import Mould
import os
import shutil
from predictor import app
from flask import send_from_directory, send_file


headerLabels = ['Fill Time s','Injection Pressure (MPa)','Holding Pressure MPa','Holding Time s','Total Pack s',
                'Mould Temp C','Clamp Force Ton','Shot Weight','Mould SA','Mould Vol','Cavity SA','Cavity Vol',
                'Melt Temp C','Mat Density','GF%','MMFR','Weight']


def serverExportCSV():
    entries = Mould.query.all()
    dataframe = []
    for entry in entries:
        data_object = [
            entry.fill_time,
            entry.injection_pres,
            entry.holding_pres,
            entry.holding_time,
            entry.cooling_time,

            entry.mould_temp,
            entry.clamp_force,
            entry.shot_weight,

            entry.mould_SA,
            entry.mould_vol,
            entry.cavity_SA,
            entry.cavity_vol,

            entry.melt_temp,
            entry.mat_density,
            entry.mat_GF,
            entry.mat_MMFR,
            entry.part_weight
        ]
        dataframe.append(data_object)
    dataframe = np.array(dataframe)
    DF = pd.DataFrame(dataframe)
    source = os.path.join(app.config['CLIENT_CSV'],  'database.csv')
    os.remove(source)
    DF.to_csv(source, index=False, header=headerLabels)
    return send_file(source, as_attachment=True, attachment_filename='database.csv')



def add_from_csv(filepath):
    dataframe = np.genfromtxt(filepath, delimiter=',')
    dataframe = np.delete(dataframe, 0, 0)
    rows = dataframe.shape[0]
    for i in range(0, rows):
        fill_time = dataframe[i][0]
        injection_pres = dataframe[i][1]
        holding_pres = dataframe[i][2]
        holding_time = dataframe[i][3]
        cooling_time = dataframe[i][4]

        mould_temp = dataframe[i][5]
        clamp_force = dataframe[i][6]
        shot_weight = dataframe[i][7]

        mould_SA = dataframe[i][8]
        mould_vol = dataframe[i][9]
        cavity_SA = dataframe[i][10]
        cavity_vol = dataframe[i][11]

        melt_temp = dataframe[i][12]
        mat_density = dataframe[i][13]
        mat_GF = dataframe[i][14]
        mat_MMFR = dataframe[i][15]
        part_weight = dataframe[i][16]
        entry_to_create = Mould(
            fill_time=fill_time,
            injection_pres=injection_pres,
            holding_pres=holding_pres,
            holding_time=holding_time,
            cooling_time=cooling_time,
            mould_temp=mould_temp,
            clamp_force=clamp_force,
            shot_weight=shot_weight,
            mould_SA=mould_SA,
            mould_vol=mould_vol,
            cavity_SA=cavity_SA,
            cavity_vol=cavity_vol,
            melt_temp=melt_temp,
            mat_density=mat_density,
            mat_GF=mat_GF,
            mat_MMFR=mat_MMFR,
            part_weight=part_weight,
        )
        entry_to_create.add_self()


def get_datasets():
    entries = Mould.query.all()
    dataframe = []

    if entries:
        for entry in entries:
            data_object = [
                entry.fill_time,
                entry.injection_pres,
                entry.holding_pres,
                entry.holding_time,
                entry.cooling_time,

                entry.mould_temp,
                entry.clamp_force,
                entry.shot_weight,

                entry.mould_SA,
                entry.mould_vol,
                entry.cavity_SA,
                entry.cavity_vol,

                entry.melt_temp,
                entry.mat_density,
                entry.mat_GF,
                entry.mat_MMFR,
                entry.part_weight
            ]
            dataframe.append(data_object)
        dataframe = np.array(dataframe)

        x = dataframe[:, :dataframe.shape[1] - 1]
        y = dataframe[:, dataframe.shape[1] - 1]

        return x, y
    else:
        return[[]], []


def exportCSVFormat():
    if os.name == 'nt':
        dest = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\format.csv')
    else:
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        dest = desktop + '/format.csv'
    if os.path.exists(dest):
        return False
    else:
        source = 'predictor/static/client/csv/format.csv'
        shutil.copyfile(source, dest)
        return True

def serverExportCSVFormat():
    source = os.path.join(app.config['CLIENT_CSV'],  'format.csv')
    return send_file(source, as_attachment=True, attachment_filename='format.csv')


def purge():
    entries = Mould.query.all()
    for entry in entries:
        entry.delete_self()


def exportCSV():
    if os.name == 'nt':
        dest = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\database.csv')
    else:
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        dest = desktop + '/database.csv'
    if os.path.exists(dest):
        return False
    else:
        entries = Mould.query.all()
        dataframe = []
        for entry in entries:
            data_object = [
                entry.fill_time,
                entry.injection_pres,
                entry.holding_pres,
                entry.holding_time,
                entry.cooling_time,

                entry.mould_temp,
                entry.clamp_force,
                entry.shot_weight,

                entry.mould_SA,
                entry.mould_vol,
                entry.cavity_SA,
                entry.cavity_vol,

                entry.melt_temp,
                entry.mat_density,
                entry.mat_GF,
                entry.mat_MMFR,
                entry.part_weight
            ]
            dataframe.append(data_object)
        dataframe = np.array(dataframe)
        DF = pd.DataFrame(dataframe)
        DF.to_csv('predictor/static/client/csv/database.csv', index=False, header=headerLabels)
        source = 'predictor/static/client/csv/database.csv'
        shutil.copyfile(source, dest)
        return True
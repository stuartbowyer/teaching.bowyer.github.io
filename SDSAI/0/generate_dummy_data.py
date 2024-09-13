# This script generates all the dummy data used in the SDSAI lectures and tutorials

import os
import logging
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

# Init
fake = Faker()
def seedinit():
  Faker.seed(0)
  random.seed(0)
  np.random.seed(0)
seedinit()

# Init logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def gen_demographics(n_rows, basepath):

  seedinit()

  gender_distribution = ["Male", "Female", "Non-binary"]
  gender_weights = [0.49, 0.49, 0.02]

  nhs_ethnicities = [
    "A	White - British", "B	White - Irish", "C	White - Any other White background",
    "D	Mixed - White and Black Caribbean", "E	Mixed - White and Black African",
    "F	Mixed - White and Asian", "G	Mixed - Any other mixed background",
    "H	Asian or Asian British - Indian", "J	Asian or Asian British - Pakistani",
    "K	Asian or Asian British - Bangladeshi", "L	Asian or Asian British - Any other Asian background",
    "M	Black or Black British - Caribbean", "N	Black or Black British - African",
    "P	Black or Black British - Any other Black background", "R	Other Ethnic Groups - Chinese",
    "S	Other Ethnic Groups - Any other ethnic group", "Z	Not stated"
  ]
  nhs_ethnicity_codes = [s[0] for s in nhs_ethnicities]

  def generate_first_name_by_gender(gender):
    if gender == "Male":
      return fake.first_name_male()
    elif gender == "Female":
      return fake.first_name_female()
    else:
      return fake.first_name()

  # Build table
  data = {
    "id": list(range(1, n_rows + 1)),
    "firstname": [0],
    "lastname": [fake.last_name() for _ in range(n_rows)],
    "date_of_birth": [fake.date_between_dates(datetime(1950,1,1),datetime(2024,10,1)) for _ in range(n_rows)],
    "gender": random.choices(gender_distribution, weights=gender_weights, k=n_rows),
    "ethnicity_code": random.choices(nhs_ethnicity_codes, k=n_rows)
  }
  data["firstname"] = [generate_first_name_by_gender(gender) for gender in data["gender"]]

  # Save
  filepath = os.path.join(basepath, "demographics.csv")
  pd.DataFrame(data).to_csv(filepath, index=False)
  logger.info(f"Saved demographics data to: {filepath}")

  return filepath


def split_demographics(fn_demographics, basepath):

  df_demographics = pd.read_csv(fn_demographics)

  get_age = lambda x: relativedelta(pd.Timestamp('now'), pd.to_datetime(x['date_of_birth'])).years
  ages = df_demographics.apply(get_age, axis=1)

  df_paediatric = df_demographics[ages < 18]
  df_adult = df_demographics[ages >= 18]

  # Save
  filepath = os.path.join(basepath, "demographics_paediatric.csv")
  df_paediatric.to_csv(filepath, index=False)
  logger.info(f"Saved paediatric demographics data to: {filepath}")

  filepath = os.path.join(basepath, "demographics_adult.csv")
  df_adult.to_csv(filepath, index=False)
  logger.info(f"Saved adult demographics data to: {filepath}")


def gen_crp(n_rows, basepath):

  seedinit()

  names = ['Oliver', 'Amelia', 'Noah', 'Emma', 'Liam']
  alpha = [0.8, 2.5, 3.1, 0.5, 0.3]

  def generate_crp_by_name(name):
    val = random.gammavariate(alpha[names.index(name)], 2.0)
    return f'{round(val, 4)} mg/L'

  data = {
    'patients': random.choices(names, k=n_rows)
  }
  data['crp'] = [generate_crp_by_name(name) for name in data["patients"]]

  # Save
  filepath = os.path.join(basepath, "dummy_crp_data.csv")
  pd.DataFrame(data).to_csv(filepath, index=False)
  logger.info(f"Saved CRP data to: {filepath}")


def gen_recovery(fn_demographics, basepath):
  
  seedinit()
  
  df_demographics = pd.read_csv(fn_demographics)
  gender_lookup = {
    "Male": (8, 4),
    "Female": (13, 4),
    "Non-binary": (10, 5)
  }
  
  def get_recovery(row):
    mu, sigma = gender_lookup[row['gender']]
    return round(abs(np.random.normal(mu, sigma)), 4)
  
  df_demographics['recovery_days'] = df_demographics.apply(get_recovery, axis=1)
  df_recovery = df_demographics[['id', 'recovery_days']]
  df_recovery = df_recovery.sample(frac=1)
  
  # Save
  filepath = os.path.join(basepath, "simple_recovery.csv")
  df_recovery.to_csv(filepath, index=False)
  logger.info(f"Saved simple recovery data to: {filepath}")
  return filepath


def gen_long_monitoring_data(n_pats, basepath):
  
  seedinit()
  
  sensor_names = ['hr','bp','temp','spo2','bis']
  n_sensors = len(sensor_names)
  
  def gen_val(sensor):
    if sensor == 'hr':
      return f"{random.randint(60, 100)} bpm"
    elif sensor == 'bp':
      return f"{random.randint(90, 120)}/{random.randint(60, 80)} mmHg"
    elif sensor == 'temp':
      return f"{round(random.uniform(34.9, 39.5), 2)} deg"
    elif sensor == 'spo2':
      return f"{round(random.uniform(94.5, 100.0), 1)} %"
    elif sensor == 'bis':
      return f"{random.randint(40, 60)}"
    else:
      return "???"
    
  d1 = datetime(2024,10,1,9)
  d2 = datetime(2024,10,1,10)
  
  data = {
    'patient_id': list(range(1, n_pats + 1)) * n_sensors,
    'taken_datetime': [fake.date_time_between(d1, d2) for _ in range(n_pats * n_sensors)],
    'sensor': np.repeat(sensor_names, n_pats),
  }
  data['value'] = [gen_val(s) for s in data['sensor']]
  df = pd.DataFrame(data).sort_values('taken_datetime')
  
  # Save
  filepath = os.path.join(basepath, "long_monitoring.csv")
  df.to_csv(filepath, index=False)
  logger.info(f"Saved long monitoring data to: {filepath}")
  return filepath


def gen_wide_robot_data(n_robots, basepath):
  
  seedinit()
  
  data = {
    'instrument_id': [f"ROBOT{str(i).zfill(4)}" for i in range(1, n_robots+1)],
    'x_pos': np.random.uniform(-.8, .8, n_robots),
    'y_pos': np.random.uniform(-.8, .8, n_robots),
    'z_pos': np.random.uniform(-.8, .8, n_robots),
    'state': random.choices(['moving', 'closed', 'open'], k=n_robots)
  }
  df = pd.DataFrame(data)
  
  # Save
  filepath = os.path.join(basepath, "wide_robot.csv")
  df.to_csv(filepath, index=False)
  logger.info(f"Saved wide robot data to: {filepath}")
  return filepath


def gen_hr_timeseries(n_values, basepath):
  
  seedinit()
  
  noisy_sine = 80 + 30 * np.sin(4 + 2 * np.pi * (1/6) * np.arange(n_values)) + np.random.randint(-15,15, n_values)
  
  data = {
    'obs_time': [datetime(2024,10,1) + timedelta(hours=4*stp) for stp in range(n_values)],
    'hr': noisy_sine.round(2).astype('str')
  }
  df = pd.DataFrame(data)
  
  # Save
  filepath = os.path.join(basepath, "hr_timeseries.csv")
  df.to_csv(filepath, index=False)
  logger.info(f"Saved HR timeseries data to: {filepath}")
  return filepath


def gen_str_data(n_values, basepath):
  
  seedinit()
  
  noisy_sine = 80 + 30 * np.sin(4 + 2 * np.pi * (1/6) * np.arange(n_values)) + np.random.randint(-15,15, n_values)
  
  data = {
    'patient_id': range(1,n_values+1),
    'hr': noisy_sine.round(2).astype('<U4') + ([' bpm'] * n_values),
    'conscious_level': random.choices(['ALERT_0','VERBAL_1','PAIN_2','UNRESPONSIVE_3'], k=n_values),
    'bp': [f"{random.randint(90, 120)}/{random.randint(60, 80)} mmHg" for _ in range(n_values)],
    'microbio_culture': random.choices(['positive','negative','POSITIVE','NEGATIVE','POS','NEG','+','-'], k=n_values),
  }
  df = pd.DataFrame(data)
  
  # Save
  filepath = os.path.join(basepath, "str_data.csv")
  df.to_csv(filepath, index=False)
  logger.info(f"Saved str data to: {filepath}")
  return filepath


def gen_laboratory_tests(fn_demographics, fn_recovery, basepath):
  
  seedinit()

  df_demographics = pd.read_csv(fn_demographics)
  df_recovery = pd.read_csv(fn_recovery)
  df = pd.merge(df_demographics, df_recovery, on='id').rename(columns={'id': 'patient_id'})
  
  def gen_crp(gender):
    if gender == 'Male':
      return abs(np.random.normal(0.5, 0.3))
    elif gender == 'Female':
      return abs(np.random.normal(1.5, 0.3))
    return abs(np.random.normal(1.0, 0.5))
  
  def fmt_crp(unit, mgl):
    if unit == 'mg/L':
      return str(mgl) + ' ' + unit
    else:
      return str(round(mgl/1000,7)) + ' ' + unit
  
  df['crp_unit'] = np.random.choice(['mg/L', 'g/L'], df.shape[0])
  df['crp_mgl'] = df['gender'].apply(gen_crp).round(4)
  df['crp'] = df.apply(lambda x: fmt_crp(x.crp_unit, x.crp_mgl), axis=1)
  df['reco_zsc'] = df['recovery_days'] / df['recovery_days'].std(ddof=0) * np.random.choice([1,-1], df.shape[0], p=[0.9,0.1])
  df['wbc_z_score'] = (df['reco_zsc'] + np.random.normal(scale=2.0, size=df['reco_zsc'].shape)).round(6)
  df['albumin_level'] = np.random.choice(
    ['high', 'HIGH', 'veryhigh', 'low', 'LOW', 'verylow', 'normal', 'NORMAL'],
    df.shape[0],
    p=[0.1, 0.1, 0.005, 0.1, 0.1, 0.005, 0.3, 0.29]
  )
  
  df = df.melt(id_vars=['patient_id'], value_vars=['crp','wbc_z_score','albumin_level'], var_name='test')
  df = df.sample(frac=1)
  df.insert(0, 'id', range(df.shape[0]))
  
  # Save
  filepath = os.path.join(basepath, "laboratory_tests.csv")
  df.to_csv(filepath, index=False)
  logger.info(f"Saved lab data to: {filepath}")
  return filepath



def main():

  # Paths
  root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
  path_l1 = os.path.join(root, '1/data')
  path_l2 = os.path.join(root, '2/data')
  path_l3 = os.path.join(root, '3/data')
  logger.info(f"Root dir:     {root}")
  logger.info(f"L1 data dir:  {path_l1}")
  logger.info(f"L3 data dir:  {path_l3}")

  # Lecture 1
  fn_crp = gen_crp(200, path_l1)
  
  # Lecture 2
  fn_demographics = gen_demographics(1000, path_l2)
  split_demographics(fn_demographics, path_l2)
  fn_recovery = gen_recovery(fn_demographics, path_l2)
  fn_long_monitoring = gen_long_monitoring_data(5, path_l2)
  fn_wide_robot = gen_wide_robot_data(4, path_l2)
  fn_hr_timeseries = gen_hr_timeseries(24, path_l2)
  fn_str_data = gen_str_data(2000, path_l2)
  fn_laboratory_tests = gen_laboratory_tests(fn_demographics, fn_recovery, path_l2)

  # Lecture 3


if __name__ == "__main__":
  main()

from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys

auth = Authorization(
  'data.colorado.gov',
  os.environ['MY_SOCRATA_USERNAME'],
  os.environ['MY_SOCRATA_PASSWORD']
)

socrata = Socrata(auth)
view = socrata.views.lookup(os.environ['DATASET_ID'])
# 4ykn-tg5h
upload_file = os.environ['UPLOAD_FILE']
# business_entities.csv
config_name = os.environ['CONFIG_NAME']
# business_entities_11-22-2021_f71d

with open(upload_file, 'rb') as my_file:
  (revision, job) = socrata.using_config(config_name, view).csv(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)
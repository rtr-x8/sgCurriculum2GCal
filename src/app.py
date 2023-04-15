from datetime import datetime, timedelta
from icalendar import Calendar, Event, vText
import pandas as pd
import hashlib

TIME_SLOTS = [
  timedelta(hours=8, minutes=50),
  timedelta(hours=10, minutes=30),
  timedelta(hours=12, minutes=50),
  timedelta(hours=14, minutes=30),
  timedelta(hours=16, minutes=10)
]

COURCE_TIME = timedelta(minutes=90)

UID_PREFIX = "92f5c2e7-bc28-495c-bc3b-f35d61145e14-"
UID_SUFFIX = ""


# この辺はおまじないっぽい
cal = Calendar()
cal.add('prodid', '-//Test//test-product//ja//')
cal.add('version', '2.0')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'REQUEST')

# read
schedules = pd.read_csv('./input_csv/input.csv', header=0)
schedules['date'] = pd.to_datetime(schedules['date'])
schedules = schedules.fillna(0)

counter = 0

for record in schedules.itertuples():
  for index, slot in enumerate(TIME_SLOTS):
    slot_name = f"time_slot_{index+1}"
    professor_name = getattr(record, slot_name)

    if professor_name == 0:
      continue

    seed = f'{record.name}-{professor_name}-{record.date}-{slot}'
    uid = hashlib.md5(seed.encode('utf-8'))
    
    #print(seed, uid.hexdigest())

    # 説明文
    description = f'担当：{professor_name}\n'
    if record.type != 0:
      description += f'種別：{record.type}\n'
    if record.note != 0:
      description += f'{record.note}\n'

    # イベント作成
    event = Event()
    event.add('summary', record.name)
    event.add('dtstart', record.date + slot)
    event.add('dtend', record.date + slot + COURCE_TIME)
    event.add('description', vText(description))
    event.add('uid', f'{UID_PREFIX}{counter}{UID_SUFFIX}')

    # イベント登録
    cal.add_component(event)
    counter += 1

# icsファイル作成
f = open('out/output_{}.ics'.format(datetime.now().timestamp()), 'wb')
f.write(cal.to_ical())
f.close()

from datetime import datetime, timedelta
from icalendar import Calendar, Event, vCalAddress, vText
import pandas as pd

time_slots = [
  timedelta(hours=8, minutes=50),
  timedelta(hours=10, minutes=30),
  timedelta(hours=12, minutes=50),
  timedelta(hours=14, minutes=30),
  timedelta(hours=16, minutes=10)
]


cal = Calendar()
cal.add('prodid', '-//Test//test-product//ja//')
cal.add('version', '2.0')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'REQUEST')

schedules = pd.read_csv('Book1.csv', header=0)
schedules['date'] = pd.to_datetime(schedules['date'])
schedules = schedules.fillna(0)

for record in schedules.itertuples():
  for index, slot in enumerate(time_slots):
    slot_name = "time_slot_{}".format(index+1)
    professor_name = getattr(record, slot_name)
    
    if professor_name == 0:
      continue

    # イベント作成
    event = Event()
    event.add('summary', record.name)
    event.add('dtstart', record.date + slot)
    event.add('dtend', record.date + slot + timedelta(minutes=90))
    event.add('description', f'担当：{professor_name}\n種別：{record.type}')

    cal.add_component(event)

# icsファイル作成
f = open('output_{}.ics'.format(datetime.now()), 'wb')
f.write(cal.to_ical())
f.close()

print(event)

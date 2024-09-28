import pandas as pd
from control import ControlCenter


df = pd.read_csv('test.csv')
df = df.sort_values(by=['created'])

list_created = []
list_uuid = []
list_link = []
list_is_duplicate = []
list_duplicate_for = []
for row in df.iterrows():
    uuid = row['link']
    created = row['created']
    link = row['link']

    # Код Назара. Система предсказывает N айдишников#
    list_id_video = ...
    list_id_text = ...

    result = ControlCenter.is_dublicate(
        list_id_video,
        list_id_text,
        mul_video=0.8,
        mul_text=0.2,
        threshold=3
    )

    is_duplicate = result['is_duplicate']
    duplicate_for = ''
    if is_duplicate:
        duplicate_for = result['duplicate_for']

    list_created.append(created)
    list_uuid.append(uuid)
    list_link.append(link)
    list_is_duplicate.append(duplicate_for)


submission = pd.DataFrame({
    'created': list_created,
    'uuid': list_uuid,
    'link': list_link,
    'is_duplicate': list_is_duplicate,
    'duplicate_for': list_duplicate_for,
})
submission.to_csv('submission.csv', index=False)

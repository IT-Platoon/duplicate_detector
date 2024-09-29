import pandas as pd

from control import ControlCenter
from .model import ModelVideo2Frames
from .model_speech import ModelSpeech2Embedding
from app.utils.detection import run_detection_by_video, run_detection_by_text

df = pd.read_csv('test.csv')
df = df.sort_values(by=['created'])

list_created = []
list_uuid = []
list_link = []
list_is_duplicate = []
list_duplicate_for = []

model1 = ModelVideo2Frames()
model2 = ModelSpeech2Embedding()

for row in df.iterrows():
    uuid = row['uuid']
    created = row['created']
    link = row['link']

    list_id_video = run_detection_by_video(link, model1)
    list_id_text = run_detection_by_text(link, model1)

    result = ControlCenter.is_dublicate(
        list_id_video,
        list_id_text,
        mul_video=0.8,
        mul_text=0.2,
        threshold=3
    )

    is_duplicate = result[0]
    duplicate_for = ''
    if is_duplicate:
        duplicate_for = result[1]

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

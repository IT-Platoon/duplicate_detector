import os
import urllib.request

import librosa
import torch

from pydub import AudioSegment
from transformers import AutoTokenizer, AutoModel, WhisperProcessor, WhisperForConditionalGeneration


class ModelSpeech2Embedding:
    """Модель, преобразующая аудиоряд в текст."""
    MODEL_NAME = 'openai/whisper-tiny'

    def __init__(self):
        self.__audio_model = WhisperForConditionalGeneration.from_pretrained(self.MODEL_NAME)
        self.__audio_processor = WhisperProcessor.from_pretrained(self.MODEL_NAME)
        self.__text_model = TextModel()

    def get_embedding_from_url(self, video_url):
        text = self.__speech2text(video_url)
        print(text)
        embedding = self.__text_model.get_emb_by_text(text)
        return embedding

    def __speech2text(self, file_url):
        filename = self.__write_audio_from_url(file_url)
        audio_data, sampling_rate = self.__get_audio_vector(filename)

        input_features = self.__audio_processor(audio_data, sampling_rate=sampling_rate, return_tensors="pt").input_features

        predicted_ids = self.__audio_model.generate(input_features)
        transcription = self.__audio_processor.batch_decode(predicted_ids, skip_special_tokens=True)

        if os.path.exists(filename):
            name = filename.split('.')[0]
            os.remove(f'{name}.wav')
            os.remove(f'{name}.mp4')

        return transcription

    def __write_audio_from_url(self, file_url):
        file_name = file_url.split('/')[-1].split('.')[0]  # Получаем id аудиозаписи
        urllib.request.urlretrieve(file_url, f'{file_name}.mp4')
        audio = AudioSegment.from_file(f'{file_name}.mp4', 'mp4')
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16_000)
        audio.export(f'{file_name}.wav', format="wav")
        return f'{file_name}.wav'

    def __get_audio_vector(self, file_name="output.wav"):
        os.system(f'ffmpeg -i {file_name} -ar 16000 -y {file_name}')
        data, sr = librosa.load(f'{file_name}', sr=16000)
        return data, sr


class TextModel:
    MODEL_NAME = 'sentence-transformers/bert-base-nli-mean-tokens'

    def __init__(self):
        self.__tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.__bert = AutoModel.from_pretrained(self.MODEL_NAME)

    def get_emb_by_text(self, text):
        with torch.no_grad():
            batch_tensors = self.__tokenizer(text[0][:500], padding=True, truncation=True, return_tensors="pt")
            out = self.__bert(**batch_tensors)
            token_embs = out.last_hidden_state
            del out

        mask = batch_tensors['attention_mask'][..., None].to(torch.float32)
        return (token_embs * mask).sum(1) / mask.sum(1)


if __name__ == '__main__':
    model = ModelSpeech2Embedding()
    model.get_embedding_from_url('https://s3.ritm.media/yappy-db-duplicates/23fac2f2-7f00-48cb-b3ac-aac8caa3b6b4.mp4')

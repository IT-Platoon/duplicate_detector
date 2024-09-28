# from app.services.metaclasses import Singleton

import clip
import cv2
import matplotlib.pyplot as plt
import numpy as np
# import os
import pandas as pd
# import requests
import torch


from PIL import Image as PILImage
from tqdm import tqdm


device = "cuda" if torch.cuda.is_available() else "cpu"


# class ModelVideo2Frames(metaclass=Singleton):
class ModelVideo2Frames():
    """Модель для преобразования видео в кадры."""

    def __init__(self):
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)

    def __extract_frames(self, video_url: str, get_every_sec_frame: float = 1.0) -> list[list[np.ndarray], list[float]]:
        """См. метод video2frames2embeddings"""
        frames = []
        seconds_frames = []

        # Считываем инфу о видео.
        cap = cv2.VideoCapture(video_url)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        # Получаем инфу о длительности видео.
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # total_seconds = total_frames / frame_rate
        # target_frame_count = int(total_seconds)

        target_frame_index = 0
        while target_frame_index < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame_index)
            ret, frame = cap.read()
            if not ret:
                break

            frames.append(frame)
            seconds_frames.append(target_frame_index / frame_rate)

            # Двигаемс к следующему кадру.
            target_frame_index += (frame_rate * get_every_sec_frame)

        cap.release()
        return frames, seconds_frames

    def __generate_embedding(self, frame: np.ndarray) -> np.ndarray:
        """Генерация эмбеддинга для кадра."""
        frame_tensor = self.preprocess(PILImage.fromarray(frame)).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = self.model.encode_image(frame_tensor).cpu().numpy()
        return embedding[0]

    def video2frames2embeddings(self, video_url: str, get_every_sec_frame: float = 1.0) -> pd.DataFrame:
        """Извлечение N кадров из видео.
        video_url: str | ссылка/путь на видео.
        get_every_sec_frame: int | раз в сколько МС берём каждый кадр(0.5 - каждые полсек.; 1.0 - каждую сек.)"""
        frames = []
        frames, seconds_frames = self.__extract_frames(video_url, get_every_sec_frame=get_every_sec_frame)
        data = [
            (video_url, i+1, seconds_frames[i], self.__generate_embedding(frame))
            for i, frame in enumerate(tqdm(
                frames,
                desc="Processing frames",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]")
            )
        ]
        df = pd.DataFrame(data, columns=['video_url', "frame_number", 'timing_second', "embedding_data"])
        df["embedding_data"] = df["embedding_data"].apply(
            lambda vec: vec / np.linalg.norm(vec)
        )
        return df

    @staticmethod
    def plot_frame_by_timing(video_url: str, sec_frame: float) -> None:
        """Рисует кадр из видео по таймнингу.
        video_url: str | ссылка/путь на видео.
        sec_frame: float | секунда видео, из которого показаться текущий кадр."""

        # Считываем инфу о видео.
        cap = cv2.VideoCapture(video_url)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        cap.set(cv2.CAP_PROP_POS_FRAMES, sec_frame * frame_rate)
        ret, frame = cap.read()
        cap.release()

        fig = plt.figure(figsize=(5, 5))
        frame_data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(frame_data)
        plt.axis("off")
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    video_url = 'https://s3.ritm.media/yappy-db-duplicates/2d53a527-5b97-43db-ba0c-0731edd04e9a.mp4'

    model = ModelVideo2Frames()
    df = model.video2frames2embeddings(video_url, get_every_sec_frame=2.5)

    model.plot_frame_by_timing(video_url, 25)

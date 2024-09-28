from app.services.metaclasses import Singleton


class YOLOWrapper(metaclass=Singleton):
    def __init__(self, path: str = "./weights/yolov8s.pt"):
        pass

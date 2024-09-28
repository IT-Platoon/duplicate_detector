class ControlCenter:
    """Центр управления результатами."""

    def __init__(self):
        pass

    @staticmethod
    def is_dublicate(
        list_id_video: list, list_id_text: list,
        mul_video = 0.8, mul_text = 0.2,
        threshold: int = 3,
    ) -> tuple[bool, str]:
        """Проверим на дубликат.
        list_id_video: list | список айдишников топ-1 по метрике сходства видеоконтекста.
        list_id_text: list | список айдишников топ-1 по метрике сходства звукового контента."""
        counter_video = {}
        for id_video in list_id_video:
            counter_video[id_video] = list_id_text.count(id_video)

        counter_text = {}
        for id_text in list_id_text:
            counter_text[id_text] = list_id_text.count(id_text)
        
        counter = {}
        for id_video in counter_video.keys():
            if id_video in counter:
                counter[id_video] += counter_video[id_video] * mul_video
            else:
                counter[id_video] = counter_video[id_video] * mul_video
        for id_text in counter_text.keys():
            if id_text in counter:
                counter[id_text] += counter_text[id_text] * mul_text
            else:
                counter[id_text] = counter_text[id_text] * mul_text
        
        counter = [max(counter.items(), key=lambda k_v: k_v[1])]

        if counter[0][1] >= len(list_id_video) // threshold:
            return True, counter[0][0]
        else:
            return False, ''


if __name__ == '__main__':
    ControlCenter.is_dublicate(
        ['abc', 'abt', 'abc', 'aq', 'ddd'], ['abc', 'kek', 'book', 'ddd', 'abc'],
        1, 1
    )

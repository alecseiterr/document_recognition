import easyocr
import numpy as np

reader = easyocr.Reader(['en', 'ru'])  # 'ru' для русского


def ocr_with_easyocr(cropped_fields):
    """
    Выполняет OCR для каждого обрезанного изображения в списке полей с использованием EasyOCR.

    :param cropped_fields: Список словарей с ключами "field_name" и "cropped_image".
    :return: Список словарей с полями "field_name" и "recognized_text".
    """
    recognized_data = []

    for field in cropped_fields:
        field_name = field['field_name']
        cropped_image = field['cropped_image']
        cropped_image_np = np.array(cropped_image)
        results = reader.readtext(cropped_image_np)
        recognized_text = " ".join([result[1] for result in results])
        recognized_data.append({
            "field_name": field_name,
            "recognized_text": recognized_text.strip()
        })
        # print(f"Распознано поле '{field_name}': {recognized_text.strip()}")

    return recognized_data

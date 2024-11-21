from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os

# Загрузка обученной модели YOLOv8
model = YOLO('best.pt')


def get_bounding_boxes_and_crops(image_path, output_folder, output_annotated_path):
    """
    Выполняет инференс YOLO на изображении, вырезает bounding boxes,
    сохраняет обрезанные изображения и аннотированное изображение с bounding boxes.

    :param image_path: Путь к исходному изображению.
    :param output_folder: Папка для сохранения обрезанных изображений.
    :param output_annotated_path: Путь для сохранения изображения с отрисованными bounding boxes.
    :return: Список словарей с полями "field_name", "cropped_image", и "bbox".
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Загружаем оригинальное изображение и создаем копию для отрисовки bounding boxes
    original_image = Image.open(image_path)
    annotated_image = original_image.copy()
    draw = ImageDraw.Draw(annotated_image)
    # Настройка шрифта
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # Выполняем инференс YOLO на изображении
    results = model(image_path)
    cropped_fields = []

    # Проходим по каждому детектированному объекту
    for result in results:
        boxes = result.boxes
        for i, box in enumerate(boxes):
            # Получаем координаты bounding box
            xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
            class_id = int(box.cls[0].item())  # Индекс класса
            field_name = model.names[class_id]  # Получаем имя класса по индексу
            # Обрезаем область изображения
            cropped_image = original_image.crop((xmin, ymin, xmax, ymax))
            # Сохраняем обрезанное изображение для наглядности (необязательно)
            cropped_image_path = os.path.join(output_folder, f"{field_name}_{i}.png")
            cropped_image.save(cropped_image_path)
            print(f"Сохранено промежуточное изображение: {cropped_image_path}")
            # Добавляем информацию о каждом поле в список
            cropped_fields.append({
                "field_name": field_name,
                "cropped_image": cropped_image,
                "bbox": (xmin, ymin, xmax, ymax)
            })

            # Отрисовка bounding box и текста на аннотированном изображении
            draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=4)
            draw.text((xmin, ymin - 20), field_name, fill="blue", font=font)

    # Сохранение аннотированного изображения с отрисованными bounding boxes
    annotated_image.save(output_annotated_path)
    print(f"Сохранено изображение с отрисованными bounding boxes: {output_annotated_path}")

    return cropped_fields

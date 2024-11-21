import fitz
import os


def pdf_to_high_res_png(pdf_path, output_folder, zoom_x=2.0, zoom_y=2.0):
    """
    Конвертирует один PDF файл в PNG изображения высокого разрешения для каждой страницы.

    :param pdf_path: Путь к PDF файлу.
    :param output_folder: Папка для сохранения PNG файлов.
    :param zoom_x: Масштабирование по оси X (для увеличения разрешения).
    :param zoom_y: Масштабирование по оси Y (для увеличения разрешения).
    :return: Список путей к сохраненным PNG файлам.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_document = fitz.open(pdf_path)
    saved_images = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        # высокое разрешение с помощью масштабирования
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        # уникальное имя файла
        image_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_num + 1}.png"
        image_path = os.path.join(output_folder, image_name)

        pix.save(image_path)
        saved_images.append(image_path)
        print(f"Сохранено изображение: {image_path}")

    pdf_document.close()
    return saved_images


# pdf_path = 'Dataset/your_pdf_file.pdf'  # Путь к PDF файлу
# output_folder = 'output_images'  # Папка для сохранения PNG файлов
# saved_images = pdf_to_high_res_png(pdf_path, output_folder, zoom_x=3.0, zoom_y=3.0)

# for img_path in saved_images:
#     print(f"Сохранено: {img_path}")

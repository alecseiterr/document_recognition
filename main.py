import streamlit as st
from yolo_1c_ux import get_bounding_boxes_and_crops
from ocr import ocr_with_easyocr
from convert_file import pdf_to_high_res_png

import os

# Streamlit
st.title("Система автоматического распознавания и заполнения финансовых документов в 1С.")
st.write("Этот инструмент позволяет загрузить PDF, преобразовать его в изображения и распознать текст.")

# Загрузка файла PDF через Streamlit
uploaded_file = st.file_uploader("Загрузите PDF файл", type=["pdf"])

if uploaded_file is not None:
    # директории для хранения данных
    output_folder = "output_images"
    intermediate_folder = "intermediate_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(intermediate_folder):
        os.makedirs(intermediate_folder)
    # Соханяем загруженный файл
    pdf_path = os.path.join(output_folder, uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Файл {uploaded_file.name} успешно загружен и сохранен.")
    # PDF в PNG
    st.write("Конвертация страниц PDF в изображения...")
    saved_images = pdf_to_high_res_png(pdf_path, output_folder, zoom_x=3.0, zoom_y=3.0)
    st.write(f"Количество изображений, сохраненных из PDF: {len(saved_images)}")
    # Обработка каждого PNG файла
    for image_path in saved_images:
        st.write(f"Обработка изображения: {os.path.basename(image_path)}")
        output_annotated_path = os.path.splitext(image_path)[0] + "_annotated.png"
        cropped_fields = get_bounding_boxes_and_crops(image_path, intermediate_folder, output_annotated_path)
        ocr_results = ocr_with_easyocr(cropped_fields)

        st.image(output_annotated_path, caption=f"Аннотированное изображение: {os.path.basename(image_path)}")
        # Выводим результаты детекции и OCR
        st.write("Распознанные поля и текст:")
        # обрезанное изображение с распознанным текстом
        for field, ocr_result in zip(cropped_fields, ocr_results):
            cropped_image = field['cropped_image']
            field_name = ocr_result['field_name']
            recognized_text = ocr_result['recognized_text']
            # изображение и распознанный текст
            st.image(cropped_image, caption=f"Поле:{field_name}")
            st.write(f"Распознанный текст:_______{recognized_text}")

    st.write("Обработка завершена.")

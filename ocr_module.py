import os
from pathlib import Path
import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model = AutoModelForSequenceClassification.from_pretrained("model")
tokenizer = AutoTokenizer.from_pretrained("model")
clf = pipeline("text-classification", model=model, tokenizer=tokenizer)

#  Preprocess Image for Better Detection

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot load image from path: {image_path}")

    # Resize to width 800 if smaller
    if image.shape[1] < 800:
        scale = 800 / image.shape[1]
        image = cv2.resize(image, (800, int(image.shape[0] * scale)))

    processed_path = Path(__file__).parent / "static" / "processed_image.jpg"

    cv2.imwrite(processed_path, image)

    return processed_path


#  Smart Filter to Remove Tiny or Low-Conf Boxes
def filter_small_boxes(result, min_width=15, min_height=10, min_area=100, min_conf=0.36):
    filtered = []
    for line in result[0]:
        box = line[0]
        conf = line[1][1]

        x_coords = [pt[0] for pt in box]
        y_coords = [pt[1] for pt in box]
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        area = width * height

        # Filter based on size and confidence
        if width >= min_width and height >= min_height and area >= min_area and conf >= min_conf:
            filtered.append(line)

    return [filtered]

#  Draw and Save OCR Boxes with Recognized Labels
def visualize_with_labels(image_path, result):
    # Load the image using OpenCV
    image_cv = cv2.imread(str(image_path))
    if image_cv is None:
        raise ValueError(f"Cannot load image for visualization from path: {image_path}")

    # Loop through the detected lines and draw a polygon for each bounding box
    for line in result[0]:
        # 'box' is a list of 4 [x, y] coordinates
        box = line[0]
        
        # Convert the coordinates to a NumPy array suitable for OpenCV
        points = np.array(box, dtype=np.int32).reshape((-1, 1, 2))
        
        # Draw the green polygon on the image
        cv2.polylines(
            img=image_cv, 
            pts=[points], 
            isClosed=True, 
            color=(0, 255, 0),  # Green color
            thickness=2
        )

    # Define the output path and save the final image
    output_path = Path(__file__).parent / "static" / "detected_output_with_labels.jpg"
    cv2.imwrite(str(output_path), image_cv)

    print(f" Bounding boxes drawn and saved at: {output_path}")

#  Main OCR Pipeline (Detection + Filtering)
def run_ocr(image_path):
    image = cv2.imread(image_path)
    min_side = min(image.shape[:2])
    det_limit_side_len = 960 if min_side < 1000 else 1216
    processed_image = preprocess_image(image_path)
    print(f"🛠️ Using det_limit_side_len: {det_limit_side_len}")
    ocr_model1 = PaddleOCR(
        det_model_dir=None,
        rec_model_dir=None,
        use_angle_cls=False,
        det_limit_side_len=det_limit_side_len,
        det_limit_type='min',
        use_gpu=False,
        drop_score=0.5,
        det_db_box_thresh=0.5,
        det_db_unclip_ratio=2,
        use_dilation=False,
        det_box_type='quad'
    )    
    result = ocr_model1.ocr(str(processed_image), cls=True)
    text_list = [line[1][0] for line in result[0]]

    result1 = clf(text_list)
    label = result1[0]['label']
    lang_map= {
    'en': 'en',
    'fr': 'fr',
    'hi': 'devanagari',
    'zh': 'ch',
    'de': 'de',
    'ja': 'japan',
    'te': 'te',
    'es': 'es',
    'ar': 'arabic',
    'ru': 'ru'
    }
    label2 = lang_map[label]
    print(label2)
    ocr_model2 = PaddleOCR(
        det_model_dir=None,
        rec_model_dir=None,
        use_angle_cls=False,
        lang=label2,
        det_limit_side_len=det_limit_side_len,
        det_limit_type='min',
        use_gpu=False,
        drop_score=0.5,
        det_db_box_thresh=0.5,
        det_db_unclip_ratio=2,
        use_dilation=False,
        det_box_type='quad'
        
    )



    print(" Running combined OCR detection and recognition...")
    result2= ocr_model2.ocr(str(processed_image), cls=True)

    if not result2[0]:
        print(" No text regions detected.")
        return []

    # Apply filtering to remove small/irrelevant boxes
    filtered_result = filter_small_boxes(result2)

    if not filtered_result[0]:
        print(" All text boxes were filtered out.")
        return []

    #  Visualize the cleaned results
    visualize_with_labels(processed_image, filtered_result)

    # Extract final recognized texts
    final_results = []
    for line in filtered_result[0]:
        box = line[0]              # Coordinates of the bounding box
        text = line[1][0]          # Detected text
        score = line[1][1]         # Confidence score

        final_results.append({
            "text": text,
            "confidence": score,
            "coordinates": box
        })
    output_path = Path(__file__).parent / "static" / "detected_output_with_labels.jpg"
    return final_results, output_path  # Return the path relative to static

def run_ocr_2(image_path, language):
    image = cv2.imread(image_path)
    min_side = min(image.shape[:2])
    det_limit_side_len = 960 if min_side < 1000 else 1216
    processed_image = preprocess_image(image_path)
    print(f" Using det_limit_side_len: {det_limit_side_len}")

    ocr_model2 = PaddleOCR(
        det_model_dir=None,
        rec_model_dir=None,
        use_angle_cls=False,
        lang= language,
        det_limit_side_len=det_limit_side_len,
        det_limit_type='min',
        use_gpu=False,
        drop_score=0.5,
        det_db_box_thresh=0.5,
        det_db_unclip_ratio=2,
        use_dilation=False,
        det_box_type='quad'
        
    )



    print(" Running combined OCR detection and recognition...")
    result2= ocr_model2.ocr(str(processed_image), cls=True)

    if not result2[0]:
        print(" No text regions detected.")
        return []

    #  Apply filtering to remove small/irrelevant boxes
    filtered_result = filter_small_boxes(result2)

    if not filtered_result[0]:
        print(" All text boxes were filtered out.")
        return []

    # #  Visualize the cleaned results
    visualize_with_labels(processed_image, filtered_result)

    #  Extract final recognized texts
    final_results = []
    for line in filtered_result[0]:
        box = line[0]              # Coordinates of the bounding box
        text = line[1][0]          # Detected text
        score = line[1][1]         # Confidence score

        final_results.append({
            "text": text,
            "confidence": score,
            "coordinates": box
        })
    output_path = Path(__file__).parent / "static" / "detected_output_with_labels.jpg"
    return final_results, output_path  # Return the path relative to static
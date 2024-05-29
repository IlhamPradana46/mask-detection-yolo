import cv2
import threading
import time


def resize_image(img, scale_percent) :
    # Calculate new size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def draw_box(img, result, class_list) :
    # Get information from results
    xyxy= result.boxes.xyxy.cpu().numpy()
    confidence= result.boxes.conf.cpu().numpy()
    class_id= result.boxes.cls.cpu().numpy().astype(int)
    # Get Class name
    class_name = [class_list[x] for x in class_id]
    # Pack together for easy use
    sum_output = list(zip(class_name, confidence,xyxy))
    # Copy image, in case that we need original image for something
    out_image = img.copy()
    for run_output in sum_output :
        # Unpack
        label, con, box = run_output

        if label == "with_mask" and con < 0.5:
            pass

        if label == "without_mask":
            box_color = (0, 0, 255)
        elif label == "with_mask":
            box_color = (0, 255, 0)


        # Choose color
        # text_color = (255,255,255)
        # Draw object box
        first_half_box = (int(box[0]),int(box[1]))
        second_half_box = (int(box[2]),int(box[3]))

        cv2.rectangle(out_image, first_half_box, second_half_box, box_color, 2)
        # Create text
        # text_print = '{label} {con:.2f}'.format(label = label, con = con)
        # Locate text position
        # text_location = (int(box[0]), int(box[1] - 10 ))
        # Get size and baseline
        # labelSize, baseLine = cv2.getTextSize(text_print, cv2.FONT_HERSHEY_SIMPLEX, 1, 2) 
        # Draw text's background
        cv2.rectangle(out_image, (int(box[0]), int(box[1])), (int(box[0]), int(box[1])), box_color , cv2.FILLED) 
        # Put text
        # cv2.putText(out_image, text_print ,text_location
        #             , cv2.FONT_HERSHEY_SIMPLEX , 1
        #             , text_color, 2 ,cv2.LINE_AA)
    return out_image
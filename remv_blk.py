import cv2
import numpy as np

selected_color = None

def select_pixel(event, x, y, flags, param):
    global selected_color
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_color = param[y, x]
        print(f"Selected color: {selected_color}")

def remove_similar_pixels(image_path, output_path, threshold=30):
    global selected_color

    # Load image
    img = cv2.imread(image_path)
    clone = img.copy()

    # Display image and let user click
    cv2.namedWindow("Select Pixel")
    cv2.setMouseCallback("Select Pixel", select_pixel, clone)

    while True:
        cv2.imshow("Select Pixel", clone)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key to break
            break

    cv2.destroyAllWindows()

    if selected_color is None:
        print("No pixel selected. Exiting.")
        return

    # Create range around selected color
    lower = np.clip(selected_color - threshold, 0, 255)
    upper = np.clip(selected_color + threshold, 0, 255)

    mask = cv2.inRange(img, lower, upper)

    # Replace matching pixels with white
    img[mask == 255] = [255, 255, 255]

    cv2.imwrite(output_path, img)
    print(f"Saved image with selected pixels removed to {output_path}")

# Example usage
remove_similar_pixels("smoke1.png", "output.jpg", threshold=30)

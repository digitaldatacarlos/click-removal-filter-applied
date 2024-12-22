import pyautogui
import cv2
import os
import time
import numpy as np

# File paths and configuration
base_directory = r"D:\\ready\\exported"
input_txt = os.path.join(base_directory, "input.txt")
output_txt = os.path.join(base_directory, "output.txt")
image_path = r"C:\\Users\\carlo\\Documents\\Coding20241205\\audacity_script\\picture_refence"
blue_image_path = os.path.join(image_path, "blue.png")
gray_image_path = os.path.join(image_path, "gray.png")
blue_image = cv2.imread(blue_image_path)
gray_image = cv2.imread(gray_image_path)

if blue_image is None or gray_image is None:
    print("Error: Unable to load reference images. Check file paths.")
    print(f"Blue image path: {blue_image_path}")
    print(f"Gray image path: {gray_image_path}")
    exit(1)

blue_image_resized = cv2.resize(blue_image, (225, 21))
gray_image_resized = cv2.resize(gray_image, (207, 22))
loop_limit = 2

def open_file(file_name):
    file_path = os.path.join(base_directory, file_name)
    print(f"Attempting to open file: {file_path}")
    try:
        os.system(f"start {file_path}")
        time.sleep(3)
        print(f"File {file_name} opened successfully.")
    except Exception as e:
        print(f"Error opening file {file_name}: {e}")
        raise

def detect_click_removal_status():
    print("Checking if click removal has been applied...")
    for attempt in range(loop_limit):
        pyautogui.press("esc")
        time.sleep(1)
        pyautogui.press("esc")
        time.sleep(1)
        pyautogui.hotkey("alt", "e")

        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result_blue = cv2.matchTemplate(screenshot, blue_image_resized, cv2.TM_CCOEFF_NORMED)
        result_gray = cv2.matchTemplate(screenshot, gray_image_resized, cv2.TM_CCOEFF_NORMED)

        max_val_blue = cv2.minMaxLoc(result_blue)[1]
        max_val_gray = cv2.minMaxLoc(result_gray)[1]

        print(f"Attempt {attempt + 1}/{loop_limit}: Blue match confidence: {max_val_blue}")
        print(f"Attempt {attempt + 1}/{loop_limit}: Gray match confidence: {max_val_gray}")

        if max_val_blue > 0.8 or max_val_gray > 0.8:
            print("Click removal detected.")
            pyautogui.press("esc")
            time.sleep(1)
            pyautogui.press("esc")
            time.sleep(1)
            return True
        else:
            print("Click removal not detected yet. Saving debug screenshot.")
            debug_path = f"debug_screenshot_attempt_{attempt + 1}.png"
            cv2.imwrite(debug_path, screenshot)
            print(f"Debug screenshot saved at: {debug_path}")
            pyautogui.press("esc")
            time.sleep(1)
            pyautogui.press("esc")
            time.sleep(1)

    print("Click removal status check reached maximum attempts without success.")
    return False

def apply_click_removal():
    print("Applying click removal filter...")
    try:
        pyautogui.hotkey("ctrl", "a")
        print("First Ctrl+A pressed.")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")
        print("Second Ctrl+A pressed.")
        time.sleep(1)
        pyautogui.press("h")
        print("H pressed to apply the filter.")
        time.sleep(1)
        pyautogui.press("enter")

        if not detect_click_removal_status():
            raise Exception("Click removal filter failed to apply.")
        print("Click removal application process completed.")
    except Exception as e:
        print(f"Error during click removal application: {e}")
        raise

def save_and_close_file(file):
    print(f"Saving and closing file: {file}")
    try:
        pyautogui.hotkey("ctrl", "s")
        print("Ctrl+S pressed to save the file.")
        time.sleep(2)

        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(base_directory, f"save_confirmation_{file}.png")
        screenshot.save(screenshot_path)
        print(f"Save confirmation screenshot saved at: {screenshot_path}")

        pyautogui.hotkey("ctrl", "w")
        print(f"File {file} closed successfully.")
        time.sleep(3)
    except Exception as e:
        print(f"Error saving or closing file {file}: {e}")
        raise

def main():
    print("Starting the automation process.")
    try:
        with open(input_txt, "r") as f:
            files = [line.strip() for line in f.readlines()]
        print(f"Loaded {len(files)} files from input.txt.")

        failed_files = []

        for idx, file in enumerate(files):
            print(f"Processing file {idx + 1}/{len(files)}: {file}")
            try:
                open_file(file)
                apply_click_removal()
                save_and_close_file(file)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                failed_files.append(file)

        with open(output_txt, "w") as f:
            print("Writing failed files to output.txt...")
            for file in failed_files:
                f.write(file + "\n")

        if failed_files:
            print(f"Process completed with errors. {len(failed_files)} files failed.")
        else:
            print("Process completed successfully. No files failed.")
    except Exception as e:
        print(f"Critical error during processing: {e}")

if __name__ == "__main__":
    main()

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
blue_image = cv2.imread(os.path.join(image_path, "blue.png"))
gray_image = cv2.imread(os.path.join(image_path, "gray.png"))
blue_image_resized = cv2.resize(blue_image, (300, 50))  # Adjust size as per requirements
gray_image_resized = cv2.resize(gray_image, (300, 50))
loop_limit = 1000

def open_file(file_name):
    file_path = os.path.join(base_directory, file_name)
    print(f"Attempting to open file: {file_path}")
    os.system(f"start {file_path}")
    time.sleep(3)  # Wait for the file to open
    print(f"File {file_name} opened successfully.")

def detect_click_removal_status():
    print("Checking if click removal has been applied...")
    while True:
        pyautogui.hotkey("alt", "e")
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result_blue = cv2.matchTemplate(screenshot, blue_image_resized, cv2.TM_CCOEFF_NORMED)
        result_gray = cv2.matchTemplate(screenshot, gray_image_resized, cv2.TM_CCOEFF_NORMED)
        
        if cv2.minMaxLoc(result_blue)[1] > 0.8 or cv2.minMaxLoc(result_gray)[1] > 0.8:
            print("Click removal detected.")
            pyautogui.press("esc")
            return True
        else:
            print("Click removal not detected yet.")

        pyautogui.press("esc")
        time.sleep(2)

def apply_click_removal():
    print("Applying click removal filter...")
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
    detect_click_removal_status()
    print("Click removal application process completed.")
    time.sleep(1)

def main():
    print("Starting the automation process.")
    with open(input_txt, "r") as f:
        files = [line.strip() for line in f.readlines()]

    failed_files = []

    for idx, file in enumerate(files):
        print(f"Processing file {idx + 1}/{len(files)}: {file}")
        try:
            open_file(file)

            loop_count = 0
            while loop_count < loop_limit:
                print(f"Starting loop {loop_count + 1} for file: {file}")
                apply_click_removal()
                loop_count += 1
                print(f"Loop {loop_count} completed for file: {file}")

                if loop_count >= loop_limit:
                    print(f"Loop limit reached for file: {file}")
                    failed_files.append(file)
                    break

            # Close the file
            print(f"Closing file: {file}")
            pyautogui.hotkey("ctrl", "w")
            time.sleep(2)
            print(f"File {file} closed successfully.")
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            failed_files.append(file)

    with open(output_txt, "w") as f:
        print("Writing failed files to output.txt...")
        for file in failed_files:
            f.write(file + "\n")

    print("Process completed. Logs written to output.txt.")

if __name__ == "__main__":
    main()

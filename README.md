

# Click Removal Filter Applied

## Overview
This repository contains a Python script designed to apply the "Click Removal" filter to audio files in Audacity automatically. The script leverages PyAutoGUI and OpenCV to handle GUI automation and image recognition, enabling seamless processing of multiple audio files.

---

## Key Features
- Automates the application of the "Click Removal" filter in Audacity.
- Utilizes image recognition to detect filter application status.
- Handles file saving and ensures smooth transitioning between files.
- Includes debugging mechanisms for error detection and troubleshooting.

---

## Configuration Details

### Parameters
- **`loop_limit`**: Specifies the number of attempts to check whether the "Click Removal" filter has been successfully applied. A value of 9 works for 1-hour 30-minute audio files, but longer audio clips (e.g., 12 hours) require a higher value.

- **`save_and_close_file()`**: This function requires a delay (default: 20 seconds) to ensure that Audacity's "Compressing File" popup disappears before proceeding. Adjust this value for longer audio files.

---

## Motivation
### Why was this script created?
Applying the "Click Removal" filter to large audio files manually can be tedious and error-prone. Existing methods, such as Nyquist or Python libraries, either lacked the necessary features or failed to support Audacity's current file formats (e.g., `.aup3`). This script automates the process effectively.

### The Problem It Solves
Nyquist scripting is outdated and unsupported, while no Python libraries offer click removal for `.aup3` or `.wav` files. This script bridges the gap by using OpenCV and GUI automation to interact with Audacity's user interface directly.

---

## How It Works
The script uses:
- **OpenCV**: To match UI elements (e.g., "Undo Click Removal") based on screenshots.
- **PyAutoGUI**: To simulate keyboard and mouse actions, ensuring smooth automation of the filtering process.

Debugging statements and screenshot captures are incorporated for error handling and diagnostics.

---

## Requirements

### Operating System
- **Windows 10**: The script's behavior depends on UI element colors, which may vary across operating systems.

### Setup Instructions
1. **Custom Screenshots**:
   - Create reference images for the "Undo Click Removal" button in both blue and gray states (visible in the Edit tab of Audacity).
   - Save these images in the `picture_reference` directory.
2. **Key Bindings**:
   - Assign the "Apply Click Removal Filter" action to the `H` key in Audacity's settings.

### Dependencies
- **Python 3.x**
- **Required Libraries**:
  - `pyautogui`
  - `opencv-python`
  - `numpy`

Install dependencies using:
```bash
pip install pyautogui opencv-python numpy
```

---

## Usage Instructions
1. Prepare your audio files and place them in the designated input folder.
2. List all file names in a text file named `input.txt` and place it in the `D:\ready\exported` directory.
3. Run the script using:
```bash
python script_name.py
```
4. Processed files will be saved, and any failed files will be logged in `output.txt`.

---

## Limitations and Known Issues
- **Cross-Platform Compatibility**:
   - The script is optimized for Windows 10 and may not work as intended on other operating systems due to UI differences.
- **File Length**:
   - Default settings are tuned for 1-hour 30-minute files. Adjust `loop_limit` and `save_and_close_file` delays for longer audio files.
- **Error Handling**:
   - Debugging screenshots are saved for failed attempts to facilitate troubleshooting.

---

## Future Improvements
- Enhance cross-platform compatibility.
- Integrate dynamic UI element detection to eliminate dependency on specific colors.
- Add support for processing `.wav` files directly.

---

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the script as needed.

---

## Contact
For questions or feedback, please reach out via GitHub issues or directly to my email.


# SnapIn TimeLog

SnapIn TimeLog is a Face Recognition Attendance System that simplifies attendance tracking through real-time facial recognition. This system is designed to offer a reliable, user-friendly, and automated solution for attendance management.

## Table of Contents
- [Hardware and Software Requirements](#hardware-and-software-requirements)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Requirements](#software-requirements)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

---

## Hardware and Software Requirements

### Hardware Requirements

The SnapIn TimeLog application requires a computer with the following specifications:

1. **Computer Specifications**  
   - Processor: Minimum Intel i3 or Ryzen 3, recommended Intel i5 or Ryzen 5.
   - RAM: 8GB to 16GB.
   - Storage: Minimum 512GB SSD.

2. **Webcam Specifications**  
   - **Resolution:** Minimum 1280x720 (720p).
   - **Frame Rate:** 30 fps.
   - **Light Handling:** Should perform well in various lighting conditions, including low-light environments.
   - **Mounting and Placement:** The camera should be securely mounted and positioned at an optimal height and angle to capture faces accurately and reduce distortions.

3. **Internet Connection**  
   - Stable broadband connection with a minimum download speed of 5 Mbps and upload speed of 1 Mbps.

### Software Requirements

1. **Integrated Development Environment (IDE)**  
   - Visual Studio Code is recommended for development.

2. **Programming Language**  
   - Python is used for both the front-end GUI and the face recognition functionality due to its extensive libraries and frameworks.

3. **Python Libraries and Frameworks**  
   - `face_recognition`: For facial recognition functionality.
   - `numpy`: For numerical operations.
   - `pandas`: For data handling.
   - `customtkinter`: For GUI components.
   - `tkinter`: For basic GUI.
   - `scipy`: For scientific computing.
   - `Pillow`: For image processing.

4. **Database**  
   - XAMPP server to store and manage data from the SnapIn TimeLog web application, including attendance records, user information, and other relevant data.

5. **Face Recognition Algorithm**  
   - **Haar Cascade Algorithm**: Developed by Paul Viola and Michael Jones, this algorithm detects facial features by applying Haar-like features to image regions. It detects variations in brightness and contrast to recognize faces effectively.

---

## Features

- Automated facial recognition attendance.
- Real-time processing and data storage.
- Flexible GUI for user interaction and management.

---

## Technologies Used

- **Programming Language**: Python
- **Database**: MySQL (via XAMPP)
- **GUI**: Tkinter with customtkinter components
- **Face Recognition Algorithm**: Haar Cascade

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/snapin-timelog.git
   cd snapin-timelog

# Photo Metadata Extractor

A simple Python script to extract metadata (EXIF) from an image.

## Features

* Camera Make & Model
* Date & Time Taken
* Image Resolution
* ISO
* Exposure Time
* Aperture
* Focal Length
* GPS Coordinates (if available)
* Place, City, State & Country
* Full Address
* Google Maps Link

## Requirements

* Python 3.9+
* Pillow
* geopy

Install dependencies:

```bash
pip install pillow geopy
```

or

```bash
py -m pip install pillow geopy
```

## Project Structure

```
project/
│── main.py
│── test.jpg
└── requirements.txt
```

## Usage

1. Copy your image into the project folder.
2. Rename the image to **test.jpg** (or update the filename in `main.py`).
3. Run the script:

```bash
python main.py
```

or

```bash
py main.py
```

## Example Output

```
PHOTO METADATA
------------------------------------------------
Camera Make      : Apple
Camera Model     : iPhone 15
Date Taken       : 2026:07:29 10:30:15
Image Size       : 4032 x 3024

GPS INFORMATION
Latitude         : 19.218560
Longitude        : 72.978421

LOCATION DETAILS
Place            : Hiranandani Estate
City             : Thane
State            : Maharashtra
Country          : India

Google Maps
https://maps.google.com/?q=19.218560,72.978421
```

## Notes

* GPS information is only available if the image contains location metadata.
* Images shared through apps like WhatsApp, Instagram, Facebook, or Telegram often have GPS metadata removed for privacy.
* If no GPS metadata exists, the script will still display the available camera and image information.

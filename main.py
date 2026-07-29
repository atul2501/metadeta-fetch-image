from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim


def convert_to_degrees(value):
    """Convert GPS coordinates to decimal degrees"""

    def rational_to_float(r):
        if isinstance(r, tuple):
            return r[0] / r[1]
        return float(r)

    d = rational_to_float(value[0])
    m = rational_to_float(value[1])
    s = rational_to_float(value[2])

    return d + (m / 60.0) + (s / 3600.0)


def get_gps_info(gps_data):
    gps_info = {}

    for key, val in gps_data.items():
        decoded = GPSTAGS.get(key, key)
        gps_info[decoded] = val

    if "GPSLatitude" not in gps_info or "GPSLongitude" not in gps_info:
        return None

    lat = convert_to_degrees(gps_info["GPSLatitude"])
    lon = convert_to_degrees(gps_info["GPSLongitude"])

    if gps_info.get("GPSLatitudeRef") != "N":
        lat = -lat

    if gps_info.get("GPSLongitudeRef") != "E":
        lon = -lon

    return lat, lon


def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent="photo_metadata")

        location = geolocator.reverse(
            (lat, lon),
            language="en",
            exactly_one=True,
        )

        if not location:
            return None

        addr = location.raw.get("address", {})

        return {
            "full_address": location.address,
            "place": addr.get("suburb")
            or addr.get("neighbourhood")
            or addr.get("village")
            or addr.get("hamlet")
            or addr.get("town")
            or addr.get("city"),
            "city": addr.get("city")
            or addr.get("town")
            or addr.get("municipality"),
            "district": addr.get("county"),
            "state": addr.get("state"),
            "country": addr.get("country"),
            "postcode": addr.get("postcode"),
        }

    except Exception as e:
        print("Reverse geocoding error:", e)
        return None


def get_metadata(image_path):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print("Image not found!")
        return

    exif = img._getexif()

    if not exif:
        print("No EXIF metadata found.")
        return

    metadata = {}

    for tag, value in exif.items():
        decoded = TAGS.get(tag, tag)
        metadata[decoded] = value

    print("=" * 70)
    print("PHOTO METADATA")
    print("=" * 70)

    print(f"Camera Make      : {metadata.get('Make', 'N/A')}")
    print(f"Camera Model     : {metadata.get('Model', 'N/A')}")
    print(f"Date Taken       : {metadata.get('DateTimeOriginal', 'N/A')}")
    print(f"Last Modified    : {metadata.get('DateTime', 'N/A')}")
    print(f"Image Size       : {img.size[0]} x {img.size[1]}")

    print(f"Lens             : {metadata.get('LensModel', 'N/A')}")
    print(f"ISO              : {metadata.get('ISOSpeedRatings', 'N/A')}")
    print(f"Exposure Time    : {metadata.get('ExposureTime', 'N/A')}")
    print(f"Aperture         : {metadata.get('FNumber', 'N/A')}")
    print(f"Focal Length     : {metadata.get('FocalLength', 'N/A')}")

    gps = metadata.get("GPSInfo")

    if gps:

        coords = get_gps_info(gps)

        if coords:

            lat, lon = coords

            print("\n" + "=" * 70)
            print("GPS INFORMATION")
            print("=" * 70)

            print(f"Latitude         : {lat}")
            print(f"Longitude        : {lon}")

            place = reverse_geocode(lat, lon)

            if place:
                print("\nLOCATION DETAILS")
                print("-" * 40)

                print(f"Place            : {place['place']}")
                print(f"City             : {place['city']}")
                print(f"District         : {place['district']}")
                print(f"State            : {place['state']}")
                print(f"Country          : {place['country']}")
                print(f"Postal Code      : {place['postcode']}")

                print("\nFull Address")
                print(place["full_address"])

                print("\nGoogle Maps")
                print(f"https://maps.google.com/?q={lat},{lon}")

            else:
                print("Unable to determine place.")

        else:
            print("\nGPS metadata exists but is incomplete.")

    else:
        print("\nNo GPS location found in this image.")


if __name__ == "__main__":
    get_metadata("test.jpg")
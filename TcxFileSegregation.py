import lxml.etree as ET
import shutil
import os

# Delete the contents of the folder before re-running the script
try:
    folder_path = '/content/Moved'
    shutil.rmtree(folder_path)
    print('Folder and its content removed')
except:
    print('Folder not deleted')

# Function to clean the XML content in the event there are any unwanted characters or whitespaces preceding the xml declaration
def clean_xml_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Remove any unwanted characters or whitespace before the XML declaration
    cleaned_content = content.lstrip()
    return cleaned_content


# Directory containing the .tcx files
source_dir = "/content"
destination_dir = '/content/Moved'

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Define the XML namespace
namespace = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}

# Iterate over all .tcx files in the source directory
for file_name in os.listdir(source_dir):
    if file_name.endswith('.tcx'):
        file_path = os.path.join(source_dir, file_name)

        # Clean the XML content
        cleaned_content = clean_xml_content(file_path)
        # Parse the cleaned XML content
        root = ET.fromstring(cleaned_content.encode('utf-8'))

        # Find the activity type
        activity = root.find('.//ns:Activity', namespaces=namespace)
        activity_type = activity.get('Sport') if activity is not None else 'Unknown'

        # Check if the activity type is 'Ride' and save a copy if true
        if activity_type == 'Ride':
            # Define the destination file path
            destination_path = os.path.join(destination_dir, file_name)

            # Copy the file to the destination directory
            shutil.copy(file_path, destination_path)
            print(f"File copied to {destination_path}")
        else:
            print(f"The activity type is not 'Ride' for file {file_path}. No file copied.")

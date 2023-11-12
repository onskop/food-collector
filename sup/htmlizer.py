import json
import re
import gcsfs

def convert_to_html(mixed_content,images, output_html_file):
    # Split the content into parts using "PIC:" as the delimiter
    parts = re.split(r'PIC:\s*', mixed_content)
    # Remove the first empty string if it exists
    if parts and not parts[0].strip():
        parts.pop(0)

    # The HTML header with the inclusion of Bootstrap for styling
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Image and JSON Viewer</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        pre {outline: 1px solid #ccc; padding: 5px; margin: 5px; }
        img {max-width: 100%; height: auto; margin-bottom: 20px;}
    </style>
</head>
<body>
<div class="container">
    '''

    # Process each part and append to HTML content
    for part in parts:
        # Extract image file name and JSON content
        img_name, json_content = part.strip().split('\n', 1)
        json_formatted = json.dumps(json.loads(json_content), indent=4)
        # Append the image and formatted JSON to the HTML content
        html_content += f'<h2>{img_name}</h2>\n'
        html_content += f'<img src="{images}\{img_name}" alt="{img_name}">\n'
        html_content += f'<pre><code class="json">{json_formatted}</code></pre>\n'

    # Close the HTML tags
    html_content += '''
</div>
</body>
</html>
'''

    # Write the HTML content to the specified file
    with open(output_html_file, 'w') as file:
        file.write(html_content)

def read_gcs(bucket_name, blob_name, key_path):

    fs = gcsfs.GCSFileSystem(token=key_path)
    
    # Use the file-like interface
    with fs.open(f'{bucket_name}/{blob_name}', 'r', encoding = 'utf-8') as f:
        content = f.read()
        
    return content


svc_key = r'C:\Projects\Python\2_Experimental\Projekty\4_nutrii\food-collector\.streamlit\gcs_gymbro.json'
file = 'img_data.json'


fs = gcsfs.GCSFileSystem(token=svc_key)

imgpath = r'C:\Users\onsko\Downloads\images'

mixed_string = read_gcs('food-bro',file,svc_key)
convert_to_html(mixed_string, imgpath, imgpath + '\output.html')

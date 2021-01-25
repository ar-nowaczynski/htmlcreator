import numpy as np
import pandas as pd
from htmlcreator import HTMLDocument

np.random.seed(123)

# Create new document with default CSS style
document = HTMLDocument()

# Set document title
document.set_title('my first document title')

# Add main header
document.add_header('my first document header level 1', level='h1', align='center')

# Add section header
document.add_header('section header level 2')  # defaults: level='h2' align='left'

# Add text paragraphs
long_text = ', '.join(['this is text'] * 50)
document.add_paragraph(long_text, size='14px', indent='15px', align='justify')
document.add_paragraph('more text')  # defaults: size='16px', indent='0' alight='left'

# Embed images
document.add_header('images section')
image_arrays = np.random.randint(0, 256, size=(50, 4, 4, 3), dtype=np.uint8)
for i in range(len(image_arrays)):
    if i % 47 == 0:
        document.add_line_break()  # Enforce new line
    # Add image
    document.add_image(
        image=image_arrays[i],  # numpy array / PIL Image / pathlib.Path
        title=f'image{i}',
        height=32,
        pixelated=True,
    )

# Embed pandas DataFrame
document.add_header('table section')
num_rows = 5
num_cols = 10
df = pd.DataFrame(
    data=np.random.randn(num_rows, num_cols),
    index=pd.date_range('19700101', periods=num_rows),
    columns=[f'c{i}' for i in range(num_cols)],
)
df['last_column'] = 'value_str'
df.index.name = 'date'
document.add_table(df)

# Enforce page break (useful when printing HTML to PDF in the browser)
document.add_header('page break example')
for i in range(15):
    document.add_paragraph('mhm')
document.add_paragraph('before page break')
document.add_page_break()
document.add_header('after page break')

# Add image link (filepath or URL)
document.add_header('image from the Internet')
image_url = 'https://spacecenter.org/wp-content/uploads/2020/01/KSC-20200117-PH-SPX01_0001_medium.jpg'
document.add_image_link(image_url, title='image from the Internet', width='60%')

# Write to file
output_filepath = '1_first_document.html'
document.write(output_filepath)
print(f'{output_filepath} has been saved successfully!')

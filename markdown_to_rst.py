import pypandoc
from pypandoc.pandoc_download import download_pandoc

download_pandoc(delete_installer=True)

output = pypandoc.convert_text(
    source=open('README.md').read(),
    to='rst', format='md'
)
with open('README.rst', 'w') as f:
    f.write(output)

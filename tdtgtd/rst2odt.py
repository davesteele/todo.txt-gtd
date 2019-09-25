try:
    import locale

    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass

from docutils.core import publish_cmdline_to_binary, default_description
from docutils.writers.odf_odt import Writer, Reader


description = (
    "Generates OpenDocument/OpenOffice/ODF documents from "
    "standalone reStructuredText sources.  " + default_description
)


def rst2odt(infile, outfile):
    args = ["--create-links", infile, outfile]

    writer = Writer()
    reader = Reader()
    publish_cmdline_to_binary(
        reader=reader, writer=writer, description=description, argv=args
    )

import sys
import os
import unicodedata
import encodings.idna

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath("src"))
    from alenia_porter.cli import main
    main()

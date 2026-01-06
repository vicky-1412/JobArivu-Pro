import streamlit.web.cli as stcli
import os, sys

if __name__ == "__main__":
    # app.py thaan unga main code file
    sys.argv = ["streamlit", "run", "app.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())
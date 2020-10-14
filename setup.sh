mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"magdieltercero@hotmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

mkdir data_store

python spreadsheet.py

python update_addresses.py
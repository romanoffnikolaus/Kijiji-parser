Content
* [Description](#Description)
* [Installation](#Installation)

## Description
Parser for https://www.kijiji.ca. You can run scrip and after few seconds get information about all apartments: title, description, currency, price, location, publication date, image link. You can check database "kijiji_data" as a result.

## Installation

1. Create virtual machine
```bash
python3 -m venv <venv_name>
```

2. Activate your virtual machine
```bash
. venv/bin/activate
```
3. Install all the dependencies
```bash
pip install -r requirements.txt
```

4. Download Selenium chrome driver
```
https://chromedriver.chromium.org/home
```

5. Create .env with templates from .env_template and input your data for connecting PSQL and path to selenium driver.
```
PSQL_secure_data = postgresql://USER:PASSWORD@HOST:PORT/DB_NAME
```
6. Run parser in parsers.py
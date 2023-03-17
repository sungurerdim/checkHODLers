# checkHODLers
A Python script that checks a list of wallets to see if they have a specific token at a specific date

### Usage

- Install necessary packages
```
pip install -r requirements.txt
```

- Create <b>".env"</b> file, must contain <b>API_URL</b> and <b>API_KEY</b> variables.
- Create <b>"input.csv"</b> file, each row must contain a wallet address and token contract address.
- Run the script:
```
python main.py
```
- Specify a <b>date</b> for token balance check.
- Check <b>output</b> directory for script results. Script will create separate files for each row of input file (with every transaction they had until the target date, only with the specified token) and a combined file (only has token balances of all wallets in input file).
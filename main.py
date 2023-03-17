from utils.common import *
from utils.network import *
from utils.colorization import *
from utils.file_operations import *

clear()
load_dotenv()

TOKEN_DECIMAL_PLACES: int = 18
API_ENDPOINT: str = envs.get('API_URL')
API_KEY: str = envs.get('API_KEY')

def validate_environment_variables() -> None:
    if not API_ENDPOINT:
        print()
        print(redLight("Please provide an API endpoint using 'API_URL' as variable name in .env file."))
        print(yellowLight("Example: API_URL = 'https://api.bscscan.com/api'"))
        exit(1)

    if not API_KEY:
        print()
        print(redLight("Please provide an API key using 'API_KEY' as variable name in .env file."))
        print(yellowLight("Example: API_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"))
        exit(1)

def main() -> None:
    input_file: str = "input.csv"
    if not file_exists(input_file):
        return

    end_date_str: str  = getUserInput("Enter the end date (dd.mm.yyyy)")
    if not end_date_str:
        end_date_str = datetime.now().strftime("%d.%m.%Y")

    end_date: int = date_str_to_timestamp(end_date_str)

    address_list: List[Tuple[str, str]] = read_csv_file(input_file)
    address_list: List[Tuple[str, str]] = [(row[0].lower(), row[1].lower()) for row in address_list]

    output_directory = "output"
    if not path.exists(output_directory):
        makedirs(output_directory)

    chdir(output_directory)

    balances: List[List[str]] = []
    balances.append(['Address', 'Token', 'Total Balance'])

    for row_ind, row in enumerate(address_list):
        wallet: str = row[0]
        token_address: str = row[1]

        if not wallet.startswith("0x") or len(wallet) != 42:
            continue

        params: dict = {
            "module": "account",
            "action": "tokentx",
            "address": wallet,
            "contractaddress": token_address,
            "startblock": "0",
            "endblock": "999999999",
            "sort": "asc",
            "apikey": API_KEY
        }

        while True:
            try:
                response: List[List[str]] = getRequestResult(API_ENDPOINT, params)
                break
            except (ConnectionError, TimeoutError):
                # API request failed, try again
                continue

        token_balance: np.float64 = np.float64(0)

        transactions: List[List[str]] = []
        transactions.append(['Address', 'Transfer Date', 'Transaction Type', 'Transferred Amount', 'Sent By', 'Sent To', 'Token Address', 'Token Name'])

        for transaction in response:
            txn_timestamp = int(transaction["timeStamp"])

            if txn_timestamp <= end_date:
                filtered_transaction_details: List[str] = process_transaction(transaction, wallet, token_address)
                transactions.append(filtered_transaction_details)

                token_name: str = filtered_transaction_details[-1]
                token_balance += filtered_transaction_details[3]

        save_list_as_xlsx(transactions, f"Transactions_row{(row_ind+1)}.xlsx")

        print()
        print(cyanLight("Balance of"), yellowLight(wallet), cyanLight(":"), white(round(token_balance,2)), cyanLight(token_name))
        balances.append([wallet, token_name, token_balance])

    output_file = "Token_Balances.xlsx"
    save_list_as_xlsx(balances, output_file)

def process_transaction(transaction, wallet, token_address):
    txn_timestamp: int = int(transaction["timeStamp"])
    transfer_date: str = datetime.utcfromtimestamp(txn_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    sent_by: str = transaction["from"].lower()
    sent_to: str = transaction["to"].lower()
    transferred_amount: np.float64 = np.divide(np.float64(transaction["value"]), np.float64(10 ** TOKEN_DECIMAL_PLACES))

    token_name: str = transaction["tokenName"]

    if sent_by == wallet:
        txn_type: str = "SENT"
        sent_by: str = "This Wallet"
        transferred_amount = transferred_amount * (-1)
    elif sent_to == wallet:
        txn_type: str = "RECEIVED"
        sent_to: str = "This Wallet"

    return [wallet, transfer_date, txn_type, transferred_amount, sent_by, sent_to, token_address, token_name]

if __name__ == "__main__":
    validate_environment_variables()
    main()

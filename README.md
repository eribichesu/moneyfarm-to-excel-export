# Moneyfarm to Excel Export

Moneyfarm to Excel Export is a Python project that authenticates with the Moneyfarm API to retrieve portfolio data and export it to an Excel file. The project prompts the user for their Moneyfarm credentials and allows them to choose whether to export the data.

## License

This project is licensed under the GNU AGPLv3 License. See the [LICENSE](LICENSE) file for details.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/eribichesu/moneyfarm-to-excel-export.git
    cd moneyfarm-to-excel-export
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:
    ```bash
    python consume_api.py
    ```

2. Enter your Moneyfarm username and password when prompted.

3. Choose whether to export the data to an Excel file (default is Yes).

The script will authenticate with the Moneyfarm API, retrieve your portfolio data, display it in the console, and optionally export it to an Excel file.

## Retrieving the Moneyfarm's web app `AUTH0_CLIENT_ID`

To retrieve the `AUTH0_CLIENT_ID` from the Moneyfarm web application:

1. Visit the [Moneyfarm login page](https://app.moneyfarm.com/it/sign-in).
2. Open the developer tools in your browser (F12 or right-click and select "Inspect").
3. Go to the "Network" tab and log in with your credentials.
4. Look for network requests related to authentication and inspect them.
5. The `AUTH0_CLIENT_ID` will be present in the request details.

## Disclaimer

I have no relationship with Moneyfarm. This code is provided as-is, without any guarantees. Use it at your own risk. Make sure to comply with Moneyfarm's terms of service and obtain the necessary permissions to access their APIs.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any issues or questions, please open an issue in the repository or contact me at edoardo.ribichesu@gmail.com
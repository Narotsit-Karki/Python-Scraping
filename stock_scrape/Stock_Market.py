import time, requests, json, datetime
import pandas as pd
import matplotlib.dates as mpldates
import mplfinance as mpl
import matplotlib.pyplot as plt


def convert_to_csv(stock_data, company):
    i = 0
    for date, open, close, high, low, volume in zip(stock_data['t'], stock_data['o'], stock_data['c'], stock_data['h'],
                                                    stock_data['l'], stock_data['v']):
        ts = datetime.datetime.fromtimestamp(date)
        stock_data['o'][i] = float(open)
    stock_data['c'][i] = float(close)
    stock_data['h'][i] = float(high)
    stock_data['l'][i] = float(low)
    stock_data['v'][i] = float(volume)

    i += 1


    stock_data['Date'] = stock_data.pop('t')
    stock_data['Open'] = stock_data.pop('o')
    stock_data['Close'] = stock_data.pop('c')
    stock_data['High'] = stock_data.pop('h')
    stock_data['Low'] = stock_data.pop('l')
    stock_data['Volume'] = stock_data.pop('v')
    dataframe = pd.DataFrame(stock_data)
    dataframe.to_csv(f'data/{company}_x.csv', index=False)


def print_graphs(company, company_name):
    # for company in lists:
    try:
        stock_graph = pd.read_csv(f'data/{company}_x.csv', index_col=0, parse_dates=True)
    except Exception:
        print(f"[❌] Data not Found for {company}")
        return

    stock_graph = stock_graph.tail(110)
    open = stock_graph["Open"]
    high = stock_graph["High"]
    low = stock_graph["Low"]
    close = stock_graph["Close"]
    plt.style.use('dark_background')
    fig, ax = plt.subplots(2, figsize=(13, 7))
    fig.suptitle(f'{company_name}', color='purple', fontsize=10)

    print('[✅] Displaying Charts...')
    ax[0].plot(open, c='green')
    ax[0].plot(close, c='red')
    ax[0].legend(['Open', 'Close'], fontsize=18)
    ax[1].plot(high)
    ax[1].plot(low)
    ax[1].legend(['High', 'Low'], fontsize=18)

    mc = mpl.make_marketcolors(up='green', down='red', inherit=True)

    s = mpl.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)

    mpl.plot(stock_graph, type="candle", mav=(2), figsize=(13, 8), style=s,
             volume=True)  # savefig=f'data/{company}_candlestick.png')
    data = stock_graph.tail(10)

    display(data.loc[::-1])
    # fig.savefig(f'data/{company}_x.png')


try:
    # for company in lists:
    company = input("[🔻] Enter Company Symbol: ").upper()
    url = f"https://nepsealpha.com/trading/1/history?symbol={company}&resolution=1D&from=1651380464&to={time.time()}&pass=ok&force=10310&currencyCode=NRS"
    url2 = f"https://nepsealpha.com/ajax/symbols?term={company}"
    dataframe = requests.get(url)
    stock_data = json.loads(dataframe.content)
    if stock_data['s'] == 'ok':
        company_name = requests.get(url2)
        company_name = json.loads(company_name.content)
        company_name = company_name[0]['label']
        del stock_data['s']
        convert_to_csv(stock_data, company)
        print(f'[✅] Fetched New Data from https://nepsealpha.com/trading/chart ==> [\033[35m{company_name}\033[00m]')
        print_graphs(company=company, company_name=company_name)
    else:
        print(f"[❌] No Data found for {company}")

except Exception as ex:
    print('[❌] Could not Fetch New Data , Check your Internet... ')
    print('[✅] Fetchig Previous Data...')
    print_graphs(company=company, company_name=company)

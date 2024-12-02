# FINT*PIO BOT FOR FINT*PIO TELEGRAM

Fint*pio Bot is a Python-based automation tool designed to interact with the Fint*pio API. This bot automates tasks such as daily check-ins, farming, and task management, streamlining your interactions with Fint*pio's services.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [CONTACT](https://t.me/imspecials)

### This bot helpfull?  Please support me by buying me a coffee: 
```
0x705C71fc031B378586695c8f888231e9d24381b4 - EVM
TDTtTc4hSnK9ii1VDudZij8FVK2ZtwChja - TRON
UQBy7ICXV6qFGeFTRWSpnMtoH6agYF3PRa5nufcTr3GVOPri - TON
```

## HOW TO REGISTER 
Fint*pio is a global fintech and cryptocurrency company that has created a cryptocurrency wallet of the same name on messaging app Telegram. Steve Milton Co-Founder and CEO Fint*pio is Ex-VP @binance and Ex-CMO  @bnbchain.

 1. Visit [Telegram Fint*pio](https://fintop.io/2uN2W9eRCj)
 2. Start the bot
 3. Create a Wallet & Backup
 4. Full Post https://t.me/Deeplchain/18347
 5. Install this Respository and Have Fun

## Features Update 2024-10-07

- **Proxy Support:** Added proxy usage to the script `proxies.txt`
- **Daily Check-In:** Revamping the daily check-in streak `enchanced`
- **Profile Management:** Fetch and display username and balance.
- **Farming Automation:** Start, monitor, and claim farming rewards with ease.
- **Task Management:** Automatically start, verify, and claim tasks for diamond rewards.
- **Play Space Tapper Game:** Automatically play the Space Tapper Game. `NEW`
- **Diamond Collection:** Automate diamond collection tasks and monitor next available timings.

## Requirements

This bot is built using Python and requires several dependencies. Install them via the `requirements.txt` file.

### Python Version

- Python 3.10 or higher

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/nadirasaid8/fintohub.git
    cd fintohub
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create and configure your `config.json` file to manage bot settings.
    ```json
    {
        "use_proxies": false,
        "auto_break_asteroid": false,
        "auto_complete_task": false,
        "auto_play_game": false,
        "game_safe_mode": false,
        "min_game_play": 3,
        "max_game_play": 7,
        "game_delay": 3,
        "account_delay": 5
    }
    ```

## Usage

1. Use PC/Laptop or Use USB Debugging Phone
2. open the `fint*pio wallet bot`
3. Inspect Element `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links "`fint*piowallet`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
    query_id=xxxxxxxxx- or user=xxxxxxxxx-
```
9. add it to `data.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
    query_id=xxxxxxxxx-Rxxxxuj&user=%7B%22id%22%3A132373337hash=xxxx
    user=xxxxxxxxx-Rxxxxuj&auth_date=xxxxxhash=xxxxxxxxxx
```

10. Create a `proxies.txt` file

The proxies.txt file should be in the root directory and contain a list of proxies in the format username:password@host:port.

```yaml
    username:password@host:port
    socks5://username:password@host:port
```

## RUN THE BOT
after that run the Fint*pio bot by writing the command

```bash
python main.py
```

## Configuration

- **use_proxy**: Enable or disable proxy Usage (Bool)
- **auto_break_asteroid**: Enable or disable automatic diamond collection (Bool).
- **auto_complete_task**: Enable or disable automatic task completion (Bool).
- **account_delay**: Delay between switching accounts in seconds (Int).

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Contact
If you have any questions or suggestions, please feel free to contact us at [ https://t.me/DeeplChain ].

 
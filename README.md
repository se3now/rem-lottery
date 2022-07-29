# RemGang Lottery

[RemGang](https://t.me/RemGanG) Lottery app made with Python's Tkinter library.

## Usage

Run the following commands to run the app

```bash
# Clone the project
git clone https://github.com/se3now/rem-lottery rem-lottery/

# change directory to project
cd rem-lottery

# Install requirements
pip3 install -r requirements.txt

# Run the GUI
python3 __main__.py
```

This app requires an SQLite database with `users` table. It can be made with the following query:

```sql
CREATE TABLE users (user_id integer, username VARCHAR(250), phone_number integer);
```

And finally click on the `Find New Winner` button to find winners.

## Note

This source code has been made public to prevent fraud in the selection of lottery winners.

## License
[MIT](https://choosealicense.com/licenses/mit/)

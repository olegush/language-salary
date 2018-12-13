# Average salary analysis

The script gets HeadHunter's and SuperJob's average developers salary on trending programming languages. Ranking bases on research over 1.25 billion events from the public GitHub timeline (April 10 2018). For details visit [https://github.com/benfred/github-analysis](https://github.com/benfred/github-analysis)


### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

.env file with enviroment variables should contain your secret key to SuperJob API.
```
SECRET_KEY=your_secret_key
```


### Quickstart

Run **salary.py** with parameters
```bash
$ python salary.py [--top] [--period] region
```

For example:
```bash
$ python salary.py St-Petersburg  --top 7 --period 7

HeadHunter's and SuperJob's average developers salary
on trending programming languages.
Ranking bases on research over 1.25 billion events from
the public GitHub timeline (April 10 2018)
For details visit https://github.com/benfred/github-analysis

+HeadHunter St-Petersburg, 7 days statistic------+---------+
| Programming | Language | Vacancies | Vacancies | Average |
| Language    |   Rank   |  founded  | Processed |  Salary |
+-------------+----------+-----------+-----------+---------+
| JavaScript  |  21.41%  |    571    |    230    | 140,088 |
| Python      |  14.69%  |    288    |     57    | 136,142 |
| Java        |  12.65%  |    400    |    100    | 165,566 |
| C++         |  8.30%   |    299    |     91    | 129,222 |
| C           |  5.84%   |    294    |    106    | 126,785 |
| PHP         |  5.31%   |    265    |    135    | 125,461 |
| C#          |  4.79%   |    222    |     71    | 143,303 |
+-------------+----------+-----------+-----------+---------+

+SuperJob St-Petersburg, 7 days statistic--------+---------+
| Programming | Language | Vacancies | Vacancies | Average |
| Language    |   Rank   |  founded  | Processed |  Salary |
+-------------+----------+-----------+-----------+---------+
| JavaScript  |  21.41%  |     24    |     15    |  70,393 |
| Python      |  14.69%  |     5     |     2     | 130,000 |
| Java        |  12.65%  |     12    |     0     |    -    |
| C++         |  8.30%   |     23    |     16    |  86,150 |
| C           |  5.84%   |     10    |     6     |  86,233 |
| PHP         |  5.31%   |     20    |     12    |  67,991 |
| C#          |  4.79%   |     22    |     10    |  79,300 |
+-------------+----------+-----------+-----------+---------+
```


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

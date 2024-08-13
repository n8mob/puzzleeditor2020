import datetime
import unittest
import requests


class MyTestCase(unittest.TestCase):
  def test_next_10_days(self):
    t = datetime.date.today()
    for i in range(10):
      t += datetime.timedelta(days=1)
      with self.subTest(f'puzzle for {t:%A, %d %B}'):
        url = f'https://puzzles.magiegame.com/puzzles/daily/{t.year}/{t.month}/{t.day}/'
        response = requests.get(url)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
  unittest.main()

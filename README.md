# -
天气
name: Weather Agent

on:
  schedule:
    - cron: "0 23 * * *"  # 每天 UTC 23点 = 北京时间7点
  workflow_dispatch:

jobs:
  run-agent:
    runs-on: ubuntu-latest

    steps:
      - name: checkout
        uses: actions/checkout@v4

      - name: setup python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: install requests
        run: pip install requests

      - name: run agent
        run: python main.py

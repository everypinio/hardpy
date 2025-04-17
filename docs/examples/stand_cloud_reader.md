# StandCloud Reader

```python
if __name__ == "__main__":
    import json

    sc_connector = StandCloudConnector(addr="demo.standcloud.io")
    reader = StandCloudReader(sc_connector)

    print("/test_run")
    response = reader.test_run("0196434d-e8f7-7ce1-81f7-e16f20487494")
    print(response.status_code)
    # print(json.dumps(response.json(), indent=4, ensure_ascii=False))

    print("/tested_dut")
    param = {
        "part_number": "part_number_2",
        "status": "pass",
    }
    response = reader.tested_dut(param)
    print(response.status_code)
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
```

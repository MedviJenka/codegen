## Login Test Plan

| Scenario                  | Description                             | Expected                      |
|:--------------------------|:----------------------------------------|:------------------------------|
| validate login            | login with right user name and password | user logged in                |
| login with wrong password | login with wrong credentials            | returns 401                   |
| username boundary testing | cannot pass more then 15 characters     | error pop up                  |
| page icon is displayed    | validate icon is displayed              | icon is displayed as expected |
| security test             | inject javascript code                  | nothing happens               |

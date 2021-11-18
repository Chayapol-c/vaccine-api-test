# Vaccine API Testing

This repo is the WCG group's API testing based on this [document](https://wcg-apis.herokuapp.com/api-doc/)

## Test case list

| ID  | Testcase                                  | Testcase Description                                      | Status |
| --- | ----------------------------------------- | --------------------------------------------------------- | ------ |
| 1   | test_post_registration()                  | create a registration                                     | pass   |
| 2   | test_post_duplicate_registration()        | create a registration 2 times                             | pass   |
| 3   | test_post_with_missing_param_citizen_id() | create a registration with missing param citizen id       | pass   |
| 4   | test_post_with_more_than_13_digits_id()   | create a registration with 13 more digits citizen id      | pass   |
| 5   | test_post_with_invalid_birth_date()       | create a registration with invalid birth date             | pass   |
| 6   | test_post_with_d_m_y_birth_date()         | create a registration with dd/mm/yyyy format              | pass   |
| 7   | test_post_with_y_m_d_birth_date()         | create a registration with yyyy/mm/dd format              | pass   |
| 8   | test_post_with_m_d_y_birth_date()         | create a registration with mm/dd/yyyy format              | pass   |
| 8   | test_post_with_m_y_d_birth_date()         | create a registration with mm/yyyy/dd format              | pass   |
| 8   | test_post_with_d_y_m_birth_date()         | create a registration with dd/yyyy/mm format              | pass   |
| 9   | test_post_with_less_than_12_years_old()   | create a registration with less than 12 years old citizen | pass   |
| 10  | test_post_with_future_date()              | create a registration with future birth date              | pass   |
| 11  | test_remove_invalid_registration()        | remove an invalid registration                            | pass   |
| 12  | test_remove_registration()                | remove a registration                                     | pass   |
| 13  | test_get_registration()                   | retrieve a registration                                   | pass   |
| 14  | test_get_invalid_registration()           | retrieve an invalid registration                          | pass   |

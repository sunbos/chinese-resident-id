import random
from typing import List
import pycountry
from faker import Faker
from faker.providers.ssn.zh_CN import Provider as SsnProvider

class MainlandSsnProvider(SsnProvider):
    area_codes = SsnProvider.area_codes
    if "710000" in area_codes:
        area_codes.remove("710000")
    if "810000" in area_codes:
        area_codes.remove("810000")
    if "820000" in area_codes:
        area_codes.remove("820000")
    if "830000" in area_codes:
        area_codes.remove("830000")

def generate_mainland_resident_id(min_age: int = 18, max_age: int = 90, gender = None) -> str:
    fake = Faker('zh_CN')
    fake.add_provider(MainlandSsnProvider)
    mainland_identity_card: str = fake.ssn(min_age = min_age, max_age = max_age, gender = gender)
    return mainland_identity_card

class HmtSsnProvider(SsnProvider):
    area_codes = ["810000","820000","830000"]

def generate_hmt_residence_permit_id(min_age: int = 18, max_age: int = 90, gender = None) -> str:
    fake = Faker('zh_CN')
    fake.add_provider(HmtSsnProvider)
    hmt_residence_permit: str = fake.ssn(min_age = min_age, max_age = max_age, gender = gender)
    return hmt_residence_permit

def calculate_check_digit_v1(resident_id_without_check_digit: str) -> int:
    weights: List[int] = [7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3]
    total: int = sum(int(digit) * weight if digit.isdigit() else (ord(digit.upper()) - 55) * weight for digit, weight in zip(resident_id_without_check_digit, weights))
    remainder: int = total % 10
    return remainder

def calculate_check_digit_v2(resident_id_without_check_digit: str) -> str:
    weights: List[int] = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_digits: List[str] = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    total: int = sum(int(digit) * weight for digit, weight in zip(resident_id_without_check_digit, weights))
    remainder: int = total % 11
    return check_digits[remainder]

def fake_alpha3_code_without_china() -> str:
    china_codes: List[str] = ['CHN', 'HKG', 'MAC', 'TWN']
    fake = Faker()
    alpha_3_country_code: str = fake.country_code(representation = "alpha-3")
    while alpha_3_country_code in china_codes:
        alpha_3_country_code = fake.country_code(representation = "alpha-3")
    return alpha_3_country_code

def alpha3_to_numeric(alpha3_code: str) -> str:
    country = pycountry.countries.get(alpha_3 = alpha3_code)
    return country.numeric

def random_number3_code_without_china() -> str:
    foreign_alpha3_code: str = fake_alpha3_code_without_china()
    foreign_number3_code: str = alpha3_to_numeric(foreign_alpha3_code)
    return foreign_number3_code

def generate_foreign_permanent_resident_id_v1(min_age: int = 18, max_age: int = 90) -> str:
    mainland_identity_card: str = generate_mainland_resident_id(min_age = min_age, max_age = max_age)
    country_code: str = fake_alpha3_code_without_china()
    admin_div_code: str = mainland_identity_card[0:4]
    birth_date: str = mainland_identity_card[8:14]
    sequence_number: str =  f"{random.randint(0, 9)}"
    resident_id_without_check_digit: str = f"{country_code}{admin_div_code}{birth_date}{sequence_number}"
    check_digit: int = calculate_check_digit_v1(resident_id_without_check_digit)
    resident_id: str = f"{resident_id_without_check_digit}{check_digit}"
    return resident_id

def generate_foreign_permanent_resident_id_v2(min_age: int = 18, max_age: int = 90, gender: str = None) -> str:
    identity_code: str = "9"
    mainland_identity_card: str = generate_mainland_resident_id(min_age = min_age, max_age = max_age)
    admin_div_code: str = mainland_identity_card[0:2]
    country_code: str = random_number3_code_without_china()
    birth_date: str = mainland_identity_card[6:14]
    if gender == 'M':
        sequence_number: str = f"{random.choice(range(1, 1000, 2)):03d}"  # 生成奇数
    elif gender == 'F':
        sequence_number: str = f"{random.choice(range(2, 1000, 2)):03d}"  # 生成偶数
    else:
        sequence_number: str = f"{random.randint(1, 999):03d}"  # 如果性别未指定，则随机生成
    resident_id_without_check_digit: str = f"{identity_code}{admin_div_code}{country_code}{birth_date}{sequence_number}"
    check_digit: str = calculate_check_digit_v2(resident_id_without_check_digit)
    resident_id: str = f"{resident_id_without_check_digit}{check_digit}"
    return resident_id

print(generate_mainland_resident_id())
print(generate_hmt_residence_permit_id())
print(generate_foreign_permanent_resident_id_v1())
print(generate_foreign_permanent_resident_id_v2())

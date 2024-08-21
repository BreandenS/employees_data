import pandas as pd
from datetime import datetime


def csv_file_reader(file_path):
    try:
        df = pd.read_csv(file_path)
        print(df.head())
        print()
        return df
    except FileNotFoundError:
        print(f"Error:The file{file_path}was not found")
        return None
    except pd.errors.EmptyDataError:
        print("Error:The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def extract_employees_date_births(df):
    try:
        date_of_birth = df["date_of_birth"]
    except KeyError:
        print("Error: The column 'date_of_birth' does not exist in the DataFrame.")

    print(f"Name: {date_of_birth.name}, dtype: {date_of_birth.dtype}")

    for date in date_of_birth:
        print(date)

    return date_of_birth


def calculate_employees_age(date_of_birth):
    if date_of_birth is None:
        print(f"Error: {date_of_birth}not found.")
        return []

    current_date = datetime.now()
    ages = []

    for dob in date_of_birth:
        try:
            date_of_birth = pd.to_datetime(dob, dayfirst=True)
            age = (
                current_date.year
                - date_of_birth.year
                - (
                    (current_date.month, current_date.day)
                    < (date_of_birth.month, date_of_birth.day)
                )
            )
            ages.append(age)
        except Exception as e:
            print(f"Error processing date of birth {dob}: {e}")
            ages.append(None)

    return ages


def years_until_retirement(age, retirement_age=68):

    if age >= retirement_age:
        return None
    else:
        return retirement_age - age


def main():
    file_path = "employees.csv"
    df = csv_file_reader(file_path)
    if df is not None:
        date_of_birth = extract_employees_date_births(df)
        print()
        ages = calculate_employees_age(date_of_birth)
        if ages:
            print("Calculated ages:")
            print(ages)
            print()
            print("Years until retirement")
            for age in ages:
                years_left = years_until_retirement(age, retirement_age=68)
                
                print(f"Age: {age}, Years until retirement: {years_left}")
        else:
            print("No ages calculated.")


if __name__ == "__main__":
    main()

import pandas as pd


def csv_file_reader(file_path):
    try:
       df = pd.read_csv(file_path)
       print(df.head())
       print()
       return df
    except FileNotFoundError:
        print(f"Error:The file{file_path}was not found")
        return 0
    except pd.errors.EmptyDataError:
        print("Error:The file is empty.")
        return 0
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


def main():
    file_path = "employees.csv"
    df = csv_file_reader(file_path)
    if df is not 0:
         extract_employees_date_births(df)


if __name__ == "__main__":
    main()

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


def csv_file_reader(file_path):
    try:
        df = pd.read_csv(file_path)

        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        print(df.head())
        print()
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def extract_employees_date_births(df):
    try:
        
        df["date_of_birth"] = df["date_of_birth"].str.strip()
        date_of_birth = df["date_of_birth"]
        print(f"Name: {date_of_birth.name}, dtype: {date_of_birth.dtype}")
        for date in date_of_birth:
            print(date)
        return date_of_birth
    except KeyError:
        print("Error: The column 'date_of_birth' does not exist in the DataFrame.")
        return None


def calculate_employees_age(date_of_birth):
    if date_of_birth is None:
        print("Error: Date of birth not found.")
        return []

    current_date = datetime.now()
    ages = []

    for dob in date_of_birth:
        try:
            
            date_of_birth = pd.to_datetime(dob, dayfirst=True, errors="coerce")
            if pd.isna(date_of_birth):
                print(f"Error processing date of birth {dob}: invalid date format")
                ages.append(None)
                continue
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
    if age is None or age >= retirement_age:
        return None
    else:
        return retirement_age - age


def main():
    file_path = "employees.csv"
    df = csv_file_reader(file_path)

    if df is not None:
        date_of_birth = extract_employees_date_births(df)

        print()
        if date_of_birth is not None:
            ages = calculate_employees_age(date_of_birth)

            if ages:
                print("Calculated ages:")
                print(ages)
                print()

                print("Years until retirement")
                years_until_retirement_list = [
                    years_until_retirement(age, retirement_age=68) for age in ages
                ]

                
                valid_indices = [
                    i
                    for i, y in enumerate(years_until_retirement_list)
                    if y is not None
                ]
                filtered_ages = [ages[i] for i in valid_indices]
                filtered_years_until_retirement = [
                    years_until_retirement_list[i] for i in valid_indices
                ]

                for age, years_left in zip(
                    filtered_ages, filtered_years_until_retirement
                ):
                    print(f"Age: {age}, Years until retirement: {years_left}")

                # Plot 1: Age Distribution
                plt.figure(figsize=(10, 6))
                plt.hist(
                    ages, bins=range(20, 80, 5), color="skyblue", edgecolor="black"
                )
                plt.title("Age Distribution of Employees")
                plt.xlabel("Age")
                plt.ylabel("Number of Employees")
                plt.grid(axis="y", linestyle="--", alpha=0.7)
                plt.show()

                # Plot 2: Years Until Retirement
                plt.figure(figsize=(10, 6))
                plt.bar(
                    filtered_ages,
                    filtered_years_until_retirement,
                    color="orange",
                    edgecolor="black",
                )
                plt.title("Years Until Retirement")
                plt.xlabel("Age")
                plt.ylabel("Years Until Retirement")
                plt.grid(axis="y", linestyle="--", alpha=0.7)
                plt.show()

                # Plot 3: Age vs. Date of Birth
                plt.figure(figsize=(10, 6))
                # Convert date_of_birth to datetime format for plotting
                df["date_of_birth"] = pd.to_datetime(
                    df["date_of_birth"], dayfirst=True, errors="coerce"
                )
                plt.scatter(df["date_of_birth"], ages, color="green")
                plt.title("Age vs. Date of Birth")
                plt.xlabel("Date of Birth")
                plt.ylabel("Age")
                plt.grid(True)
                plt.show()

                # Plot 4: Cumulative Employees Reaching Retirement Over Time
                current_year = datetime.now().year
                retirement_years = [
                    current_year + y if y is not None else current_year
                    for y in years_until_retirement_list
                ]
                retirement_years_sorted = sorted(retirement_years)
                cumulative_retirement = range(1, len(retirement_years_sorted) + 1)

                plt.figure(figsize=(10, 6))
                plt.plot(
                    retirement_years_sorted,
                    cumulative_retirement,
                    marker="o",
                    color="purple",
                )
                plt.title("Cumulative Employees Reaching Retirement Over Time")
                plt.xlabel("Year")
                plt.ylabel("Cumulative Number of Employees Retiring")
                plt.grid(True)
                plt.show()
            else:
                print("No ages calculated.")
        else:
            print("No valid date of birth column found.")
    else:
        print("DataFrame is empty or not loaded.")


if __name__ == "__main__":
    main()

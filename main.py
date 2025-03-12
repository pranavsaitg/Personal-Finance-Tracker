# Handle main flow of the program
import pandas as pd
import csv
from datetime import datetime #Module that allows you to work with dates and times
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    #Initializing CSV File
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["date", "amount", "category", "description"])
            # data frame is an object within Pandas, that allows us to access different rows/columns from a CSV file
            df.to_csv(cls.CSV_FILE, index=False)

    #Adding the Entry
    @classmethod
    def add_entry(cls, date, amount, category, description):
        # Being stored in a python dictionary
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile: #context manager: once code inside is done, it will automatically close file
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) #take a dictionary, write into csv file
            #fieldname=cls.COLUMNS is used, so program knows how to take data from dictionary, and write into csv file
            writer.writerow(new_entry)
        print("Entry added successfully")
    #Next, Ask User for Entries, to Add into CSV file, so we don't need to write it manually

#Convert all of the dates inside date column, to datetime object, to filter transactions using date, and use built-in properties of datetime object
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        print(df.columns)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT) #We are able to directly access date column by using Pandas data frame, and not just the rows
        start_date = datetime.strptime(start_date, CSV.FORMAT) #start date will be string, so we want to convert to correct format (dd,mm,yyyy)
        end_date = datetime.strptime(end_date, CSV.FORMAT) #start date will be string, so we want to convert to correct format (dd,mm,yyyy)       
        
        #Create mask to filter the different objects inside the data frame
        mask = (df["date"] >= start_date) & (df["date"] <= end_date) #Check if df date is greater than start_date, and less than end_date
        #This comparison is possible because all the variables are datetime objects, so they can be directly compared
        
        filtered_df = df.loc[mask]
        #The above line will only return the rows, where the mask condition was true

        if filtered_df.empty: #If the dataframe is empty
            print('No transactions found in the given date range') 
        else: #If its not empty, create a summary of the transactions
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}") #Transactions from the start_date to end_date
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)})) #One line anonymous function? Lambda function? Research it on my own

            #We look for all of the rows where category is equal to Income, and then look for those amounts and add them up
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum() 
            
            #Now we look for all of the rows where the category is equal to Expense, and then look for those amounts and add them up
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}") #.2f rounds to two decimal places when using f string
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df

# A function that will call the functions from "data_entry" file in the order that we want in order to collect our data
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyy) or enter for today's date: ")
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date, amount, category, description)

#Function to create graph of income and expenses 
def plot_transactions(df):
    df.set_index('date', inplace=True)

    #Income df
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    
    #Expense df
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color = "g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show() #Shows the plot on the screen

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add() #Run "add data entry" function
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ") #Enter start date
            end_date = get_date("Enter the end date (dd-mm-yyyy): ") #Enter end date
            df = CSV.get_transactions(start_date, end_date) #Get the transactions only between the start and end date

            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...") #Exit program
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
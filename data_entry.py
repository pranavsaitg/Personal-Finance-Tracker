# Collect Data from User in this Class

from datetime import datetime

#This is a recursive function, so you keep calling get_date function until user provides valid date

#Asking user for prompt,allow_default is set to false: 
# if allow_default = true though, it would allow user to just get current date if they don't enter it

date_format = "%d-%m-%Y" #create variable so if you want to change it, you can do it right here
CATEGORIES = {"I": "Income", "E": "Expense"} #Map 'I' to Income and 'E' to Expense

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    #if allow_default = true, since not allow_default = true, and no date is entered, then return today's date
    if not allow_default and not date_str:
        return datetime.today().strftime(date_format) #Then return current date and formatting date in day, month, year
    
    #Otherwise, we need to validate the date, and make sure its valid
    try:
        valid_date = datetime.strptime(date_str, date_format) #if date is not entered in d, m, Y, then try to use format and make it valid
        return valid_date.strftime(date_format) #Clean up date user gives, and put it into the d, m, Y format we need
    # But this statement might not work, that is why it is in a "try" statement, so that if it doesn't work, the program won't just crash

    #If try statement doesn't work
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)
    

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount #If all of this works, just return amount
    # If not, accept the valueerror as e, and then print e, and then return to get_amount function
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper() #Self explanatory: choose category I or E
    if category in CATEGORIES: #Validate the category is one of the categories
        return CATEGORIES[category] #Rather than returning I or E, we are returning Income or Expense
    
    else:
        print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
        return get_category() #Run function until we get the category

def get_description():
    return input("Enter a description (optional): ")
    #Not much coding needed, since its optional, no need for conditional statements
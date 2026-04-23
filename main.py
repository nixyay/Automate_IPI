import pandas as pd

# This reads the template csv and converts it into a data fram
df = pd.read_csv("/Users/oliverberridge/Coding/Automate IPI/Automatic IPI template.csv")

# This reads the template excel file and converts it into a data frame
template = pd.read_csv("/Users/oliverberridge/Coding/Automate IPI/cmpdrive2trmsoffer_IPI_WHSTPC_WindowsUserID_DDMMYYYY01.csv")

# This creates a new column in the data frame that combines the product sku and price to create a unique identifier for each line of data
df["unique"] = df["Product Sku"].astype(str) + df["New Price"].astype(str)
line_code_price = df["unique"]

#Removes duplicates from the store IDs column to get a list of each store
def remove_duplicates(line_code_price):
    unique_line_codes = list(dict.fromkeys(line_code_price))
    return unique_line_codes

# This creates a list of the unique line code and prices
unique_skus = remove_duplicates(line_code_price)

# inputs the data from the template file to the IPI template

template.iloc[1,1] = df["Promotion Description (Optional)"][0]
template.iloc[1,2] = df["Comments  (Optional)"][0]
template.iloc[1,3] = df["Promotion Start Date"][0]
template.iloc[1,4] = df["Promotion End Date "][0]
template.iloc[1,5] = df["Your Email Address"][0]
template.iloc[1,6] = df["Store Count (Optional)"][0]

# grabs the user ID from the template CSV file to use in the naming of the output files
user_id = df["User ID"][0]

name = {}
counter = 0
promo_name_list = {}

while counter < len(unique_skus):
        template_copy = template.copy()
        sku_counter = 0
        list_counter = 1
        for skus in line_code_price:
            if unique_skus[counter] == skus:
                template_copy.iloc[list_counter,9] = df["Store IDs"][sku_counter]
                template_copy.iloc[list_counter,12] = df["Product Sku"][sku_counter]
                template_copy.iloc[list_counter,13] = df["New Price"][sku_counter]
                sku = df["Product Sku"][sku_counter]
                price = df["New Price"][sku_counter]
                sku_counter += 1
                list_counter += 1
            else:
                sku_counter += 1
        template_copy.iloc[1,0] = "TPC "+ price.astype(str) + " " + sku.astype(str)
        # promo_name_list = {"Promotion Name": template_copy.iloc[1,0]}
        # promo_name_list = {"Count of SKUs": list_counter - 1}
        template_copy.iloc[template_copy.index[2:],[12, 13]] = pd.NA      
        template_copy.to_csv(f"cmpdrive2trmsoffer_IPI_WHSTPC_{user_id}"+unique_skus[counter]+"v2.csv", index = False)
        
        counter += 1

# pd.DataFrame(promo_name_list)
# print(promo_name_list)
# pd.DataFrame({"Promotion Name": promo_name_list}).to_csv(f"Promotion Names {user_id}.csv", index = False)

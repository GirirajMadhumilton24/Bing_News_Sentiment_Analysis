#!/usr/bin/env python
# coding: utf-8

# ## process_bing_news
# 
# New notebook

# loading the data into the note using spark 

# In[23]:


df = spark.read.option("multiline", "true").json("Files/bing-latest-news.json")
# df now is a Spark DataFrame containing JSON data from "Files/bing-latest-news.json".
display(df)


# In[24]:


#extracting only value column
df = df.select("value")


# In[25]:


#displaying value column
display(df)


# exploding the value column to get individual values

# In[26]:


#exploding value column 
from pyspark.sql.functions import explode #importing required function
df_exploded = df.select(explode(df["value"]).alias("json_object"))


# In[27]:


#dispalying exploded df
display(df_exploded)


# converting the exploded json objects into an list

# In[28]:


# converitng the rows from df_exploded to json list 
json_list = df_exploded.toJSON().collect()# collect fucntion collect the values from toJSON function ina list


# we can use this list on an online json parser to get the hierarchy of the objects in the list

# In[29]:


#printing the list
print(json_list[1])


# next few line of codes are example 

# creating an dictionary to store the list so that we can extract the data we need into an list or an column for further analysis

# In[30]:


import json

news_json = json.loads(json_list[1]) #laoding the joan list to an python dictonary


# In[31]:


print(news_json)


# extracting the values we need

# In[32]:


print(news_json['json_object']['name'])
print(news_json['json_object']['description'])
print(news_json['json_object']['category'])
print(news_json['json_object']['image']['thumbnail']['contentUrl'])
print(news_json['json_object']['url'])
print(news_json['json_object']['provider'][0]['name'])
print(news_json['json_object']['datePublished'])


# part off the project code again starts from here

# creating an list on top to store the extracted values. then creating an loop to process all the data from the json list and all the required values will be appended on the list above. the try block will give us an idea of where are the inconstancy on the json list so that we can add an if condition to remove those lists.

# In[33]:


title = []
description =[]
category = []
image = []
url = []
provider = []
datePublished = []

#processing each json file in the list 
for json_str in json_list:
    try:
        #parcing the json string into an dictionary
        article = json.loads(json_str)

        #extract info form the dicti0nary
        title.append(article['json_object']['name'])
        description.append(article['json_object']['description'])
        category.append(article['json_object']['category'])
        image.append(article['json_object']['image']['thumbnail']['contentUrl'])
        url.append(article['json_object']['url'])
        provider.append(article['json_object']['provider'][0]['name'])
        datePublished.append(article['json_object']['datePublished'])

    except Exception as e:
        print(f"Error Processing JSON object: {e}")


# with if condition to remove the inconsistent data 

# In[34]:


title = []
description =[]
category = []
image = []
url = []
provider = []
datePublished = []

#processing each json file in the list 
for json_str in json_list:
    try:
        #parcing the json string into an dictionary
        article = json.loads(json_str)

        if article["json_object"].get("category") and article["json_object"].get("image",{}).get("thumbnail",{}).get("contentUrl",{}):
            
            #extract info form the dicti0nary
            title.append(article['json_object']['name'])
            description.append(article['json_object']['description'])
            category.append(article['json_object']['category'])
            image.append(article['json_object']['image']['thumbnail']['contentUrl'])
            url.append(article['json_object']['url'])
            provider.append(article['json_object']['provider'][0]['name'])
            datePublished.append(article['json_object']['datePublished'])

    except Exception as e:
        print(f"Error Processing JSON object: {e}")


# In[35]:


# viewing the title list
title


# we are using an zip function to combine all the all we have together. we are also defining an schema and storing the data into an new df_cleaned

# In[36]:


from pyspark.sql.types import StructType, StructField, StringType

#Combine the lists
data = list(zip(title, description, category, url, image, provider, datePublished))

#Define schema
schema = StructType([
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("category", StringType(), True),
    StructField("url", StringType(), True),
    StructField("image", StringType(), True),
    StructField("provider", StringType(), True),
    StructField("datePublished", StringType(), True)
])

#Create DataFrame
df_cleaned = spark.createDataFrame (data, schema=schema)


# In[37]:


# viewing the cleaned df
display(df_cleaned)


# the datepublished column is in date time format we are changing it to an data format for more reliable processing

# In[38]:


from pyspark.sql.functions import to_date,date_format

df_cleaned_final = df_cleaned.withColumn("datePublished", date_format(to_date("datePublished"),"dd-MMM-yyyy"))


# In[39]:


# displaying the final df 
display(df_cleaned_final)


# writing the final db to the lakehouse data base in delta db format

# In[40]:


# df_cleaned_final.write.format("delta").saveAsTable("bing_news_db.tbl_latest_news")
#if we run this again if will create an AnalysisException error 


# we are using type 1 data ware housing method to write the data in the lake house

# In[41]:


from pyspark.sql.utils import AnalysisException

try:

    table_name = 'bing_news_db.tbl_latest_news'

    df_cleaned_final.write.format("delta").saveAsTable(table_name)

except AnalysisException:

    print("Table Already Exists")

    df_cleaned_final.createOrReplaceTempView("vw_df_cleaned_final") #--> name of the view

    spark.sql(f"""  MERGE INTO {table_name} target_table --alias orginal tabel as target
                    USING vw_df_cleaned_final source_view --alias view as source

                    ON source_view.url = target_table.url --joining

                    WHEN MATCHED AND --condition

                    source_view.title <> target_table.title OR -- if there is any change in the column
                    source_view.description <> target_table.description OR
                    source_view.category <> target_table.category OR
                    source_view. image <> target_table.image OR
                    source_view.provider <> target_table.provider OR
                    source_view.datePublished <> target_table.datePublished

                    THEN UPDATE SET * --will update whole row on the source

                    WHEN NOT MATCHED THEN INSERT * --if it is a new data insted of overwriting the row it will get inserted to the source
                """)


# checking if there are any duplicate entries on the table using shell magic command of sql

# In[42]:


# The command is not a standard IPython magic command. It is designed for use within Fabric notebooks only.
# %%sql
# select count(*) from bing_news_db.tbl_latest_news


# In[ ]:





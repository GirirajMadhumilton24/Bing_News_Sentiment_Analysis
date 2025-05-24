#!/usr/bin/env python
# coding: utf-8

# ## news_sentiment_analysis
# 
# New notebook

# reading data using spark

# In[2]:


df = spark.sql("SELECT * FROM bing_news_db.tbl_latest_news")
display(df)


# importing required libraries for text analysis

# In[3]:


import synapse.ml.core
from synapse.ml.services import AnalyzeText


# we are gonna analyze the sentiment of description  

# In[4]:


model = (AnalyzeText()
        .setTextCol("description")
        .setKind("SentimentAnalysis")
        .setOutputCol("response")
        .setErrorCol("error"))


# In[5]:


#then we are tranformning the result into an df 
result = model.transform(df)


# In[6]:


display(result)


# we are only taking the sentiment value form the response column and creating an new column as sentiment and storing everything in a new df

# In[7]:


from pyspark.sql.functions import col #col function used to refer the column in a df

sentiment_df = result.withColumn("sentiment", col("response.documents.sentiment"))


# In[8]:


display(sentiment_df)


# In[9]:


# droppoing unwanted column for reporting
sentiment_df_final = sentiment_df.drop("error","response")


# In[10]:


display(sentiment_df_final)


# changing the datatype of the datetype column so that the future data will have proper format schema

# In[11]:


from pyspark.sql.functions import col, to_date

sentiment_df_final = sentiment_df_final.withColumn("datePublished", to_date(col("datePublished"), "dd-MMM-yyyy"))


# using type 1 method to create and tabel in lake house 

# In[12]:


from pyspark.sql.utils import AnalysisException

try:

    table_name = 'bing_news_db.tbl_sentiment_analysis'

    sentiment_df_final.write.format("delta").saveAsTable(table_name)

except AnalysisException:

    print("Table Already Exists")

    sentiment_df_final.createOrReplaceTempView("vw_sentiment_df_final") #--> name of the view

    spark.sql(f"""  MERGE INTO {table_name} target_table --alias orginal tabel as target
                    USING vw_sentiment_df_final source_view --alias view as source

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


# In[13]:


display(sentiment_df_final)


# **temp codes for fixing the datePublished column**

# df = spark.sql("SELECT * FROM bing_news_db.tbl_sentiment_analysis")

# from pyspark.sql.functions import col, to_date
# 
# df = df.withColumn("datePublished", to_date(col("datePublished"), "dd-MMM-yyyy"))
# 

# display(df)

# df.printSchema()

# df.write.format('delta').mode("overwrite").option("overwriteSchema","True").saveAsTable(table_name)

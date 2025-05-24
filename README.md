# Bing_News_Sentiment_Analysis
pulling latest news data from Bing API. Transforming the raw data and finding the sentiment and analyzing using Power-bi  report doing all these steps using Microsoft Fabric.

Project Overview:
The objective of this project is to develop an Bing News data analytics platform. This platform will leverage Bing search to integrate news data into the Fabric workspace. Subsequently, the data will undergo processing, and a comprehensive report will be generated. This report will serve as a novel dashboard, providing direct access to the most recent news and other analytics data.

Key Component:
The Bing API serves as the primary data source for this project.

Project Architecture:
The project architecture will follow these steps:

1. Create and Configure the Bing API in Azure: This step involves setting up the Bing API within Azure.
2. Data Ingestion using Data Factory from Fabric: Utilizing the Data Factory from Fabric, we will establish a connection to the Bing API, enabling the retrieval of recent news data and its subsequent integration into the Fabric workspace as a JSON file. This data will be stored in a single lake.
3. Data Transformation: Subsequently, we will transform the data into a structured table with a predefined schema. This transformed data will be stored as a structured delta table using Synapse Data Engineering and a Spark Notebook. This delta table will also be saved in Delta Lake.
4. Sentiment Analysis: This step involves conducting sentiment analysis on the data.
Following the completion of the data cleansing process, we will proceed with sentiment analysis utilizing a text analysis model. Each news set will be assigned a descriptive label, which will subsequently be employed to ascertain its sentiment as positive, negative, or neutral. The resultant sentiment analysis outcome will be stored in Delta Lake via Synapse Data Science.

Step 5: Power BI Dashboard Development
Subsequently, we will construct a dashboard utilizing Data Activator. This dashboard will serve as the foundation for establishing alerts. Specifically, we will configure the activator to transmit alerts via email or Teams, contingent upon our preferences. For this project, we will opt for Teams.

Important Note: We will leverage the Data Factory to orchestrate the entire project by establishing a pipeline.

AGENDA

1. Environment Configuration: We will configure an environment to facilitate resource creation.
2. Data Ingestion: We will ingest the data into the Fabric workspace.
3. Data Transformation: We will transform the data, accompanied by an increased load.
4. Model Building for Sentiment Analysis: We will construct a model for sentiment analysis, which will also necessitate an increased load.
5. Data Reporting on Power BI: We will report the data on Power BI.
6. Pipeline Construction: We will construct the pipeline.
7. Alert Setting: We will set alerts.

Data Acquisition and Loading, and Pipeline Construction
Now, we will utilize Azure Portal to establish the environment and create resources.
Step 1: Access the resource group page.
Step 2: Proceed to the “Create” button and select the appropriate subscription.
Step 3: Name the resource group as “rg-bing-data-analytics.”
Step 4: Select the most suitable region.
Step 5: Utilize tags primarily as a key-value pair to enhance resource identification.  name = (created by), value = (Giri)**Step**Resource Creation**

1. **Review and Create the Resource Group:**

* Thoroughly review the requirements and create a resource group accordingly.
* Refresh and select the newly created resource group name to view its details.
* Proceed to the “Create” button located at the top of the page.
* This action will redirect you to the Azure Marketplace, where you can conduct a search for “Bing” using the provided search bar.
* From the search results, select “Bing Search V7” and click “Create” to initiate the creation process.
* At this stage, you have the option to choose a subscription, resource group, and provide an instance name.
* Proceed to select the pricing tier, with the initial option being free.
* As previously done, add a tag to the resource.
* Finally, review and create the resource as desired.

**Note:** Please note that the Bing API is no longer available in Azure.

**Step 2: Work Space Creation**

2. **Create a Workspace on Power BI:**

* Develop a workspace on Power BI for this project, naming it “Bing-News.” This workspace will serve as the central hub for all project-related activities.
* Navigate to the Fabric workspace and select “Add New Item.”
* Under the “Data Engineering” category, choose “Lakehouse.”
* Provide a suitable name for the data lakehouse, such as “Bing-Lake-DB.”

DATA INGESTION 

- Although the resource has not been fully created due to the API’s unavailability, we have acquired the necessary key and URL for the project.
- To initiate data ingestion, select the resource you created and access its associated keys and endpoints.
- Open the workspace that contains the newly created lakehouse.
- In Fabric, navigate to the data pipeline and select “Data Pipeline” from the dropdown menu.
- Assign the name “News_Ingestion_Pipeline” to the data pipeline.
- Copy the data activity from the top of the page and select “Data Canvas.”
- Provide a name for the copied data activity, such as “Copy Latest News.”
- Select the source for data ingestion and click on the “Connection” dropdown menu.
- Select “REST” to connect the two APIs.
- Configure the REST connection by providing the URL for the data source. This URL can be obtained from the Azure portal.
- If the resource has been fully ingested, the URL will be available in the resource overview.
- The documentation for the ingested API will be found under the “Endpoint” link.
- Subsequently, we proceed to open the remaining connections and paste the URLs. Under the “Create New Connections” section, modify the connection name to “(bing-news-search-connection).” Adjust the authentication type to “Anonymous.” Finally, select “Connect.”
- To verify the connection, click on the “Test Connection” option.
- Although we have established a connection, we still lack the authentication credentials to access data from the Bing API. Therefore, we must refer to the Bing API documentation.
- Locate the header section on the left side of the documentation. This section provides information on the headers we can include with the URL. When utilizing REST APIs, it is essential to authenticate with the API using headers. The documentation will specify the required headers for the base URL.
- Since we intend to use the header as a key for authentication, we select “Anonymous” as the authentication method.
- To incorporate the key header, expand the “Advanced” section under “Source.” Proceed to the “Additional Headers” option and select “New” to create a new header. Assign it the name “Ocp-Apim-Subscription-Key” and provide the corresponding key from the portal for the Bing-News-API key and endpoints key. Two keys are available, and any of them can be utilized. 
- The most recent news will suffice for that purpose. purpose.q=**Latest News**
- We must insert this URL comment beneath the relative URL.
- For instance, when conducting a search on Google, for example, Instagram, we will receive a URL such as: (https://www.google.com/search?q=site:instagram.com+your_search_term).
- Let us examine the URL (https://www.google.com/search):
- This is the actual Google search engine (URL?).).q=Site: Instagram —> This is the relative URL, similar to a filter.
- Once we mention the relative URL, we can click on the preview to verify its functionality.
- The document (https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/reference/headers) provides a comprehensive list of query parameters available for Bing search APIs. Currently, we are utilizing the count parameter in our application. count=100Kindly provide the latest news. articles.q=Latest newscount=100)With a count of 100, the preview will be presented in JSON format.
- (?q=latest+news&count=100&freshness=Day)We are currently employing freshness = dayPlease compile all published articles. We can use either the week, year, or month as the date.
- Typically, when utilizing this API, we retrieve regional data. The MKT query parameter allows us to access global news. There will be a link referred to as market codes, from which we can retrieve the country codes (?).q=Latest newscount=100&freshness=Day&mkt=en-IN)Now, we will obtain all the articles specific to the Indian region.
- Next, let’s proceed to the destination and select the database lake we created. Subsequently, choose the root folder as “file” since we will receive a JSON file. Therefore, there is no need for a table. For the file path, name the file as “(bing-latest-news.json).” Ensure that the file name matches the file type and fills in the destination.
- Change the file format from CSV to JSON.
- Finally, save the pipeline with the save button at the top.

DATA TRANSFORMATION

- After completing the data ingestion process, we can utilize a notebook to transform the raw JSON data into clean data. To do this, click on “New Item” and add a notebook. Rename it as “(process_bing_news).”
- Under the “Explorer,” add the data from our existing lake house. Once added, click on the “File” icon under the uploaded data to view the raw JSON file.
- Next, click on the three dots next to the file name and select “Load Data.” Choose the desired loading method (Spark or Pandas, depending on the programming language). In this project, we will use Spark.
- Spark will automatically generate a code to upload the data to the notebook.
- Now, run the code to load the data as a data frame (df). One advantage of Fabric is its serverless compute model, eliminating the need to create a cluster like we did in DataBricks.
- Currently, our attention is solely focused on the value column, as that is the required JSON data we need. (df =df.select(“value”) will only select the value column and store it on the same DataFrame.
- The next step is to explode the value column and rename the DataFrame as df_expoded and the column name as json_object.
* from pyspark.sql.functions import explode #importing the required function
* df_exploded = df.select(explode(df["```javascript
* value).alias(“json_object”);

- Next, we will convert these exploded rows into a JSON list. The toJSON function converts them into a JSON format, and the collect built-in functions collect them as a list.
* json_list = df_Exploded.toJSON().collect();

* Subsequently, we can print the list using the index 0, as indicated by the first news article.
* print(json_list[0]);

- Example Code to Understand Dictionaries
- Next, we need to load the list into a dictionary so that we can retrieve the required fields from the list using the json.load function.
* import json
* news_json = json.loads(json_list[1]) #laoding the joan list to an python dictonary

- Viewing the dictionary formatted data we just loaded one entry form he list we have
* print(news_json)

- Extracting the values we needed form the dictionary string 
* print(news_json['json_object']['name'])
* print(news_json['json_object']['description'])
* print(news_json['json_object']['category'])
* print(news_json['json_object']['image']['thumbnail']['contentUrl'])
* print(news_json['json_object']['url'])
* print(news_json['json_object']['provider'][0]['name'])
* print(news_json['json_object']['datePublished'])

- Lets again  go back to the project code
- creating an list on top to store the extracted values. then creating an loop to process all the data from the json list and all the required values will be appended on the list above. the try block will give us an idea of where are the inconstancy on the json list so that we can add an if condition to remove those lists.
* title = []
* description =[]
* category = []
* image = []
* url = []
* provider = []
* datePublished = []
* 
* #processing each json file in the list 
* for json_str in json_list:
*     try:
*         #parcing the json string into an dictionary
*         article = json.loads(json_str)
* 
*         #extract info form the dicti0nary
*         title.append(article['json_object']['name'])
*         description.append(article['json_object']['description'])
*         category.append(article['json_object']['category'])
*         image.append(article['json_object']['image']['thumbnail']['contentUrl'])
*         url.append(article['json_object']['url'])
*         provider.append(article['json_object']['provider'][0]['name'])
*         datePublished.append(article['json_object']['datePublished'])
* 
*     except Exception as e:
*         print(f"Error Processing JSON object: {e}")

- Adding an i condition to the data to remove the inconsistency 
* title = []
* description =[]
* category = []
* image = []
* url = []
* provider = []
* datePublished = []
* 
* #processing each json file in the list 
* for json_str in json_list:
*     try:
*         #parcing the json string into an dictionary
*         article = json.loads(json_str)
* 
*         if article["json_object"].get("category") and article["json_object"].get("image",{}).get("thumbnail",{}).get("contentUrl",{}):
*             
*             #extract info form the dictionary
*             title.append(article['json_object']['name'])
*             description.append(article['json_object']['description'])
*             category.append(article['json_object']['category'])
*             image.append(article['json_object']['image']['thumbnail']['contentUrl'])
*             url.append(article['json_object']['url'])
*             provider.append(article['json_object']['provider'][0]['name'])
*             datePublished.append(article['json_object']['datePublished'])
* 
*     except Exception as e:
*         print(f"Error Processing JSON object: {e}")

- we are using an zip function to combine all the all we have together. we are also defining an schema and storing the data into an new df_cleaned
* from pyspark.sql.types import StructType, StructField, StringType
* #Combine the lists
* data = list(zip(title, description, category, url, image, provider, datePublished))
* #Define schema
* schema = StructType([
*     StructField("title", StringType(), True),
*     StructField("description", StringType(), True),
*     StructField("category", StringType(), True),
*     StructField("url", StringType(), True),
*     StructField("image", StringType(), True),
*     StructField("provider", StringType(), True),
*     StructField("datePublished", StringType(), True)
* ])
* 
* #Create DataFrame
* df_cleaned = spark.createDataFrame (data, schema=schema)

- Then we can display the df_cleaned to view the values in a table and we can see that he published date is in date time format so we are changing into an date format using the function today. And store the value in a new db 
* display(df_cleaned)
* from pyspark.sql.functions import to_date,date_format
* df_cleaned_final = df_cleaned.withColumn("datePublished", date_format(to_date("datePublished"),"dd-MMM-yyyy"))

- Then now we can write our table into the lake house we created as in a delta table format 
* df_cleaned_final.write.format("delta").saveAsTable("bing_news_db.tbl_latest_news")

- Upon refreshing the table, we can observe the tbl_latest_news, which was stored in the lake house in Delta format.
 
INCRIMENTAL LOAD

- Type 1 Data Warehouse
- In a Type 1 data warehouse, when adding new data to a table, it first checks if there is any existing data with the same identifier. If there is no matching data, the new value is added to the table. If there is matching data, the values in the existing row are compared with the new values. If any values differ, the new values are added to the ID. If all values are the same, no changes are made.

- Type 2 Data Warehouse
- Type 2 data warehouse is similar to Type 1, but it does not overwrite the previous record. Instead, it adds the new record as a separate entry, even if the identifier is the same. If any content in the row changes, a new record is added, regardless of whether it has the same identifier as the previous record.

- Identifying the Latest Record
- To determine which record is the latest for a table with multiple entries with the same identifier, a concept called a “flag” is used in data warehouses. This flag is a column that can be set to “Y” or “N” to indicate whether the record is the latest or not.
- For example, if the latest record has a “Y” flag and the history data has an “X” flag, the latest record is considered the most recent.

- We are going to use type 1 for this project.
- First we are using the same logic to code to write the data into the data lake but we are using it inside the try block so If he hit the error the execution handling will active and use the type 1 logic we have created under the exception.
- The type 1 merge logic was created with sql create or replace temp view.
* from pyspark.sql.utils import AnalysisException
* try:
* 
*     table_name = 'bing_news_db.tbl_latest_news'
* 
*     df_cleaned_final.write.format("delta").saveAsTable(table_name)
* 
* except AnalysisException:
* 
*     print("Table Already Exists")
* 
*     df_cleaned_final.createOrReplaceTempView("vw_df_cleaned_final") #--> name of the view
* 
*     spark.sql(f"""  MERGE INTO {table_name} target_table --alias orginal tabel as target
*                     USING vw_df_cleaned_final source_view --alias view as source
* 
*                     ON source_view.url = target_table.url --joining
* 
*                     WHEN MATCHED AND --condition
* 
*                     source_view.title <> target_table.title OR -- if there is any change in the column
*                     source_view.description <> target_table.description OR
*                     source_view.category <> target_table.category OR
*                     source_view. image <> target_table.image OR
*                     source_view.provider <> target_table.provider OR
*                     source_view.datePublished <> target_table.datePublished
* 
*                     THEN UPDATE SET * --will update whole row on the source
* 
*                     WHEN NOT MATCHED THEN INSERT * --if it is a new data insted of overwriting the row it will get inserted to the source
*                 """)

SENTIMENT ANLAYSIS

- This sentiment analysis will be conducted using the Synapse data science tool within Fabric. Unlike regular data science experiments that involve model training, prediction, and processing, this experiment will utilize a pre-trained model. We will create a new notebook titled “news_sentiment_analysis” and add the existing Lakehouse data we created to it, following the same process as before.
- Next, we will select the “tbl_latest_news” table and click on the three dots next to it. Then, we will select “Load” and click on “Spark.” This will automatically generate code for us to read the data into the notebook.
* df = spark.sql("SELECT * FROM bing_news_db.tbl_latest_news")
* display(df)

- We will conduct a sentiment analysis on the description column of the news.
- To accomplish this, we need to import the necessary libraries. 
* import synapse.ml.core
* from synapse.ml.services import AnalyzeText

- In the subsequent step, we need to configure a model.
- We are utilizing the analyze text function, where we set the text for analysis as the description and select the sentiment analysis option. However, we also employ various keywords for language analysis and other types of text analysis. Subsequently, we define an output column for the sentiment analysis response and an error column to store any errors encountered during execution. If no errors occur, the error column will be null. All these components will be stored in a variable we previously mentioned as the model.
* model = (AnalyzeText()
*         .setTextCol("description")
*         .setKind("SentimentAnalysis")
*         .setOutputCol("response")
*         .setErrorCol("error"))

- Subsequently, we will transform the data contained within the result column into a data frame.
* result = model.transform(df)

- Subsequently, we can visualize the results in a DataFrame format. This will include two new columns, “Error” and “Response,” where the “Response” column will contain the sentiment.
* display(result)

- The response column will contain the sentiment in JSON format. Upon clicking on a row, only the sentiment will be displayed.
* "{"documents":{"sentences":[{"sentiment":"neutral",..."
* documents: "{"sentences":[{"sentiment":"neutral","confidenceSc..."
* 	3	modelVersion: ""2025-01-01"" ——> this is the format we can see on the result column we only need the sentiment inside the document.
- Code
- We have created a DataFrame named sentiment_df using the data from the previous DataFrame. In this iteration, we are extracting the sentiment values from the response column and storing them in a new column named sentiment.
* from pyspark.sql.functions import col —>col function used to refer the column in a df
* sentiment_df = result.withColumn("sentiment", col("response.documents.sentiment"))
* display(sentiment_df)

- Subsequently, we can eliminate the redundant columns, namely “error” and “response,” thereby optimizing the reporting process. The modified DataFrame containing all relevant columns will be stored for further analysis.
* sentiment_df_final = sentiment_df.drop("error","response")
* display(sentiment_df_final)

- Now, we will employ the same type 1 method as previously to write the file into the lake house we created. However, we can utilize the same code from the process_bing_news notebook, but we must make some modifications.
- Specifically, we need to alter the name of the data frame to our sentiment final data frame and the name of the view to match that. All other aspects remain unchanged.
* from pyspark.sql.utils import AnalysisException
* try:
* 
*     table_name = 'bing_news_db.tbl_sentiment_analysis'
* 
*     sentiment_df_final.write.format("delta").saveAsTable(table_name)
* 
* except AnalysisException:
* 
*     print("Table Already Exists")
* 
*     sentiment_df_final.createOrReplaceTempView("vw_sentiment_df_final") #--> name of the view
* 
*     spark.sql(f"""  MERGE INTO {table_name} target_table --alias original table as target
*                     USING vw_sentiment_df_final source_view --alias view as source
* 
*                     ON source_view.url = target_table.url --joining
* 
*                     WHEN MATCHED AND --condition
* 
*                     source_view.title <> target_table.title OR -- if there is any change in the column
*                     source_view.description <> target_table.description OR
*                     source_view.category <> target_table.category OR
*                     source_view. image <> target_table.image OR
*                     source_view.provider <> target_table.provider OR
*                     source_view.datePublished <> target_table.datePublished
* 
*                     THEN UPDATE SET * --will update whole row on the source
* 
*                     WHEN NOT MATCHED THEN INSERT * --if it is a new data instead of overwriting the row it will get inserted to the source
*                 """)

POWER-BI DATA REPORTING

- Now, we can utilize the final sentiment table we created to construct a dashboard. To achieve this, we need to connect this table to Power BI using a new schematic model. The decision to employ a schematic model is driven by the ability to integrate data security governance and other necessary functionalities directly within Power BI, eliminating the need for external storage like the lake house. This model will remain separate from the lake house, facilitating easier management.
- With the schematic model in place, we can select the specific tables required for the report rather than loading all datasets from the lake house.
- Next, we click on the schematic model and provide it with a name, such as “bing-news-dashboard-dataset.” Subsequently, we select the table necessary for the report and click on “Confirm.”
- Upon confirming, Power BI will display the dataset. To access the workspace and the schematic model we created for the dashboard, we click on the bottom left fabric logo and select “Power BI.”
- Upon opening the workspace, we find the schematic model we created for the dashboard.
- To begin building the report, we can create a table containing all the necessary data. We observe that the URL is not clickable. To save the dashboard, we select “Save” and provide it with a name, such as “news-dashboard.”
- Next, we return to the schematic model we created to modify the URL.
- We click on the three dots next to the schematic model and select “Open Data Model.” In the right-top corner, we change “Editing” to “Viewing.” Subsequently, we click on the “URL” column and select “Advanced.” In the “Data Type” option, we change “Uncategorized” to “Web URL.” Finally, we return to the dashboard, where the URL will now be properly formatted.
- Additionally, we add a slicer for the year to enhance the dashboard’s functionality.
- The primary purpose of this dashboard is to display the latest news. To achieve this, we add a filter to the table we created using the “Top N” feature, setting the value to 1 and the “By Value” to “Date Published.” It will now sort by the recent date. Then we click the lock symbol on top of the filter lock on this visual so when ever an data is added this will apply the filter.
- Now we can add some measures to the report by going back to schematic model and on top we can see open data model button.

- Creating an new measure for positive sentiment. This is an if condition if the sentiment is positive it will count the value. If yes then it will divide the value with total no of rows. This will give us the total positive %.
* Positive Sentiment % = 
* IF(  
*     COUNTROWS(
*         FILTER(
*             'tbl_sentiment_analysis',
*             'tbl_sentiment_analysis'[sentiment] = "positive"
*         )
*     ) > 0, 
*     DIVIDE(
*         CALCULATE(
*             COUNTROWS(
*                 FILTER(
*                     'tbl_sentiment_analysis',
*                     'tbl_sentiment_analysis'[sentiment] = "positive"
*                 )
*             )
*         ), 
*         COUNTROWS('tbl_sentiment_analysis')
*     ), 
*     0
* )
- We can use the same code but just by changing the key values to negative and neutral we can add two measurements.

- Then we can give open data model form the top of the dashboard and on the left side under model we can choose our measure on filter we can change it to percentage and after that we can add 3 cards each for one sentiment and add the same filter as before so that we can have. The percentage of sentiment per day as of recent day.

PIPELINE

- Let us commence the pipeline we have already established.
- We have already incorporated a pipeline for data ingestion.
- Subsequently, select the notebook from the top, and a green tick sign will indicate its activation. This signifies that when the data ingestion is successful, it proceeds to the next step, which is the notebook.
- Now, let us name the notebook in the pipeline as (Data_Transformation). Proceed to the settings of the notebook and select the workspace (process_bing_data).
- Add another notebook, maintaining the same name as before, (Sentiment_Analysis), and select the (news_sentiment_analysis) notebook.
- This pipeline’s functionality is as follows: The initial pipeline we created ingests data from an API and loads it into the lakehouse. Upon successful completion, the data passes to the next pipeline, which is responsible for transforming the data. This pipeline preprocesses the data for sentiment analysis. Upon success, the data is reloaded into the lakehouse in Delta table format and subsequently loaded into the next notebook (Sentiment_Analysis) for sentiment prediction of new articles.
- Now, let us address the requirement mentioned earlier that we need only the latest news. Although we provided a command for freshness to the day, this may not suffice for specific needs, such as new related to football. To address this, we will introduce a search term into the pipeline.
- To do this, select the white space and choose the parameter option. Select “new” as the parameter name and type it as a string. Set the default value to (latest news).
- Now that we have created a parameter, let’s add it to the ingestion process. If we go to the source, we can see the relative URL we already created (?q=latest+news&count=100&freshness=Day&mkt=en-IN).
- The next step is to click on “Add dynamic content” under the relative URL. On the right-side pane, we see the parameter we created. If we click on it, we get the expression of the parameter (@pipeline().parameters.Search_term).
- Now, let’s paste it on the relative URL we created by replacing the “latest+news” term. However, we need to mention the expression inside an {} after the @ symbol (?q=@{pipeline().parameters.Search_term}&count=100&freshness=Day&mkt=en-IN).
- After this, if we give preview data, it will show the parameter we passed. We can then change the value if we want. If we keep the “latest news” as the value, it will give us the latest news as we can see in the preview.
- Now, we can set a schedule for this pipeline. For that, click on the “Schedule” button at the top and change the schedule run to “On” and the repeat to “Daily.” Change the time to 6:00 AM, set a start and end date for the schedule, and select the appropriate time zone.
- Now, we can manually run the pipeline using the “Run” button at the top and mention an value for the parameter. The pipeline execution will start.
Changing the datePublished column to a string by going back to the sentiment analysis notebook after creating the pipeline should have fixed this issue.
- We need to write some temporary code to fix this. 

- Initially, we import the loading data into a pandas DataFrame.
* #temp code delete after run 
* df = spark.sql("SELECT * FROM bing_news_db.tbl_sentiment_analysis")

- Subsequently, import the requisite functions.
- We can then sue the to_date function to modify the data type.
* from pyspark.sql.functions import col, to_date
* df = df.withColumn("datePublished", to_date(col("datePublished"),"dd-MM-yyyy"))

- Then print the schema to verify.
* df.printSchema()

- After that we can manually overwrite the schema of the table 
* df.write.format('delta').mode("overwrite").option("overwriteSchema","True").saveAsTable(table_name)

- Subsequently, we can verify the data type of the table by extending the left side under the table drop-down menu.
- Upon completion of these tasks, please comment or markdown the newly added cells.

- However, it is advisable to place the code for merging the data type cell for future ingestion just past the code provided above. This is because we only modify the final sentient table we have already created. When we run the pipeline according to sentiment analysis, this will prepare the data from the (tbl_atest_news) table that will be inputted.

- For the transform data notebook, which still retains the data type as string for upcoming data, we can paste the code before the merge cell to modify the data type of the future ingested data. However, before executing the code, we need to change df to the previous data frame on the book, which is “sentiment_df_final.” This is because df is a temporary data frame we created to rectify the previously existing table.
* from pyspark.sql.functions import col, to_date
* sentiment_df_final = sentiment_
* df = df.withColumn("datePublished", to_date(col("datePublished"),"dd-MMM-yyyy"))

- Now let’s check the report. then we can go to data model an edit table and then click refresh to add the new changes on schema to this report and confirm then click on datePublished we can see that its in date time format. Change to desired date time format.
- Then on the filters we already we created we can notice some changes like we ca see that the filter type has been changed form firstdatePublished to earliestdatePublished now we change it to latestdatePublished. These changes are happening because of the date conversiion.

SET UP ALERTS USING DATA ACTIVATOR

- Now, let us open our workspace and select “Get Item” and choose the “Item Activator.” If we click on “Get Data,” we will find two options to set the activator on Power BI and be prompted to return to the Power BI dashboard to set alerts on the visuals using additional options.
- Next, let us delete the activator and return to the dashboard.
- We can observe that there is also a sentiment called “Mixed” for which we can add the same measurement as before for reporting.
- To check the run history of the pipeline, we can access the schedule runs. Additionally, we can utilize the Monitor Hub at the bottom to monitor all events on the pipeline.
- Now, let us return to Power BI and select any of the visual elements. If we click on the three dots located at the bottom, an option to set alerts will appear.
- This will open a window on the right side, where we can select the condition using two options: “Change” and “Becomes.” In this case, we can use “Becomes” as specified. We can add a measure, such as 6%, and select the desired location for receiving the alert, such as Outlook or email. Now, we are choosing teams. When the positive sentiment reaches 6%, we will receive an alert on Outlook for the selected user. Click “Apply.”
- Next, on the bottom right corner, click on the three dots and select the “Select Activator Location” option. Choose the workspace and name the new activator item, such as “Positive_News_Alert.”
- We can now see the new “Positive_News_Alert” item created on our workspace. Open it to view all the details about the activator, including the message we will receive on Outlook when the condition is true. We can also edit the alert in this instance.
- Let’s verify if everything is functioning by running the pipeline again using the new value, “Movies.”
- Currently, we are not receiving any alerts. This is because, upon reviewing the activator, the time set to one hour indicates that it will automatically refresh every hour. To address this, we can select “Send Me a Test Action” at the top to receive a sample alert via email to confirm its functionality.
- This concludes the entirety of the project.

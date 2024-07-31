# YouTube Data Harvesting and Warehousing

YouTube Data Harvesting and Warehousing is a project designed to provide users with the ability to access and analyze data from numerous YouTube channels. This project utilizes SQL, MongoDB, and Streamlit to develop a user-friendly application for retrieving, saving, and querying YouTube channel and video data.

## Tools and Libraries Used

### Streamlit
Streamlit is used to create an interactive user interface for the application. It enables users to perform data retrieval and analysis operations through a web-based application.

### Python
Python is the primary programming language used for the development of this application. It is utilized for data retrieval, processing, analysis, and visualization.

### Google API Client
The `googleapiclient` library is used to interact with YouTube's Data API v3. This library facilitates the retrieval of essential information such as channel details, video specifics, and comments from YouTube.

### MySQL
MySQL is an open-source relational database management system used to store and manage structured data. It supports various data types and advanced SQL capabilities for efficient data management and querying.

## Features

1. **Retrieval of Channel and Video Data**: Access detailed information about YouTube channels and videos using the YouTube API.
2. **Data Storage**: Store the retrieved data in a MongoDB database for scalable data management.
3. **Data Migration**: Migrate data from MongoDB to a MySQL database for efficient querying and analysis.
4. **Data Retrieval and Analysis**: Use various query options to search and retrieve data from the MySQL database.

## Libraries Required

1. `googleapiclient.discovery`
2. `streamlit`
3. `re` (Regular Expression)
4. `datetime`, `timedelta`
5. `pandas`

## Ethical Considerations

When scraping YouTube data, it is essential to adhere to ethical practices:
- **Respect YouTube's Terms of Service**: Ensure that the scraping activities comply with YouTube's terms and conditions.
- **Obtain Authorization**: Use appropriate API keys and authorization methods.
- **Data Protection**: Handle collected data responsibly, ensuring privacy and confidentiality.
- **Impact on Platform**: Consider the potential impact on the platform and its community, aiming for fair and sustainable data extraction.

## Installation and Setup

1. **Install Dependencies**: Ensure that you have all the required libraries installed. You can install them using pip:
    ```bash
    pip install google-api-python-client pandas streamlit mysql-connector-python
    ```

2. **API Key**: Replace the `api_id` in the code with your YouTube Data API v3 key.

3. **Database Setup**:
    - **MySQL**: Set up MySQL and create the necessary databases and tables as described in the code.

4. **Run the Application**:
    - Start the Streamlit application by executing the following command:
      ```bash
      streamlit run your_script.py
      ```

## Usage

1. **Enter the Channel ID**: Input the desired YouTube channel ID in the Streamlit UI.
2. **Migrate Data to SQL**: Click the "Migrate to SQL" button to transfer data from MongoDB to the MySQL database.
3. **Select Queries**: Use the provided options to query and view data from the MySQL database.



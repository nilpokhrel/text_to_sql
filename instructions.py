
user_query_exploration = """

Exploring the User Query in Detail
Step 1: Preprocess the Query

    Convert query to lowercase.
    Remove unnecessary punctuation (except those needed for meaning).
    Tokenize into words.

Step 2: Identify Query Type

Classify the query into one of the following categories:

    Retrieval → “Show me all flights” → SELECT * FROM flights
    Aggregation → “What’s the average delay?” → SELECT AVG(delay) FROM flights
    Filtering → “Flights from NYC to LA” → WHERE origin = 'NYC' AND destination = 'LA'
    Sorting & Ranking → “Top 10 longest flights” → ORDER BY duration DESC LIMIT 10
    Joining Data → “Flights and weather conditions” → JOIN flights ON weather.date = flights.date

Step 3: Detect Key Entities & Filters

    Tables & Columns: Extract potential table and column names.
    Conditions: Look for filtering words (greater than, before, after, between, etc.).
    Time References: Detect dates, durations (last year, in 2020).
    Sorting & Limits: Look for ranking or ordering cues (top 10, most delayed).

Step 4: Validate User Intent

    Check if the query needs extra context → Ask for missing details.
    Detect ambiguity → Clarify vague terms (recent flights = last 7 days?).
    Ensure user’s request is reasonable → Prevent overly broad queries.
    
return clear and concise summary of your findings.

"""


user_query_to_sql = """

Generating a Safe and very clear SQL Query After Exploration with reference to below data hints

Information of Flights, Airlines and Airports:
{}

Step 1: Map Query Elements to SQL

    Identify SELECT columns (or use * if unspecified but safe).
    Identify FROM table based on detected keywords.
    Construct WHERE conditions from filters.
    Add ORDER BY & LIMIT if ranking or pagination is needed.

Step 2: Ensure Security & Validity

    Validate Table & Column Names → Check against a predefined schema.
    Use Parameterized Queries → Prevent SQL injection.
    Restrict Modifications → Allow only SELECT unless explicitly permitted.
    Limit Result Size → Use LIMIT to prevent excessive data retrieval.

Step 3: Generate the Final SQL Query

    Assemble the query structure dynamically.
    Format the query properly.
    Log the generated SQL for debugging.
    
return only the final SQL query
"""

flight_context = """ 
You are provided with 3 table names and its column names.
Theres one table named airlines with column name IATA_Code, Airline . 
    where in Airline Table 
    IATA is 2 character code , 
    Airline is Name of Airline Company.
    
Then another table is of Airport where there are following column names respectively:
    IATA_CODE  3 character code
    AIRPORT Name of Airport
    CITY Location of Airport
    STATE State name of Country
    COUNTRY Name of the Country
    LATITUDE latitude values
    LONGITUDE longitude values

And finally, there is a Flights data where every activities of Air flights are recorded.
YEAR,MONTH,DAY,DAY_OF_WEEK,AIRLINE,FLIGHT_NUMBER,TAIL_NUMBER,ORIGIN_AIRPORT,DESTINATION_AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY,TAXI_OUT,WHEELS_OFF,SCHEDULED_TIME,ELAPSED_TIME,AIR_TIME,DISTANCE,WHEELS_ON,TAXI_IN,SCHEDULED_ARRIVAL,ARRIVAL_TIME,ARRIVAL_DELAY,DIVERTED,CANCELLED,CANCELLATION_REASON,AIR_SYSTEM_DELAY,SECURITY_DELAY,AIRLINE_DELAY,LATE_AIRCRAFT_DELAY,WEATHER_DELAY
"""

combined_instruction = """

Prompt:

You are provided with 3 tables with the following structure:

    Airlines Table:
        IATA_Code (CHAR(2)): The 2-character code for the airline (primary key).
        Airline (VARCHAR): The name of the airline company.

    Airports Table:
        IATA_Code (CHAR(3)): The 3-character code for the airport (primary key).
        Airport (VARCHAR): The name of the airport.
        City (VARCHAR): The location city of the airport.
        State (CHAR(2)): The state name where the airport is located.
        Country (VARCHAR): The name of the country where the airport is located.
        Latitude (FLOAT): Latitude value of the airport.
        Longitude (FLOAT): Longitude value of the airport.

    Flights Table:
        Year (INT): The year of the flight.
        Month (INT): The month of the flight.
        Day (INT): The day of the flight.
        Day_of_Week (INT): The day of the week of the flight (0-6, where 0 = Sunday).
        Airline (CHAR(2)): The 2-character IATA code of the airline.
        Flight_Number (VARCHAR): The flight number.
        Tail_Number (VARCHAR): The tail number of the airplane.
        Origin_Airport (CHAR(3)): The 3-character IATA code of the origin airport.
        Destination_Airport (CHAR(3)): The 3-character IATA code of the destination airport.
        Scheduled_Departure (INT): The scheduled departure time in UNIX timestamp format.
        Departure_Time (INT): The actual departure time in UNIX timestamp format.
        Departure_Delay (INT): Delay in departure time in minutes.
        Taxi_Out (INT): Taxi out time in minutes.
        Wheels_Off (INT): Time when the plane took off in UNIX timestamp format.
        Scheduled_Time (INT): The scheduled flight duration in minutes.
        Elapsed_Time (INT): The total flight duration in minutes.
        Air_Time (INT): The time spent in the air, excluding taxi time.
        Distance (INT): The distance flown in miles.
        Wheels_On (INT): Time when the plane landed in UNIX timestamp format.
        Taxi_In (INT): Taxi-in time in minutes.
        Scheduled_Arrival (INT): The scheduled arrival time in UNIX timestamp format.
        Arrival_Time (INT): The actual arrival time in UNIX timestamp format.
        Arrival_Delay (INT): Arrival delay in minutes.
        Diverted (INT): 1 if the flight was diverted, 0 if not.
        Cancelled (INT): 1 if the flight was cancelled, 0 if not.
        Cancellation_Reason (CHAR(1)): A single character representing the cancellation reason.
        Air_System_Delay (INT): Delay due to air system issues in minutes.
        Security_Delay (INT): Delay due to security in minutes.
        Airline_Delay (INT): Delay caused by the airline in minutes.
        Late_Aircraft_Delay (INT): Delay due to late arriving aircraft in minutes.
        Weather_Delay (INT): Delay due to weather in minutes.

Your Task:
The Sql query should first load all tables and join by relation IATA code and Airline and Airport columns. 
Here relation of table is by IATA_Code (CHAR(2)) in Flight and Airline table. Similarly, IATA_Code (CHAR(3)) in Airport table is related to Origin and destination airports.
Given the above table structures and column names, generate a valid SQL query for the following types of requests:

    Queries to filter records by specific attributes, such as airlines, airports, or flight details.
    Aggregated queries to summarize flight data, like average delays, flight counts, etc.
    Join queries to combine data from airlines, airports, and flights.

Example Requests:

    Find all flights operated by a specific airline (e.g., "AA" for American Airlines) between two airports.
    Get the total number of cancelled flights for each airline.
    Retrieve the airport information for a specific airport code.
    Get the average delay for flights departing from a particular airport.
    Find all flights that were diverted and their reason.
    List the flights between two airports (e.g., 'JFK' and 'LAX') that were delayed more than 30 minutes.

Expected Output:

Based on the request, generate a valid SQL query to fetch the required information from the tables. Ensure the SQL query is syntactically correct and optimized for performance.

"""
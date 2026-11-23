
# 1. Import libraries
import streamlit as st
import pandas as pd
import altair as alt

# 2. Set up the app
st.set_page_config(                           #Referred to: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
    page_title="Bigfoot Sightings Explorer",                                   
    layout="wide"
)

st.title("Bigfoot Sightings Explorer")

st.write(
    "This app explores reported Bigfoot sightings "
    "across different years and states."
)

# 3. Load the dataset
url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/bfro_reports_fall2022.csv"
df = pd.read_csv(url)

# 4. Prepare the data
df_clean = df.copy()

# Convert date to datetime and extract the year
df_clean["date"] = pd.to_datetime(                              #Referred to: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
    df_clean["date"], errors="coerce"
)
df_clean["year"] = df_clean["date"].dt.year

# Count sightings by year
yearly_counts = df_clean.groupby("year").size().reset_index(name="count")       #Referred to: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html

# Count sightings by state
state_counts = df_clean.groupby("state").size().reset_index(name="count")
state_counts = state_counts.sort_values("count", ascending=False)


# 5. Visualization 1: Bigfoot Sightings Over Time
st.header("1. Bigfoot Sightings Over Time")

# Add a slider to select the starting year
start_year = st.slider(                                 #Referred to: https://docs.streamlit.io/develop/api-reference/widgets/st.slider
    "Select Starting Year",
    min_value=1869,
    max_value=2018,
    value=1869    ##default & minimum value: 1869
)

# Filter the data based on the selected year
filtered_years = yearly_counts[yearly_counts["year"] >= start_year]

# Create a line chart
chart1 = alt.Chart(filtered_years).mark_line(strokeWidth=3).encode(        #Referred to: https://altair-viz.github.io/user_guide/marks/line.html
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d")),
    y=alt.Y("count:Q", title="Number of Sightings"),
    tooltip=["year:Q", "count:Q"]
).properties(
    title="Bigfoot Sightings Over Time",
    height=350
)

# Display the chart in Streamlit
st.altair_chart(chart1, use_container_width=True)


# Add the write-up for Visualization 1
st.markdown("""
### Visualization 1 Write-up

This line chart shows **how the number of reported Bigfoot sightings has changed over time**. I used a **line chart** because it makes it easier to see trends across years. The x-axis represents the **year**, while the y-axis shows the **number of reports**.

I also made the line slightly thicker to improve visibility and make hovering easier. I added a slider so users can explore the data from different starting years. If I had more time, I would like to compare the trends across different states to see whether they follow similar patterns.
""")


# 6. Visualization 2: Bigfoot Sightings by State
st.header("2. Bigfoot Sightings by State")

# Add a slider to select the number of states
top_n = st.slider(
    "Select Number of States",
    min_value=5,
    max_value=20,
    value=10
)

# Select the top states based on the slider
top_states = state_counts.head(top_n)

# Create a horizontal bar chart
chart2 = alt.Chart(top_states).mark_bar().encode(             #Referred to: https://altair-viz.github.io/user_guide/marks/bar.html
    x=alt.X("count:Q", title="Number of Sightings"),
    y=alt.Y("state:N", sort="-x", title="State"),
    tooltip=["state:N", "count:Q"]
).properties(
    title="Top States by Bigfoot Sightings",
    height=450
)

# Display the chart in Streamlit
st.altair_chart(chart2, use_container_width=True)



# Add the write-up for Visualization 2
st.markdown("""
### Visualization 2 Write-up

This horizontal bar chart compares the number of reported Bigfoot sightings across different states. Washington has the highest number of reports (563), followed by California (402) and Florida (292). I used a **horizontal bar chart** because it makes it easier to compare the counts across states and read their names.

The bars are sorted in descending order to highlight the states with the most reports. I also added a slider so users can choose how many states to display, from 5 to 20. If I had more time, I would like to compare the number of sightings relative to each state's population, since states with larger populations may naturally have more reports.
""")



# Explain the difference from Homework 5
st.markdown("""
### Comparison with Homework 5

For this homework, I used the **Bigfoot sightings dataset** instead of the UFO dataset from Homework 5. Both visualizations were created for this assignment, and I did not reuse any plots or written descriptions from Homework 5.
""")

import streamlit as st
from langchain.chat_models import ChatOpenAI

# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate
# from langchain.chains import SimpleSequentialChain

# Langchain config
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=st.secrets["api_key"],
    max_tokens=1500,
)

## Page and inputs
# Streamlit layout settings
st.set_page_config(page_title="Lotus Bakeries", layout="wide")

# Streamlit app layout
st.markdown(
    '<h1 style="font-size:44px;"><span style="color:#a9202b;">Lotus Bakeries</span> Campaign Advisor</h1>',
    unsafe_allow_html=True,
)

# App description
st.subheader(
    "A demonstration of Generative AI's capabilities in Marketing Campaigns.",
    divider="grey",
)

## Sidebar form:
season = st.sidebar.selectbox(
    "Season",
    (
        "Christmas",
        "Saint Nicholas Day",
        "Valentine's Day",
        "Easter",
        "Halloween",
    ),
)

product_launch = st.sidebar.radio(
    "Product Launch Type",
    ("New product", "Seasonal product"),
)

product_launch_date = st.sidebar.date_input("Product Launch Date", format="MM/DD/YYYY")

budget = st.sidebar.slider(
    "Budget (€)", value=50000, min_value=10000, max_value=500000, step=1000
)

channels = st.sidebar.multiselect(
    "Channels", ["TV", "Radio", "Cinema", "Bus Stop", "Social Media"]
)
joined_channels = "".join(channels)

## Prompt chaining
# Chain 1
# analysis_template = """
# You are a data analyst, I'll give you data and you'll give an short sum up analysis. The data : {data}
# """
# analysis_prompt_template = PromptTemplate(
#     input_variables=["data"], template=analysis_template
# )
# analysis_chain = LLMChain(llm=llm, prompt=analysis_prompt_template)

# Chain 2
# final_template = """
#         You are a marketing expert, and your task is to help me launch a marketing campaign for Lotus Bakeries in Belgium.
#         I'll provide you with essential data. Determine the best timing to maximize the impact of our campaign.
#         Give a very detailed planning of the timing, begin with the campaign start date. Include the steps duration. Don't recap the input data.
#         Please consider all the following details when providing your timing recommendation:
#         Season: The campaign is related to {season}.
#         Product Launch: We are planning to either launch a {product_launch} on {product_launch_date}.
#         Budget: Our campaign budget is set at {budget} €.
#         Channels: We are considering using the following marketing channels : {joined_channels}.
#         """
# final_prompt_template = PromptTemplate(
#     input_variables=[
#         "season",
#         "product_launch",
#         "product_launch_date",
#         "budget",
#         "joined_channels",
#     ],
#     template=final_template,
# )
# final_chain = LLMChain(llm=llm, prompt=final_prompt_template)

# SequentialChain
# overall_chain = SimpleSequentialChain(
#     chains=[analysis_chain, final_chain], verbose=True
# )

## Button to generate exercise
if st.sidebar.button("Generate"):
    with st.spinner("Generating :robot_face:..."):
        prompt = f"""
        You are a marketing expert, and your task is to help me launch a marketing campaign for Lotus Bakeries in Belgium.
        I'll provide you with essential data. Determine the best timing to maximize the impact of our campaign.
        Give a very detailed planning of the timing, begin by giving the campaign start date. Include the steps duration. Don't recap the input data.
        Please consider all the following details when providing your timing recommendation:
        Season: The campaign is related to {season} season.
        Product Launch: We are planning to either launch a {product_launch} on {product_launch_date}.
        Budget: Our campaign budget is set at {budget} €.
        Channels: We are considering using the following marketing channels : {"".join(channels)}.
        """
        # Send the prompt to OpenAI API via Langchain
        completion = llm.predict(prompt)

        # Add csv file as parameter
        # completion = overall_chain.run()

        if completion:
            # Display the generated exercise and other informations
            st.subheader(":sparkles: Campaign advice :sparkles:")
            st.write(completion)
        else:
            st.error("Error generating the advice. Please try again.")

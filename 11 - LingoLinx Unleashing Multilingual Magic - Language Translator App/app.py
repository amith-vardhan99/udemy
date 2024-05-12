from ibm_watson import *
from ibm_cloud_sdk_core.authenticators import *
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

def translate_text(normal_text,src,dest):
    API_key = "J9tu8EU1jUcPDgzACNB0rMKgvcHGEEZqiUOcsdL01Fvz"
    url = "https://api.au-syd.language-translator.watson.cloud.ibm.com/instances/639b27de-b9fc-4bed-89c0-594fb661f917"
    authenticator = IAMAuthenticator(apikey=API_key)
    language_translator = LanguageTranslatorV3(version="2018-05-01",authenticator=authenticator)
    language_translator.set_service_url(service_url=url)
    translate_code = src+"-"+dest
    translated_text = language_translator.translate(text=normal_text,model_id=translate_code)
    teu = translated_text.get_result()["translations"][0]["translation"]
    return teu


st.title("Language Translator")

source_language = st.selectbox(label="Select the source language : ",options=("Telugu","Hindi","English","Spanish","Bengali","Korean"))

source_text = st.text_area(label="Enter the text in the source language that you want to translate",height=300)

destination_language = st.selectbox(label="Select the destination language : ",options=("Telugu","Hindi","English","Spanish","Bengali","Korean"))

languages = {
    "Telugu" : "te",
    "Hindi" : "hi",
    "English" : "en",
    "Spanish" : "es",
    "Bengali" : "bn",
    "Korean" : "ko",
}


if st.button(label="Translate Text"):
    if source_language == destination_language:
        st.write("Please use different languages for translation")
    else:
        st.write(translate_text(source_text,languages[source_language],languages[destination_language]))
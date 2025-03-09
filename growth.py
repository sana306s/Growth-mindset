import streamlit as st
import pandas as pd 
from io import BytesIO

st.set_page_config(page_title="Project 1",layout="wide")
st.title("Project 1 & Cleaner")
st.write("Upload csv or excel files, clean data,and convert formula.")

files=st.file_uploader("Uploader CSV or EXcel Files.",type=["csv","xlsx"],accept_multiple_files=True)
if files :
    for file in files :
        ext=file.name.splir(".")[-1]
        df = pd.read_cvs(files)if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if checkbox(f"Remove Duplicates -{file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

            if checkbox(f"Fill Missing Valus - {file.name}"):
                df = filna(df.select_dtypes(include=[number]).mean(), inplace=True)
                st.success("Missing Values with mean")
                st.dataframe(df.head())

                selected_columns=st.multiselect(f"SelectCOLumns -{file.name}",df.columns, default =df.columns)
                df = df[selected_columns]
                st.dataframe(df.head())

                if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
                    st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

                format_choice = st.radio(f"Convert {file.name} to:", ["csv","Excel"], key=file.name) 

                if st.button(f"Download{file.name} as {format_choise}"):
                    output = BytesIO()
                    if format_choise == "csv":
                        df.to_csv(output, index=False)
                        mine= "text/csv"
                        new_name= file.name.replace(ext, "csv")

                    else : 
                            df.to_excel(output, index=False, engine= 'openpyxl')
                            mine = "Application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            new_name = file.name.replace(ext, "xlsx")

                            output.seek(0)
                            st.set_download_button("Download file", filename=new_name, data=output, mime=mine)

                            st.success("Processing Complete")



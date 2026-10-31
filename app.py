import pandas as pd
import streamlit as st

st.set_page_config(page_title="Universal DMED Analizator", page_icon="📊", layout="wide")

st.title("📊 Universal DMED va Hisobot Tahlili Paneli")
st.markdown("Исталган турдаги Excel ёки CSV ҳисобот файлини юкланг, тизим уни автоматик равишда таҳлил қилиб беради.")

uploaded_file = st.file_uploader("Ҳисобот файлини юкланг (Excel / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Fayl turini aniqlab o'qish
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
            
        st.success("Маълумотлар муваффақиятли юкланди!")
        
        # Asosiy statistikalar
        st.subheader("📈 Асосий кўрсаткичлар")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Жами қаторлар (сони)", len(df))
        with col2:
            st.metric("Устунлар сони", len(df.columns))
        with col3:
            # Agar raqamli ustun bo'lsa o'rtachasini chiqarish
            num_cols = df.select_dtypes(include=['number']).columns
            if len(num_cols) > 0:
                st.metric(f"Жами суммар ({num_cols[0]})", int(df[num_cols[0]].sum()) if not df[num_cols[0]].isna().all() else 0)
            else:
                st.metric("Маълумот тури", "Матнли")

        # Jadvalni ko'rsatish
        with st.expander("📄 Юкланган маълумотлар жадвалини кўриш"):
            st.dataframe(df)

        # Avtomatik tahlil va grafiklar
        st.subheader("📊 Автоматик тақсимот графклари")
        
        # Matnli ustunlardan birini tanlab diagramma chizish
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            selected_col = st.selectbox("Таҳлил қилиш учун устунни Танланг:", cat_cols)
            if selected_col:
                val_counts = df[selected_col].value_counts().head(10).reset_index()
                val_counts.columns = [selected_col, 'Сони']
                st.bar_chart(val_counts.set_index(selected_col))
        else:
            st.info("График чизиш учун матнли устунлар топилмади.")

    except Exception as e:
        st.error(f"Файлни ўқишда хатолик юз берди: {e}")
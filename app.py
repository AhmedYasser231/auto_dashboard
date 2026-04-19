import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="DataDash Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dashboard
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .header-title {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chart-container {
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .divider {
        margin: 2rem 0;
        border-top: 2px solid #e5e7eb;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'datasets' not in st.session_state:
    st.session_state.datasets = {}
if 'current_dataset' not in st.session_state:
    st.session_state.current_dataset = None
if 'dashboard_config' not in st.session_state:
    st.session_state.dashboard_config = {}

# ============ SIDEBAR ============
with st.sidebar:
    st.title("🎛️ التحكم والإدارة")
    
    # File upload section
    st.subheader("📁 رفع البيانات")
    uploaded_file = st.file_uploader(
        "اختر ملف CSV أو Excel",
        type=['csv', 'xlsx'],
        help="يمكنك رفع ملفات متعددة"
    )
    
    if uploaded_file is not None:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Generate dataset name
            dataset_name = uploaded_file.name.replace('.csv', '').replace('.xlsx', '')
            
            # Store in session
            st.session_state.datasets[dataset_name] = df
            st.session_state.current_dataset = dataset_name
            
            st.success(f"✅ تم تحميل: {dataset_name}")
            st.info(f"📊 {len(df)} صف | {len(df.columns)} عمود")
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")
    
    st.divider()
    
    # Dataset selection
    if st.session_state.datasets:
        st.subheader("📚 البيانات المحملة")
        
        dataset_list = list(st.session_state.datasets.keys())
        selected_dataset = st.selectbox(
            "اختر مجموعة البيانات",
            dataset_list,
            index=dataset_list.index(st.session_state.current_dataset) if st.session_state.current_dataset in dataset_list else 0
        )
        
        st.session_state.current_dataset = selected_dataset
        
        # Delete dataset option
        if st.button("🗑️ حذف المجموعة الحالية", use_container_width=True):
            del st.session_state.datasets[selected_dataset]
            st.session_state.current_dataset = list(st.session_state.datasets.keys())[0] if st.session_state.datasets else None
            st.rerun()
        
        st.divider()
        
        # Show dataset info
        current_df = st.session_state.datasets[st.session_state.current_dataset]
        st.metric("عدد الصفوف", len(current_df))
        st.metric("عدد الأعمدة", len(current_df.columns))
        st.metric("الذاكرة", f"{current_df.memory_usage(deep=True).sum() / 1024:.1f} KB")

# ============ MAIN CONTENT ============

# Header
st.markdown('<div class="header-title">📊 DataDash Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">منصة تحليل البيانات والداشبوردات الذكية</div>', unsafe_allow_html=True)

if not st.session_state.datasets:
    # Empty state
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 من فضلك، اختر ملف من الشريط الجانبي لبدء التحليل")
        
        # Show features
        st.divider()
        st.subheader("✨ المميزات")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("📁 **رفع متعدد**\nحمّل ملفات متعددة")
        with col2:
            st.write("📊 **مخططات ذكية**\n6 أنواع مخططات")
        with col3:
            st.write("📈 **إحصائيات**\nتحليل شامل")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("💾 **تصدير**\nCSV, Excel, JSON")
        with col2:
            st.write("🎨 **تصميم احترافي**\nواجهة أنيقة")
        with col3:
            st.write("⚡ **سريع**\nمعالجة فورية")

else:
    # Get current dataset
    current_df = st.session_state.datasets[st.session_state.current_dataset]
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 الداشبورد",
        "📋 البيانات",
        "📈 المخططات",
        "📉 الإحصائيات",
        "💾 التصدير"
    ])
    
    # ============ TAB 1: DASHBOARD ============
    with tab1:
        st.subheader("📊 الداشبورد المتكامل")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 إجمالي الصفوف", f"{len(current_df):,}")
        with col2:
            st.metric("📋 عدد الأعمدة", len(current_df.columns))
        with col3:
            numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
            st.metric("🔢 أعمدة رقمية", len(numeric_cols))
        with col4:
            categorical_cols = current_df.select_dtypes(include=['object']).columns.tolist()
            st.metric("🏷️ أعمدة نصية", len(categorical_cols))
        
        st.divider()
        
        # Dashboard charts
        numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = current_df.select_dtypes(include=['object']).columns.tolist()
        
        if numeric_cols and categorical_cols:
            # Row 1: Bar and Line charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📊 مخطط بياني**")
                try:
                    fig_bar = px.bar(
                        current_df,
                        x=categorical_cols[0],
                        y=numeric_cols[0],
                        color_discrete_sequence=["#667eea"],
                        title=f"{numeric_cols[0]} حسب {categorical_cols[0]}"
                    )
                    fig_bar.update_layout(height=350, showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)
                except:
                    st.warning("لا يمكن إنشاء المخطط البياني")
            
            with col2:
                st.write("**📈 مخطط خطي**")
                try:
                    if len(numeric_cols) >= 2:
                        fig_line = px.line(
                            current_df,
                            y=numeric_cols[:2],
                            markers=True,
                            title="اتجاه البيانات"
                        )
                    else:
                        fig_line = px.line(
                            current_df,
                            y=numeric_cols[0],
                            markers=True,
                            title="اتجاه البيانات"
                        )
                    fig_line.update_layout(height=350)
                    st.plotly_chart(fig_line, use_container_width=True)
                except:
                    st.warning("لا يمكن إنشاء المخطط الخطي")
            
            # Row 2: Pie and Area charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🥧 مخطط دائري**")
                try:
                    value_counts = current_df[categorical_cols[0]].value_counts().head(10)
                    fig_pie = px.pie(
                        values=value_counts.values,
                        names=value_counts.index,
                        title=f"توزيع {categorical_cols[0]}"
                    )
                    fig_pie.update_layout(height=350)
                    st.plotly_chart(fig_pie, use_container_width=True)
                except:
                    st.warning("لا يمكن إنشاء المخطط الدائري")
            
            with col2:
                st.write("**📊 مخطط مساحة**")
                try:
                    if len(numeric_cols) >= 2:
                        fig_area = px.area(
                            current_df,
                            y=numeric_cols[:2],
                            title="مخطط المساحة"
                        )
                    else:
                        fig_area = px.area(
                            current_df,
                            y=numeric_cols[0],
                            title="مخطط المساحة"
                        )
                    fig_area.update_layout(height=350)
                    st.plotly_chart(fig_area, use_container_width=True)
                except:
                    st.warning("لا يمكن إنشاء مخطط المساحة")
            
            # Row 3: Histogram and Scatter
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📊 توزيع البيانات**")
                try:
                    fig_hist = px.histogram(
                        current_df,
                        x=numeric_cols[0],
                        nbins=30,
                        color_discrete_sequence=["#764ba2"],
                        title=f"توزيع {numeric_cols[0]}"
                    )
                    fig_hist.update_layout(height=350, showlegend=False)
                    st.plotly_chart(fig_hist, use_container_width=True)
                except:
                    st.warning("لا يمكن إنشاء مخطط التوزيع")
            
            with col2:
                st.write("**📍 مخطط التشتت**")
                try:
                    if len(numeric_cols) >= 2:
                        fig_scatter = px.scatter(
                            current_df,
                            x=numeric_cols[0],
                            y=numeric_cols[1],
                            title=f"{numeric_cols[1]} vs {numeric_cols[0]}"
                        )
                    else:
                        fig_scatter = px.scatter(
                            current_df,
                            y=numeric_cols[0],
                            title="مخطط التشتت"
                        )
                    fig_scatter.update_layout(height=350)
                    st.plotly_chart(fig_scatter, use_container_width=True)
                except:
                    st.warning("لا يمكن إنشاء مخطط التشتت")
        
        elif numeric_cols:
            st.info("📌 البيانات تحتوي على أعمدة رقمية فقط. سيتم عرض مخططات التوزيع.")
            
            col1, col2 = st.columns(2)
            with col1:
                fig_hist = px.histogram(current_df, x=numeric_cols[0], nbins=30)
                st.plotly_chart(fig_hist, use_container_width=True)
            with col2:
                fig_box = px.box(current_df, y=numeric_cols[0])
                st.plotly_chart(fig_box, use_container_width=True)
        
        else:
            st.warning("⚠️ لا توجد بيانات رقمية للعرض")
    
    # ============ TAB 2: DATA PREVIEW ============
    with tab2:
        st.subheader("📋 معاينة البيانات")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            rows_to_show = st.slider("عدد الصفوف المعروضة", 5, 100, 10)
        
        st.dataframe(current_df.head(rows_to_show), use_container_width=True)
        
        st.divider()
        st.subheader("📊 أنواع البيانات")
        
        dtype_df = pd.DataFrame({
            'العمود': current_df.columns,
            'النوع': current_df.dtypes,
            'عدد القيم الفارغة': current_df.isnull().sum()
        })
        st.dataframe(dtype_df, use_container_width=True)
    
    # ============ TAB 3: CHARTS ============
    with tab3:
        st.subheader("📈 المخططات التفاعلية")
        
        numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = current_df.select_dtypes(include=['object']).columns.tolist()
        
        chart_type = st.selectbox(
            "اختر نوع المخطط",
            ["مخطط بياني", "مخطط خطي", "مخطط دائري", "مخطط مساحة", "مخطط التشتت", "توزيع البيانات"]
        )
        
        if chart_type == "مخطط بياني" and categorical_cols and numeric_cols:
            x_col = st.selectbox("المحور X", categorical_cols)
            y_col = st.selectbox("المحور Y", numeric_cols)
            fig = px.bar(current_df, x=x_col, y=y_col, color_discrete_sequence=["#667eea"])
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط خطي" and numeric_cols:
            if len(numeric_cols) >= 2:
                y_cols = st.multiselect("اختر الأعمدة", numeric_cols, default=numeric_cols[:2])
                fig = px.line(current_df, y=y_cols, markers=True)
            else:
                fig = px.line(current_df, y=numeric_cols[0], markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط دائري" and categorical_cols:
            col = st.selectbox("اختر العمود", categorical_cols)
            value_counts = current_df[col].value_counts().head(10)
            fig = px.pie(values=value_counts.values, names=value_counts.index)
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط مساحة" and numeric_cols:
            if len(numeric_cols) >= 2:
                y_cols = st.multiselect("اختر الأعمدة", numeric_cols, default=numeric_cols[:2])
                fig = px.area(current_df, y=y_cols)
            else:
                fig = px.area(current_df, y=numeric_cols[0])
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط التشتت" and numeric_cols:
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("المحور X", numeric_cols)
                y_col = st.selectbox("المحور Y", numeric_cols)
                fig = px.scatter(current_df, x=x_col, y=y_col)
            else:
                fig = px.scatter(current_df, y=numeric_cols[0])
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "توزيع البيانات" and numeric_cols:
            col = st.selectbox("اختر العمود", numeric_cols)
            fig = px.histogram(current_df, x=col, nbins=30, color_discrete_sequence=["#764ba2"])
            st.plotly_chart(fig, use_container_width=True)
    
    # ============ TAB 4: STATISTICS ============
    with tab4:
        st.subheader("📉 الإحصائيات التفصيلية")
        
        numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            col = st.selectbox("اختر العمود", numeric_cols)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("المتوسط", f"{current_df[col].mean():.2f}")
            with col2:
                st.metric("الوسيط", f"{current_df[col].median():.2f}")
            with col3:
                st.metric("الحد الأدنى", f"{current_df[col].min():.2f}")
            with col4:
                st.metric("الحد الأقصى", f"{current_df[col].max():.2f}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("الانحراف المعياري", f"{current_df[col].std():.2f}")
            with col2:
                st.metric("التباين", f"{current_df[col].var():.2f}")
            with col3:
                st.metric("القيم الفريدة", current_df[col].nunique())
            with col4:
                st.metric("القيم الفارغة", current_df[col].isnull().sum())
            
            st.divider()
            st.write("**الملخص الإحصائي:**")
            st.dataframe(current_df[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("لا توجد أعمدة رقمية")
    
    # ============ TAB 5: EXPORT ============
    with tab5:
        st.subheader("💾 تصدير البيانات")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = current_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 تحميل CSV",
                data=csv,
                file_name=f"{st.session_state.current_dataset}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                current_df.to_excel(writer, index=False, sheet_name='البيانات')
            excel_buffer.seek(0)
            st.download_button(
                label="📥 تحميل Excel",
                data=excel_buffer.getvalue(),
                file_name=f"{st.session_state.current_dataset}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col3:
            json_data = current_df.to_json(orient='records', indent=2, force_ascii=False)
            st.download_button(
                label="📥 تحميل JSON",
                data=json_data,
                file_name=f"{st.session_state.current_dataset}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

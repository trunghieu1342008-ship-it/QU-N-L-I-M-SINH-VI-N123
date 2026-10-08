import streamlit as st
import pandas as pd
import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Quản lý Chi tiêu - Lê Minh Tuấn",
    page_icon="💰",
    layout="wide"
)

# Thông tin sinh viên & Tiêu đề
st.title("💰 Ứng Dụng Quản Lý Chi Tiêu Cá Nhân")
st.markdown("### Thông Tin Người Tạo")
st.write(f"- **Họ và tên:** Lê Minh Tuấn")
st.write(f"- **MSSV:** 051208004610")
st.markdown("---")

# Khởi tạo dữ liệu mẫu trong st.session_state để lưu trữ các khoản chi tiêu
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {"Ngày": "2026-06-01", "Khoản mục": "Ăn uống", "Số tiền (VNĐ)": 50000, "Ghi chú": "Bữa sáng & trưa"},
        {"Ngày": "2026-06-02", "Khoản mục": "Học tập", "Số tiền (VNĐ)": 150000, "Ghi chú": "Mua sách chuyên ngành"},
        {"Ngày": "2026-06-03", "Khoản mục": "Đi lại", "Số tiền (VNĐ)": 30000, "Ghi chú": "Đổ xăng xe máy"},
        {"Ngày": "2026-06-04", "Khoản mục": "Giải trí", "Số tiền (VNĐ)": 100000, "Ghi chú": "Đi cà phê cùng bạn"}
    ])

# Thanh bên (Sidebar) để thêm giao dịch mới
st.sidebar.header("➕ Thêm Khoản Chi Tiêu Mới")
with st.sidebar.form("expense_form"):
    date_val = st.date_input("Ngày giao dịch", datetime.date.today())
    category = st.selectbox("Khoản mục", ["Ăn uống", "Học tập", "Đi lại", "Giải trí", "Hóa đơn & Khác"])
    amount = st.number_input("Số tiền (VNĐ)", min_value=0, step=10000, value=50000)
    note = st.text_input("Ghi chú chi tiết")
    
    submit_btn = st.form_submit_button("Thêm khoản chi")
    
    if submit_btn:
        new_row = {
            "Ngày": str(date_val),
            "Khoản mục": category,
            "Số tiền (VNĐ)": amount,
            "Ghi chú": note
        }
        st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_row])], ignore_index=True)
        st.sidebar.success("Đã thêm khoản chi thành công!")

# Hiển thị tổng quan
total_spent = st.session_state.expenses["Số tiền (VNĐ)"].sum()
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Tổng số tiền đã chi", value=f"{total_spent:,.0f} VNĐ")
with col2:
    st.metric(label="Tổng số giao dịch", value=len(st.session_state.expenses))

st.markdown("---")

# Hiển thị bảng dữ liệu
st.subheader("📋 Danh Sách Các Khoản Chi Tiêu")
st.dataframe(st.session_state.expenses, use_container_width=True)

# Biểu đồ thống kê theo khoản mục
st.subheader("📊 Thống Kê Chi Tiêu Theo Khoản Mục")
if not st.session_state.expenses.empty:
    chart_data = st.session_state.expenses.groupby("Khoản mục")["Số tiền (VNĐ)"].sum()
    st.bar_chart(chart_data)
else:
    st.info("Chưa có dữ liệu để hiển thị biểu đồ.")

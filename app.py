import streamlit as st
import pandas as pd
from datetime import datetime
st.image("TRASUA.jpg")
# ---------------------------------------------------------
# CẤU HÌNH TRANG & CƠ SỞ DỮ LIỆU SẢN PHẨM
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hệ Thống Tính Tiền Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# Danh sách menu & giá (VND)
MENU_TEA = {
    "Trà Sữa Truyền Thống": 30000,
    "Trà Sữa Trân Châu Đường Đen": 35000,
    "Trà Sữa Thái Xanh": 32000,
    "Trà Sữa Ô Long": 35000,
    "Trà Sữa Matcha": 38000,
    "Trà Sữa Dâu Tây": 35000,
    "Trà Đào Cam Sả": 35000,
    "Trà Dâu Tằm": 32000,
}

SIZE_OPTIONS = {
    "S (Vừa)": 0,
    "M (Lớn)": 5000,
    "L (Đặc biệt)": 10000
}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}

SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đường)"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đá)"]

# Khởi tạo session state lưu trữ giỏ hàng và trạng thái hóa đơn
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False

# ---------------------------------------------------------
# HÀM XUẤT HÓA ĐƠN DẠNG TEXT (.TXT)
# ---------------------------------------------------------
def create_txt_invoice(customer_name, cart, total_amount, discount, final_amount):
    """Tạo file hóa đơn dạng văn bản (TXT)"""
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    content = f"{'='*40}\n"
    content += f"{'HÓA ĐƠN BÁN HÀNG - BOBA TEA':^40}\n"
    content += f"{'='*40}\n"
    content += f"Ngày: {now}\n"
    content += f"Khách hàng: {customer_name if customer_name else 'Khách vãng lai'}\n"
    content += f"{'-'*40}\n"
    
    for idx, item in enumerate(cart, 1):
        content += f"{idx}. {item['Tên món']} ({item['Size']})\n"
        content += f"   - Đường: {item['Đường']} | Đá: {item['Đá']}\n"
        if item['Topping'] != "Không":
            content += f"   - Topping: {item['Topping']}\n"
        content += f"   SL: {item['Số lượng']} x {item['Đơn giá']:,} = {item['Thành tiền']:,} VNĐ\n"
        
    content += f"{'-'*40}\n"
    content += f"Tổng tiền món: {total_amount:,} VNĐ\n"
    content += f"Giảm giá: {discount}%\n"
    content += f"TỔNG THANH TOÁN: {final_amount:,} VNĐ\n"
    content += f"{'='*40}\n"
    content += f"{'Cảm ơn quý khách và hẹn gặp lại!':^40}\n"
    return content

# ---------------------------------------------------------
# GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("TIỆM TRÀ SỮA NIE")
st.markdown("---")

col_left, col_right = st.columns([1.1, 0.9])

# ==================== CỘT TRÁI: NHẬP THÔNG TIN ====================
with col_left:
    st.subheader("📝 Thông tin đơn hàng")
    
    # 1. Thông tin khách hàng
    customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách hàng...")
    
    st.markdown("#### Chọn món nước & Tùy chọn")
    
    # 2. Chọn trà sữa & số lượng
    col_item, col_qty = st.columns([3, 1])
    with col_item:
        selected_tea = st.selectbox("Loại trà sữa:", list(MENU_TEA.keys()))
    with col_qty:
        quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)

# Ảnh tương ứng với từng món nước
TEA_IMAGES = {
    "Trà Sữa Truyền Thống": "truyen_thong.jpg",
    "Trà Sữa Trân Châu Đường Đen": "tran_chau_duong_den.jpg",
    "Trà Sữa Thái Xanh": "thai_xanh.jpg",
    "Trà Sữa Ô Long": "o_long.jpg",
    "Trà Sữa Matcha": "matcha.jpg",
    "Trà Sữa Dâu Tây": "dau_tay.jpg",
    "Trà Đào Cam Sả": "dao_cam_sa.jpg",
    "Trà Dâu Tằm": "dau_tam.jpg",
}

# Hiển thị ảnh món nước đang được chọn
image_path = TEA_IMAGES.get(selected_tea)

if image_path:
    st.image(
        image_path,
        caption=selected_tea,
        width=300
    )

    # 3. Size, Đường, Đá
    c_size, c_sugar, c_ice = st.columns(3)
    with c_size:
        selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
    with c_sugar:
        selected_sugar = st.selectbox("Mức đường:", SUGAR_LEVELS)
    with c_ice:
        selected_ice = st.selectbox("Mức đá:", ICE_LEVELS)

    # 4. Chọn topping
    selected_toppings = st.multiselect(
        "Loại Topping (có thể chọn nhiều):",
        options=list(TOPPING_OPTIONS.keys())
    )

# ================= VÒNG QUAY MAY MẮN =================
import random
import streamlit.components.v1 as components

st.markdown("---")
st.subheader("🎡 VÒNG QUAY MAY MẮN")
st.write("Quay thưởng để nhận ưu đãi cho đơn trà sữa của bạn!")

# Các phần thưởng
PRIZES = [
    {"name": "Giảm 5%", "discount": 5, "color": "#FF7777"},
    {"name": "Free Topping", "discount": 0, "color": "#77D7F7"},
    {"name": "Tặng Bánh", "discount": 0, "color": "#B9F57A"},
    {"name": "Giảm 10%", "discount": 10, "color": "#FFD080"},
    {"name": "Giảm 15%", "discount": 15, "color": "#A6F5E8"},
    {"name": "Giảm 20%", "discount": 20, "color": "#B38AF5"},
]

if "wheel_prize" not in st.session_state:
    st.session_state.wheel_prize = None

if "wheel_discount" not in st.session_state:
    st.session_state.wheel_discount = 0

# Chọn phần thưởng khi bấm nút
if st.button("🎯 BẮT ĐẦU QUAY", type="primary",
             use_container_width=True):
    st.session_state.wheel_prize = random.choice(PRIZES)
    st.session_state.wheel_discount = 0

# Vẽ vòng quay bằng HTML/CSS

# ===== TẠO VÒNG QUAY CÓ ĐỦ CHỮ TRÊN 6 Ô =====

wheel_colors = [p["color"] for p in PRIZES]

segments = ", ".join(
    f"{color} {i * 60}deg {(i + 1) * 60}deg"
    for i, color in enumerate(wheel_colors)
)

# Tính góc dừng sao cho phần thưởng trúng nằm dưới mũi tên

# Tính góc dừng để phần thưởng trúng nằm chính giữa mũi tên
if st.session_state.wheel_prize:
    prize_index = PRIZES.index(st.session_state.wheel_prize)

    # Mỗi ô rộng 60 độ, tính từ đỉnh vòng quay theo chiều kim đồng hồ
    center_angle = prize_index * 60 + 30

    # Quay 5 vòng đầy đủ rồi căn chính giữa ô trúng thưởng
    stop_angle = 360 * 5 + (360 - center_angle) % 360
else:
    stop_angle = 0

# Tạo nhãn cho cả 6 ô, tự động đặt đúng vị trí
labels_html = ""

for i, prize in enumerate(PRIZES):
    middle_angle = i * 60 + 30

    labels_html += f"""
    <div style="
        position:absolute;
        left:50%;
        top:50%;
        width:0;
        height:0;
        transform:rotate({middle_angle}deg) translateY(-105px);
        z-index:2;
        pointer-events:none;
    ">
        <span style="
            position:absolute;
            left:0;
            top:0;
            transform:translate(-50%,-50%)
                      rotate(-{middle_angle}deg);
            font-size:13px;
            font-weight:bold;
            color:#222;
            white-space:nowrap;
            text-align:center;
        ">{prize['name']}</span>
    </div>
    """

wheel_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        padding: 12px 0;
        background: transparent;
        font-family: Arial, sans-serif;
    }}

    .wheel-container {{
        position: relative;
        width: min(82vw, 360px);
        aspect-ratio: 1;
        margin: 15px auto;
    }}

    .pointer {{
        position: absolute;
        top: -5px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 17px solid transparent;
        border-right: 17px solid transparent;
        border-top: 30px solid #e32626;
        z-index: 10;
    }}

    #wheel {{
        position: absolute;
        inset: 0;
        border: 8px solid white;
        border-radius: 50%;
        box-shadow: 0 3px 18px #aaa;
        background: conic-gradient({segments});
        overflow: hidden;
        transform: rotate(0deg);
    }}

    .center {{
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: white;
        border: 7px solid orange;
        z-index: 5;
    }}
</style>
</head>
<body>
    <div class="wheel-container">
        <div class="pointer"></div>

        <div id="wheel">
            {labels_html}
            <div class="center"></div>
        </div>
    </div>

    <script>
        const wheel = document.getElementById("wheel");
        const targetAngle = {stop_angle};

        wheel.animate(
            [
                {{ transform: "rotate(0deg)" }},
                {{ transform: "rotate(" + targetAngle + "deg)" }}
            ],
            {{
                duration: 4000,
                easing: "cubic-bezier(0.15, 0.75, 0.12, 1)",
                fill: "forwards"
            }}
        );
    </script>
</body>
</html>
"""

components.html(wheel_html, height=410, scrolling=False)

# Hiển thị kết quả
if st.session_state.wheel_prize:
    prize = st.session_state.wheel_prize

    st.success(f"🎉 Chúc mừng! Bạn nhận được: {prize['name']}")

    if prize["discount"] > 0:
        if st.button(
            f"🎁 Áp dụng giảm {prize['discount']}%",
            use_container_width=True
        ):
            st.session_state.wheel_discount = prize["discount"]
            st.success("Đã chọn mức giảm giá từ vòng quay!")
    else:
        st.info(
            "Bạn nhận được quà tặng. "
            "Nhân viên có thể xác nhận và áp dụng quà tại quầy."
        )

    # Tính giá tiền từng ly
    base_price = MENU_TEA[selected_tea]
    size_price = SIZE_OPTIONS[selected_size]
    topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity

    st.info(f"💡 Đơn giá 1 ly (đã gồm size & topping): **{unit_price:,} VNĐ**")

    # Nút thêm món vào giỏ
    if st.button("➕ Thêm vào hóa đơn", type="primary", use_container_width=True):
        topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
        item_data = {
            "Tên món": selected_tea,
            "Size": selected_size.split()[0], # Lấy ký tự S, M, L
            "Đường": selected_sugar.split()[0],
            "Đá": selected_ice.split()[0],
            "Topping": topping_str,
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        }
        st.session_state.cart.append(item_data)
        st.session_state.invoice_paid = False
        st.toast(f"Đã thêm **{quantity}x {selected_tea}** vào giỏ!", icon="✅")

# ==================== CỘT PHẢI: CHI TIẾT HÓA ĐƠN ====================
with col_right:
    st.subheader("🛒 Danh sách món đã gọi")

    if not st.session_state.cart:
        st.warning("Giỏ hàng hiện đang trống. Vui lòng chọn món ở cột bên trái.")
    else:
        # Hiển thị giỏ hàng bằng Bảng Pandas
        df_cart = pd.DataFrame(st.session_state.cart)
        
        # Format bảng hiển thị
        st.dataframe(
            df_cart[["Tên món", "Size", "Topping", "Số lượng", "Đơn giá", "Thành tiền"]],
            use_container_width=True,
            hide_index=True
        )

        # Nút xóa giỏ hàng
        if st.button("🗑️ Xóa tất cả món"):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()

        st.markdown("---")
        
        # Tính tổng tiền
        total_price = df_cart["Thành tiền"].sum()
        
        col_disc, col_pay = st.columns(2)
        with col_disc:
           discount = st.number_input(
    "Giảm giá tổng (%):",
    min_value=0,
    max_value=100,
    value=st.session_state.get("wheel_discount", 0),
    step=5,
    key="discount_input"
)
        
        final_price = int(total_price * (1 - discount / 100))

        st.markdown(f"### Tổng tiền: **{total_price:,} VNĐ**")
        if discount > 0:
            st.markdown(f"### Sau giảm giá ({discount}%): <span style='color:red'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

        # Nút Bấm Thanh Toán
        if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
            st.session_state.invoice_paid = True
            st.balloons()

# ---------------------------------------------------------
# XUẤT HÓA ĐƠN KHI ĐÃ THANH TOÁN
# ---------------------------------------------------------
if st.session_state.get("invoice_paid") and st.session_state.cart:
    st.markdown("---")
    st.success("🎉 Thanh toán thành công! Dưới đây là hóa đơn chi tiết:")

    # Hiển thị hóa đơn trực quan
    invoice_box = st.container(border=True)
    with invoice_box:
        st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🧋 HÓA ĐƠN BÁN HÀNG - TRA SUA NIE</h2>", unsafe_allow_html=True)
        st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'}")
        
        st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Đường", "Đá", "Topping", "Số lượng", "Thành tiền"]])
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Tổng tiền món:** {total_price:,} VNĐ")
            st.write(f"**Giảm giá:** {discount}%")
        with c2:
            st.markdown(f"### TỔNG CỦA BẠN: <span style='color:red'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

    # Chuẩn bị file tải về dạng TXT
    txt_data = create_txt_invoice(customer_name, st.session_state.cart, total_price, discount, final_price)
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Tải hóa đơn (.TXT)",
            data=txt_data,
            file_name=f"HoaDon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl2:
        if st.button("🔄 Tạo đơn hàng mới", use_container_width=True):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()

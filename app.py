import streamlit as st
import time

# 1. AI ka Data
products = [
    {"name": "HP Omen 15", "price": 169990, "gpu": "RTX 3060", "image": "https://images.unsplash.com/photo-1603302576837-37561b2e0533?q=80&w=800"},
    {"name": "Acer Predator Helios 300", "price": 149990, "gpu": "GTX 1660 Ti", "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?q=80&w=800"},
    {"name": "Lenovo Legion Y540", "price": 179990, "gpu": "RTX 2060", "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?q=80&w=800"},
]

# 2. Session State setup
if "cart" not in st.session_state:
    st.session_state.cart = []
if "show_cart" not in st.session_state:
    st.session_state.show_cart = False
    
import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI E-commerce Store", layout="wide")

# --- HEADER SECTION ---
st.title("AI E-commerce Store")
st.caption("Ask AI or shop from the products below")

# 1. INITIALIZE CART - This runs only once
if "cart" not in st.session_state:
    st.session_state.cart = []

# Show cart count in top-right corner
col1, col2 = st.columns([4, 1])
with col2:
    st.metric(label="Cart Items", value=len(st.session_state.cart))
    if st.button("View Cart", use_container_width=True):
        st.session_state.show_cart = True

st.divider() # Aesthetic divider line

# 2. LOAD PRODUCTS FROM JSON
@st.cache_data
def load_products():
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)

products = load_products()

# --- AI SEARCH BAR ---
st.markdown("### AI Search")
search_query = st.text_input("Type here: e.g. `RTX under 1.7 lakh` or `Acer`", placeholder="RTX, Acer, under 150000...")

# Filter logic
filtered_products = products
if search_query:
    query = search_query.lower()
    filtered_products = []
    
    for p in products:
        name_match = query in f"{p['brand']} {p['model']}".lower()
        specs_match = query in p["gpu"].lower()
        price_match = False
        
        if "under" in query:
            try:
                price_limit = int(''.join(filter(str.isdigit, query)))
                price_match = p["price"] < price_limit
            except:
                pass
        
        if name_match or specs_match or price_match:
            filtered_products.append(p)

if not filtered_products:
    st.warning("No products found. Try `RTX` or `Acer`.")

# 3. DISPLAY PRODUCTS AS AESTHETIC CARDS
if 'cart_count' not in st.session_state:
    st.session_state.cart_count = 0
st.metric("🛒 Cart Items", st.session_state.cart_count)
st.subheader("Featured Laptops")
cols = st.columns(3, gap="large") # Large gap between cards

for i, product in enumerate(filtered_products):
    with cols[i % 3]:
        with st.container(border=True): # Card with border
            #st.image(product["image"], width='stretch') # Fixed warning
            st.markdown(f"### {product['brand']} {product['model']}")
            st.markdown(f"**Price: ₹{product['price']}**")
            st.markdown(f"*{product['gpu']}, {product['ram']} RAM, {product['storage']} SSD*")

            # Add to Cart Button
            if st.button("🛒 Add to Cart", key=f"cart_{product['id']}", use_container_width=True):
                st.session_state.cart.append(product)
                st.session_state.cart_count = len(st.session_state.cart)
                st.toast(f"{product['brand']} {product['model']} added!")
                st.rerun()

st.divider()

# 4. VIEW CART SIDEBAR LOGIC
if st.session_state.get("show_cart", False):
    with st.sidebar:
        st.title("Your Cart")
        
        if not st.session_state.cart:
            st.write("Your cart is empty")
        else:
            total_price = 0
            for i, item in enumerate(st.session_state.cart):
                st.write(f"**{item['brand']} {item['model']}**")
                st.write(f"Price: ₹{item['price']}")
                total_price += item['price']
                if st.button("❌ Remove", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
                st.divider()
            
            st.subheader(f"Total: ₹{total_price}")
        
        if st.button("Proceed to Checkout"):
            st.session_state.checkout = True
            st.rerun()
# 5. CHECKOUT FORM
if st.session_state.get("checkout", False):
    st.title("Checkout")
    with st.form("checkout_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email") 
        address = st.text_area("Shipping Address")
        st.subheader(f"Total Amount: ₹{sum(item['price'] for item in st.session_state.cart)}")
        
        if st.form_submit_button("Place Order"):
            st.success(f"Order Placed Successfully! Thanks {name}")
            st.balloons()
            time.sleep(2)
            st.session_state.cart = []
            st.session_state.cart_count = 0
            st.session_state.checkout = False
            st.session_state.show_cart = False
            st.rerun()

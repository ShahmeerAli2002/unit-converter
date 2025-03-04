import streamlit as st
import plotly.express as px
from datetime import datetime
import time
import random
import plotly.graph_objects as go

def transform_value(value, source, target, group):
    transformations = {
        'Distance': {'meters': 1, 'kilometers': 0.001, 'miles': 0.000621371, 'yards': 1.09361, 'feet': 3.28084, 'inches': 39.3701},
        'Weight': {'grams': 1, 'kilograms': 0.001, 'pounds': 0.00220462, 'ounces': 0.035274, 'tons': 0.000001},
        'Temperature': {'Celsius': lambda x: x, 'Fahrenheit': lambda x: (x * 9/5) + 32, 'Kelvin': lambda x: x + 273.15},
        'Time': {'seconds': 1, 'minutes': 1/60, 'hours': 1/3600, 'days': 1/86400},
        'Speed': {'kph': 1, 'mph': 0.621371, 'mps': 0.277778, 'fps': 0.911344},
        'Data': {'bytes': 1, 'kilobytes': 0.001, 'megabytes': 1e-6, 'gigabytes': 1e-9},
    }
    
    units = transformations.get(group, {})
    if source in units and target in units:
        if callable(units[source]):
            base = units[source](value)
        else:
            base = value / units[source]
        
        if callable(units[target]):
            return units[target](base)
        return base * units[target]
    return None

st.set_page_config(page_title="Magic Unit Transformer", layout="wide")

# Add custom CSS for animations
st.markdown("""
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    .floating { animation: float 3s ease-in-out infinite; }
    </style>
    """, unsafe_allow_html=True)

st.title('🌟 Magic Unit Transformer')
st.markdown('<p class="floating">Transform your units with magical animations! ✨</p>', unsafe_allow_html=True)

categories = ['Distance', 'Weight', 'Temperature', 'Time', 'Speed', 'Data']
units_map = {
    'Distance': ['meters', 'kilometers', 'miles', 'yards', 'feet', 'inches'],
    'Weight': ['grams', 'kilograms', 'pounds', 'ounces', 'tons'],
    'Temperature': ['Celsius', 'Fahrenheit', 'Kelvin'],
    'Time': ['seconds', 'minutes', 'hours', 'days'],
    'Speed': ['kph', 'mph', 'mps', 'fps'],
    'Data': ['bytes', 'kilobytes', 'megabytes', 'gigabytes'],
}

with st.container():
    st.markdown("### 🎨 Choose Your Magic Category")
    category = st.selectbox('Select Category:', categories, key='category_select')

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🎭 Source")
    source_unit = st.selectbox('From:', units_map[category])
    value = st.number_input('Enter Value:', value=0.0, step=0.1)

with col2:
    st.markdown("### 🎪 Target")
    target_unit = st.selectbox('To:', units_map[category])

if st.button('✨ Transform!', key='transform_button'):
    with st.spinner('Casting magic spell...'):
        time.sleep(1)  # Add dramatic pause
        result = transform_value(value, source_unit, target_unit, category)
        
        if result is not None:
            st.balloons()
            st.success(f"🌈 Magic Result: {value} {source_unit} = {result:.4f} {target_unit}")
            
            # Animated visualization
            fig = go.Figure()
            
            fig.add_trace(go.Indicator(
                mode = "gauge+number",
                value = result,
                title = {'text': f"Transformation Result in {target_unit}"},
                gauge = {
                    'axis': {'range': [None, result * 2]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, result], 'color': "cyan"},
                    ],
                }
            ))
            
            fig.update_layout(
                template='plotly_dark',
                height=400,
                margin=dict(l=50, r=50, t=50, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Store in history with animation
            if 'magic_history' not in st.session_state:
                st.session_state.magic_history = []
            st.session_state.magic_history.append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'from_value': value,
                'from_unit': source_unit,
                'to_value': result,
                'to_unit': target_unit,
                'color': f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})"
            })

if 'magic_history' in st.session_state and st.session_state.magic_history:
    st.markdown("### 📚 Magical History")
    for item in reversed(st.session_state.magic_history[-5:]):
        st.markdown(
            f"""<div style='padding:10px; margin:5px; border-radius:10px; 
            background-color:{item['color']}; animation: float 3s ease-in-out infinite;'>
            ⏰ {item['time']}: {item['from_value']} {item['from_unit']} ➡️ 
            {item['to_value']:.4f} {item['to_unit']}</div>""", 
            unsafe_allow_html=True
        )
"""
MediFederate UI Helpers
Custom loading animations, toast notifications, animated counters, Plotly charts
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def inject_ui_css():
    """Inject CSS for animations and toasts"""
    st.markdown("""
    <style>
        /* ===== SMOOTH FADE-IN ===== */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in { animation: fadeInUp 0.6s ease-out; }
        
        /* ===== PULSE ===== */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        .pulse { animation: pulse 1.5s ease-in-out infinite; }
        
        /* ===== SHIMMER SKELETON ===== */
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        .skeleton {
            background: linear-gradient(90deg, rgba(102,126,234,0.08) 0%, rgba(102,126,234,0.18) 50%, rgba(102,126,234,0.08) 100%);
            background-size: 1000px 100%;
            animation: shimmer 1.8s infinite linear;
            border-radius: 8px;
            height: 20px;
            margin-bottom: 10px;
        }
        
        /* ===== COUNTER POP ===== */
        @keyframes countUp {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }
        .counter-pop { animation: countUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }
        
        /* ===== SPINNER ===== */
        .custom-spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid rgba(102, 126, 234, 0.2);
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .loading-box {
            background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 14px;
            padding: 25px;
            text-align: center;
            margin: 15px 0;
        }
        .loading-box p {
            color: #a0a0b0;
            margin-top: 15px;
            font-size: 0.95rem;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* ===== TOASTS ===== */
        @keyframes slideInRight {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .toast-success {
            position: fixed; top: 20px; right: 20px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white; padding: 16px 24px; border-radius: 12px;
            box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4);
            font-weight: 600; z-index: 99999;
            animation: slideInRight 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex; align-items: center; gap: 12px;
        }
        .toast-error {
            position: fixed; top: 20px; right: 20px;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white; padding: 16px 24px; border-radius: 12px;
            box-shadow: 0 8px 30px rgba(239, 68, 68, 0.4);
            font-weight: 600; z-index: 99999;
            animation: slideInRight 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex; align-items: center; gap: 12px;
        }
        .toast-info {
            position: fixed; top: 20px; right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 16px 24px; border-radius: 12px;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
            font-weight: 600; z-index: 99999;
            animation: slideInRight 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex; align-items: center; gap: 12px;
        }
        
        /* ===== RESULT REVEAL ===== */
        @keyframes resultReveal {
            0% { opacity: 0; transform: scale(0.9) translateY(20px); }
            60% { opacity: 1; transform: scale(1.02) translateY(-3px); }
            100% { opacity: 1; transform: scale(1) translateY(0); }
        }
        .result-reveal { animation: resultReveal 0.7s cubic-bezier(0.34, 1.56, 0.64, 1); }
        
        .stSpinner > div > div { border-top-color: #667eea !important; }
    </style>
    """, unsafe_allow_html=True)


def show_toast(message, toast_type="success", emoji="✅"):
    class_map = {"success": "toast-success", "error": "toast-error", "info": "toast-info"}
    css_class = class_map.get(toast_type, "toast-success")
    st.markdown(f"""
    <div class="{css_class}">
        <span style="font-size: 1.4rem;">{emoji}</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)


def show_loading(message="Processing...", subtext="AI model is analyzing data"):
    st.markdown(f"""
    <div class="loading-box">
        <div class="custom-spinner"></div>
        <p>{message}</p>
        <p style="font-size: 0.8rem; color: #667eea; margin-top: 5px;">{subtext}</p>
    </div>
    """, unsafe_allow_html=True)


def show_skeleton(lines=3):
    html = '<div style="padding: 15px 0;">'
    for i in range(lines):
        width = 100 - (i * 15)
        html += f'<div class="skeleton" style="width: {width}%;"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def animated_metric_card(emoji, label, value, subtitle="", pill_text="", pill_type="success"):
    pill_class = f"pill-{pill_type}"
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div style="font-size: 2rem;">{emoji}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value counter-pop">{value}</div>
        {'<div><span class="status-pill ' + pill_class + '">' + pill_text + '</span></div>' if pill_text else ''}
        {'<div style="color: #808090; font-size: 0.75rem; margin-top: 8px;">' + subtitle + '</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def prediction_loading_animation(disease_name):
    disease_emoji = {"Diabetes": "🩸", "Heart Disease": "❤️", "Stroke": "🧠", "Kidney Disease": "🫘"}
    emoji = disease_emoji.get(disease_name, "🔬")
    st.markdown(f"""
    <div class="loading-box fade-in">
        <div style="font-size: 3rem; margin-bottom: 10px;" class="pulse">{emoji}</div>
        <div class="custom-spinner"></div>
        <p>Analyzing {disease_name} risk...</p>
        <p style="font-size: 0.8rem; color: #667eea; margin-top: 5px;">
            Running Federated Learning model • Preserving privacy
        </p>
    </div>
    """, unsafe_allow_html=True)


def result_card_with_animation(is_high_risk, title, probability, description):
    box_class = "result-high" if is_high_risk else "result-low"
    emoji = "🔴" if is_high_risk else "🟢"
    st.markdown(f"""
    <div class="result-box {box_class} result-reveal">
        <div class="result-title">{emoji} {title}</div>
        <div class="result-prob counter-pop">{probability:.1f}%</div>
        <div class="result-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


# ========================================
# PLOTLY CHART HELPERS
# ========================================

def plotly_model_comparison(df):
    """Interactive horizontal bar chart for model comparison"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Accuracy (%)'],
        y=df['Disease'],
        orientation='h',
        marker=dict(
            color=df['Accuracy (%)'],
            colorscale=[[0, '#764ba2'], [0.5, '#667eea'], [1, '#10b981']],
            line=dict(color='rgba(255,255,255,0.2)', width=1),
        ),
        text=[f'{x:.2f}%' for x in df['Accuracy (%)']],
        textposition='outside',
        textfont=dict(color='white', size=14, family='Inter'),
        hovertemplate='<b>%{y}</b><br>Accuracy: %{x:.2f}%<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30,30,46,0.4)',
        font=dict(color='#e0e0e0', family='Inter'),
        xaxis=dict(
            title='Accuracy (%)',
            gridcolor='rgba(102,126,234,0.15)',
            range=[0, 110],
            tickfont=dict(color='#a0a0b0'),
            title_font=dict(color='#a0a0b0'),
        ),
        yaxis=dict(
            tickfont=dict(color='#ffffff', size=12),
            gridcolor='rgba(0,0,0,0)',
        ),
        height=320,
        margin=dict(l=10, r=40, t=20, b=40),
        showlegend=False,
        hoverlabel=dict(bgcolor='#667eea', font_size=13, font_family='Inter', font_color='white'),
    )
    return fig


def plotly_disease_donut(df, title="Disease Distribution"):
    """Interactive donut chart for disease distribution"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data yet", xref="paper", yref="paper",
            showarrow=False, font=dict(color='#808090', size=14),
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=280, margin=dict(l=10, r=10, t=30, b=10),
        )
        return fig
    
    colors = ['#667eea', '#764ba2', '#10b981', '#f59e0b', '#ef4444']
    fig = go.Figure(data=[go.Pie(
        labels=df['disease'],
        values=df['count'],
        hole=0.55,
        marker=dict(colors=colors[:len(df)]),
        textinfo='label+percent',
        textfont=dict(size=12, color='white', family='Inter'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
    )])
    
    total = df['count'].sum()
    fig.add_annotation(
        text=f"<b>{total}</b><br><span style='font-size:0.8em;color:#a0a0b0;'>Total</span>",
        x=0.5, y=0.5,
        font=dict(size=20, color='#ffffff', family='Inter'),
        showarrow=False,
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', family='Inter'),
        height=280,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False,
        title=dict(text=title, font=dict(color='#ffffff', size=14)),
        hoverlabel=dict(bgcolor='#667eea', font_size=13, font_family='Inter', font_color='white'),
    )
    return fig


def plotly_risk_bars(df, title="Risk Distribution"):
    """Interactive bar chart for risk distribution"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data yet", xref="paper", yref="paper",
            showarrow=False, font=dict(color='#808090', size=14),
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=280, margin=dict(l=10, r=10, t=30, b=10),
        )
        return fig
    
    color_map = {'High Risk': '#ef4444', 'Low Risk': '#10b981'}
    colors = [color_map.get(x, '#667eea') for x in df['risk_level']]
    
    fig = go.Figure(data=[go.Bar(
        x=df['risk_level'],
        y=df['count'],
        marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.2)', width=1)),
        text=df['count'],
        textposition='outside',
        textfont=dict(color='white', size=14, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30,30,46,0.4)',
        font=dict(color='#e0e0e0', family='Inter'),
        xaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#ffffff', size=13)),
        yaxis=dict(gridcolor='rgba(102,126,234,0.15)', tickfont=dict(color='#a0a0b0')),
        height=280,
        margin=dict(l=10, r=40, t=30, b=40),
        showlegend=False,
        title=dict(text=title, font=dict(color='#ffffff', size=14)),
        hoverlabel=dict(bgcolor='#667eea', font_size=13, font_family='Inter', font_color='white'),
    )
    return fig


def plotly_accuracy_gauge(value, label="Accuracy", max_value=100):
    """Interactive gauge chart for single accuracy value"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label, 'font': {'color': '#ffffff', 'size': 14, 'family': 'Inter'}},
        number={'font': {'color': '#ffffff', 'size': 30, 'family': 'Inter'}, 'suffix': '%'},
        gauge={
            'axis': {'range': [None, max_value], 'tickcolor': '#a0a0b0', 'tickfont': {'color': '#a0a0b0'}},
            'bar': {'color': '#667eea'},
            'bgcolor': 'rgba(30,30,46,0.4)',
            'borderwidth': 2,
            'bordercolor': 'rgba(102,126,234,0.3)',
            'steps': [
                {'range': [0, 60], 'color': 'rgba(239,68,68,0.15)'},
                {'range': [60, 80], 'color': 'rgba(245,158,11,0.15)'},
                {'range': [80, 100], 'color': 'rgba(16,185,129,0.15)'},
            ],
            'threshold': {'line': {'color': '#10b981', 'width': 4}, 'thickness': 0.75, 'value': value},
        },
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=250,
        margin=dict(l=20, r=20, t=40, b=10),
        font=dict(family='Inter'),
    )
    return fig
"""
MediFederate Settings & Account Page
Profile, account details, security, and preferences
"""

import streamlit as st
from datetime import datetime
import auth
import history_db as hist


def inject_settings_css():
    """CSS for settings page"""
    st.markdown("""
    <style>
        .profile-card {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid rgba(102, 126, 234, 0.25);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .profile-avatar { font-size: 4rem; margin-bottom: 12px; line-height: 1; }
        .profile-name { font-size: 1.3rem; font-weight: 800; color: #ffffff; margin-bottom: 4px; }
        
        .profile-role {
            display: inline-block;
            background: rgba(102, 126, 234, 0.2);
            color: #667eea;
            padding: 4px 14px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 6px;
        }
        
        .profile-email { color: #a0a0b0; font-size: 0.85rem; margin-top: 10px; }
        
        .setting-section {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 14px;
            padding: 20px 22px;
            margin-bottom: 16px;
        }
        
        .setting-section-title {
            font-size: 1rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(102, 126, 234, 0.25);
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px dashed rgba(102, 126, 234, 0.15);
        }
        
        .info-row:last-child { border-bottom: none; }
        .info-label { color: #a0a0b0; font-size: 0.85rem; font-weight: 500; }
        .info-value { color: #ffffff; font-size: 0.9rem; font-weight: 600; text-align: right; }
        
        .stat-mini-card {
            background: rgba(102, 126, 234, 0.08);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 14px;
            text-align: center;
        }
        
        .stat-mini-value {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-mini-label {
            font-size: 0.7rem;
            color: #a0a0b0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        
        .warning-box {
            background: rgba(245, 158, 11, 0.1);
            border-left: 4px solid #f59e0b;
            border-radius: 10px;
            padding: 14px 18px;
            color: #fcd34d;
            font-size: 0.85rem;
            line-height: 1.6;
            margin-top: 12px;
        }
        
        .danger-box {
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
            border-radius: 10px;
            padding: 14px 18px;
            color: #fca5a5;
            font-size: 0.85rem;
            line-height: 1.6;
            margin-top: 12px;
        }
    </style>
    """, unsafe_allow_html=True)


def _render_profile_tab(current_user, is_patient, user_email):
    """Profile tab content"""
    avatar = "👤" if is_patient else "👨‍⚕️"
    role_display = "Patient (Guest)" if is_patient else "Doctor"
    
    html = '<div class="profile-card">'
    html += '<div class="profile-avatar">' + avatar + '</div>'
    html += '<div class="profile-name">' + current_user.get('full_name', 'User') + '</div>'
    html += '<div class="profile-role">' + role_display + '</div>'
    html += '<div class="profile-email">📧 ' + user_email + '</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    
    if not is_patient:
        try:
            all_users = auth.get_all_users()
            user_row = None
            for u in all_users:
                if u[2] == user_email:
                    user_row = u
                    break
            if user_row:
                created = user_row[5] if len(user_row) > 5 else "N/A"
                last_login = user_row[6] if len(user_row) > 6 and user_row[6] else "First login"
            else:
                created = "N/A"
                last_login = "N/A"
        except Exception:
            created = "N/A"
            last_login = "N/A"
        
        html = '<div class="setting-section">'
        html += '<div class="setting-section-title">👤 Account Information</div>'
        html += '<div class="info-row"><span class="info-label">Full Name</span><span class="info-value">' + current_user.get('full_name', 'N/A') + '</span></div>'
        html += '<div class="info-row"><span class="info-label">Email</span><span class="info-value">' + user_email + '</span></div>'
        html += '<div class="info-row"><span class="info-label">Role</span><span class="info-value">' + role_display + '</span></div>'
        html += '<div class="info-row"><span class="info-label">Hospital</span><span class="info-value">' + current_user.get('hospital', 'N/A') + '</span></div>'
        html += '<div class="info-row"><span class="info-label">Account Created</span><span class="info-value">' + created + '</span></div>'
        html += '<div class="info-row"><span class="info-label">Last Login</span><span class="info-value">' + last_login + '</span></div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    else:
        html = '<div class="setting-section">'
        html += '<div class="setting-section-title">👤 Guest Information</div>'
        html += '<div class="info-row"><span class="info-label">Status</span><span class="info-value">Patient (Guest)</span></div>'
        html += '<div class="info-row"><span class="info-label">Email</span><span class="info-value">' + user_email + '</span></div>'
        html += '<div class="info-row"><span class="info-label">Account Type</span><span class="info-value">Guest Access</span></div>'
        html += '</div>'
        html += '<div class="warning-box"><strong>👤 Guest Mode:</strong> You are currently using MediFederate as a guest. To create a permanent account, please logout and register as a doctor.</div>'
        st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("##### 🚪 Session")
    st.caption("Click the button below to logout of your account")
    
    if st.button("🚪  Logout", use_container_width=True, key="settings_logout_btn"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.show_chat_page = False
        st.session_state.show_settings_page = False
        st.session_state.welcome_toast_shown = False
        st.rerun()


def _render_security_tab(current_user, is_patient, user_email):
    """Security tab content"""
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">🔐 Change Password</div>
    """, unsafe_allow_html=True)
    
    if is_patient:
        st.info("👤 Guest users do not have a password. Please logout to create an account.")
    else:
        with st.form("change_password_form"):
            current_password = st.text_input("Current Password", type="password", key="cp_current")
            new_password = st.text_input("New Password", type="password", key="cp_new")
            confirm_password = st.text_input("Confirm New Password", type="password", key="cp_confirm")
            
            submit = st.form_submit_button("🔐  Update Password", type="primary", use_container_width=True)
            
            if submit:
                if not current_password or not new_password or not confirm_password:
                    st.error("⚠️ Please fill all fields.")
                elif new_password != confirm_password:
                    st.error("⚠️ New passwords do not match.")
                elif len(new_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters.")
                else:
                    success, msg, _ = auth.login(user_email, current_password)
                    if not success:
                        st.error("❌ Current password is incorrect.")
                    else:
                        success2, msg2 = auth.reset_password(user_email, new_password)
                        if success2:
                            st.success("✅ Password updated successfully!")
                        else:
                            st.error("❌ " + msg2)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">🖥️ Session Information</div>
        <div class="info-row"><span class="info-label">Current Session</span><span class="info-value" style="color: #10b981;">● Active</span></div>
        <div class="info-row"><span class="info-label">Login Time</span><span class="info-value">Just now</span></div>
        <div class="info-row"><span class="info-label">Browser</span><span class="info-value">Active</span></div>
    </div>
    """, unsafe_allow_html=True)


def _render_preferences_tab():
    """Preferences tab content"""
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">🎨 Display Preferences</div>
    """, unsafe_allow_html=True)
    
    theme = st.selectbox("Theme", ["Dark (Default)", "Light"], key="pref_theme")
    language = st.selectbox("Preferred Language", ["English"], index=0, key="pref_lang")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">🔔 Notifications</div>
    """, unsafe_allow_html=True)
    
    st.checkbox("High-risk prediction alerts", value=True, key="pref_notif1")
    st.checkbox("Weekly health summary", value=False, key="pref_notif2")
    st.checkbox("New feature announcements", value=True, key="pref_notif3")
    st.checkbox("Emergency health tips", value=True, key="pref_notif4")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">📊 Data & Privacy</div>
    """, unsafe_allow_html=True)
    
    st.checkbox("Auto-save my predictions", value=True, key="pref_autosave")
    st.checkbox("Share anonymous usage statistics", value=True, key="pref_share")
    
    st.markdown("""
    <div class="warning-box">
        <strong>🔒 Privacy Note:</strong> MediFederate uses Federated Learning 
        and Differential Privacy. Patient data is never shared.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("💾  Save Preferences", type="primary", use_container_width=True, key="save_pref_btn"):
        st.success("✅ Preferences saved! (Demo)")


def _render_activity_tab(user_email):
    """Activity tab content"""
    try:
        stats = hist.get_statistics(user_email=user_email)
    except Exception:
        stats = {'total': 0, 'high_risk': 0, 'low_risk': 0}
    
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">📊 Your Activity Summary</div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            '<div class="stat-mini-card">'
            '<div class="stat-mini-value">' + str(stats['total']) + '</div>'
            '<div class="stat-mini-label">Predictions</div>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            '<div class="stat-mini-card">'
            '<div class="stat-mini-value" style="background: linear-gradient(135deg, #ef4444, #dc2626); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">'
            + str(stats['high_risk']) +
            '</div>'
            '<div class="stat-mini-label">High Risk</div>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            '<div class="stat-mini-card">'
            '<div class="stat-mini-value" style="background: linear-gradient(135deg, #10b981, #059669); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">'
            + str(stats['low_risk']) +
            '</div>'
            '<div class="stat-mini-label">Low Risk</div>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            '<div class="stat-mini-card">'
            '<div class="stat-mini-value">4</div>'
            '<div class="stat-mini-label">Diseases</div>'
            '</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">🕐 Recent Predictions</div>
    """, unsafe_allow_html=True)
    
    try:
        recent = hist.get_user_predictions(user_email, limit=5)
        if not recent.empty:
            for _, row in recent.iterrows():
                prob = row['probability'] * 100 if row['probability'] <= 1 else row['probability']
                html = '<div class="info-row">'
                html += '<span class="info-label">' + str(row['disease']) + ' · ' + str(row['timestamp']) + '</span>'
                html += '<span class="info-value">' + str(row['risk_level']) + ' (' + f'{prob:.1f}' + '%)</span>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("📭 No predictions yet.")
    except Exception:
        st.info("📭 No activity data available.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="setting-section">
        <div class="setting-section-title">⚠️ Danger Zone</div>
        <div class="danger-box">
            <strong>Delete Account:</strong> You can permanently delete your account. 
            This action cannot be undone.
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_settings_content():
    """Shared content — used by both dialog and full-page"""
    current_user = st.session_state.get('user', {})
    is_patient = current_user.get('role') == 'patient'
    user_email = current_user.get('email', 'guest@medifederate')
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Profile",
        "🔐 Security",
        "🎨 Preferences",
        "📊 Activity"
    ])
    
    with tab1:
        _render_profile_tab(current_user, is_patient, user_email)
    
    with tab2:
        _render_security_tab(current_user, is_patient, user_email)
    
    with tab3:
        _render_preferences_tab()
    
    with tab4:
        _render_activity_tab(user_email)


@st.dialog("⚙️ Settings & Account", width="large")
def show_settings_dialog():
    """Render settings as a popup dialog"""
    inject_settings_css()
    _render_settings_content()


def render_settings_page():
    """Render settings as full page (legacy support)"""
    inject_settings_css()
    
    if st.button("🏠  Back to Dashboard", use_container_width=False, key="back_from_settings"):
        st.session_state.show_settings_page = False
        st.rerun()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 30px 35px; border-radius: 16px; color: white; margin-bottom: 25px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
        <div style="font-size: 1.8rem; font-weight: 800; margin: 0;">⚙️ Settings & Account</div>
        <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 6px;">Manage your profile, security, and preferences</div>
    </div>
    """, unsafe_allow_html=True)
    
    _render_settings_content()
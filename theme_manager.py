import streamlit as st
from typing import Dict, Any

class ThemeManager:
    def __init__(self):
        pass
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get modern light color palette"""
        return {
            'background': '#FFFFFF',
            'foreground': '#1F2937',
            'card': '#F8FAFC',
            'card_foreground': '#1F2937',
            'popover': '#FFFFFF',
            'popover_foreground': '#1F2937',
            'primary': '#3B82F6',
            'primary_foreground': '#FFFFFF',
            'secondary': '#F1F5F9',
            'secondary_foreground': '#475569',
            'muted': '#F8FAFC',
            'muted_foreground': '#64748B',
            'accent': '#6366F1',
            'accent_foreground': '#FFFFFF',
            'destructive': '#EF4444',
            'destructive_foreground': '#FFFFFF',
            'border': '#E2E8F0',
            'input': '#FFFFFF',
            'ring': '#3B82F6',
            'chart_1': '#3B82F6',
            'chart_2': '#10B981',
            'chart_3': '#F59E0B',
            'chart_4': '#8B5CF6',
            'chart_5': '#EF4444',
            'success': '#10B981',
            'warning': '#F59E0B',
            'info': '#3B82F6',
        }
    
    def get_modern_css(self) -> str:
        """Generate modern light CSS with clean design and centered layout"""
        colors = self.get_theme_colors()
        
        return f"""
        :root {{
            --background: {colors['background']};
            --foreground: {colors['foreground']};
            --card: {colors['card']};
            --card-foreground: {colors['card_foreground']};
            --popover: {colors['popover']};
            --popover-foreground: {colors['popover_foreground']};
            --primary: {colors['primary']};
            --primary-foreground: {colors['primary_foreground']};
            --secondary: {colors['secondary']};
            --secondary-foreground: {colors['secondary_foreground']};
            --muted: {colors['muted']};
            --muted-foreground: {colors['muted_foreground']};
            --accent: {colors['accent']};
            --accent-foreground: {colors['accent_foreground']};
            --destructive: {colors['destructive']};
            --destructive-foreground: {colors['destructive_foreground']};
            --border: {colors['border']};
            --input: {colors['input']};
            --ring: {colors['ring']};
            --chart-1: {colors['chart_1']};
            --chart-2: {colors['chart_2']};
            --chart-3: {colors['chart_3']};
            --chart-4: {colors['chart_4']};
            --chart-5: {colors['chart_5']};
            --success: {colors['success']};
            --warning: {colors['warning']};
            --info: {colors['info']};
            --radius: 1rem;
        }}

        /* Global Styles */
        .stApp {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
            color: var(--foreground);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
        }}

        /* Centered Layout Container */
        .centered-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .compact-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .auth-container {{
            max-width: 400px;
            margin: 0 auto;
            padding: 0 1rem;
        }}

        /* Modern Header */
        .modern-header {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            position: relative;
            overflow: hidden;
        }}

        .modern-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        }}

        .modern-header h1 {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.5rem;
            font-weight: 800;
            margin: 0 0 1rem 0;
            line-height: 1.1;
            letter-spacing: -0.025em;
        }}

        .modern-header p {{
            color: var(--muted-foreground);
            font-size: 1.25rem;
            margin: 0;
            font-weight: 500;
        }}

        .modern-tagline {{
            color: var(--accent);
            font-size: 1rem;
            font-weight: 600;
            margin-top: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Feature Grid */
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }}

        .feature-card {{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            position: relative;
            overflow: hidden;
        }}

        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}

        .feature-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-color: var(--primary);
        }}

        .feature-card:hover::before {{
            transform: scaleX(1);
        }}

        .feature-icon {{
            font-size: 3.5rem;
            margin-bottom: 1.5rem;
            display: block;
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
        }}

        .feature-title {{
            color: var(--foreground);
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            line-height: 1.3;
        }}

        .feature-description {{
            color: var(--muted-foreground);
            font-size: 1rem;
            line-height: 1.6;
            font-weight: 400;
        }}

        /* Modern Cards */
        .modern-card {{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            position: relative;
            overflow: hidden;
        }}

        .modern-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        }}

        .modern-card h3 {{
            color: var(--foreground);
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            line-height: 1.3;
        }}

        .modern-card p {{
            color: var(--muted-foreground);
            margin: 0;
            line-height: 1.6;
            font-size: 1rem;
        }}

        /* Compact Auth Cards */
        .auth-card {{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 2rem;
            margin: 2rem auto;
            max-width: 400px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            position: relative;
            overflow: hidden;
        }}

        .auth-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        }}

        .auth-card h2 {{
            color: var(--foreground);
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            text-align: center;
            line-height: 1.3;
        }}

        .auth-card p {{
            color: var(--muted-foreground);
            margin: 0 0 1rem 0;
            text-align: center;
            line-height: 1.6;
            font-size: 0.9rem;
        }}

        /* Auth form styling */
        .auth-card .stForm {{
            margin: 0;
        }}

        .auth-card .stTextInput {{
            margin-bottom: 1rem;
        }}

        .auth-card .stButton {{
            margin-top: 1rem;
        }}

        /* Tabs styling */
        .stTabs > div > div {{
            background: transparent;
            border: none;
            padding: 0;
            margin: 0 0 1.5rem 0;
        }}

        .stTabs > div > div > div {{
            background: var(--muted);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            margin: 0 0.25rem;
            color: var(--muted-foreground);
            font-size: 0.875rem;
            font-weight: 500;
        }}

        .stTabs > div > div > div[aria-selected="true"] {{
            background: var(--primary);
            color: var(--primary-foreground);
            border-color: var(--primary);
        }}



        /* Forgot password link */
        .forgot-password-link {{
            color: var(--accent);
            text-decoration: none;
            font-size: 0.875rem;
        }}

        /* Password requirements box */
        .password-requirements {{
            background: var(--muted);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid var(--border);
        }}

        .password-requirements h4 {{
            margin: 0 0 0.5rem 0;
            font-size: 0.875rem;
            color: var(--foreground);
            font-weight: 600;
        }}

        .password-requirements ul {{
            margin: 0;
            padding-left: 1rem;
            font-size: 0.8rem;
            color: var(--muted-foreground);
        }}

        .password-requirements li {{
            margin-bottom: 0.25rem;
        }}

        /* Status Cards */
        .status-card {{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin: 1.5rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }}

        .status-card.success {{
            border-left: 4px solid var(--success);
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, #FFFFFF 100%);
        }}

        .status-card.warning {{
            border-left: 4px solid var(--warning);
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, #FFFFFF 100%);
        }}

        .status-card.error {{
            border-left: 4px solid var(--destructive);
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, #FFFFFF 100%);
        }}

        .status-card.info {{
            border-left: 4px solid var(--info);
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, #FFFFFF 100%);
        }}

        /* Buttons */
        .modern-btn {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: var(--primary-foreground);
            border: none;
            border-radius: var(--radius);
            padding: 1rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}

        .modern-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }}

        .modern-btn.secondary {{
            background: var(--secondary);
            color: var(--secondary-foreground);
            border: 1px solid var(--border);
        }}

        /* Progress Bars */
        .modern-progress {{
            background: var(--muted);
            border-radius: var(--radius);
            height: 0.75rem;
            overflow: hidden;
        }}

        .modern-progress-bar {{
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
            height: 100%;
            border-radius: var(--radius);
            transition: width 0.3s ease;
        }}

        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .fade-in {{
            animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes slideIn {{
            from {{ transform: translateX(-100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}

        .slide-in {{
            animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .modern-header h1 {{
                font-size: 2.5rem;
            }}
            
            .feature-grid {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}
            
            .modern-card {{
                padding: 1.5rem;
            }}
            
            .feature-card {{
                padding: 1.5rem;
            }}

            .auth-card {{
                padding: 2rem;
                margin: 1rem;
            }}

            .centered-container,
            .compact-container {{
                padding: 0 1rem;
            }}
        }}

        /* Streamlit Component Overrides */
        .stButton > button {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: var(--primary-foreground);
            border: none;
            border-radius: var(--radius);
            padding: 1rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }}

        .stTextInput > div > div > input {{
            background: var(--input);
            border: 2px solid var(--border);
            border-radius: var(--radius);
            color: var(--foreground);
            padding: 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}

        .stTextInput > div > div > input:focus {{
            border-color: var(--ring);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            outline: none;
        }}

        .stFileUploader > div {{
            background: var(--card);
            border: 2px dashed var(--border);
            border-radius: var(--radius);
            padding: 3rem 2rem;
            text-align: center;
        }}

        /* Sidebar Styling */
        .css-1d391kg {{
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
            border-right: 1px solid var(--border);
        }}

        /* Main Content Area - Centered Layout */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--muted);
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--primary);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent);
        }}

        /* Success/Error Messages */
        .stSuccess {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, #FFFFFF 100%);
            border: 1px solid var(--success);
            border-radius: var(--radius);
            color: var(--success);
        }}

        .stError {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, #FFFFFF 100%);
            border: 1px solid var(--destructive);
            border-radius: var(--radius);
            color: var(--destructive);
        }}

        /* Spinner */
        .stSpinner {{
            border-color: var(--primary) !important;
        }}

        /* Progress */
        .stProgress > div > div {{
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        }}

        .stProgress > div {{
            background: var(--muted);
        }}
        """
    
    def apply_theme(self):
        """Apply the modern light theme to Streamlit"""
        css = self.get_modern_css()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Global theme manager instance
theme_manager = ThemeManager()

def apply_modern_theme():
    """Apply the modern light theme"""
    theme_manager.apply_theme() 
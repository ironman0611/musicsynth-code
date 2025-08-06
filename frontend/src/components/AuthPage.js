import React, { useState } from 'react';

const AuthPage = ({ supabase }) => {
  const [activeTab, setActiveTab] = useState('login');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  // Form states
  const [loginData, setLoginData] = useState({
    email: '',
    password: ''
  });

  const [registerData, setRegisterData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [resetEmail, setResetEmail] = useState('');

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => {
      setMessage('');
      setMessageType('');
    }, 5000);
  };

  const isValidEmail = (email) => {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
  };

  const isValidPassword = (password) => {
    if (password.length < 8) return false;
    if (!/[A-Z]/.test(password)) return false;
    if (!/[a-z]/.test(password)) return false;
    if (!/\d/.test(password)) return false;
    return true;
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!loginData.email || !loginData.password) {
      showMessage('Please fill in all fields', 'error');
      return;
    }

    if (!isValidEmail(loginData.email)) {
      showMessage('Invalid email format', 'error');
      return;
    }

    setLoading(true);
    
    try {
      const { error } = await supabase.auth.signInWithPassword({
        email: loginData.email,
        password: loginData.password
      });

      if (error) {
        if (error.message.includes('invalid_credentials') || 
            error.message.includes('Invalid login credentials')) {
          showMessage('Invalid email or password. Please try again.', 'error');
        } else {
          showMessage(`Login failed: ${error.message}`, 'error');
        }
      } else {
        showMessage('Login successful!', 'success');
      }
    } catch (error) {
      showMessage(`Login failed: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    
    if (!registerData.email || !registerData.password || !registerData.confirmPassword) {
      showMessage('Please fill in all fields', 'error');
      return;
    }

    if (!isValidEmail(registerData.email)) {
      showMessage('Invalid email format', 'error');
      return;
    }

    if (!isValidPassword(registerData.password)) {
      showMessage('Password must be at least 8 characters long and contain uppercase, lowercase, and digit', 'error');
      return;
    }

    if (registerData.password !== registerData.confirmPassword) {
      showMessage('Passwords do not match', 'error');
      return;
    }

    setLoading(true);
    
    try {
      const { error } = await supabase.auth.signUp({
        email: registerData.email,
        password: registerData.password
      });

      if (error) {
        if (error.message.includes('already_registered') || 
            error.message.includes('already been registered')) {
          showMessage('Email already registered. Please use a different email or try logging in.', 'error');
        } else {
          showMessage(`Registration failed: ${error.message}`, 'error');
        }
      } else {
        showMessage('Registration successful! Please check your email for verification.', 'success');
        setRegisterData({ email: '', password: '', confirmPassword: '' });
      }
    } catch (error) {
      showMessage(`Registration failed: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordReset = async (e) => {
    e.preventDefault();
    
    if (!resetEmail) {
      showMessage('Please enter your email address', 'error');
      return;
    }

    if (!isValidEmail(resetEmail)) {
      showMessage('Invalid email format', 'error');
      return;
    }

    setLoading(true);
    
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(resetEmail);

      if (error) {
        showMessage(`Password reset failed: ${error.message}`, 'error');
      } else {
        showMessage('Password reset email sent! Please check your inbox.', 'success');
        setResetEmail('');
      }
    } catch (error) {
      showMessage(`Password reset failed: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container fade-in">
      <div className="header">
        <h1>🎵 MusicSynth</h1>
        <p>Transform Sheet Music into Visual Magic</p>
        <p className="tagline">Sign in to experience the future of music learning</p>
      </div>

      <div className="auth-tabs">
        <button 
          className={`auth-tab ${activeTab === 'login' ? 'active' : ''}`}
          onClick={() => setActiveTab('login')}
        >
          🎵 Sign In
        </button>
        <button 
          className={`auth-tab ${activeTab === 'register' ? 'active' : ''}`}
          onClick={() => setActiveTab('register')}
        >
          ✨ Get Started
        </button>
      </div>

      {message && (
        <div className={`alert ${messageType}`}>
          {message}
        </div>
      )}

      {activeTab === 'login' && (
        <div className="slide-in">
          <form onSubmit={handleLogin}>
            <h3>Welcome Back to MusicSynth</h3>
            <p>Continue your musical journey</p>
            
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                className="input"
                placeholder="Enter your email address"
                value={loginData.email}
                onChange={(e) => setLoginData({...loginData, email: e.target.value})}
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                className="input"
                placeholder="Enter your password"
                value={loginData.password}
                onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                disabled={loading}
              />
            </div>

            <button 
              type="submit" 
              className="button"
              disabled={loading}
              style={{ width: '100%', marginTop: '1rem' }}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border)' }}>
            <h4>Forgot Your Password?</h4>
            <p>No worries! Enter your email and we'll send you a reset link</p>
            
            <form onSubmit={handlePasswordReset}>
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  className="input"
                  placeholder="Enter your email address"
                  value={resetEmail}
                  onChange={(e) => setResetEmail(e.target.value)}
                  disabled={loading}
                />
              </div>

              <button 
                type="submit" 
                className="button secondary"
                disabled={loading}
                style={{ width: '100%' }}
              >
                {loading ? 'Sending...' : 'Send Reset Link'}
              </button>
            </form>
          </div>
        </div>
      )}

      {activeTab === 'register' && (
        <div className="slide-in">
          <form onSubmit={handleRegister}>
            <h3>Join the MusicSynth Community</h3>
            <p>Start transforming your sheet music into visual magic today!</p>
            
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                className="input"
                placeholder="Enter your email address"
                value={registerData.email}
                onChange={(e) => setRegisterData({...registerData, email: e.target.value})}
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                className="input"
                placeholder="Create a strong password"
                value={registerData.password}
                onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                className="input"
                placeholder="Confirm your password"
                value={registerData.confirmPassword}
                onChange={(e) => setRegisterData({...registerData, confirmPassword: e.target.value})}
                disabled={loading}
              />
            </div>

            <button 
              type="submit" 
              className="button"
              disabled={loading}
              style={{ width: '100%', marginTop: '1rem' }}
            >
              {loading ? 'Creating Account...' : 'Start Creating'}
            </button>
          </form>

          <div className="card" style={{ marginTop: '2rem', backgroundColor: 'var(--muted)' }}>
            <h4>🔐 Password Requirements</h4>
            <ul style={{ paddingLeft: '1.5rem', color: 'var(--muted-foreground)' }}>
              <li>At least 8 characters long</li>
              <li>Contains uppercase and lowercase letters</li>
              <li>Contains at least one digit</li>
            </ul>
          </div>
        </div>
      )}

      <div className="developer-note">
        <h4>Built with Passion ❤️</h4>
        <p>Created by a high school student passionate about music education technology</p>
      </div>

      <div style={{ textAlign: 'center', padding: '24px', opacity: 0.7 }}>
        <p style={{ margin: '0', fontSize: '0.9rem' }}>
          🎼 <strong>Transform</strong> • 🎨 <strong>Visualize</strong> • 🚀 <strong>Learn</strong>
        </p>
        <p style={{ margin: '8px 0 0 0', fontSize: '0.8rem', opacity: 0.6 }}>
          Built with React, Supabase, Modal, and ❤️
        </p>
      </div>
    </div>
  );
};

export default AuthPage; 
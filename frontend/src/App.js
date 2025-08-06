import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { createClient } from '@supabase/supabase-js';
import './App.css';

// Components
import AuthPage from './components/AuthPage';
import Dashboard from './components/Dashboard';
import LoadingSpinner from './components/LoadingSpinner';

// Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase configuration. Please check your environment variables.');
}

const supabase = createClient(supabaseUrl, supabaseKey);

function App() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Get initial session
    const getSession = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession();
        setSession(session);
        setUser(session?.user ?? null);
      } catch (error) {
        console.error('Error getting session:', error);
      } finally {
        setLoading(false);
      }
    };

    getSession();

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log('Auth state changed:', event, session);
        setSession(session);
        setUser(session?.user ?? null);
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    try {
      await supabase.auth.signOut();
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  if (loading) {
    return (
      <div className="app">
        <div className="container">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="app">
        <div className="container">
          <Routes>
            <Route 
              path="/" 
              element={
                session ? (
                  <Dashboard user={user} signOut={signOut} supabase={supabase} />
                ) : (
                  <Navigate to="/auth" replace />
                )
              } 
            />
            <Route 
              path="/auth" 
              element={
                session ? (
                  <Navigate to="/" replace />
                ) : (
                  <AuthPage supabase={supabase} />
                )
              } 
            />
            <Route 
              path="*" 
              element={<Navigate to="/" replace />} 
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App; 
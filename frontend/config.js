// Frontend Configuration for Modal API
const config = {
  // Modal API Endpoints - Updated with working music processing endpoints
  MODAL_API_URL: process.env.REACT_APP_MODAL_API_URL || 'https://cotoyota09--musicsynth-simple-music-process-music-file.modal.run',
  MODAL_HEALTH_URL: process.env.REACT_APP_MODAL_HEALTH_URL || 'https://cotoyota09--musicsynth-simple-music-health.modal.run',
  
  // Alternative endpoints (basic functionality)
  MODAL_GREET_URL: process.env.REACT_APP_MODAL_GREET_URL || 'https://cotoyota09--musicsynth-correct-greet.modal.run',
  MODAL_BASIC_PROCESS_URL: process.env.REACT_APP_MODAL_BASIC_PROCESS_URL || 'https://cotoyota09--musicsynth-correct-process-music.modal.run',
  
  // Supabase Configuration
  SUPABASE_URL: process.env.REACT_APP_SUPABASE_URL,
  SUPABASE_ANON_KEY: process.env.REACT_APP_SUPABASE_ANON_KEY,
  
  // API Endpoints
  ENDPOINTS: {
    PROCESS_MUSIC: '/',  // POST to root endpoint
    HEALTH_CHECK: '/',   // GET to root endpoint
    GREET: '/'           // GET to root endpoint with query param
  }
};

export default config; 
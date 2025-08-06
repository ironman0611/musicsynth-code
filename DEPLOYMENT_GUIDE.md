# MusicSynth Deployment Guide

This guide explains how to deploy the MusicSynth application in a distributed architecture with:
- **Frontend**: React app deployed on GitHub Pages
- **Backend**: Modal serverless API with GPU processing
- **Authentication**: Supabase authentication

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Pages  │    │    Supabase     │    │     Modal       │
│   (Frontend)    │◄──►│ (Authentication)│    │   (Backend)     │
│                 │    │                 │    │                 │
│ React App       │    │ User Auth       │    │ GPU Processing  │
│ File Upload     │    │ Session Mgmt    │    │ Video Gen       │
│ UI/UX           │    │ Password Reset  │    │ REST API        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+ for Modal backend
- Supabase account
- Modal account
- GitHub account

## Part 1: Supabase Setup

### 1.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Note down your project URL and anon key from Settings > API
3. Authentication is automatically enabled

### 1.2 Configure Authentication

```sql
-- No additional SQL needed - Supabase handles auth automatically
-- Users table is created automatically
```

### 1.3 Email Templates (Optional)

1. Go to Authentication > Email Templates
2. Customize the email templates for:
   - Email confirmation
   - Password reset
   - Magic link

## Part 2: Modal Backend Deployment

### 2.1 Install Modal

```bash
pip install modal
```

### 2.2 Setup Modal Account

```bash
# Create account and get API key
modal token new

# This will open a browser to authenticate
```

### 2.3 Deploy Backend

```bash
cd modal_backend

# Install dependencies
pip install -r requirements.txt

# Deploy to Modal
python deploy.py
```

Or deploy manually:

```bash
modal deploy app.py
```

### 2.4 Get API URL

After deployment, Modal will provide a URL like:
```
https://your-app-name--musicsynth-backend.modal.run
```

Save this URL - you'll need it for the frontend configuration.

### 2.5 Test Backend

```bash
# Health check
curl https://your-modal-url.modal.run/health

# Test file upload (with a sample file)
curl -X POST https://your-modal-url.modal.run/process-music \
  -F "file=@sample.musicxml" \
  -o output.mp4
```

## Part 3: Frontend Deployment

### 3.1 Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```env
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your_anon_key_here
REACT_APP_MODAL_API_URL=https://your-modal-url.modal.run
```

### 3.2 Update GitHub Repository

1. Create a new GitHub repository
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/musicsynth-frontend.git
git push -u origin main
```

### 3.3 Configure GitHub Secrets

Go to your GitHub repository > Settings > Secrets and variables > Actions

Add these secrets:
- `REACT_APP_SUPABASE_URL`: Your Supabase project URL
- `REACT_APP_SUPABASE_ANON_KEY`: Your Supabase anon key  
- `REACT_APP_MODAL_API_URL`: Your Modal API URL

### 3.4 Enable GitHub Pages

1. Go to Settings > Pages
2. Source: Deploy from a branch
3. Branch: gh-pages
4. The GitHub Action will automatically create this branch

### 3.5 Update Package.json

Update the `homepage` field in `frontend/package.json`:

```json
{
  "homepage": "https://yourusername.github.io/musicsynth-frontend"
}
```

### 3.6 Deploy

Push to main branch to trigger deployment:

```bash
git add .
git commit -m "Configure deployment"
git push origin main
```

The GitHub Action will automatically build and deploy your app.

## Part 4: Testing the Full System

### 4.1 Test Authentication

1. Visit your GitHub Pages URL
2. Try registering a new account
3. Check your email for verification
4. Try logging in

### 4.2 Test File Processing

1. Log in to your app
2. Upload a MusicXML file or sheet music image
3. Wait for processing (should take 1-2 minutes)
4. Verify video generation and download

### 4.3 Test Error Handling

1. Try uploading invalid file formats
2. Try uploading files that are too large
3. Verify proper error messages

## Part 5: Monitoring and Maintenance

### 5.1 Modal Monitoring

- Check logs: `modal logs list`
- Monitor usage: Modal dashboard
- Scale automatically based on usage

### 5.2 Supabase Monitoring

- Monitor auth activity in Supabase dashboard
- Check for suspicious login attempts
- Monitor API usage

### 5.3 GitHub Pages Monitoring

- Check deployment status in Actions tab
- Monitor build failures
- Update dependencies regularly

## Part 6: Custom Domain (Optional)

### 6.1 Set up Custom Domain

1. Buy a domain (e.g., musicsynth.com)
2. In GitHub Pages settings, add custom domain
3. Update CNAME in GitHub Actions workflow
4. Configure DNS records:

```
Type: CNAME
Name: www
Value: yourusername.github.io
```

### 6.2 SSL Certificate

GitHub Pages automatically provides SSL certificates for custom domains.

## Troubleshooting

### Common Issues

1. **Modal deployment fails**
   - Check Python version (3.9+)
   - Verify Modal token: `modal token show`
   - Check dependencies in requirements.txt

2. **GitHub Pages deployment fails**
   - Check GitHub Actions logs
   - Verify secrets are set correctly
   - Check Node.js version in workflow

3. **Authentication not working**
   - Verify Supabase URL and keys
   - Check CORS settings in Supabase
   - Confirm email verification is working

4. **File upload fails**
   - Check Modal API URL is correct
   - Verify CORS is enabled in Modal
   - Check file size limits

### Performance Optimization

1. **Modal Backend**
   - Use GPU instances for faster processing
   - Implement caching for repeated requests
   - Monitor cold start times

2. **Frontend**
   - Enable compression in build
   - Use CDN for static assets
   - Implement lazy loading

3. **Supabase**
   - Monitor connection pooling
   - Implement proper indexes
   - Use row-level security

## Cost Estimation

### Monthly Costs (Approximate)

- **Supabase**: Free tier supports 50MB database, 500MB storage
- **Modal**: Pay-per-use, ~$0.10 per minute of GPU usage
- **GitHub Pages**: Free for public repositories
- **Domain**: $10-15/year (optional)

### Scaling Considerations

- Modal automatically scales based on demand
- Supabase can handle thousands of concurrent users
- GitHub Pages has excellent CDN performance

## Security Considerations

1. **Environment Variables**
   - Never commit secrets to repository
   - Use GitHub Secrets for sensitive data
   - Rotate keys regularly

2. **Authentication**
   - Enable email verification
   - Set up password complexity rules
   - Monitor for suspicious activity

3. **File Uploads**
   - Validate file types and sizes
   - Scan for malicious content
   - Implement rate limiting

## Backup and Recovery

1. **Database Backups**
   - Supabase provides automatic backups
   - Export user data regularly
   - Test restoration procedures

2. **Code Backups**
   - Code is backed up in GitHub
   - Tag releases for easy rollback
   - Document deployment procedures

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**
   - Monitor error logs
   - Check system performance
   - Review user feedback

2. **Monthly**
   - Update dependencies
   - Review cost usage
   - Backup important data

3. **Quarterly**
   - Security audit
   - Performance optimization
   - Feature updates

### Getting Help

- Modal Support: [modal.com/support](https://modal.com/support)
- Supabase Support: [supabase.com/support](https://supabase.com/support)
- GitHub Support: [support.github.com](https://support.github.com)

## Conclusion

This distributed architecture provides:
- **Scalability**: Automatically scales based on demand
- **Reliability**: Multiple service providers ensure uptime
- **Performance**: GPU processing for fast video generation
- **Security**: Industry-standard authentication and encryption
- **Cost-effectiveness**: Pay-per-use pricing model

The system is designed to handle everything from individual users to thousands of concurrent users processing music files simultaneously.

For questions or issues, please refer to the troubleshooting section or contact support through the appropriate channels. 
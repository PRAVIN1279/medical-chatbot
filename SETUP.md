# 🚀 Medical Chatbot Setup Guide

Complete setup instructions for the Medical Assistant Chatbot with breathing UI and Google search integration.

## 📋 Prerequisites

### **Required Software**
- **Python 3.9+** ([Download](https://python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/))

### **Optional but Recommended**
- **VS Code** with Python extension
- **Vercel CLI** for deployment
- **GitHub account** for version control

## 🔧 Installation Steps

### **1. Clone the Repository**
```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/medical-chatbot.git
cd medical-chatbot

# Or download ZIP and extract
```

### **2. Setup Python Environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Verify activation (should show (.venv) in prompt)
```

### **3. Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Verify installation
pip list
```

### **4. Environment Configuration**
```bash
# Copy environment template (if exists)
cp .env.example .env

# Edit .env file with your settings (if needed)
# Note: Currently no API keys required
```

## 🏃‍♂️ Running the Application

### **Local Development**
```bash
# Method 1: Direct Python execution
python api/index.py

# Method 2: Flask development server
export FLASK_APP=api/index.py
export FLASK_ENV=development
flask run

# Application will be available at:
# http://localhost:5000
```

### **Testing Features**
Once running, test these features:
1. **🫁 Breathing UI** - Watch background animations
2. **🔍 Medical Search** - Try "migraine" or "diabetes"
3. **💡 Health Tips** - Click health tip button
4. **📷 File Upload** - Upload medical images
5. **🏥 Hospital Search** - Test location services

## 🌐 Deployment Options

### **Option 1: Vercel (Recommended)**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow prompts for first deployment
```

### **Option 2: Manual Deployment**
1. **Create Vercel account** at [vercel.com](https://vercel.com)
2. **Connect GitHub repository**
3. **Import project** from GitHub
4. **Deploy automatically** on git push

### **Option 3: Other Platforms**
- **Heroku**: Use `runtime.txt` and `requirements.txt`
- **AWS Lambda**: Configure serverless deployment
- **Google Cloud**: Use Cloud Functions
- **Netlify**: For static deployment with functions

## 📁 Project Structure

```
medical-chatbot/
├── 📄 README.md              # Main documentation
├── 📄 requirements.txt       # Python dependencies
├── 📄 vercel.json            # Vercel configuration
├── 📄 package.json           # Node.js metadata
├── 📄 runtime.txt            # Python version
├── 📄 LICENSE                # MIT License
├── 📄 CONTRIBUTING.md        # Contribution guide
├── 📄 SETUP.md               # This setup guide
├── 📄 .gitignore             # Git ignore rules
├── 📄 .vercelignore          # Vercel ignore rules
├── 📁 .github/               # GitHub workflows
│   └── 📁 workflows/
│       └── 📄 deploy.yml     # Auto-deployment
├── 📁 api/                   # Backend API
│   └── 📄 index.py           # Main Flask application
├── 📁 templates/             # Frontend templates
│   └── 📄 index.html         # Main UI with breathing animations
└── 📁 docs/                  # Additional documentation
    ├── 📄 deploy.md          # Deployment guide
    └── 📄 api-docs.md        # API documentation
```

## 🔧 Configuration

### **Flask Configuration**
```python
# In api/index.py
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['DEBUG'] = False  # Set to True for development
```

### **Vercel Configuration**
```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### **Python Dependencies**
```txt
# requirements.txt
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
Werkzeug==2.3.7
```

## 🧪 Testing

### **Manual Testing**
1. **Start application** locally
2. **Open browser** to http://localhost:5000
3. **Test each feature**:
   - Medical search functionality
   - Health tips system
   - File upload capability
   - Location services
   - Emergency information

### **Automated Testing** (Future Enhancement)
```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/

# Generate coverage report
pytest --cov=api tests/
```

## 🔍 Troubleshooting

### **Common Issues**

#### **Python/Pip Issues**
```bash
# Issue: pip not found
# Solution: Reinstall Python with pip

# Issue: Virtual environment not working
# Solution: 
python -m venv .venv --clear
```

#### **Flask Issues**
```bash
# Issue: Flask not starting
# Solution: Check if port 5000 is available
netstat -an | grep 5000

# Issue: Import errors
# Solution: Verify virtual environment is activated
```

#### **Vercel Deployment Issues**
```bash
# Issue: Build failures
# Solution: Check Python version in runtime.txt

# Issue: Function timeout
# Solution: Optimize code for serverless environment
```

### **Debug Mode**
```bash
# Enable Flask debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python api/index.py
```

### **Logs and Monitoring**
```bash
# View Vercel logs
vercel logs

# Check function metrics
vercel --debug
```

## 🔒 Security Considerations

### **Production Setup**
- ✅ **Disable debug mode** in production
- ✅ **Use HTTPS** for all deployments
- ✅ **Validate file uploads** properly
- ✅ **Sanitize user inputs**
- ✅ **Set appropriate CORS** policies

### **Environment Variables**
```bash
# For future API keys (if needed)
export MEDICAL_API_KEY="your-key-here"
export GOOGLE_SEARCH_API="your-key-here"
```

## 📱 Mobile Development

### **Responsive Design**
- ✅ **Mobile-first approach** in CSS
- ✅ **Touch-friendly interactions**
- ✅ **Optimized animations** for mobile
- ✅ **Fast loading times**

### **PWA Features** (Future)
- 📱 **Service worker** for offline capability
- 📱 **Web app manifest** for installation
- 📱 **Push notifications** for health reminders

## 🔄 Updates and Maintenance

### **Keeping Dependencies Updated**
```bash
# Check for outdated packages
pip list --outdated

# Update packages
pip install --upgrade package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### **Git Workflow**
```bash
# Regular maintenance
git pull origin main
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add: New feature"
git push origin feature/new-feature
# Create pull request
```

## 💡 Tips for Success

### **Development Best Practices**
- 🧪 **Test locally** before deploying
- 📝 **Document changes** clearly
- 🔒 **Follow security** guidelines
- 🏥 **Verify medical accuracy**
- 📱 **Test on mobile** devices

### **Performance Optimization**
- ⚡ **Minimize file sizes**
- 🗜️ **Compress images** (if added)
- 📦 **Bundle assets** efficiently
- 🚀 **Use CDN** for static files

## 📞 Support

### **Getting Help**
- 📖 **Documentation**: Check README.md
- 🐛 **Issues**: Create GitHub issue
- 💬 **Discussions**: Use GitHub discussions
- 📧 **Contact**: [Your email/contact]

### **Resources**
- 🌐 **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- ⚡ **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- 🐍 **Python Guide**: [python.org](https://python.org)

---

## ✅ Setup Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Application runs locally
- [ ] All features tested
- [ ] Ready for deployment
- [ ] GitHub repository setup
- [ ] Vercel deployment working

**🎉 Congratulations! Your Medical Chatbot is ready to help users! 🏥✨** 
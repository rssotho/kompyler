<template>
    <div class="kompyler-landing">
      <!-- Navigation -->
      <nav class="navbar">
        <div class="logo">
          <img src="@/assets/Kompyler_logo.svg" alt="Kompyler Logo">
          <span>Kompyler</span>
        </div>
        <div class="nav-links">
          <a href="#features">Features</a>
          <a href="#pricing">Pricing</a>
          <button @click="openSignupModal" class="cta-button">Get Started</button>
        </div>
      </nav>
  
      <!-- Hero Section -->
      <header class="hero-section">
        <div class="hero-content">
          <h1>AI-Powered Task Evaluation</h1>
          <p>Intelligent performance assessment platform</p>
          <div class="hero-cta">
            <button @click="openDemoModal" class="btn btn-primary">
              Watch Demo
            </button>
            <button @click="$router.push('/')" class="btn btn-secondary">
  Start Free Trial
</button>

          </div>
        </div>
        <div class="hero-visual">
          <div class="dashboard-mockup">
            <img src="@/assets/dashboard.png" alt="Kompyler Dashboard" class="mockup-image">
            <div class="glow-effect"></div>
          </div>
        </div>
      </header>
  
      <!-- Features Section -->
      <section id="features" class="features-section">
        <h2>The Best AI Features For You</h2>
        <div class="features-grid">
          <div 
            v-for="feature in features" 
            :key="feature.id" 
            class="feature-card"
          >
            <div class="feature-icon" :class="feature.colorClass">
                <i class="fa-solid fa-chart-simple"></i>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </section>
  
      <!-- Data Processing Section -->
      <section class="data-section">
        <h2>Data Can Be Processed</h2>
        <p class="section-desc">Analyze performance metrics and deliver actionable insights with our AI-powered platform</p>
        
        <div class="data-cards">
          <div class="data-card">
            <h3>Raw Data Generate Summary</h3>
            <p>Transform complex datasets into clear insights automatically</p>
            <button class="btn btn-outline">Learn More</button>
          </div>
          
          <div class="data-card">
            <h3>Summary Data Product</h3>
            <p>Get automated evaluations and customized reports</p>
            <div class="data-preview"></div>
          </div>
          
          <div class="data-card metrics-card">
            <h3>Percentage Insights</h3>
            <p>Track improvement metrics</p>
            <div class="metrics-circle">
              <span class="percentage">58%</span>
              <span class="label">Improved</span>
            </div>
          </div>
          
          <div class="data-card chart-card">
            <h3>Export Chart Data</h3>
            <p>Visualize performance trends</p>
            <div class="chart-preview"></div>
          </div>
        </div>
        
        <div class="processing-flow">
          <div class="flow-icons">
            <div class="flow-icon"><i class="fa-solid fa-upload"></i></div>
            <div class="flow-icon"><i class="fa-solid fa-microchip"></i></div>
            <div class="flow-icon active"><i class="fa-solid fa-chart-line"></i></div>
            <div class="flow-icon"><i class="fa-solid fa-flag"></i></div>
            <div class="flow-icon"><i class="fa-solid fa-share-from-square"></i></div>
          </div>
          <div class="flow-line"></div>
          <div class="flow-label">Analyze</div>
        </div>
      </section>
  
      <!-- Pricing Section -->
      <section id="pricing" class="pricing-section">
        <h2>Flexible Pricing Plans</h2>
        <div class="pricing-cards">
          <div 
            v-for="plan in pricingPlans" 
            :key="plan.id" 
            class="pricing-card"
            :class="{ 'recommended': plan.recommended }"
          >
            <h3>{{ plan.name }}</h3>
            <div class="price">
              <span class="amount">${{ plan.price }}</span>
              <span class="period">/month</span>
            </div>
            <ul class="features-list">
              <li v-for="feature in plan.features" :key="feature">
                ✓ {{ feature }}
              </li>
            </ul>
            <button @click="selectPlan(plan)" class="plan-button">Choose Plan</button>
          </div>
        </div>
      </section>
  
      <!-- Signup Modal -->
      <div v-if="isSignupModalOpen" class="modal signup-modal">
        <div class="modal-content">
          <span @click="closeSignupModal" class="close-btn">&times;</span>
          <h2>Sign Up for Kompyler</h2>
          <form @submit.prevent="submitSignup">
            <input 
              type="text" 
              v-model="signupForm.name" 
              placeholder="Full Name" 
              required
            >
            <input 
              type="email" 
              v-model="signupForm.email" 
              placeholder="Work Email" 
              required
            >
            <input 
              type="password" 
              v-model="signupForm.password" 
              placeholder="Password" 
              required
            >
            <button type="submit" class="btn btn-primary">Create Account</button>
          </form>
        </div>
      </div>
  
      <!-- Demo Modal -->
      <div v-if="isDemoModalOpen" class="modal demo-modal">
        <div class="modal-content">
          <span @click="closeDemoModal" class="close-btn">&times;</span>
          <h2>Kompyler Demo</h2>
          <div class="video-container">
            <iframe 
              width="560" 
              height="315" 
              src="https://www.youtube.com/embed/your-demo-video" 
              frameborder="0" 
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
  
      <!-- Footer -->
      <footer class="site-footer">
        <div class="footer-content">
          <div class="footer-logo">
            <img src="@/assets/Kompyler.png" alt="Kompyler Logo" class="logo-image">
            <p>© 2025 Kompyler. All rights reserved.</p>
          </div>
          <div class="footer-links">
            <a href="#privacy">Privacy Policy</a>
            <a href="#terms">Terms of Service</a>
            <a href="#contact">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isSignupModalOpen: false,
        isDemoModalOpen: false,
        signupForm: {
          name: '',
          email: '',
          password: ''
        },
        features: [
          {
            id: 1,
            icon: 'icon-analytics',
            title: 'AI-Powered Analytics',
            description: 'Advanced algorithms analyze performance patterns',
            colorClass: 'purple-icon'
          },
          {
            id: 2,
            icon: 'icon-speed',
            title: 'Fast Processing',
            description: 'Process large datasets in seconds',
            colorClass: 'orange-icon'
          },
          {
            id: 3,
            icon: 'icon-customize',
            title: 'Seamless Integration',
            description: 'Connect with your existing workflow tools',
            colorClass: 'purple-icon'
          },
          {
            id: 4,
            icon: 'icon-security',
            title: 'Advanced Security',
            description: 'Enterprise-grade protection for your data',
            colorClass: 'orange-icon'
          }
        ],
        pricingPlans: [
          {
            id: 1,
            name: 'Starter',
            price: 29,
            recommended: false,
            features: [
              'Up to 10 Users',
              'Basic Reporting',
              'Standard Support'
            ]
          },
          {
            id: 2,
            name: 'Pro',
            price: 99,
            recommended: true,
            features: [
              'Unlimited Users',
              'Advanced Analytics',
              'Priority Support',
              'Custom Integrations'
            ]
          }
        ]
      }
    },
    methods: {
      openSignupModal() {
        this.isSignupModalOpen = true
      },
      closeSignupModal() {
        this.isSignupModalOpen = false
      },
      openDemoModal() {
        this.isDemoModalOpen = true
      },
      closeDemoModal() {
        this.isDemoModalOpen = false
      },
      submitSignup() {
        // Implement signup logic
        console.log('Signup submitted', this.signupForm)
        // Add API call or validation
        this.closeSignupModal()
      },
      selectPlan(plan) {
        // Implement plan selection logic
        console.log('Selected plan:', plan)
        this.openSignupModal()
      }
    }
  }
  </script>
  
  <style lang="scss">
  :root {
    // Color Palette
    --primary-bg: #0B0B13;
    --secondary-bg: #14141F;
    --card-bg: #8d111176;
    --primary-purple: rgba(255, 0, 0, 0.61);
    --primary-purple-glow: red;
    --accent-orange: #FF5F1F;
    --text-white: #FFFFFF;
    --text-light: #fafafa;
    --text-gray: #ffffff;
    
    // Typography
    --font-primary: 'Poppins', sans-serif;
    --transition-speed: 0.3s;
  }
  
  // Global Styles
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body {
    font-family: var(--font-primary);
    background-color: var(--primary-bg);
    color: var(--text-white);
    line-height: 1.6;
  }
  
  // Navbar Styles
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 5%;
    background-color: var(--secondary-bg);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  
    .logo {
      display: flex;
      align-items: center;
      
      img {
        height: 40px;
        margin-right: 10px;
      }
  
      span {
        font-weight: 700;
        background: linear-gradient(to right, var(--primary-purple), var(--accent-orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
    }
  
    .nav-links {
      display: flex;
      align-items: center;
      
      a {
        color: var(--text-white);
        text-decoration: none;
        margin: 0 15px;
        transition: color var(--transition-speed);
  
        &:hover {
          color: var(--primary-purple);
        }
      }
  
      .cta-button {
        background-color: var(--primary-purple);
        color: var(--text-white);
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: all var(--transition-speed);
  
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 0 15px var(--primary-purple-glow);
        }
      }
    }
  }
  
  // Hero Section
  .hero-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5rem 5%;
    background-color: var(--primary-bg);
    position: relative;
    overflow: hidden;
  
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at top, var(--primary-purple-glow), transparent 60%);
      opacity: 0.8;
      z-index: 0;
    }
  
    .hero-content {
      flex: 1;
      position: relative;
      z-index: 1;
  
      h1 {
        font-size: 3rem;
        color: white;
        margin-bottom: 1rem;
        font-weight: 700;
      }
  
      p {
        font-size: 1.2rem;
        color: white;
        margin-bottom: 2rem;
      }
  
      .hero-cta {
        display: flex;
        gap: 1rem;
  
        .btn {
          padding: 12px 24px;
          border-radius: 5px;
          text-transform: uppercase;
          font-weight: bold;
          transition: all var(--transition-speed);
          cursor: pointer;
  
          &-primary {
            background-color: var(--primary-purple);
            color: var(--text-white);
            border: none;
  
            &:hover {
              transform: translateY(-2px);
              box-shadow: 0 0 15px var(--primary-purple-glow);
            }
          }
  
          &-secondary {
            background-color: transparent;
            color: var(--text-white);
            border: 2px solid var(--text-white);
  
            &:hover {
              background-color: rgba(255, 255, 255, 0.1);
              transform: translateY(-2px);
            }
          }
        }
      }
    }
  
    .hero-visual {
      flex: 1;
      display: flex;
      justify-content: center;
      position: relative;
      z-index: 1;
  
      .dashboard-mockup {
        position: relative;
        width: 100%;
        max-width: 600px;
        
        .mockup-image {
          width: 100%;
          border-radius: 10px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
  
        .glow-effect {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border-radius: 10px;
          box-shadow: 0 0 30px var(--primary-purple-glow);
          z-index: -1;
        }
      }
    }
  }
  
  // Features Section
  .features-section {
    padding: 5rem 5%;
    text-align: center;
    
    h2 {
      font-size: 2.5rem;
      margin-bottom: 2rem;
      position: relative;
      display: inline-block;
      color: white;
      
      &::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(to right, var(--primary-purple), var(--accent-orange));
      }
    }
    
    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 2rem;
      margin-top: 3rem;
      
      .feature-card {
        background-color: var(--card-bg);
        padding: 2rem;
        border-radius: 10px;
        transition: transform var(--transition-speed);
        color: rgb(197, 197, 197);
        
        &:hover {
          transform: translateY(-10px);
        }
        
        .feature-icon {
          width: 70px;
          height: 70px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 1.5rem;
          font-size: 1.5rem;
          
          &.purple-icon {
            background-color: rgba(127, 90, 240, 0.2);
            color: var(--primary-purple);
          }
          
          &.orange-icon {
            background-color: rgba(255, 95, 31, 0.2);
            color: var(--accent-orange);
          }
        }
        
        h3 {
          margin-bottom: 1rem;
          font-weight: 600;
        }
        
        p {
          color: var(--text-gray);
        }
      }
    }
  }
  
  // Data Section
  .data-section {
    padding: 5rem 5%;
    text-align: center;
    
    h2 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
      color: white;
    }
    
    .section-desc {
      color: var(--text-gray);
      max-width: 600px;
      margin: 0 auto 3rem;
    }
    
    .data-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.5rem;
      margin-bottom: 4rem;
      
      .data-card {
        background-color: var(--card-bg);
        padding: 2rem;
        border-radius: 10px;
        text-align: left;
        height: 100%;
        
        h3 {
          font-size: 1.5rem;
          margin-bottom: 1rem;
          color: var(--text-white);
        }
        
        p {
          color: var(--text-gray);
          margin-bottom: 1.5rem;
        }
        
        .btn-outline {
          background: transparent;
          border: 1px solid var(--primary-purple);
          color: var(--primary-purple);
          padding: 8px 16px;
          border-radius: 5px;
          cursor: pointer;
          transition: all var(--transition-speed);
          
          &:hover {
            background-color: var(--primary-purple);
            color: var(--text-white);
          }
        }
        
        .data-preview {
          height: 120px;
          background-color: rgba(127, 90, 240, 0.1);
          border-radius: 5px;
          margin-top: 1rem;
        }
        
        &.metrics-card {
          .metrics-circle {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(127, 90, 240, 0.2), rgba(255, 95, 31, 0.2));
            margin: 1rem auto 0;
            position: relative;
            
            &::before {
              content: '';
              position: absolute;
              top: 5px;
              left: 5px;
              right: 5px;
              bottom: 5px;
              border-radius: 50%;
              border: 3px solid var(--primary-purple);
              border-top-color: var(--accent-orange);
            }
            
            .percentage {
              font-size: 2.5rem;
              font-weight: 700;
              color: #4ADE80;
            }
            
            .label {
              color: var(--text-light);
              text-transform: uppercase;
              font-size: 0.8rem;
            }
          }
        }
        
        &.chart-card {
          .chart-preview {
            height: 120px;
            background: linear-gradient(to right, rgba(127, 90, 240, 0.1), rgba(127, 90, 240, 0.3));
            border-radius: 5px;
            margin-top: 1rem;
            position: relative;
            overflow: hidden;
            
            &::after {
              content: '';
              position: absolute;
              bottom: 0;
              left: 0;
              width: 100%;
              height: 50px;
              background: linear-gradient(to right, transparent, var(--primary-purple), transparent);
              clip-path: polygon(0 100%, 5% 50%, 10% 70%, 15% 30%, 20% 50%, 25% 20%, 30% 40%, 35% 10%, 40% 30%, 45% 50%, 50% 20%, 55% 40%, 60% 30%, 65% 50%, 70% 20%, 75% 40%, 80% 30%, 85% 50%, 90% 20%, 95% 50%, 100% 30%, 100% 100%);
            }
          }
        }
      }
    }
    
    .processing-flow {
      position: relative;
      padding: 3rem 0;
      
      .flow-icons {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 600px;
        margin: 0 auto;
        position: relative;
        z-index: 2;
        
        .flow-icon {
          width: 50px;
          height: 50px;
          background-color: var(--card-bg);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--text-gray);
          
          &.active {
            background-color: var(--primary-purple);
            color: var(--text-white);
            box-shadow: 0 0 15px var(--primary-purple-glow);
          }
        }
      }
      
      .flow-line {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 2px;
        height: 150px;
        background: linear-gradient(to bottom, var(--primary-purple), transparent);
        z-index: 1;
      }
      
      .flow-label {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        background-color: var(--card-bg);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--primary-purple);
      }
    }
  }
  
  // Pricing Section
  .pricing-section {
    padding: 5rem 5%;
    text-align: center;
    
    h2 {
      font-size: 2.5rem;
      margin-bottom: 3rem;
      position: relative;
      display: inline-block;
      color: white;
      
      &::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(to right, var(--primary-purple), var(--accent-orange));
      }
    }
    
    .pricing-cards {
      display: flex;
      justify-content: center;
      gap: 2rem;
      flex-wrap: wrap;
      color: white;

      .pricing-card {
        background-color: var(--card-bg);
        padding: 2.5rem;
        border-radius: 10px;
        max-width: 350px;
        width: 100%;
        position: relative;
        transition: transform var(--transition-speed);
        
        &:hover {
          transform: translateY(-10px);
        }
        
        &.recommended {
          border: 2px solid var(--primary-purple);
          
          &::before {
            content: 'Recommended';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background-color: var(--primary-purple);
            color: var(--text-white);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
          }
        }
        
        h3 {
          font-size: 1.8rem;
          margin-bottom: 1rem;
        }
        
        .price {
          margin-bottom: 2rem;
          
          .amount {
            font-size: 3rem;
            font-weight: 700;
            color: var(--text-white);
          }
          
          .period {
            color: var(--text-gray);
          }
        }
        
        .features-list {
          list-style: none;
          margin-bottom: 2rem;
          text-align: left;
          
          li {
            margin-bottom: 10px;
            color: var(--text-light);
          }
        }
        
        .plan-button {
          width: 100%;
          padding: 12px;
          background-color: var(--primary-purple);
          color: var(--text-white);
          border: none;
          border-radius: 5px;
          font-weight: 600;
          cursor: pointer;
          transition: all var(--transition-speed);
          
          &:hover {
            box-shadow: 0 0 15px var(--primary-purple-glow);
          }
        }
      }
    }
  }
  
  // Modal Styles
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  
    .modal-content {
      background: var(--secondary-bg);
      padding: 2.5rem;
      border-radius: 10px;
      width: 100%;
      max-width: 500px;
      position: relative;
      border: 1px solid var(--primary-purple);
      box-shadow: 0 0 30px var(--primary-purple-glow);
  
      .close-btn {
        position: absolute;
        top: 15px;
        right: 15px;
        font-size: 1.8rem;
        cursor: pointer;
        color: var(--text-gray);
        transition: color var(--transition-speed);
  
        &:hover {
          color: var(--primary-purple);
        }
      }
  
      h2 {
        margin-bottom: 1.5rem;
        text-align: center;
        font-size: 1.8rem;
      }
  
      form {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
  
        input {
          padding: 12px;
          border: 1px solid var(--card-bg);
          background-color: var(--primary-bg);
          color: var(--text-white);
          border-radius: 5px;
          transition: border-color var(--transition-speed);
  
          &:focus {
            outline: none;
            border-color: var(--primary-purple);
          }
        }
  
        button {
          padding: 12px;
          background-color: var(--primary-purple);
          color: var(--text-white);
          border: none;
          border-radius: 5px;
          font-weight: 600;
          cursor: pointer;
          transition: all var(--transition-speed);
          margin-top: 1rem;
  
          &:hover {
            box-shadow: 0 0 15px var(--primary-purple-glow);
          }
        }
      }
    }
  }
  
  // Footer Styles
  .site-footer {
    background-color: var(--secondary-bg);
    padding: 3rem 5%;
    
    .footer-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 2rem;
      
      .footer-logo {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        
        
        p {
          color: var(--text-gray);
          font-size: 0.9rem;
        }
      }
      
      .footer-links {
        display: flex;
        gap: 1.5rem;
        
        a {
          color: var(--text-light);
          text-decoration: none;
          font-size: 0.9rem;
          transition: color var(--transition-speed);
          
          &:hover {
            color: var(--primary-purple);
          }
        }
      }
    }
  }
  
  // Responsive Design
  @media (max-width: 992px) {
    .hero-section {
      flex-direction: column;
      text-align: center;
      
      .hero-content {
        margin-bottom: 3rem;
        
        .hero-cta {
          justify-content: center;
        }
      }
    }
    
    .pricing-cards {
      .pricing-card {
        max-width: 100%;
      }
    }
  }
  
  @media (max-width: 768px) {
    .navbar {
      flex-direction: column;
      padding: 1rem 5%;
      
      .logo {
        margin-bottom: 1rem;
      }
      
      .nav-links {
        width: 100%;
        justify-content: space-around;
        
        a {
          margin: 0 10px;
        }
      }
    }
    
    .features-section .features-grid {
      grid-template-columns: 1fr;
    }
    
    .footer-content {
      flex-direction: column;
      text-align: center;
      
      .footer-logo {
        align-items: center;
      }
    }
  }

  .logo-image{
  height: 150px;
  max-width: 130px;
  object-fit: contain;
  transition: opacity 0.3s ease;
  }
  </style>
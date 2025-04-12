<template>
    <div class="profile-container">
      <header class="header">
        <div class="logo">
        <img src="@/assets/Kompyler.png" alt="Komplyer Logo" class="logo-image">
    </div>
        <div class="header-actions">
          <button class="btn-outline">Evaluations</button>
          <div class="user-menu">
            <div class="avatar">JD</div>
          </div>
        </div>
      </header>
  
      <div class="banner">
        <h1>Manage Your Profile</h1>
        <p>Update your information to help us personalize your task evaluations</p>
      </div>
  
      <div class="tabs">
        <div class="tab active">Profile</div>
        <div class="tab">Contract</div>
      </div>
  
      <div class="scrollable-content">
        <div class="content">
          <div class="profile-main">
            <div class="profile-section">
              <div class="section-header">
                <h2>Personal Information</h2>
              </div>
    
              <div class="form-grid">
                <div class="form-group">
                  <label>First Name<span class="required">*</span></label>
                  <input type="text" value="John" />
                </div>
                <div class="form-group">
                  <label>Last Name<span class="required">*</span></label>
                  <input type="text" value="Doe" />
                </div>
                <div class="form-group">
                  <label>Email<span class="required">*</span></label>
                  <input type="email" value="john.doe@example.com" />
                </div>
                <div class="form-group">
                  <label>Phone Number</label>
                  <div class="phone-input">
                    <select class="country-code">
                      <option>+1</option>
                      <option>+44</option>
                      <option>+33</option>
                    </select>
                    <input type="tel" value="555-123-4567" />
                  </div>
                </div>
                <div class="form-group">
                  <label>Role<span class="required">*</span></label>
                  <select>
                    <option>Evaluator</option>
                    <option>Team Member</option>
                    <option>Team Leader</option>
                    <option>Manager</option>
                    <option>Administrator</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Title</label>
                  <select>
                    <option>Graphic Design</option>
                    <option>Front end</option>
                    <option>Sales Person</option>
                    <option>Tech Lead</option>
                  </select>
                </div>
              </div>
            </div>
    
            <div class="profile-section">
              <div class="section-header">
                <h2>Address Information</h2>
              </div>
    
              <div class="form-grid">
                <div class="form-group">
                  <label>Country</label>
                  <select>
                    <option selected disabled>Select country</option>
                    <option>United States</option>
                    <option>Canada</option>
                    <option>United Kingdom</option>
                    <option>Australia</option>
                    <option>Other</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Province/State</label>
                  <input type="text" placeholder="Enter province or state" />
                </div>
                <div class="form-group">
                  <label>City</label>
                  <input type="text" placeholder="Enter city" />
                </div>
                <div class="form-group">
                  <label>Postal Code</label>
                  <input type="text" placeholder="Enter postal code" />
                </div>
                <div class="form-group full-width">
                  <label>Street Address</label>
                  <input type="text" placeholder="Enter street address" />
                </div>
              </div>
            </div>
    
            <div class="action-buttons">
              <button class="btn-primary">Save Changes</button>
              <router-link to="/dashboard" class="btn-outline text-decoration-none">Back to Dashboard</router-link>
            </div>
          </div>
    
          <div class="profile-sidebar">
            <div class="profile-card">
              <div class="profile-image-container">
                <div class="profile-image">
                  <img src="@/assets/Avatar.png" alt="Profile" />
                  <div class="edit-photo-btn">
                    <span class="camera-icon">📷</span>
                  </div>
                </div>
              </div>
              
              <div class="profile-info">
                <h3 class="profile-name">John Doe</h3>
                <p class="profile-role">Senior Evaluator</p>
                <div class="profile-stats">
                  <div class="stat">
                    <span class="stat-number">127</span>
                    <span class="stat-label">Tasks Evaluated</span>
                  </div>
                  <div class="stat">
                    <span class="stat-number">4.8</span>
                    <span class="stat-label">Rating</span>
                  </div>
                </div>
              </div>
    
              <div class="card-section">
                <h4>Performance Metrics</h4>
                <div class="metric">
                  <div class="metric-label">Speed</div>
                  <div class="progress-bar">
                    <div class="progress" style="width: 78%"></div>
                  </div>
                  <div class="metric-value">78%</div>
                </div>
                <div class="metric">
                  <div class="metric-label">Quality</div>
                  <div class="progress-bar">
                    <div class="progress" style="width: 92%"></div>
                  </div>
                  <div class="metric-value">92%</div>
                </div>
                <div class="metric">
                  <div class="metric-label">Tasks Completed</div>
                  <div class="progress-bar">
                    <div class="progress" style="width: 85%"></div>
                  </div>
                  <div class="metric-value">85%</div>
                </div>
              </div>
    
              <div class="card-section">
                <h4>Upcoming Tasks</h4>
                <div class="task-list">
                  <div class="task-item">
                    <div class="task-icon priority-high">!</div>
                    <div class="task-details">
                      <div class="task-title">Website Redesign Review</div>
                      <div class="task-due">Due: Today</div>
                    </div>
                  </div>
                  <div class="task-item">
                    <div class="task-icon priority-medium">!</div>
                    <div class="task-details">
                      <div class="task-title">Mobile App UX Evaluation</div>
                      <div class="task-due">Due: Tomorrow</div>
                    </div>
                  </div>
                  <div class="task-item">
                    <div class="task-icon priority-low">!</div>
                    <div class="task-details">
                      <div class="task-title">API Documentation Review</div>
                      <div class="task-due">Due: In 3 days</div>
                    </div>
                  </div>
                </div>
                <button class="view-all-btn">View All Tasks</button>
              </div>
    
              <div class="card-section">
                <h4>Account Status</h4>
                <div class="status-item">
                  <div class="status-icon not-verified">!</div>
                  <div class="status-text">Profile form not filled completely</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TaskEvaluationProfile',
    data() {
      return {
        // You can add reactive data here
      }
    },
    methods: {
      // Methods can be added here
    }
  }
  </script>
  
  <style scoped>
  .profile-container {
    max-width: 100%;
    padding-left: 200px;
    padding-right: 200px;
    margin: 0 auto;
    color: #f8f8f8;
    background-color: #121212;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  /* Header styling */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #000;
    color: white;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  
  .logo {
    font-size: 1.5rem;
    font-weight: 700;
  }
  
  .logo-accent {
    color: #ff3333;
  }
  
  .header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .btn-primary {
    background-color: #ff3333;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
  }
  
  .btn-outline {
    background-color: transparent;
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none !important;
  }
  
  .banner {
    background: linear-gradient(135deg, #1a1a1a 0%, #380101 35%, #ff3333 100%);
    color: white;
    padding: 2rem;
    border-radius: 0 0 12px 12px;
    position: sticky;
    top: 68px; /* Header height */
    z-index: 99;
  }
  
  .banner h1 {
    font-size: 2rem;
    margin: 0 0 0.5rem;
    font-weight: 600;
  }
  
  .banner p {
    margin: 0;
    opacity: 0.8;
  }
  
  /* Tabs styling */
  .tabs {
    display: flex;
    gap: 1rem;
    margin: 0;
    border-bottom: 1px solid #333;
    padding: 1rem 0 0.5rem;
    position: sticky;
    top: 188px; /* Header + banner height */
    background-color: #121212;
    z-index: 98;
  }
  
  .tab {
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-weight: 500;
    color: #aaa;
  }
  
  .tab.active {
    color: #ff3333;
    border-bottom: 2px solid #ff3333;
  }
  
  /* Scrollable content area */
  .scrollable-content {
    flex: 1;
    overflow-y: auto;
    padding-bottom: 2rem;
  }
  
  /* Content layout */
  .content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
    padding: 1rem 0;
  }
  
  .profile-section {
    background-color: #1e1e1e;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  h2 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #fff;
    margin: 0;
  }
  
  .edit-btn {
    background-color: #2a2a2a;
    border: 1px solid #444;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    color: #ddd;
    cursor: pointer;
  }
  
  .edit-btn:hover {
    background-color: #333;
  }
  
  /* Form styling */
  .form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .full-width {
    grid-column: span 2;
  }
  
  label {
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    color: #bbb;
  }
  
  .required {
    color: #ff3333;
    margin-left: 2px;
  }
  
  input, select {
    padding: 0.75rem;
    border: 1px solid #444;
    border-radius: 4px;
    font-size: 0.9rem;
    background-color: #2a2a2a;
    color: #fff;
  }
  
  input::placeholder {
    color: #777;
  }
  
  input:focus, select:focus {
    border-color: #ff3333;
    outline: none;
    box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.2);
  }
  
  .phone-input {
    display: flex;
  }
  
  .country-code {
    width: 80px;
    border-right: none;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
  
  .phone-input input {
    flex: 1;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }
  
  .action-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .action-buttons .btn-outline {
    color: #ddd;
    border-color: #444;
  }
  
  /* Profile sidebar styling */
  .profile-card {
    background-color: #1e1e1e;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    overflow: hidden;
  }
  
  .profile-image-container {
    background: linear-gradient(135deg, #1a1a1a 0%, #380101 35%, #ff3333 100%);
    padding: 2rem 0;
    display: flex;
    justify-content: center;
  }
  
  .profile-image {
    position: relative;
    width: 120px;
    height: 120px;
  }
  
  .profile-image img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 4px solid #2a2a2a;
    object-fit: cover;
  }
  
  .edit-photo-btn {
    position: absolute;
    bottom: 5px;
    right: 5px;
    width: 32px;
    height: 32px;
    background-color: #ff3333;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: white;
  }
  
  .profile-info {
    padding: 1.5rem;
    text-align: center;
    border-bottom: 1px solid #333;
  }
  
  .profile-name {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #fff;
  }
  
  .profile-role {
    color: #aaa;
    margin: 0.25rem 0 1rem;
  }
  
  .profile-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
  }
  
  .stat {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .stat-number {
    font-size: 1.5rem;
    font-weight: 600;
    color: #ff3333;
  }
  
  .stat-label {
    font-size: 0.8rem;
    color: #aaa;
  }
  
  .card-section {
    padding: 1.5rem;
    border-bottom: 1px solid #333;
  }
  
  .card-section:last-child {
    border-bottom: none;
  }
  
  h4 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1rem;
    color: #fff;
  }
  
  .metric {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
  }
  
  .metric-label {
    width: 80px;
    font-size: 0.9rem;
    color: #bbb;
  }
  
  .progress-bar {
    flex: 1;
    height: 6px;
    background-color: #333;
    border-radius: 3px;
    margin: 0 0.5rem;
  }
  
  .progress {
    height: 100%;
    background-color: #ff3333;
    border-radius: 3px;
  }
  
  .metric-value {
    font-size: 0.9rem;
    font-weight: 500;
    color: #ddd;
  }
  
  .task-list {
    margin-bottom: 1rem;
  }
  
  .task-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid #333;
  }
  
  .task-item:last-child {
    border-bottom: none;
  }
  
  .task-icon {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.8rem;
    color: white;
  }
  
  .priority-high {
    background-color: #ff3333;
  }
  
  .priority-medium {
    background-color: #ff9933;
  }
  
  .priority-low {
    background-color: #33aa33;
  }
  
  .task-details {
    flex: 1;
  }
  
  .task-title {
    font-weight: 500;
    font-size: 0.9rem;
    color: #ddd;
  }
  
  .task-due {
    font-size: 0.8rem;
    color: #888;
  }
  
  .view-all-btn {
    display: block;
    width: 100%;
    padding: 0.5rem;
    text-align: center;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #2a2a2a;
    color: #ddd;
    cursor: pointer;
    margin-top: 0.5rem;
  }
  
  .status-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }
  
  .status-icon {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    color: white;
  }
  
  .verified {
    background-color: #33aa33;
  }
  
  .not-verified {
    background-color: #ff9933;
  }
  
  .status-text {
    flex: 1;
    font-size: 0.9rem;
    color: #ddd;
  }

  /* Custom scrollbar styles */
.scrollable-content::-webkit-scrollbar {
  width: 6px; /* Thin scrollbar */
  height: 6px; /* For horizontal scroll if needed */
}

.scrollable-content::-webkit-scrollbar-track {
  background: transparent; /* No background */
}

.scrollable-content::-webkit-scrollbar-thumb {
  background: #ff3333; /* Red color */
  border-radius: 3px; /* Slightly rounded corners */
}

.scrollable-content::-webkit-scrollbar-thumb:hover {
  background: #ff5555; /* Lighter red on hover */
}

/* For Firefox */
.scrollable-content {
  scrollbar-width: thin;
  scrollbar-color: #ff3333 transparent;
}

.logo {
  display: flex;
  align-items: center;
  height: 100%; /* Take full height of header */
}

.logo-image {
  height: 32px; /* Adjust this to fit within your header */
  width: auto;
  max-height: 80% /* Ensures it never exceeds header height */
}

  </style>
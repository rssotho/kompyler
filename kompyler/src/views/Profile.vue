<template>
  <div class="profile-container">
    <header class="header">
      <div class="logo">
        <img
          src="@/assets/Kompyler_logo.svg"
          alt="Komplyer Logo"
          class="logo-image"
        />
        <p class="profile-logo">KOMPYLER</p>
      </div>
      <div class="header-actions">
        <router-link
          to="/dashboard"
          class="btn-outline md:inline-block flex items-center space-x-2 no-underline dashboard-btn"
        >
          <span>Back to Dashboard</span>
        </router-link>

        <div class="user-menu">
          <div class="avatar">JD</div>
        </div>
      </div>
    </header>

    <div class="banner">
      <div class="banner-content">
        <h1>Manage Your Profile</h1>
        <p>
          Update your information to help us personalize your task evaluations
        </p>
      </div>
    </div>

    <div class="tabs-container">
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: activeTab === 'profile' }"
          @click="activeTab = 'profile'"
        >
          Profile
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'contract' }"
          @click="activeTab = 'contract'"
        >
          Contract
        </button>
      </div>
    </div>

    <div class="scrollable-content">
      <div class="content-wrapper">
        <div v-if="activeTab === 'profile'" class="content">
          <div class="profile-main">
            <div class="profile-section">
              <div class="section-header">
                <h2>Personal Information</h2>
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label>First Name<span class="required">*</span></label>
                  <input type="text" v-model="profile.firstName" />
                </div>
                <div class="form-group">
                  <label>Last Name<span class="required">*</span></label>
                  <input type="text" v-model="profile.lastName" />
                </div>
                <div class="form-group">
                  <label>Email<span class="required">*</span></label>
                  <input type="email" v-model="profile.email" />
                </div>
                <div class="form-group">
                  <label>Phone Number</label>
                  <div class="phone-input">
                    <select v-model="profile.countryCode" class="country-code">
                      <option value="+1">+1</option>
                      <option value="+44">+44</option>
                      <option value="+33">+33</option>
                      <option value="+49">+49</option>
                      <option value="+61">+61</option>
                    </select>
                    <input type="tel" v-model="profile.phone" />
                  </div>
                </div>
                <div class="form-group">
                  <label>Role<span class="required">*</span></label>
                  <select v-model="profile.role">
                    <option value="evaluator">Evaluator</option>
                    <option value="team-member">Team Member</option>
                    <option value="team-leader">Team Leader</option>
                    <option value="manager">Manager</option>
                    <option value="admin">Administrator</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Title</label>
                  <select v-model="profile.title">
                    <option value="graphic-design">Graphic Design</option>
                    <option value="frontend">Front End Developer</option>
                    <option value="sales">Sales Person</option>
                    <option value="tech-lead">Tech Lead</option>
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
                  <select v-model="profile.country">
                    <option value="" disabled>Select country</option>
                    <option value="us">United States</option>
                    <option value="ca">Canada</option>
                    <option value="uk">United Kingdom</option>
                    <option value="au">Australia</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Province/State</label>
                  <input
                    type="text"
                    v-model="profile.state"
                    placeholder="Enter province or state"
                  />
                </div>
                <div class="form-group">
                  <label>City</label>
                  <input
                    type="text"
                    v-model="profile.city"
                    placeholder="Enter city"
                  />
                </div>
                <div class="form-group">
                  <label>Postal Code</label>
                  <input
                    type="text"
                    v-model="profile.postalCode"
                    placeholder="Enter postal code"
                  />
                </div>
                <div class="form-group full-width">
                  <label>Street Address</label>
                  <input
                    type="text"
                    v-model="profile.streetAddress"
                    placeholder="Enter street address"
                  />
                </div>
              </div>
            </div>

            <div class="action-buttons">
              <button class="btn-primary" @click="saveChanges">
                Save Changes
              </button>
              <button class="btn-outline">Back to Dashboard</button>
            </div>
          </div>

          <div class="profile-sidebar">
            <div class="profile-card">
              <div class="profile-image-container">
                <div class="profile-image">
                  <img
                    :src="profile.avatar || '@/assets/Avatar.png'"
                    alt="Profile"
                  />
                  <button class="edit-photo-btn" @click="uploadPhoto">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path
                        d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"
                      ></path>
                      <circle cx="12" cy="13" r="4"></circle>
                    </svg>
                  </button>
                </div>
              </div>

              <div class="profile-info">
                <h3 class="profile-name">
                  {{ profile.firstName }} {{ profile.lastName }}
                </h3>
                <p class="profile-role">{{ getRoleTitle() }}</p>
                <div class="profile-stats">
                  <div class="stat">
                    <span class="stat-number">{{ stats.tasksEvaluated }}</span>
                    <span class="stat-label">Tasks Evaluated</span>
                  </div>
                  <div class="stat">
                    <span class="stat-number">{{ stats.rating }}</span>
                    <span class="stat-label">Rating</span>
                  </div>
                </div>
              </div>

              <div class="card-section performance">
                <h4>Performance Metrics</h4>
                <div
                  class="metric"
                  v-for="(metric, index) in performanceMetrics"
                  :key="index"
                >
                  <div class="metric-label">{{ metric.label }}</div>
                  <div class="progress-bar">
                    <div
                      class="progress"
                      :style="{ width: metric.value + '%' }"
                    ></div>
                  </div>
                  <div class="metric-value">{{ metric.value }}%</div>
                </div>
              </div>

              <div class="card-section">
                <h4>Upcoming Tasks</h4>
                <div class="task-list">
                  <div
                    class="task-item"
                    v-for="(task, index) in upcomingTasks"
                    :key="index"
                  >
                    <div class="task-icon" :class="'priority-' + task.priority">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                      </svg>
                    </div>
                    <div class="task-details">
                      <div class="task-title">{{ task.title }}</div>
                      <div class="task-due">Due: {{ task.due }}</div>
                    </div>
                  </div>
                </div>
                <button class="view-all-btn">View All Tasks</button>
              </div>

              <div class="card-section">
                <h4>Account Status</h4>
                <div
                  class="status-item"
                  v-for="(item, index) in accountStatus"
                  :key="index"
                >
                  <div
                    class="status-icon"
                    :class="item.verified ? 'verified' : 'not-verified'"
                  >
                    <svg
                      v-if="item.verified"
                      xmlns="http://www.w3.org/2000/svg"
                      width="14"
                      height="14"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <svg
                      v-else
                      xmlns="http://www.w3.org/2000/svg"
                      width="14"
                      height="14"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                  </div>
                  <div class="status-text">{{ item.text }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'contract'" class="contract-tab">
          <div class="profile-section">
            <div class="section-header">
              <h2>Contract Information</h2>
            </div>

            <div v-if="!contractFile" class="file-upload-container">
              <input
                type="file"
                ref="contractFileInput"
                @change="handleFileUpload"
                accept=".pdf"
                style="display: none"
              />
              <div
                class="file-drop-zone"
                @click="triggerFileInput"
                @dragover.prevent="dragOver"
                @dragleave.prevent="dragLeave"
                @drop.prevent="handleFileDrop"
                :class="{ 'drag-over': isDragOver }"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="50"
                  height="50"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path
                    d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                  ></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="12" y1="18" x2="12" y2="12"></line>
                  <line x1="9" y1="15" x2="15" y2="15"></line>
                </svg>
                <p>Drag and drop your contract PDF here</p>
                <button class="btn-outline">Browse Files</button>
              </div>
            </div>

            <div v-else class="contract-preview">
              <div class="contract-header">
                <h3>{{ contractFile.name }}</h3>
                <div class="contract-actions">
                  <button @click="viewContract" class="btn-primary">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path
                        d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"
                      ></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                    View
                  </button>
                  <button @click="removeContract" class="btn-outline">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path
                        d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                      ></path>
                    </svg>
                    Remove
                  </button>
                </div>
              </div>

              <div class="contract-details">
                <div class="detail-item">
                  <span>File Size:</span>
                  <span>{{ formatFileSize(contractFile.size) }}</span>
                </div>
                <div class="detail-item">
                  <span>Upload Date:</span>
                  <span>{{ formatDate(new Date()) }}</span>
                </div>
              </div>

              <div class="contract-preview-iframe">
                <object
                  v-if="contractFileUrl"
                  :data="contractFileUrl"
                  type="application/pdf"
                  width="100%"
                  height="500"
                >
                  <p>
                    Your browser doesn't support PDF preview.
                    <a :href="contractFileUrl" download>Download PDF</a>
                  </p>
                </object>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
import axios from "axios";
import { get_token, get_user_details } from "@/router";

const GLOBAL_URL = process.env.VUE_APP_GLOBAL_URL;

export default {
  name: "TaskEvaluationProfile",
  data() {
    return {
      activeTab: "profile",
      profile: {
        firstName: "",
        lastName: "",
        email: "",
        countryCode: "",
        phone: "",
        role: "",
        title: "",
        country: "",
        state: "",
        city: "",
        postalCode: "",
        streetAddress: "",
        avatar: require("@/assets/Avatar.png"),
      },

      // Contract File Upload Properties
      contractFile: null,
      contractFileUrl: null,
      isDragOver: false,

      // Dynamic Data Properties
      stats: {
        tasksEvaluated: 0,
        rating: 0,
      },
      performanceMetrics: [],
      upcomingTasks: [],
      accountStatus: [],

      role: "",
      last_name: "",
      first_name: "",
    };
  },
  mounted() {
    this.get_user_detail();
    this.loadDashboardData();
  },
  methods: {
    async get_user_detail() {
      var view_url = `${GLOBAL_URL}/system_management/view_user/`;
      var header = {
        "Content-Type": "application/json",
        Authorization: `Token ${get_token()}`,
      };
      const userDetails = get_user_details();
      const userId = userDetails.user_id;
      console.log("User ID", userId);
      console.log("userDetails URL", userDetails);
      try {
        var response = await axios.get(view_url, { 
          headers: header,
          params: { user_id: userId }
        });
        var response_data = JSON.parse(response.data);
        if (response_data.status === "success") {
          this.first_name = response_data.data.first_name;
          this.last_name = response_data.data.last_name;
          this.role = response_data.data.role;
        } else {
        }
      } catch (error) {}
    },
    async loadDashboardData() {
      try {
        // Add API calls here to fetch:
        // - Performance metrics
        // - Upcoming tasks
        // - Account status
        // - Stats
      } catch (error) {
        console.error("Error loading dashboard data:", error);
      }
    },
    // Role Title Method
    getRoleTitle() {
      const roles = {
        evaluator: "Senior Evaluator",
        "team-member": "Team Member",
        "team-leader": "Team Leader",
        manager: "Manager",
        admin: "Administrator",
      };
      return roles[this.profile.role] || "Senior Evaluator";
    },

    // Photo Upload Method
    uploadPhoto() {
      // Logic to upload a photo would go here
      console.log("Upload photo triggered");
      // Implement file selection and upload logic
      const input = document.createElement("input");
      input.type = "file";
      input.accept = "image/*";
      input.onchange = (event) => {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.profile.avatar = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      };
      input.click();
    },

    // Save Changes Method
    saveChanges() {
      // Comprehensive validation before saving
      const requiredFields = [
        "firstName",
        "lastName",
        "email",
        "phone",
        "country",
        "city",
      ];

      const missingFields = requiredFields.filter(
        (field) => !this.profile[field] || this.profile[field].trim() === ""
      );

      if (missingFields.length > 0) {
        alert(
          `Please fill in the following fields: ${missingFields.join(", ")}`
        );
        return;
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.profile.email)) {
        alert("Please enter a valid email address");
        return;
      }

      console.log("Saving profile changes", this.profile);
      // Implement actual save logic (API call, etc.)
    },

    // Contract File Upload Methods
    triggerFileInput() {
      this.$refs.contractFileInput.click();
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      this.processFile(file);
    },

    handleFileDrop(event) {
      const file = event.dataTransfer.files[0];
      this.processFile(file);
      this.isDragOver = false;
    },

    processFile(file) {
      // Comprehensive PDF validation
      if (!file) {
        alert("No file selected");
        return;
      }

      // Check file type
      const validTypes = ["application/pdf", "pdf"];
      const isValidType =
        validTypes.includes(file.type) ||
        file.name.toLowerCase().endsWith(".pdf");

      // Check file size (limit to 10MB)
      const maxSize = 10 * 1024 * 1024; // 10MB
      const isValidSize = file.size <= maxSize;

      if (isValidType && isValidSize) {
        this.contractFile = file;

        // Use FileReader for better compatibility
        const reader = new FileReader();
        reader.onload = (e) => {
          this.contractFileUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        // Detailed error messaging
        if (!isValidType) {
          alert("Please upload a valid PDF file");
        }
        if (!isValidSize) {
          alert("File is too large. Maximum file size is 10MB.");
        }

        // Reset file input
        this.$refs.contractFileInput.value = "";
      }
    },

    dragOver() {
      this.isDragOver = true;
    },

    dragLeave() {
      this.isDragOver = false;
    },

    viewContract() {
      if (this.contractFileUrl) {
        // Open in new tab or use PDF viewer
        window.open(this.contractFileUrl, "_blank");
      }
    },

    removeContract() {
      // Reset contract file and URL
      this.contractFile = null;
      this.contractFileUrl = null;

      // Reset file input
      if (this.$refs.contractFileInput) {
        this.$refs.contractFileInput.value = "";
      }
    },

    // Utility Methods
    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },

  // Lifecycle Hook for Cleanup
  beforeDestroy() {
    // Prevent memory leaks
    if (this.contractFileUrl) {
      URL.revokeObjectURL(this.contractFileUrl);
    }
  },
};
</script>

<style scoped>
.dashboard-btn {
  text-decoration: none;
  font-size: 12px;
}

/* Base styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.profile-container {
  color: #f8f8f8;
  background-color: #121212;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header styling */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background-color: #000;
  color: white;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  height: 40px;
  display: flex;
  align-items: center;
}

.logo-image {
  height: 32px;
  max-width: 100%;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar {
  width: 36px;
  height: 36px;
  background-color: #ff3333;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  cursor: pointer;
}

/* Banner styling */
.banner {
  background: linear-gradient(135deg, #1a1a1a 0%, #380101 35%, #ff3333 100%);
  color: white;
  padding: 1.5rem 1.5rem;
  position: relative;
}

.banner-content {
  max-width: 1400px;
  margin: 0 auto;
}

.banner h1 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem;
  font-weight: 600;
}

.banner p {
  margin: 0;
  opacity: 0.8;
}

/* Tabs styling */
.tabs-container {
  background-color: #121212;
  position: sticky;
  top: 55px;
  z-index: 95;
  border-bottom: 1px solid #333;
}

.tabs {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.tab {
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-weight: 500;
  color: #aaa;
  background: transparent;
  border: none;
  position: relative;
  transition: color 0.3s;
}

.tab.active {
  color: #ff3333;
}

.tab.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #ff3333;
}

/* Content layout */
.scrollable-content {
  flex: 1;
  overflow-y: auto;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem;
}

.content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .content {
    grid-template-columns: 3fr 2fr;
  }
}

@media (min-width: 1024px) {
  .content {
    grid-template-columns: 2fr 1fr;
  }
}

/* Buttons */
.btn-primary {
  background-color: #ff3333;
  color: white;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #ff5555;
}

.btn-outline {
  background-color: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1.25rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
}

.btn-outline:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Form styling */
.profile-section {
  background-color: #1e1e1e;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
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

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.form-group {
  display: flex;
  flex-direction: column;
}

.full-width {
  grid-column: 1 / -1;
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

input,
select {
  padding: 0.75rem;
  border: 1px solid #444;
  border-radius: 4px;
  font-size: 0.9rem;
  background-color: #2a2a2a;
  color: #fff;
  width: 100%;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input::placeholder {
  color: #777;
}

input:focus,
select:focus {
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
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* Profile sidebar styling */
.profile-card {
  background-color: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  height: fit-content;
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
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: background-color 0.3s;
}

.edit-photo-btn:hover {
  background-color: #ff5555;
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
  width: 100px;
  font-size: 0.9rem;
  color: #bbb;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background-color: #333;
  border-radius: 3px;
  margin: 0 0.5rem;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #ff3333;
  border-radius: 3px;
  transition: width 0.5s ease-out;
}

.metric-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: #ddd;
  min-width: 40px;
  text-align: right;
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
  transition: background-color 0.3s, border-color 0.3s;
}

.view-all-btn:hover {
  background-color: #333;
  border-color: #555;
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
  width: 6px;
  height: 6px;
}

.scrollable-content::-webkit-scrollbar-track {
  background: transparent;
}

.scrollable-content::-webkit-scrollbar-thumb {
  background: #ff3333;
  border-radius: 3px;
}

.scrollable-content::-webkit-scrollbar-thumb:hover {
  background: #ff5555;
}

/* For Firefox */
.scrollable-content {
  scrollbar-width: thin;
  scrollbar-color: #ff3333 transparent;
}

/* Contract tab styles */
.contract-tab {
  max-width: 900px;
  margin: 0 auto;
}

/* Responsive tweaks */
@media (max-width: 767px) {
  .profile-sidebar {
    order: -1;
  }

  .banner h1 {
    font-size: 1.5rem;
  }

  .banner p {
    font-size: 0.9rem;
  }

  .action-buttons {
    justify-content: center;
  }

  .tab {
    padding: 0.75rem 1rem;
  }
}

@media (max-width: 480px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .header {
    padding: 0.5rem 1rem;
  }

  .banner {
    padding: 1.25rem 1rem;
  }

  .content-wrapper {
    padding: 1rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons button {
    width: 100%;
  }
}

.file-drop-zone {
  border: 2px dashed #444;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
}

.file-drop-zone.drag-over {
  background-color: rgba(255, 51, 51, 0.1);
  border-color: #ff3333;
}

.file-drop-zone svg {
  color: #ff3333;
  margin-bottom: 1rem;
}

.file-drop-zone p {
  margin: 0.5rem 0;
  color: #aaa;
}

.contract-preview {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 1.5rem;
}

.contract-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.contract-actions {
  display: flex;
  gap: 1rem;
}

.contract-details {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  color: #aaa;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item span:first-child {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.contract-preview-iframe {
  background-color: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
}

.profile-logo {
  color: red;
  font-weight: bold;
}
</style>

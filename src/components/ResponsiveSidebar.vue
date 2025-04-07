<template>
  <div :class="['sidebar', { collapsed: isCollapsed, 'dark-sidebar': isDarkMode }]">
    <div class="sidebar-header">
      <div class="header-content">
        <!-- Logo image that disappears when collapsed -->
        <img v-show="!isCollapsed" src="@/assets/Kompyler.png" alt="Logo" class="sidebar-logo" />
        
        <!-- Toggle button -->
        <button class="toggle-button" @click="toggleSidebar" aria-label="Toggle Sidebar">
          <i class="fas" :class="isCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'"></i>
        </button>
      </div>
    </div>
    
    <div class="sidebar-content">
      <div class="nav-section">
        <nav class="nav-menu">
          <div 
            v-for="(item, index) in navItems" 
            :key="index" 
            class="nav-item" 
            :class="{ active: currentRoute === item.route }"
            @click="navigateTo(item.route)"
          >
            <div class="nav-icon">
              <i :class="item.icon"></i>
            </div>
            <span class="nav-text">{{ item.title }}</span>
            <div class="tooltip" v-if="isCollapsed">{{ item.title }}</div>
          </div>
        </nav>
      </div>
    </div>
    
    <div class="sidebar-footer">
      <div class="nav-item" @click="logout">
        <div class="nav-icon">
          <i class="fas fa-sign-out-alt"></i>
        </div>
        <span class="nav-text">Logout</span>
        <div class="tooltip" v-if="isCollapsed">Logout</div>
      </div>
    </div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'ResponsiveSidebar',
  data() {
    return {
      isCollapsed: false,
      isDarkMode: false,
      currentRoute: '',
      navItems: [
        { title: 'Dashboard', icon: 'fas fa-tachometer-alt', route: '/' },
        { title: 'Create Task', icon: 'fas fa-tasks', route: '/create-task' },
        { title: 'Evaluate Task', icon: 'fas fa-users', route: '/evaluate-task' },
        { title: 'View Evaluations', icon: 'fas fa-eye', route: '/view-evaluations' },
        { title: 'Export Summary', icon: 'fa-solid fa-download', route: '/' }
      ]
    };
  },
  mounted() {
    // Set initial collapsed state based on screen size
    this.checkScreenSize();
    // Listen for window resize events
    window.addEventListener('resize', this.checkScreenSize);
    // Get current route
    this.currentRoute = this.$route.path;
    // Listen for route changes
    this.$router.afterEach((to) => {
      this.currentRoute = to.path;
    });
    // Add event listeners for tooltip positioning
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('mouseenter', (e) => {
        const rect = e.target.getBoundingClientRect();
        e.target.style.setProperty('--tooltip-y', `${rect.top + rect.height/2}px`);
      });
    });
  },
  beforeDestroy() {
    // Remove event listener
    window.removeEventListener('resize', this.checkScreenSize);
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
      // Store preference in localStorage for persistence
      localStorage.setItem('sidebarCollapsed', this.isCollapsed);
    },
    checkScreenSize() {
      // Check if user had a saved preference
      const savedState = localStorage.getItem('sidebarCollapsed');
      
      if (savedState !== null) {
        // Use saved preference if available
        this.isCollapsed = savedState === 'true';
      } else {
        // Default behavior: collapsed on mobile, expanded on larger screens
        this.isCollapsed = window.innerWidth < 768;
      }
    },
    navigateTo(route) {
      this.$router.push(route);
      
      // On mobile, auto-collapse after navigation
      if (window.innerWidth < 768) {
        this.isCollapsed = true;
      }
    },
    logout() {
      // Implement logout logic here
      console.log('Logging out...');
      // Example: this.$store.dispatch('auth/logout');
    }
  }
};
</script>

<style scoped>
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  background-color: #000000;  /* Changed from gradient to solid black */
  color: #ffffff;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 99999; /* Make sidebar appear above dashboard content */
  width: 240px; /* Default width when expanded */
}

.sidebar.collapsed {
  width: 68px;
}

.sidebar-header {
  height: 68px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-between;
}

.sidebar-logo {
  height: 400px;
  max-width: 130px;
  object-fit: contain;
  transition: opacity 0.3s ease;
}

.toggle-button {
  min-width: 32px;
  height: 32px;
  border-radius: 8px;
  background-color: #1a1a1a;
  border: none;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.toggle-button:hover {
  background-color: #2c2c2c;
  transform: scale(1.05);
}

.sidebar-content {
  flex: 1;
  padding: 16px 0;
  overflow: hidden; /* Remove scroll and hide overflow */
}

.user-profile {
  display: flex;
  align-items: center;
  padding: 0 16px;
  margin-bottom: 8px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #3498db;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  margin-left: 12px;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.user-role {
  font-size: 12px;
  color: #bdc3c7;
}

.nav-section {
  display: flex;
  flex-direction: column;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 140px); /* Account for header and footer */
  padding: 0 8px; /* Add some padding for spacing */
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin: 4px 8px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  flex-shrink: 0; /* Prevent items from shrinking */
}

/* This is the key fix for icon alignment when collapsed */
.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px 0;
}

.nav-item:hover {
  background: linear-gradient(135deg, rgba(255, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.1) 100%);
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(0, 0, 0, 0.2) 100%);
  box-shadow: 0 4px 8px rgba(255, 0, 0, 0.1);
}

.nav-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 36px;
  font-size: 18px;
  color: #ff3333;
}

.nav-text {
  margin-left: 12px;
  transition: opacity 0.2s ease, width 0.2s ease, margin 0.2s ease;
  font-size: 14px;
}

.sidebar.collapsed .nav-text {
  opacity: 0;
  width: 0;
  margin-left: 0;
}

.tooltip {
  position: fixed;
  left: calc(68px + 10px);
  background: linear-gradient(135deg, #1a0000 0%, #000000 100%);
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s ease;
  z-index: 999999;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  border: 1px solid #ff0000;
}

.tooltip::before {
  content: '';
  position: absolute;
  top: 50%;
  right: 100%;
  transform: translateY(-50%);
  border-width: 8px;
  border-style: solid;
  border-color: transparent #1a0000 transparent transparent;
}

.nav-item:hover .tooltip {
  opacity: 1;
  top: var(--tooltip-y);
  transform: translateY(-50%);
}

.sidebar-footer {
  padding: 16px 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Also align footer items when collapsed */
.sidebar.collapsed .sidebar-footer .nav-item {
  justify-content: center;
  padding: 12px 0;
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .sidebar {
    position: fixed;
    z-index: 1000;
  }
  
  .sidebar:not(.collapsed) {
    box-shadow: 0 0 25px rgba(0, 0, 0, 0.3);
  }
}

/* Animations for smoother experience */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.nav-item {
  animation: fadeIn 0.3s ease-in-out;
}

/* Shadow transition */
.sidebar {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
              box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar.collapsed:hover {
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
}

.dark-sidebar {
  background-color: #000000;  /* Changed from gradient to solid black */
  color: #ffffff;
}
</style>
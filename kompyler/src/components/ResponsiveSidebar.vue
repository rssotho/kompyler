<template>
  <div>
    <!-- Traditional sidebar for mid and large devices -->
    <div
      :class="[

        'sidebar',
        { collapsed: isCollapsed, 'dark-sidebar': isDarkMode },
      ]"
      v-show="!isMobile"
    >
      <div class="sidebar-header">
        <div class="header-content">
          <img
            v-show="!isCollapsed"
            src="@/assets/Kompyler.png"
            alt="Logo"
            class="sidebar-logo2"
          />
          <button
            class="toggle-button"
            @click="toggleSidebar"
            aria-label="Toggle Sidebar"
          >
            <i
              class="fas"
              :class="isCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'"
            ></i>
          </button>
        </div>
      </div>

      <div class="sidebar-content">
        <div class="nav-section">
          <nav class="nav-menu">
            <template v-for="(item, index) in navItems" :key="`item-${index}`">
              <div class="nav-item-container">
                <div
                  class="nav-item"
                  :class="{
                    active: currentRoute === item.route,
                    'has-dropdown-open':
                      item.dropdown && expandedDropdowns.includes(index),
                    'system-management': item.title === 'System Management',
                  }"
                  @click="
                    item.dropdown
                      ? toggleDropdown(index)
                      : navigateTo(item.route)
                  "
                >
                  <div class="nav-icon">
                    <i :class="item.icon"></i>
                  </div>
                  <span
                    class="nav-text"
                    :class="{
                      'system-text': item.title === 'System Management',
                    }"
                    >{{ item.title }}</span
                  >
                  <i
                    v-if="item.dropdown && !isCollapsed"
                    class="fas dropdown-arrow"
                    :class="

                      expandedDropdowns.includes(index)
                        ? 'fa-chevron-up'
                        : 'fa-chevron-down'
                    "
                  ></i>
                  <div class="tooltip" v-if="isCollapsed">{{ item.title }}</div>
                </div>

                <transition name="dropdown">
                  <div
                    v-if="item.dropdown && expandedDropdowns.includes(index)"
                    class="dropdown-container"
                    :class="{ 'side-dropdown': isCollapsed }"
                  >
                    <template
                      v-for="(dropdownItem, dropIndex) in item.dropdownItems"
                      :key="`drop-${index}-${dropIndex}`"
                    >
                      <div
                        class="dropdown-item"
                        :class="{ active: currentRoute === dropdownItem.route }"
                        @click="navigateTo(dropdownItem.route)"
                      >
                        <div class="dropdown-icon">
                          <i :class="dropdownItem.icon"></i>
                        </div>
                        <span class="dropdown-text">{{
                          dropdownItem.title
                        }}</span>
                        <div class="tooltip" v-if="isCollapsed">
                          {{ dropdownItem.title }}
                        </div>
                      </div>
                    </template>
                  </div>
                </transition>
              </div>
            </template>
          </nav>
        </div>
      </div>
      <div v-if="error_message" class="error-toast">
        {{ error_message }}
      </div>
      <div class="sidebar-footer">
        <div class="nav-item" @click="showLogoutModal = true">
          <div class="nav-icon">
            <i class="fas fa-sign-out-alt"></i>
          </div>
          <span class="nav-text">Logout</span>
          <div class="tooltip" v-if="isCollapsed">Logout</div>
        </div>
      </div>

      <!-- Logout Confirmation Modal -->
      <div class="modal" v-if="showLogoutModal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>Confirm Logout</h2>
            <button class="close-btn" @click="showLogoutModal = false">&times;</button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to logout?</p>
          </div>
          <div class="modal-footer">
            <button class="modal-btn" @click="logout">Yes, Logout</button>
            <button class="modal-btn cancel" @click="showLogoutModal = false">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom navigation for mobile devices -->
    <div class="mobile-nav-container" v-show="isMobile">
      <div class="mobile-nav-scroll-indicator left" v-if="hasMoreItemsLeft">
        <i class="fas fa-chevron-left"></i>
      </div>
      <div class="mobile-nav" ref="mobileNav" @scroll="checkScrollPosition">
        <template v-for="(item, index) in mobileNavItems" :key="index">
          <div
            class="mobile-nav-item"
            :class="{ active: currentRoute === item.route }"
            @click="

              item.dropdown
                ? toggleMobileDropdown(item)
                : navigateTo(item.route)
            "
          >
            <div class="mobile-nav-icon">
              <i :class="item.icon"></i>
            </div>
            <span class="mobile-nav-text">{{
              item.title === "System Management" ? "System" : item.title
            }}</span>
          </div>
          <transition name="dropdown">
            <div
              v-if="item.dropdown && mobileExpanded.includes(item.title)"
              class="mobile-dropdown"
            >
              <div
                class="dropdown-item"
                v-for="(dropdownItem, dropIndex) in item.dropdownItems"
                :key="`mobile-drop-${dropIndex}`"
                @click="navigateTo(dropdownItem.route)"
              >
                {{ dropdownItem.title }}
              </div>
            </div>
          </transition>
        </template>
      </div>
      <div class="mobile-nav-scroll-indicator right" v-if="hasMoreItemsRight">
        <i class="fas fa-chevron-right"></i>
      </div>
    </div>

    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "ResponsiveSidebar",
  data() {
    return {
      isCollapsed: false,
      isDarkMode: false,
      isMobile: false,
      currentRoute: "",
      expandedDropdowns: [],
      mobileExpanded: [],
      hasMoreItemsLeft: false,
      hasMoreItemsRight: true,
      error_message: '',
      showLogoutModal: false,
      navItems: [
        {
          title: "Dashboard",
          icon: "fas fa-tachometer-alt",
          route: "/dashboard",
        },
        // { title: "Create Task", icon: "fas fa-tasks", route: "/create-task" },
        { title: "Evaluate", icon: "fas fa-users", route: "/evaluate-task" },
        { title: "View", icon: "fas fa-eye", route: "/view-evaluations" },
        { title: "Export", icon: "fa-solid fa-download", route: "/export" },
        {
          title: "Management",
          icon: "fas fa-cog",
          dropdown: true,
          dropdownItems: [
            {
              title: "Manage users",
              icon: "fas fa-user-cog",
              route: "/ManageUsers",
            },
            { title: "Profile", icon: "fas fa-sliders-h", route: "/Profile" },
          ],
        },
      ],
    };
  },
  computed: {
    mobileNavItems() {
      let items = [];
      this.navItems.forEach((item) => {
        if (item.dropdown) {
          items.push(item);
        } else {
          items.push(item);
        }
      });
      return items;
    },
  },
  mounted() {
    this.checkScreenSize();
    window.addEventListener("resize", this.checkScreenSize);
    this.currentRoute = this.$route.path;
    this.$router.afterEach((to) => {
      this.currentRoute = to.path;
      this.handleRouteChange(to);
    });
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.checkScreenSize);
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
      localStorage.setItem("sidebarCollapsed", this.isCollapsed);

      // Close any open dropdowns when sidebar is collapsed
      if (this.isCollapsed) {
        this.expandedDropdowns = [];
      }
    },
    toggleDropdown(index) {
      const expandedIndex = this.expandedDropdowns.indexOf(index);
      if (expandedIndex === -1) {
        // Close other dropdowns if any are open
        this.expandedDropdowns = [index];
      } else {
        this.expandedDropdowns = [];
      }
    },
    checkScreenSize() {
      this.isMobile = window.innerWidth < 768;
      const savedState = localStorage.getItem("sidebarCollapsed");
      this.isCollapsed =
        savedState !== null
          ? savedState === "true"
          : window.innerWidth < 992 && window.innerWidth >= 768;
    },
    navigateTo(route) {
      this.$router.push(route);

      // Close mobile dropdown after navigation
      if (this.isMobile) {
        this.mobileExpanded = [];
      }
    },
    async logout() {
      const logout_url = `${GLOBAL_URL}/system_management/user_logout/`;
      const header = {
        "Content-Type": "application/json",
        Authorization: `Token ${get_token()}`,
      };

      try {
        const response = await axios.post(logout_url, {}, { headers: header });
        const response_data = JSON.parse(response.data);

        if (response_data.status === "success") {
          localStorage.removeItem("token");
          this.$router.push("/");
        } else {
          this.error_message = response_data.message;
          setTimeout(() => {
            this.error_message = '';
          }, 3000);
        }
      } catch (error) {
        if (error.response) {
          // Handle API error responses
          try {
            const error_data = JSON.parse(error.response.data);
            this.error_message = error_data.message;
          } catch (e) {
            this.error_message = error.response.data || "Failed to logout. Please try again.";
          }
        } else if (error.request) {
          this.error_message = "Network error. Please check your connection.";
        } else {
          this.error_message = "An error occurred. Please try again.";
        }
        setTimeout(() => {
          this.error_message = '';
        }, 3000);
      }
    },
    checkScrollPosition() {
      if (!this.$refs.mobileNav) return;
      const nav = this.$refs.mobileNav;
      this.hasMoreItemsLeft = nav.scrollLeft > 10;
      const isAtEnd =
        Math.abs(nav.scrollWidth - nav.clientWidth - nav.scrollLeft) < 10;
      this.hasMoreItemsRight = !isAtEnd;
    },
    toggleMobileDropdown(item) {
      const index = this.mobileExpanded.indexOf(item.title);
      if (index === -1) {
        // Close other mobile dropdowns
        this.mobileExpanded = [item.title];
      } else {
        this.mobileExpanded = [];
      }
    },
    handleRouteChange(to) {
      // For desktop
      this.navItems.forEach((item, index) => {
        if (item.dropdown) {
          const containsRoute = item.dropdownItems.some(
            (dropItem) => dropItem.route === to.path
          );
          if (containsRoute) {
            if (!this.expandedDropdowns.includes(index)) {
              this.expandedDropdowns.push(index);
            }
          } else {
            const dropdownIndex = this.expandedDropdowns.indexOf(index);
            if (dropdownIndex !== -1) {
              this.expandedDropdowns.splice(dropdownIndex, 1);
            }
          }
        }
      });

      // For mobile
      this.mobileNavItems.forEach((item) => {
        if (item.dropdown) {
          const containsRoute = item.dropdownItems.some(
            (dropItem) => dropItem.route === to.path
          );
          if (containsRoute) {
            if (!this.mobileExpanded.includes(item.title)) {
              this.mobileExpanded.push(item.title);
            }
          } else {
            const mobileDropdownIndex = this.mobileExpanded.indexOf(item.title);
            if (mobileDropdownIndex !== -1) {
              this.mobileExpanded.splice(mobileDropdownIndex, 1);
            }
          }
        }
      });
    },
  },
};
</script>

<style scoped>
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  background-color: #000000;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 99;
  width: 260px; /* Increased from 240px to 260px */
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

.sidebar-logo2 {
  height: 120px;
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
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-section {
  display: flex;
  flex-direction: column;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  padding: 0 8px;
}

.nav-item-container {
  position: relative;
  margin-bottom: 4px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin: 0 8px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.nav-item.system-management {
  padding-right: 8px; /* Reduce right padding for System Management */
}

.nav-item.has-dropdown-open {
  border-radius: 10px 10px 0 0;
  margin-bottom: 0;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px 0;
}

.nav-item:hover {
  background: linear-gradient(
    135deg,
    rgba(255, 0, 0, 0.1) 0%,
    rgba(0, 0, 0, 0.1) 100%
  );
}

.nav-item.active {
  background: linear-gradient(
    135deg,
    rgba(255, 0, 0, 0.2) 0%,
    rgba(0, 0, 0, 0.2) 100%
  );
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
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 130px;
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
  z-index: 9999;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  border: 1px solid #ff0000;
}

.tooltip::before {
  content: "";
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

.sidebar.collapsed .sidebar-footer .nav-item {
  justify-content: center;
  padding: 12px 0;
}

/* Mobile bottom navigation styling - now horizontally scrollable */
.mobile-nav-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background-color: #000000;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
}

.mobile-nav {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  flex: 1;
  height: 100%;
}

/* Hide scrollbar */
.mobile-nav::-webkit-scrollbar {
  display: none;
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 20%; /* Show 5 items */
  flex: 0 0 20%; /* Fixed size for each item */
  height: 100%;
  padding: 8px 0;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.2s ease;
  overflow: hidden;
}

.mobile-nav-item.active {
  color: #ff3333;
  background-color: rgba(255, 0, 0, 0.05);
}

.mobile-nav-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.mobile-nav-text {
  font-size: 10px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  padding: 0 4px;
}

/* Scroll indicators for mobile nav */
.mobile-nav-scroll-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.8) 0%,
    rgba(0, 0, 0, 0.4) 100%
  );
  width: 24px;
  height: 100%;
  position: relative;
  color: #ff3333;
  font-size: 12px;
  z-index: 1;
}

.mobile-nav-scroll-indicator.left {
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.8) 0%,
    rgba(0, 0, 0, 0.4) 100%
  );
  left: 0;
}

.mobile-nav-scroll-indicator.right {
  background: linear-gradient(
    270deg,
    rgba(0, 0, 0, 0.8) 0%,
    rgba(0, 0, 0, 0.4) 100%
  );
  right: 0;
}

/* Adjust main content to account for mobile nav */
@media (max-width: 767px) {
  :deep(.app-content) {
    padding-bottom: 64px; /* Match height of mobile nav */
  }
}

/* Dropdown styling */
.dropdown-arrow {
  margin-left: auto;
  font-size: 14px;
  transition: transform 0.3s ease;
  color: #ff3333;
  padding-left: 4px; /* Less padding to save space */
}

.dropdown-container {
  width: calc(100% - 16px);
  margin: 0 8px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 0 0 10px 10px;
  overflow: hidden;
  box-shadow: inset 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

/* Side dropdown styling for collapsed sidebar */
.dropdown-container.side-dropdown {
  position: absolute;
  left: 60px; /* Position next to collapsed sidebar */
  top: 0;
  width: 200px;
  margin: 0;
  background-color: #1a1a1a;
  border-radius: 0 10px 10px 0;
  box-shadow: 5px 0 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.dropdown-item {
  position: relative;
  display: flex;
  align-items: center;
  padding: 10px 16px;
  margin: 0;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  background-color: rgba(255, 255, 255, 0.05);
}

.dropdown-item:hover {
  background: linear-gradient(
    135deg,
    rgba(255, 0, 0, 0.1) 0%,
    rgba(0, 0, 0, 0.1) 100%
  );
}

.dropdown-item.active {
  background: linear-gradient(
    135deg,
    rgba(255, 0, 0, 0.15) 0%,
    rgba(0, 0, 0, 0.15) 100%
  );
}

.dropdown-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 24px;
  font-size: 14px;
  color: #ff3333;
}

.dropdown-text {
  margin-left: 10px;
  font-size: 12px;
  transition: opacity 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
}

.sidebar.collapsed .dropdown-container.side-dropdown {
  position: fixed; /* Change from absolute to fixed */
  left: 68px; /* Adjust to match collapsed sidebar width */
  top: auto; /* Remove fixed top positioning */
  bottom: auto; /* Remove fixed bottom positioning */
  width: 200px;
  margin: 0;
  background-color: #1a1a1a;
  border-radius: 0 10px 10px 0;
  box-shadow: 5px 0 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  transition: all 0.3s ease;
}

.sidebar.collapsed .dropdown-container.side-dropdown .dropdown-item {
  position: relative;
  display: flex;
  align-items: center;
  padding: 10px 16px;
  margin: 4px 0; /* Add slight margin between items */
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px; /* Add rounded corners */
}

.sidebar.collapsed .dropdown-container.side-dropdown .dropdown-item:hover {
  background: linear-gradient(
    135deg,
    rgba(255, 0, 0, 0.1) 0%,
    rgba(0, 0, 0, 0.1) 100%
  );
}

.sidebar.collapsed .dropdown-container.side-dropdown .dropdown-item.active {
  background: linear-gradient(
    135deg,
    rgba(255, 0, 0, 0.15) 0%,
    rgba(0, 0, 0, 0.15) 100%
  );
}

.sidebar.collapsed .dropdown-container.side-dropdown .dropdown-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 24px;
  font-size: 14px;
  color: #ff3333;
  margin-right: 10px; /* Add some spacing between icon and text */
}

.sidebar.collapsed .dropdown-container.side-dropdown .dropdown-text {
  margin-left: 0; /* Remove left margin as we added margin to icon */
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
}

/* Additional improvements for positioning and visibility */
.sidebar.collapsed .nav-item-container {
  position: relative;
}

.sidebar.collapsed .nav-item-container:hover .dropdown-container.side-dropdown {
  display: block;
  opacity: 1;
  visibility: visible;
}

/* Collapsed state dropdown */
.sidebar.collapsed .dropdown-container {
  position: absolute;
  left: 100%;
  top: 0;
  width: 200px;
  background-color: #1a1a1a;
  border-radius: 0 10px 10px 10px;
  box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 9000;
  padding: 8px;
  margin: 0;
}

.sidebar.collapsed .dropdown-item {
  padding: 10px 16px;
  margin: 4px 0;
  background-color: transparent;
  border-radius: 6px;
}

.sidebar.collapsed .dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Dropdown animations */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.3s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-enter-to,
.dropdown-leave-from {
  max-height: 300px;
  opacity: 1;
  transform: translateY(0);
}

.dropdown-text {
  margin-left: 10px;
  font-size: 12px; /* Keep the same font size as nav-text */
  transition: opacity 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px; /* Adjust as necessary */
}

/* Mobile Dropdown Specific Styles */
.mobile-dropdown {
  position: fixed;
  bottom: 64px; /* Height of mobile nav */
  left: 0;
  right: 0;
  background-color: #000000;
  z-index: 1001;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-dropdown .dropdown-item {
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  display: flex;
  align-items: center;
}

.mobile-dropdown .dropdown-item:last-child {
  border-bottom: none;
}

.mobile-dropdown .dropdown-item:hover {
  background-color: rgba(255, 0, 0, 0.1);
}

.error-toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: rgba(255, 51, 51, 0.1);
  border: 1px solid #ff3333;
  color: #ff3333;
  padding: 12px 24px;
  border-radius: 8px;
  z-index: 9999;
  font-size: 14px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #2a2a2a;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #333333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #ffffff;
}

.close-btn {
  background: none;
  border: none;
  color: #888888;
  font-size: 24px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
  color: #cccccc;
  text-align: center;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #333333;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.modal-btn:not(.cancel) {
  background-color: #ff3333;
  color: white;
}

.modal-btn:not(.cancel):hover {
  background-color: #ff4444;
}

.modal-btn.cancel {
  background-color: #333333;
  color: white;
}

.modal-btn.cancel:hover {
  background-color: #444444;
}
</style>

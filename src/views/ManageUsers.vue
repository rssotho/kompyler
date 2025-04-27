<template>
    <div class="dashboard dark-mode">
      <header class="header">
  <div class="header-left">
    <router-link to="/dashboard" class="back-to-dashboard">
    <i class="fas fa-arrow-left"></i>
    <span class="back-text">Back to Dashboard</span>
    </router-link>

    
    <div class="logo">
      <img src="@/assets/Kompyler_logo.svg" alt="Kompyler Logo" class="sidebar-logo2">
      <span class="logo-name">Kompyler</span>
    </div>
  </div>

  <div class="user-profile">
    <span class="user-name">Hashim Briccam</span>
    <img src="@/assets/Avatar.png" alt="User Avatar" class="avatar" />
  </div>
</header>

  
      <div class="content">
        <div class="page-header">
          <div class="breadcrumb">
          </div>
          <h1 class="title">User Management</h1>
          <div class="search-add">
            <div class="search-bar">
              <input type="text" placeholder="Search User" v-model="searchQuery" />
              <button class="search-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </button>
            </div>
            <button class="add-user-btn" @click="showAddUserModal = true"><i class="fa-solid fa-user-plus"></i></button>
          </div>
        </div>
  
        <div class="user-table desktop-view">
          <table>
            <thead>
              <tr>
                <th class="checkbox-column">
                  <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
                </th>
                <th>Name</th>
                <th>User Role</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr class="subheader-row">
                <td colspan="5" class="showing-text">Showing {{ paginatedUsers.length }} of {{ filteredUsers.length }} total users</td>
              </tr>
              <tr v-for="user in paginatedUsers" :key="user.id">
                <td>
                  <input type="checkbox" v-model="user.selected" />
                </td>
                <td class="user-info">
                  <img :src="user.avatar" alt="User Avatar" class="avatar" />
                  <div class="user-details">
                    <div class="user-name">{{ user.name }}</div>
                    <div class="user-email">{{ user.email }}</div>
                  </div>
                </td>
                <td>
                  <div class="role-badges">
                    <span
                      v-for="role in user.roles"
                      :key="role"
                      :class="['badge', 
                        role === 'Manager' ? 'manager' : 
                        role === 'Admin' ? 'admin' : 
                        role === 'Editor' ? 'editor' : '']"
                    >
                      {{ role }}
                    </span>
                    <span v-if="user.lastLoggedIn" class="last-login-badge">
                      last logged in
                    </span>
                  </div>
                </td>
                <td>
                  <span :class="['status-badge', user.status === 'Available' ? 'available' : 'busy']">
                    {{ user.status }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button class="action-btn edit" @click="editUser(user)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                      <span>Edit</span>
                    </button>
                    <button v-if="user.active" class="action-btn deactivate" @click="toggleUserActive(user)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="8" y1="12" x2="16" y2="12"></line>
                      </svg>
                      <span>Deactivate</span>
                    </button>
                    <button v-else class="action-btn activate" @click="toggleUserActive(user)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="16"></line>
                        <line x1="8" y1="12" x2="16" y2="12"></line>
                      </svg>
                      <span>Activate</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mobile-view">
      <div v-for="user in paginatedUsers" :key="user.id" class="user-card">
        <div class="user-card-header">
          <div class="user-info">
            <img :src="user.avatar" alt="User Avatar" class="user-avatar" />
            <div class="user-details">
              <div class="user-name">{{ user.name }}</div>
              <div class="user-email">{{ user.email }}</div>
            </div>
          </div>
          <div class="user-status">
            <span :class="['status-badge', user.status === 'Available' ? 'available' : 'busy']">
              {{ user.status }}
            </span>
          </div>
        </div>
        
        <div class="user-card-body">
          <div class="user-roles">
            <span 
              v-for="role in user.roles" 
              :key="role"
              :class="['badge', 
                role === 'Manager' ? 'manager' : 
                role === 'Admin' ? 'admin' : 
                role === 'Editor' ? 'editor' : '']"
            >
              {{ role }}
            </span>
          </div>
          
          <div class="user-actions">
            <button class="action-btn edit" @click="editUser(user)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              <span>Edit</span>
            </button>
            <button v-if="user.active" class="action-btn deactivate" @click="toggleUserActive(user)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="8" y1="12" x2="16" y2="12"></line>
              </svg>
              <span>Deactivate</span>
            </button>
            <button v-else class="action-btn activate" @click="toggleUserActive(user)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="16"></line>
                <line x1="8" y1="12" x2="16" y2="12"></line>
              </svg>
              <span>Activate</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  
        <div class="pagination">
          <button class="pagination-btn first" @click="goToPage(1)" :disabled="currentPage === 1">First</button>
          <button class="pagination-btn prev" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">«</button>
          <template v-for="page in displayedPages" :key="page">
            <button v-if="page === '...'" class="pagination-btn dots">...</button>
            <button v-else 
              :class="['pagination-btn', 'number', page === currentPage ? 'active' : '']" 
              @click="goToPage(page)">
              {{ page }}
            </button>
          </template>
          <button class="pagination-btn next" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">»</button>
          <button class="pagination-btn last" @click="goToPage(totalPages)" :disabled="currentPage === totalPages">Last</button>
        </div>
      </div>
  
      <!-- Add/Edit User Modal -->
      <div v-if="showAddUserModal || showEditUserModal" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>{{ showEditUserModal ? 'Edit User' : 'Add New User' }}</h2>
            <button class="close-btn" @click="closeModals">&times;</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>Name</label>
              <input type="text" v-model="currentUser.name" />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" v-model="currentUser.email" />
            </div>
            <div class="form-group">
              <label>Roles</label>
              <div class="checkbox-group">
                <label>
                  <input type="checkbox" value="Manager" v-model="currentUser.roles" />
                  Manager
                </label>
                <label>
                  <input type="checkbox" value="Admin" v-model="currentUser.roles" />
                  Admin
                </label>
                <label>
                  <input type="checkbox" value="Editor" v-model="currentUser.roles" />
                  Editor
                </label>
              </div>
            </div>
            <div class="form-group">
              <label>Status</label>
              <div class="radio-group">
                <label>
                  <input type="radio" value="Available" v-model="currentUser.status" />
                  Available
                </label>
                <label>
                  <input type="radio" value="Busy" v-model="currentUser.status" />
                  Busy
                </label>
              </div>
            </div>
            <div class="form-group">
              <label>Account Status</label>
              <div class="radio-group">
                <label>
                  <input type="radio" :value="true" v-model="currentUser.active" />
                  Active
                </label>
                <label>
                  <input type="radio" :value="false" v-model="currentUser.active" />
                  Inactive
                </label>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="closeModals">Cancel</button>
            <button class="save-btn" @click="saveUser">
              {{ showEditUserModal ? 'Save Changes' : 'Add User' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: '',
        selectAll: false,
        showAddUserModal: false,
        showEditUserModal: false,
        currentPage: 1,
        itemsPerPage: 5,
        currentUser: {
          name: '',
          email: '',
          roles: [],
          status: 'Available',
          active: true
        },
        editingUserId: null,
        users: [
          {
            id: 1,
            name: 'Taras Rozales',
            email: 'taras@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Manager', 'Admin', 'Editor'],
            lastLoggedIn: true,
            status: 'Available',
            active: true,
            selected: false
          },
          {
            id: 2,
            name: 'Vernon Nepdayshvk',
            email: 'vernon@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Manager', 'Admin'],
            lastLoggedIn: false,
            status: 'Busy',
            active: true,
            selected: false
          },
          {
            id: 3,
            name: 'Tylan Collins',
            email: 'tylan@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Admin', 'Editor'],
            lastLoggedIn: false,
            status: 'Available',
            active: false,
            selected: false
          },
          {
            id: 4,
            name: 'Adeeva Apsharlie',
            email: 'adeeva@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Admin', 'Editor'],
            lastLoggedIn: true,
            status: 'Busy',
            active: true,
            selected: false
          },
          {
            id: 5,
            name: 'Adriana Hejlm',
            email: 'adriana@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Manager'],
            lastLoggedIn: false,
            status: 'Available',
            active: true,
            selected: false
          },
          {
            id: 6,
            name: 'Szalvko Bezukinds',
            email: 'szalvko@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Editor'],
            lastLoggedIn: false,
            status: 'Busy',
            active: false,
            selected: false
          },
          {
            id: 7,
            name: 'Uteh Isadev',
            email: 'uteh@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Editor'],
            lastLoggedIn: true,
            status: 'Available',
            active: true,
            selected: false
          },
          {
            id: 8,
            name: 'Noell El-Ayen',
            email: 'noell@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Editor'],
            lastLoggedIn: false,
            status: 'Busy',
            active: true,
            selected: false
          },
          {
            id: 9,
            name: 'Jane Smith',
            email: 'jane@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Admin'],
            lastLoggedIn: false,
            status: 'Available',
            active: true,
            selected: false
          },
          {
            id: 10,
            name: 'John Doe',
            email: 'john@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Manager', 'Editor'],
            lastLoggedIn: true,
            status: 'Busy',
            active: true,
            selected: false
          },
          {
            id: 11,
            name: 'Emily Johnson',
            email: 'emily@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Editor'],
            lastLoggedIn: false,
            status: 'Available',
            active: false,
            selected: false
          },
          {
            id: 12,
            name: 'Michael Brown',
            email: 'michael@example.com',
            avatar: require('@/assets/Avatar.png'),
            roles: ['Admin'],
            lastLoggedIn: true,
            status: 'Busy',
            active: true,
            selected: false
          }
        ]
      };
    },
    computed: {
      filteredUsers() {
        if (!this.searchQuery) {
          return this.users;
        }
        
        const query = this.searchQuery.toLowerCase();
        return this.users.filter(user => 
          user.name.toLowerCase().includes(query) || 
          user.email.toLowerCase().includes(query) ||
          user.roles.some(role => role.toLowerCase().includes(query)) ||
          user.status.toLowerCase().includes(query)
        );
      },
      totalPages() {
        return Math.ceil(this.filteredUsers.length / this.itemsPerPage);
      },
      paginatedUsers() {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.filteredUsers.slice(startIndex, endIndex);
      },
      displayedPages() {
        const pages = [];
        const maxVisiblePages = 5;
        
        if (this.totalPages <= maxVisiblePages) {
          // Show all pages if there are few
          for (let i = 1; i <= this.totalPages; i++) {
            pages.push(i);
          }
        } else {
          // Always show first page
          pages.push(1);
          
          // Current page neighborhood
          let startPage = Math.max(2, this.currentPage - 1);
          let endPage = Math.min(this.totalPages - 1, this.currentPage + 1);
          
          // Add ellipsis if needed
          if (startPage > 2) {
            pages.push('...');
          }
          
          // Add pages around current
          for (let i = startPage; i <= endPage; i++) {
            pages.push(i);
          }
          
          // Add ellipsis if needed
          if (endPage < this.totalPages - 1) {
            pages.push('...');
          }
          
          // Always show last page
          pages.push(this.totalPages);
        }
        
        return pages;
      }
    },
    methods: {
      toggleSelectAll() {
        this.users.forEach(user => {
          user.selected = this.selectAll;
        });
      },
      goToPage(page) {
        if (page >= 1 && page <= this.totalPages) {
          this.currentPage = page;
        }
      },
      closeModals() {
        this.showAddUserModal = false;
        this.showEditUserModal = false;
        this.resetCurrentUser();
      },
      resetCurrentUser() {
        this.currentUser = {
          name: '',
          email: '',
          roles: [],
          status: 'Available',
          active: true
        };
        this.editingUserId = null;
      },
      editUser(user) {
        this.editingUserId = user.id;
        this.currentUser = {
          name: user.name,
          email: user.email,
          roles: [...user.roles],
          status: user.status,
          active: user.active
        };
        this.showEditUserModal = true;
      },
      toggleUserActive(user) {
        const index = this.users.findIndex(u => u.id === user.id);
        if (index !== -1) {
          this.users[index].active = !this.users[index].active;
        }
      },
      saveUser() {
        if (this.currentUser.name && this.currentUser.email && this.currentUser.roles.length > 0) {
          if (this.showEditUserModal && this.editingUserId) {
            // Update existing user
            const index = this.users.findIndex(u => u.id === this.editingUserId);
            if (index !== -1) {
              this.users[index] = {
                ...this.users[index],
                name: this.currentUser.name,
                email: this.currentUser.email,
                roles: [...this.currentUser.roles],
                status: this.currentUser.status,
                active: this.currentUser.active
              };
            }
          } else {
            // Add new user
            const newId = Math.max(...this.users.map(u => u.id)) + 1;
            this.users.push({
              id: newId,
              name: this.currentUser.name,
              email: this.currentUser.email,
              avatar: '/api/placeholder/40/40',
              roles: [...this.currentUser.roles],
              lastLoggedIn: false,
              status: this.currentUser.status,
              active: this.currentUser.active,
              selected: false
            });
          }
          
          this.closeModals();
        }
      }
    }
  };
  </script>
  
  <style>

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .header-left {
    width: 100%;
    justify-content: space-between;
  }

  .user-profile {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 0.75rem;
  }

  .logo-name {
    display: none; /* Hide logo text on very small screens */
  }

  .sidebar-logo2 {
    height: 24px;
    max-width: 24px;
  }
}

.back-to-dashboard {
  display: flex;
  align-items: center;
  background-color: transparent;
  color: #ff3e3e;
  border: 1px solid rgba(255, 62, 62, 0.2);
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  width: 40px; /* Fixed width for icon */
  text-decoration: none !important;
  font-size: 0.8rem;
}

.back-to-dashboard i {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.back-to-dashboard .back-text {
  white-space: nowrap;
  opacity: 0;
  width: 0;
  transition: all 0.3s ease;
  margin-left: 0;
}

.back-to-dashboard:hover {
  width: 200px; /* Expanded width */
  background-color: rgba(255, 62, 62, 0.1);
}

.back-to-dashboard:hover .back-text {
  opacity: 1;
  width: auto;
  margin-right: 1.5rem;
}

@media (max-width: 768px) {
  .back-to-dashboard {
    width: 40px;
  }

  .back-to-dashboard:hover {
    width: 180px;
  }
}

@media (max-width: 480px) {
  .back-to-dashboard {
    width: 40px;
  }

  .back-to-dashboard:hover {
    width: 150px;
  }
}

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  
  .dashboard {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  
  /* Dark Mode Styles */
  .dark-mode {
    background-color: #1a1a1a;
    color: #f5f5f5;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1.5rem;
    background-color: #151515;
    color: white;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .logo-section {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .logo-text {
    font-weight: 600;
    font-size: 1.125rem;
    color: #ff3e3e;
  }

  .logo {
      display: flex;
      align-items: center;
      
      img {
        height: 40px;
        margin-right: 10px;
      }
  
      span {
        font-weight: 700;
        color : red;
        -webkit-background-clip: text;
      }
    }
  
  .user-profile {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .avatar {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ff3e3e;
  }
  
  .content {
    padding: 1.5rem;
    background-color: #1a1a1a;
    flex: 1;
  }
  
  .page-header {
    margin-bottom: 1.5rem;
  }
  
  .breadcrumb {
    color: #999;
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }
  
  .title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #ffffff;
  }
  
  .search-add {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
  }
  
  .search-bar {
    display: flex;
    align-items: center;
    position: relative;
    width: 300px;
  }
  
  .search-bar input {
    width: 100%;
    padding: 0.625rem 2.5rem 0.625rem 1rem;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 0.875rem;
    background-color: #252525;
    color: #f5f5f5;
  }
  
  .search-button {
    position: absolute;
    right: 0.5rem;
    background: none;
    border: none;
    color: #999;
    cursor: pointer;
  }
  
  .add-user-btn {
    padding: 0.625rem 1rem;
    background-color: #ff3e3e;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .add-user-btn:hover {
    background-color: #d63030;
  }
  
  .user-table {
    background: #252525;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th {
    padding: 1rem;
    text-align: left;
    font-weight: 500;
    color: #f5f5f5;
    border-bottom: 1px solid #333;
    background-color: #202020;
  }
  
  td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #333;
  }
  
  .checkbox-column {
    width: 40px;
  }
  
  input[type="checkbox"] {
    accent-color: #ff3e3e;
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
  
  .showing-text {
    color: #999;
    font-size: 0.75rem;
    font-style: italic;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .user-avatar {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #444;
  }
  
  .user-details {
    display: flex;
    flex-direction: column;
  }
  
  .user-name {
    font-weight: 500;
    color: #f5f5f5;
  }
  
  .user-email {
    color: #999;
    font-size: 0.75rem;
  }
  
  .role-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  .badge {
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .manager {
    background-color: #ff3e3e;
    color: white;
  }
  
  .admin {
    background-color: #343434;
    color: #f5f5f5;
    border: 1px solid #444;
  }
  
  .editor {
    background-color: #555555;
    color: #f5f5f5;
  }
  
  .status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .available {
    background-color: #3e9c35;
    color: white;
  }
  
  .busy {
    background-color: #d63030;
    color: white;
  }
  
  .last-login-badge {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    color: #999;
    font-style: italic;
  }
  
  .action-buttons {
    display: flex;
    gap: 0.5rem;
  }
  
  .action-btn {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.375rem 0.75rem;
    border-radius: 4px;
    border: none;
    font-size: 0.75rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .edit {
    background-color: #444;
    color: #f5f5f5;
  }
  
  .edit:hover {
    background-color: #555;
  }
  
  .deactivate {
    background-color: #d63030;
    color: white;
  }
  
  .deactivate:hover {
    background-color: #c52828;
  }
  
  .activate {
    background-color: #3e9c35;
    color: white;
  }
  
  .activate:hover {
    background-color: #348b2d;
  }
  
  .pagination {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
    justify-content: flex-end;
  }
  
  .pagination-info {
    color: #999;
    font-size: 0.75rem;
    margin-right: 0.5rem;
  }
  
  .pagination-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #444;
    background-color: #252525;
    color: #f5f5f5;
    border-radius: 4px;
    font-size: 0.75rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .pagination-btn.active {
    background-color: #ff3e3e;
    color: white;
    border-color: #ff3e3e;
  }
  
  .pagination-btn:hover:not(.active):not(:disabled) {
    background-color: #333;
  }
  
  .pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .pagination-btn.dots {
    border: none;
    background: none;
  }
  
  /* Modal Styles */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: #252525;
    border-radius: 8px;
    width: 500px;
    max-width: 90%;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  }
  
  .modal-header {
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #333;
    background-color: #202020;
  }
  
  .modal-header h2 {
    color: #ff3e3e;
    font-size: 1.25rem;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #999;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1.25rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #f5f5f5;
  }
  
  .form-group input[type="text"],
  .form-group input[type="email"] {
    width: 100%;
    padding: 0.625rem;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #333;
    color: #f5f5f5;
  }
  
  .checkbox-group, .radio-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .checkbox-group label, .radio-group label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: normal;
    cursor: pointer;
  }
  
  input[type="radio"] {
    accent-color: #ff3e3e;
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
  
  .modal-footer {
    padding: 1rem;
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    border-top: 1px solid #333;
    background-color: #202020;
  }
  
  .cancel-btn {
    padding: 0.625rem 1rem;
    background-color: #444;
    color: #f5f5f5;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .cancel-btn:hover {
    background-color: #555;
  }
  
  .save-btn {
    padding: 0.625rem 1rem;
    background-color: #ff3e3e;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .save-btn:hover {
    background-color: #d63030;
  }

  .sidebar-logo2 {
  height: 30px;
  max-width: 30px;
  object-fit: contain;
  transition: opacity 0.3s ease;
}

.user-table {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
}

@media (max-width: 768px) {
  .desktop-view {
    display: none;
  }

  .mobile-view {
    display: block;
  }

  .user-card {
    background-color: #252525;
    border-radius: 8px;
    margin-bottom: 1rem;
    padding: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  }

  .user-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    border-bottom: 1px solid #333;
    padding-bottom: 1rem;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .user-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #444;
  }

  .user-name {
    font-weight: 600;
    color: #f5f5f5;
  }

  .user-email {
    color: #999;
    font-size: 0.875rem;
  }

  .user-card-body {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .user-roles {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .user-actions {
    display: flex;
    gap: 0.5rem;
  }

  .action-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.5rem;
    border-radius: 4px;
  }
}

@media (min-width: 769px) {
  .mobile-view {
    display: none;
  }
}

@media (max-width: 768px) {
  .header {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    gap: 1rem;
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .user-profile {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
}

/* Additional responsive adjustments */
@media (max-width: 480px) {
  .header {
    padding: 0.75rem;
    gap: 0.5rem;
  }

  .back-to-dashboard {
    padding: 0.25rem 0.5rem;
  }

  .logo-name {
    display: none; /* Optional: hide logo text on very small screens */
  }

  .sidebar-logo2 {
    max-width: 24px;
    max-height: 24px;
  }

  .user-name {
    font-size: 14px;
  }
}

  </style>
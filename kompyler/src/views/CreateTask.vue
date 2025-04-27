<template>
  <div class="wrapper">
    <ResponsiveSidebar/>
    <div class="content-wrapper">
      <div class="dashboard-container">
        <div class="dashboard-header sticky-header">
          <h4 class="title">Team Management & Task Creation</h4>
          <p class="description">Manage your team members and create new tasks efficiently.</p>
        </div>
        
        <!-- Team Members Section -->
        <div class="card team-card">
          <div class="card-header">
            <h3>Team Members</h3>
            <button class="btn-primary" @click="showAddMemberModal">
              <i class="fas fa-plus"></i> Add Member
            </button>
          </div>
          <div class="card-content">
            <div class="table-container" v-if="teamMembers.length > 0">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Total Tasks</th>
                    <th>Pending</th>
                    <th>Completed</th>
                    <th>Postponed</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="member in teamMembers" :key="member.name" @click="showMemberTasks(member)" class="member-row">
                    <td>
                      <div class="member-info">
                        <div class="avatar">{{ member.name.split(' ').map(n => n[0]).join('') }}</div>
                        <span>{{ member.name }}</span>
                      </div>
                    </td>
                    <td>{{ member.role }}</td>
                    <td>
                      <div class="task-count">{{ member.tasks }}</div>
                    </td>
                    <td>
                      <div class="stat pending">
                        <i class="fas fa-clock"></i> {{ getTaskStats(member.id).pending }}
                      </div>
                    </td>
                    <td>
                      <div class="stat completed">
                        <i class="fas fa-check"></i> {{ getTaskStats(member.id).completed }}
                      </div>
                    </td>
                    <td>
                      <div class="stat postponed">
                        <i class="fas fa-clock"></i> {{ getTaskStats(member.id).postponed }}
                      </div>
                    </td>
                    <td>
                      <span class="status-badge" :class="getMemberStatus(member).class">
                        {{ getMemberStatus(member).text }}
                      </span>
                    </td>
                    <td>
                      <div class="action-buttons">
                        <button class="btn-icon" @click.stop="editMember(member)">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-icon btn-danger" @click.stop="deleteMember(member)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else>
              <p>No team members found. Please add members to manage tasks.</p>
            </div>
          </div>
        </div>

        <div class="dashboard-grid">
          <!-- Task Creation Form -->
          <div class="card task-card">
            <div class="card-header">
              <h3>Create New Task</h3>
            </div>
            <div class="card-content">
              <form @submit.prevent="createTask">
                <div class="form-group">
                  <label>Task Title</label>
                  <input type="text" class="form-input" v-model="newTask.title" required placeholder="Enter task title">
                </div>
                
                <div class="form-group">
                  <label>Description</label>
                  <textarea class="form-input" rows="3" v-model="newTask.description" required placeholder="Describe the task details"></textarea>
                </div>
                
                <div class="form-row">
                  <div class="form-group">
                    <label>Assign To</label>
                    <select class="form-input dropdown-red-black" v-model="newTask.assignedTo" required>
                      <option value="" disabled selected>Select team member</option>
                      <option v-for="member in teamMembers" :key="member.id" :value="member.name">
                        {{ member.name }} ({{ member.tasks }} tasks)
                      </option>
                    </select>
                  </div>
                  
                  <div class="form-group">
                    <label>Due Date</label>
                    <input type="date" class="form-input" v-model="newTask.dueDate" required>
                  </div>
                </div>
                
                <div class="form-group">
                  <label>Priority Level</label>
                  <div class="priority-selector">
                    <div v-for="priority in ['minor', 'mid', 'major']" :key="priority"
                         class="priority-option" 
                         :class="{ active: newTask.priority === priority }"
                         @click="newTask.priority = priority">
                      <div class="priority-indicator" :class="priority"></div>
                      <span>{{ priority.charAt(0).toUpperCase() + priority.slice(1) }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="form-actions">
                  <button type="button" class="btn-secondary">
                    Cancel
                  </button>
                  <button type="submit" class="btn-primary">
                    <i class="fas fa-plus"></i> Create Task
                  </button>
                </div>
              </form>
            </div>
          </div>
          
          <!-- Recent Activity -->
          <div class="card activity-card">
            <div class="card-header">
              <h3>Recent Activity</h3>
            </div>
            <div class="card-content">
              <div class="activity-timeline">
                <div v-for="(activity, index) in activities" :key="index" class="activity-item">
                  <div :class="['activity-icon', getActivityIcon(activity.type)]">
                    <i :class="getActivityIconClass(activity.type)"></i>
                  </div>
                  <div class="activity-content">
                    <div class="activity-title">
                      {{ activity.title }}
                      <span v-if="activity.type === 'task' || activity.type === 'delete'" 
                            :class="['activity-badge', getTaskStatusClass(activity)]">
                        {{ getTaskStatusText(activity) }}
                      </span>
                    </div>
                    <div class="activity-meta">
                      <span class="activity-user">{{ activity.user }}</span>
                      <span class="activity-timestamp">{{ formatTimeAgo(activity.time) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Custom Modal for Add/Edit Member -->
  <div v-if="showModal" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>{{ isEditing ? 'Edit Team Member' : 'Add Team Member' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Name</label>
          <input v-model="newMember.name" type="text" class="form-input" required 
                 placeholder="Enter member name">
        </div>
        <div class="form-group">
          <label>Role</label>
          <input v-model="newMember.role" type="text" class="form-input" required 
                 placeholder="Enter member role">
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-primary">
            {{ isEditing ? 'Update Member' : 'Add Member' }}
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Add new Modal for Member Tasks -->
  <div v-if="showTasksModal" class="modal">
    <div class="modal-content task-details-modal">
      <span class="close" @click="closeTasksModal">&times;</span>
      
      <div class="member-task-header">
        <div class="member-info-large">
          <div class="avatar large">
            {{ selectedMember?.name.split(' ').map(n => n[0]).join('') }}
          </div>
          <div class="member-details">
            <h2>{{ selectedMember?.name }}</h2>
            <span class="member-role">{{ selectedMember?.role }}</span>
          </div>
        </div>
        <div class="task-stats">
          <span class="stat-label">Total Tasks</span>
          <span class="stat-value">{{ selectedMember?.tasks || 0 }}</span>
        </div>
      </div>

      <div class="tasks-list" v-if="memberTasks.length > 0">
        <div v-for="task in memberTasks" :key="task.id" class="task-item">
          <div class="task-header">
            <div class="task-title-section">
              <h3>{{ task.title }}</h3>
              <span class="task-creation-date">Created: {{ formatDate(task.createdAt) }}</span>
            </div>
            <div class="task-badges">
              <span class="task-priority" :class="task.priority">
                <i class="fas fa-flag"></i> {{ task.priority }}
              </span>
              <span class="task-status" :class="task.status">
                {{ task.status }}
              </span>
            </div>
          </div>
          <div class="task-description">
            <p>{{ task.description }}</p>
          </div>
          <div class="task-meta">
            <div class="task-dates">
              <span class="countdown" :class="getTimeStatus(task.dueDate)">
                {{ getTimeRemaining(task.dueDate) }}
              </span>
            </div>
            <div class="task-actions">
              <button v-if="task.status !== 'completed'" 
                      class="action-btn complete" 
                      @click="completeTask(task)">
                <i class="fas fa-check"></i> Complete
              </button>
              <button v-if="task.status === 'pending'" 
                      class="action-btn postpone" 
                      @click="postponeTask(task)">
                <i class="fas fa-clock"></i> Postpone
              </button>
              <button class="action-btn delete" 
                      @click="deleteTask(task)">
                <i class="fas fa-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-tasks">
        <i class="fas fa-clipboard-list no-tasks-icon"></i>
        <p class="no-tasks-title">No Tasks Yet</p>
        <p class="no-tasks-message">This team member hasn't been assigned any tasks.</p>
      </div>
    </div>
  </div>
</template>

<script>
import ResponsiveSidebar from '@/components/ResponsiveSidebar.vue';

export default {
  name: 'CreateTask',
  components: {
    ResponsiveSidebar
  },
  data() {
    return {
      teamMembers: [],
      showModal: false,
      isEditing: false,
      selectedMember: null,
      newMember: {
        name: '',
        role: '',
        tasks: 0
      },
      showDeleteModal: false,
      memberToDelete: null,
      newTask: {
        title: '',
        description: '',
        assignedTo: '',
        dueDate: '',
        priority: 'mid',
        status: 'pending'
      },
      showTasksModal: false,
      memberTasks: [],
      activities: []
    }
  },
  created() {
    this.loadTeamMembers();
    this.loadActivities();
  },
  methods: {
    loadTeamMembers() {
      const savedMembers = localStorage.getItem('teamMembers');
      this.teamMembers = savedMembers ? JSON.parse(savedMembers) : [];
    },
    saveTeamMembers() {
      localStorage.setItem('teamMembers', JSON.stringify(this.teamMembers));
    },
    showAddMemberModal() {
      this.isEditing = false;
      this.selectedMember = null;
      this.newMember = { name: '', role: '', tasks: 0 };
      this.showModal = true;
    },
    editMember(member) {
      this.isEditing = true;
      this.selectedMember = member;
      this.newMember = { ...member };
      this.showModal = true;
    },
    async deleteMember(member) {
      const result = await Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ff0000',
        cancelButtonColor: '#1a1a1a',
        confirmButtonText: 'Yes, delete it!',
        background: '#1a1a1a',
        color: '#ffffff'
      });

      if (result.isConfirmed) {
        this.teamMembers = this.teamMembers.filter(m => m.name !== member.name);
        this.saveTeamMembers();
        
        Swal.fire({
          icon: 'success',
          title: 'Deleted!',
          text: 'Team member has been deleted.',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });

        const activity = {
          type: 'delete',
          title: `Team member ${member.name} removed`,
          user: 'Admin',
          time: new Date().toISOString(),
          isNew: true // Mark as new
        };
        this.addActivity(activity);
      }
    },
    handleSubmit() {
      if (!this.newMember.name || !this.newMember.role) {
        Swal.fire({
          icon: 'error',
          title: 'Error!',
          text: 'Please fill in all fields',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
        return;
      }

      const newMemberData = {
        id: Date.now(), // Add unique ID
        name: this.newMember.name,
        role: this.newMember.role,
        tasks: 0, // Explicitly set initial tasks to 0
        createdAt: new Date().toISOString()
      };

      if (this.isEditing && this.selectedMember) {
        const index = this.teamMembers.findIndex(m => m.id === this.selectedMember.id);
        if (index !== -1) {
          this.teamMembers[index] = { ...this.teamMembers[index], ...newMemberData };
        }
      } else {
        this.teamMembers.push(newMemberData);
      }
      
      this.saveTeamMembers();
      this.closeModal();
      
      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: 'Team member updated successfully',
        background: '#1a1a1a',
        color: '#ffffff',
        confirmButtonColor: '#ff0000'
      });

      const activity = {
        type: 'member',
        title: `${this.isEditing ? 'Updated' : 'Added new'} team member ${this.newMember.name}`,
        user: 'Admin',
        time: new Date().toISOString(),
        isNew: true // Mark as new
      };
      this.addActivity(activity);
    },
    async createTask() {
      try {
        // Validate assigned member exists
        const member = this.teamMembers.find(m => m.name === this.newTask.assignedTo);
        if (!member) {
          Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: 'Please select a valid team member',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonColor: '#ff0000'
          });
          return;
        }

        const taskData = {
          id: Date.now(),
          title: this.newTask.title,
          description: this.newTask.description,
          priority: this.newTask.priority,
          dueDate: this.newTask.dueDate,
          assignedTo: member.id, // Use member ID instead of name
          status: 'pending',
          createdAt: new Date().toISOString()
        };

        // Get existing tasks
        let existingTasks = [];
        try {
          existingTasks = JSON.parse(localStorage.getItem('allTasks')) || [];
        } catch (e) {
          console.error('Error parsing existing tasks:', e);
          existingTasks = [];
        }

        // Add new task
        const updatedTasks = [...existingTasks, taskData];
        localStorage.setItem('allTasks', JSON.stringify(updatedTasks));

        // Update member's task count
        const memberIndex = this.teamMembers.findIndex(m => m.id === member.id);
        if (memberIndex !== -1) {
          this.teamMembers[memberIndex].tasks++;
          this.saveTeamMembers();
        }

        // Show success modal first
        await Swal.fire({
          icon: 'success',
          title: 'Task Created Successfully!',
          html: `
            <div style="text-align: left; color: #ffffff;">
              <p style="margin: 10px 0;"><span style="color: #10b981;">✓</span> Title: ${taskData.title}</p>
              <p style="margin: 10px 0;"><span style="color: #10b981;">✓</span> Assigned to: ${member.name}</p>
              <p style="margin: 10px 0;"><span style="color: #10b981;">✓</span> Priority: ${taskData.priority}</p>
              <p style="margin: 10px 0;"><span style="color: #10b981;">✓</span> Due date: ${new Date(taskData.dueDate).toLocaleDateString()}</p>
            </div>
          `,
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#10b981',
          confirmButtonText: 'Done'
        });

        // Reset form after success
        this.newTask = {
          title: '',
          description: '',
          assignedTo: '',
          dueDate: '',
          priority: 'mid',
          status: 'pending'
        };

        // Add to activity log
        this.addActivity({
          type: 'task',
          title: `New task "${taskData.title}" assigned to ${member.name}`,
          user: 'System',
          time: new Date().toISOString(),
          status: 'pending'
        });

        // Emit event to update dashboard
        this.$emit('task-created', taskData);

      } catch (error) {
        console.error('Error creating task:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error Creating Task',
          text: 'There was a problem creating the task. Please try again.',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
      }
    },
    closeModal() {
      this.showModal = false;
      this.selectedMember = null;
      this.newMember = { name: '', role: '', tasks: 0 };
      this.isEditing = false;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.memberToDelete = null;
    },
    showMemberTasks(member) {
      this.selectedMember = member;
      this.memberTasks = this.loadMemberTasks(member.id);
      this.memberTaskStats = this.getTaskStats(member.id);
      this.showTasksModal = true;
    },
    loadMemberTasks(memberId) {
      try {
        const allTasks = JSON.parse(localStorage.getItem('allTasks')) || [];
        const memberTasks = allTasks.filter(task => Number(task.assignedTo) === Number(memberId));
        
        console.log(`Loading tasks for member ${memberId}:`, memberTasks);
        
        return memberTasks.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      } catch (error) {
        console.error('Error loading member tasks:', error);
        return [];
      }
    },
    closeTasksModal() {
      this.showTasksModal = false;
      this.selectedMember = null;
      this.memberTasks = [];
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    getTimeRemaining(dueDate) {
      const now = new Date();
      const due = new Date(dueDate);
      const diff = due - now;
      
      // For overdue tasks
      if (diff < 0) {
        const absDiff = Math.abs(diff);
        const days = Math.floor(absDiff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((absDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((absDiff % (1000 * 60 * 60)) / (1000 * 60));
        return `${days}d ${hours}h ${minutes}m overdue`;
      }
      
      // For upcoming tasks
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      
      if (days === 0 && hours === 0 && minutes === 0) return 'Due now';
      if (days === 0) return `${hours}h ${minutes}m remaining`;
      return `${days}d ${hours}h ${minutes}m remaining`;
    },
    getTimeStatus(dueDate) {
      const now = new Date();
      const due = new Date(dueDate);
      const diff = due - now;
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      
      if (diff < 0) return 'overdue';
      if (days <= 1) return 'urgent';
      if (days <= 3) return 'warning';
      return 'normal';
    },
    async completeTask(task) {
      const result = await Swal.fire({
        title: 'Complete Task',
        text: 'Are you sure you want to mark this task as completed?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#10b981',
        cancelButtonColor: '#1a1a1a',
        confirmButtonText: 'Yes, complete it!',
        background: '#1a1a1a',
        color: '#ffffff'
      });

      if (result.isConfirmed) {
        this.updateTaskStatus(task, 'completed');
        await Swal.fire({
          icon: 'success',
          title: 'Task Completed!',
          text: 'The task has been marked as completed.',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#10b981'
        });
      }
    },

    async postponeTask(task) {
      const { value: formValues } = await Swal.fire({
        title: 'Postpone Task',
        html: `
          <div class="postpone-form">
            <input type="datetime-local" id="postpone-date" class="swal2-input" style="background: #1a1a1a; color: #fff; border: 1px solid rgba(141, 0, 0, 0.519);">
          </div>
        `,
        background: '#1a1a1a',
        color: '#ffffff',
        confirmButtonColor: '#f59e0b',
        showCancelButton: true,
        cancelButtonColor: '#1a1a1a',
        preConfirm: () => {
          const date = document.getElementById('postpone-date').value;
          if (!date) {
            Swal.showValidationMessage('Please select a date and time');
            return false;
          }
          return date;
        }
      });

      if (formValues) {
        const newDueDate = new Date(formValues);
        task.dueDate = newDueDate.toISOString();
        task.status = 'postponed';
        this.updateTaskStatus(task, 'postponed');
        
        await Swal.fire({
          icon: 'success',
          title: 'Task Postponed!',
          text: `The task has been postponed to ${this.formatDate(newDueDate)}`,
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#f59e0b'
        });
      }
    },

    async cancelTask(task) {
      const result = await Swal.fire({
        title: 'Cancel Task',
        text: 'Are you sure you want to cancel this task?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#1a1a1a',
        confirmButtonText: 'Yes, cancel it!',
        background: '#1a1a1a',
        color: '#ffffff'
      });

      if (result.isConfirmed) {
        this.updateTaskStatus(task, 'cancelled');
        // Decrease the team member's task count
        const memberIndex = this.teamMembers.findIndex(m => m.name === task.assignedTo);
        if (memberIndex !== -1) {
          this.teamMembers[memberIndex].tasks--;
          this.saveTeamMembers();
        }
        
        await Swal.fire({
          icon: 'success',
          title: 'Task Cancelled!',
          text: 'The task has been cancelled.',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ef4444'
        });
      }
    },

    async deleteTask(task) {
      try {
        const result = await Swal.fire({
          title: 'Delete Task',
          text: 'Are you sure you want to delete this task? This action cannot be undone.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#ef4444',
          cancelButtonColor: '#1a1a1a',
          confirmButtonText: 'Yes, delete it!',
          background: '#1a1a1a',
          color: '#ffffff'
        });
    
        if (result.isConfirmed) {
          // Get current tasks from correct storage key
          const allTasks = JSON.parse(localStorage.getItem('allTasks') || '[]');
          const updatedTasks = allTasks.filter(t => t.id !== task.id);
          localStorage.setItem('allTasks', JSON.stringify(updatedTasks));
          
          // Find and update team member's task count
          const teamMembers = JSON.parse(localStorage.getItem('teamMembers') || '[]');
          const memberIndex = teamMembers.findIndex(m => m.id === task.assignedTo);
          
          if (memberIndex !== -1) {
            teamMembers[memberIndex].tasks = Math.max(0, teamMembers[memberIndex].tasks - 1);
            localStorage.setItem('teamMembers', JSON.stringify(teamMembers));
            
            // Update local teamMembers array
            this.teamMembers = teamMembers;

            // Update selected member if this task belonged to them
            if (this.selectedMember && this.selectedMember.id === task.assignedTo) {
              this.selectedMember = teamMembers[memberIndex];
            }
          }
          
          // Update local task list
          this.memberTasks = this.memberTasks.filter(t => t.id !== task.id);
          
          // Add activity
          this.addActivity({
            type: 'delete',
            title: `Task "${task.title}" deleted`,
            user: 'System',
            time: new Date().toISOString(),
            status: 'deleted'
          });
          
          await Swal.fire({
            icon: 'success',
            title: 'Task Deleted!',
            text: 'The task has been permanently deleted.',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonColor: '#ef4444'
          });
        }
      } catch (error) {
        console.error('Error deleting task:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to delete task. Please try again.',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
      }
    },
    updateTaskStatus(task, status) {
      try {
        // Get all tasks from localStorage
        const allTasks = JSON.parse(localStorage.getItem('allTasks') || '[]');
        const taskIndex = allTasks.findIndex(t => t.id === task.id);
        
        if (taskIndex !== -1) {
          // Update task status in allTasks
          allTasks[taskIndex] = { ...task, status };
          localStorage.setItem('allTasks', JSON.stringify(allTasks));
          
          // Update local task list
          const memberTaskIndex = this.memberTasks.findIndex(t => t.id === task.id);
          if (memberTaskIndex !== -1) {
            this.memberTasks[memberTaskIndex] = { ...task, status };
          }

          // Update member stats
          const member = this.teamMembers.find(m => m.id === task.assignedTo);
          if (member) {
            const memberStats = this.getTaskStats(member.id);
            this.$nextTick(() => {
              // Force stats refresh
              this.loadTeamMembers();
              this.memberTaskStats = memberStats;
            });
          }

          // Add to activity timeline
          const activity = {
            type: 'task',
            title: `Task "${task.title}" ${status}`,
            status: status,
            user: 'Admin',
            time: new Date().toISOString()
          };
          this.addActivity(activity);
        }
      } catch (error) {
        console.error('Error updating task status:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to update task status. Please try again.',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
      }
    },
    getTaskStats(memberId) {
      try {
        const memberTasks = this.loadMemberTasks(memberId);
        return {
          completed: memberTasks.filter(task => task.status === 'completed').length,
          pending: memberTasks.filter(task => task.status === 'pending').length,
          postponed: memberTasks.filter(task => task.status === 'postponed').length,
          total: memberTasks.length
        };
      } catch (error) {
        console.error('Error getting task stats:', error);
        return { completed: 0, pending: 0, postponed: 0, total: 0 };
      }
    },
    getMemberStatus(member) {
      try {
        // Get member's tasks
        const memberTasks = this.loadMemberTasks(member.id);
        
        // Count pending tasks
        const pendingTasks = memberTasks.filter(task => task.status === 'pending').length;
        
        // If there are any pending tasks, member is busy
        if (pendingTasks > 0) {
          return { class: 'busy', text: 'Busy' };
        }
        
        // If no pending tasks (all completed or postponed), member is available
        return { class: 'available', text: 'Available' };
      } catch (error) {
        console.error('Error getting member status:', error);
        return { class: 'available', text: 'Available' };
      }
    },
    loadActivities() {
      const activities = JSON.parse(localStorage.getItem('activities') || '[]');
      this.activities = activities;
    },
    
    getActivityIcon(type) {
      const icons = {
        'task': 'task',
        'member': 'member',
        'status': 'status',
        'edit': 'update',
        'delete': 'alert'
      };
      return icons[type] || 'info';
    },
    
    getActivityIconClass(type) {
      const icons = {
        'task': 'fas fa-tasks',
        'member': 'fas fa-user',
        'status': 'fas fa-info-circle',
        'edit': 'fas fa-edit',
        'delete': 'fas fa-trash'
      };
      return icons[type] || 'fas fa-info';
    },
    
    formatTimeAgo(timestamp) {
      const now = new Date();
      const date = new Date(timestamp);
      const diff = Math.floor((now - date) / 1000);
      
      if (diff < 60) return 'just now';
      if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
      if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
      if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
      return this.formatDate(timestamp);
    },
    
    addActivity(activity) {
      try {
        // Format activity data
        const enhancedActivity = {
          ...activity,
          title: this.formatActivityTitle(activity),
          user: activity.user === 'Admin' ? 'System' : activity.user,
          time: new Date().toISOString()
        };

        // Update activities in localStorage
        const activities = JSON.parse(localStorage.getItem('activities') || '[]');
        activities.unshift(enhancedActivity);
        if (activities.length > 15) {
          activities.length = 15;
        }
        localStorage.setItem('activities', JSON.stringify(activities));
        this.loadActivities();
      } catch (error) {
        console.error('Error in addActivity:', error);
      }
    },

    formatActivityTitle(activity) {
      switch (activity.type) {
        case 'task':
          // Show completed/postponed status if available
          if (activity.status === 'completed') {
            return `Task Completed: ${activity.title}`;
          }
          if (activity.status === 'postponed') {
            return `Task Postponed: ${activity.title}`;
          }
          return `New Task: ${activity.title}`;
        case 'member':
          return `Team Update: ${activity.title}`;
        case 'delete':
          return `Removed: ${activity.title}`;
        default:
          return activity.title;
      }
    },
    isPendingTask(activity) {
      return activity.type === 'task' && (!activity.status || activity.status === 'pending');
    },
    getTaskStatusClass(activity) {
      if (activity.type === 'delete') return 'status-deleted';
      if (activity.status === 'completed') return 'status-completed';
      if (activity.status === 'postponed') return 'status-postponed';
      if (!activity.status || activity.status === 'pending') return 'status-pending';
      return '';
    },

    getTaskStatusText(activity) {
      if (activity.type === 'delete') return 'Deleted';
      if (!activity.status || activity.status === 'pending') return 'Pending';
      return activity.status.charAt(0).toUpperCase() + activity.status.slice(1);
    }
  }
}
</script>

<style scoped>
  .wrapper {
    display: flex;
    width: 100%;
    align-items: stretch;
    min-height: 100vh;
    background: #000000;
    color: #ffffff;
    font-size: 16px;
  }
  
  .content-wrapper {
    padding-left : 5px ;
    width: 100%;
    min-height: 100vh;
    transition: all 0.3s;
    background: #000000;
  }
  
  .dashboard-container {
    padding: 1.5rem;
  }
  
  .dashboard-header {
    margin-bottom: 1.5rem;
    background-color: #000000;
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .sticky-header {
    position: sticky;
    top: 0;
  }
  
  .dashboard-header h1 {
    font-size: 1.75rem;
    font-weight: 500;
    margin: 0;
    color: #ffffff;
  }

  .dashboard-header .description {
    font-size: 1rem;
    color: #9e9e9e;
    margin-top: 0.5rem;
  }
  
  .dashboard-grid {
    display: grid;
    grid-template-columns: 3fr 2fr;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }
  
  .card {
    background-color: #1a1a1a;/* Ensure all cards have the same background */
    border: 1px solid rgba(141, 0, 0, 0.519);
    border-radius: 0.75rem;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background-color: linear-gradient(145deg, #1a1a1a 0%, #0a0a0a 100%);
    border-bottom: 1px solid rgba(141, 0, 0, 0.519);
  }
  
  .card-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    color: #ffffff;
  }
  
  .card-content {
    padding: 1.5rem;
  }
  
  /* Table Styles */
  .table-container {
    overflow-x: auto;
    max-height: 300px; /* Match activity timeline height */
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #ff0000 #1a1a1a;
    padding-right: 0.5rem;
  }
  
  .table-container::-webkit-scrollbar {
    width: 8px; /* Chrome, Safari, Opera */
  }
  
  .table-container::-webkit-scrollbar-track {
    background: #1a1a1a; /* Chrome, Safari, Opera */
  }
  
  .table-container::-webkit-scrollbar-thumb {
    background-color: #ff0000; /* Chrome, Safari, Opera */
    border-radius: 10px; /* Chrome, Safari, Opera */
    border: 3px solid #1a1a1a; /* Chrome, Safari, Opera */
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    background-color: transparent;
  }
  
  th {
    text-align: left;
    padding: 1rem;
    background-color: transparent;
    color: #fff;
    font-weight: 500;
    font-size: 0.875rem;
    border-bottom: 1px solid rgba(141, 0, 0, 0.519);
  }
  
  td {
    padding: 1rem;
    border-bottom: 1px solid rgba(141, 0, 0, 0.519);
    font-size: 0.875rem;
    color: #fff;
  }
  
  .member-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .avatar {
    width: 2.5rem;
    height: 2.5rem;
    background: linear-gradient(to bottom right, #ff0000, #660000);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.875rem;
  }
  
  .status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .status-badge.online {
    background-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }
  
  .status-badge.busy {
    background-color: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }
  
  .status-badge.away {
    background-color: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }
  
  .task-count {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background-color: rgb(152, 0, 0);
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 600;
  }
  
  .action-buttons {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn-icon {
    width: 2rem;
    height: 2rem;
    border-radius: 0.5rem;
    background-color: rgb(152, 0, 0);
    border: none;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-icon:hover {
    background-color: red;
    color: #e6eaef;
  }
  
  .btn-icon.btn-danger:hover {
    background-color: #ef4444;
    color: #ffffff;
  }
  
  /* Form Styles */
  .form-group {
    margin-bottom: 1.25rem;
  }
  
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #fff;
    font-size: 0.875rem;
  }
  
  .form-input {
    width: 100%;
    padding: 0.75rem 1rem;
    background-color: rgba(255, 0, 0, 0.2);
    border: 1px solid rgba(141, 0, 0, 0.519);
    border-radius: 0.5rem;
    color: #ffffff;
    font-size: 0.875rem;
    transition: all 0.2s;
  }
  
  .form-input:focus {
    outline: none;
    background-color: transparent;
    border-color: #ff0000;
    box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.2);
  }
  
  .form-input::placeholder {
    color: #fff;
  }
  
  textarea.form-input {
    resize: vertical;
    min-height: 100px;
  }
  
  .priority-selector {
    display: flex;
    gap: 1rem;
  }
  
  .priority-option {
    flex: 1;
    padding: 0.75rem;
    background-color: transparent;
    border: 1px solid rgba(141, 0, 0, 0.519);
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .priority-option:hover {
    background-color: rgba(141, 0, 0, 0.519);
  }
  
  .priority-option.active {
    background-color: rgba(255, 0, 0, 0.1);
    border-color: #ff0000;
  }
  
  .priority-indicator {
    width: 0.75rem;
    height: 0.75rem;
    border-radius: 50%;
  }
  
  .priority-indicator.minor {
    background-color: #10b981;
  }
  
  .priority-indicator.mid {
    background-color: #f59e0b;
  }
  
  .priority-indicator.major {
    background-color: #ef4444;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .btn-primary {
    background: linear-gradient(to right, #ff0000, #990000);
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .btn-primary:hover {
    background: linear-gradient(to right, #cc0000, #800000);
  }
  
  .btn-secondary {
    background-color: rgba(141, 0, 0, 0.726);
    color: #fff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-secondary:hover {
    background-color: rgba(141, 0, 0, 0.519);
    color: #fff;
  }
  
  /* Activity Timeline */
  .activity-timeline {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    min-height: 400px; /* Set minimum height */
    max-height: 400px; /* Set maximum height */
    overflow-y: auto;
    padding-right: 0.5rem;
    scrollbar-width: thin;
    scrollbar-color: #ff0000 #1a1a1a;
  }
  
  .activity-item {
    display: flex;
    gap: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #2d3748;
    transition: all 0.2s ease;
  }
  
  .activity-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  
  .activity-icon {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  
  .activity-icon.task {
    background-color: rgba(255, 0, 0, 0.2);
    color: #ff0000;
  }
  
  .activity-icon.member {
    background-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }
  
  .activity-icon.comment {
    background-color: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }
  
  .activity-icon.info {
    background-color: rgba(0, 123, 255, 0.2);
    color: #0077ff;
  }

  .activity-icon.tip {
    background-color: rgba(255, 193, 7, 0.2);
    color: #ffc107;
  }

  .activity-icon.alert {
    background-color: rgba(255, 0, 0, 0.2);
    color: #ff0000;
  }

  .activity-icon.update {
    background-color: rgba(40, 167, 69, 0.2);
    color: #28a745;
  }
  
  .activity-content {
    flex-grow: 1;
  }
  
  .activity-title {
    font-weight: 500;
    margin-bottom: 0.25rem;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .activity-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
    color: #fff;
    font-size: 0.75rem;
  }
  
  .activity-user {
    font-weight: 500;
  }
  
  @media (max-width: 992px) {
    .dashboard-grid {
      grid-template-columns: 1fr;
    }
    
    .form-row {
      grid-template-columns: 1fr;
    }
    
    .priority-selector {
      flex-direction: column;
    }
  }
  
  @media (max-width: 768px) {
    .dashboard-container {
      padding: 1rem;
    }
    
    .card-header, .card-content {
      padding: 1rem;
    }
    
    th, td {
      padding: 0.75rem 0.5rem;
    }
    
    .member-info {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.25rem;
    }
    
    .action-buttons {
      flex-direction: column;
    }

  }

  .modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000; /* Ensure the modal is above other content */
  }
  
  .modal-content {
    background: #1a1a1a;
    padding: 2rem;
    border-radius: 0.5rem;
    width: 90%;
    max-width: 500px;
    position: relative;
  }
  
  .close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-size: 1.5rem;
    cursor: pointer;
    color: #fff;
  }

  .status-badge.available {
    background-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }
  
  .status-badge.busy {
    background-color: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }

  .dropdown-red-black {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: 1px solid rgba(141, 0, 0, 0.519) !important;
    -webkit-appearance: none !important;
    -moz-appearance: none !important;
    appearance: none !important;
    background-image: linear-gradient(45deg, transparent 50%, #ff0000 50%),
                      linear-gradient(135deg, #ff0000 50%, transparent 50%) !important;
    background-position: calc(100% - 20px) calc(1em + 2px),
                        calc(100% - 15px) calc(1em + 2px) !important;
    background-size: 5px 5px,
                    5px 5px !important;
    background-repeat: no-repeat !important;
    padding-right: 30px !important;
  }

  .dropdown-red-black option {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: none !important;
  }

  select.dropdown-red-black::-ms-expand {
    display: none;
  }

  /* Style the dropdown when open */
  select.dropdown-red-black:focus {
    border-color: #ff0000 !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.2) !important;
  }

  /* Target Webkit browsers specifically */
  @media screen and (-webkit-min-device-pixel-ratio:0) {
    select.dropdown-red-black {
      background-color: #1a1a1a !important;
    }
    
    select.dropdown-red-black option {
      background-color: #1a1a1a !important;
      color: #ffffff !important;
    }
  }

  /* Target Firefox specifically */
  @-moz-document url-prefix() {
    select.dropdown-red-black {
      background-color: #1a1a1a !important;
      color: #ffffff !important;
    }
    
    select.dropdown-red-black option {
      background-color: #1a1a1a !important;
      color: #ffffff !important;
    }
  }

  /* Add shared scrollbar styles */
  .table-container::-webkit-scrollbar,
  .activity-timeline::-webkit-scrollbar {
    width: 4px;
  }

  .table-container::-webkit-scrollbar-track,
  .activity-timeline::-webkit-scrollbar-track {
    background: rgba(255, 0, 0, 0.1);
    border-radius: 2px;
  }

  .table-container::-webkit-scrollbar-thumb,
  .activity-timeline::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ff3333, #990000);
    border-radius: 2px;
  }

  /* Add these new styles */
  .task-details-modal {
    max-width: 700px;
    max-height: 80vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .member-task-header {
    flex-shrink: 0;
  }

  .tasks-list {
    flex: 1;
    overflow-y: auto;
    padding-right: 0.5rem;
    margin: 1rem -0.5rem;
    scrollbar-width: thin;
    scrollbar-color: #ff0000 #1a1a1a;
  }

  .tasks-list::-webkit-scrollbar {
    width: 4px;
  }

  .tasks-list::-webkit-scrollbar-track {
    background: rgba(255, 0, 0, 0.1);
    border-radius: 2px;
  }

  .tasks-list::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ff3333, #990000);
    border-radius: 2px;
  }

  .task-status.postponed {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.4);
  }

  /* Sweet Alert custom styles */
  :deep(.swal2-popup) {
    background: #1a1a1a !important;
  }

  :deep(.swal2-input) {
    background: #1a1a1a !important;
    color: #fff !important;
    border: 1px solid rgba(141, 0, 0, 0.519) !important;
  }

  :deep(.swal2-input:focus) {
    border-color: #ff0000 !important;
    box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.2) !important;
  }

  .member-task-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 0, 0, 0.2);
  }

  .member-info-large {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .avatar.large {
    width: 4rem;
    height: 4rem;
    font-size: 1.5rem;
  }

  .member-details h2 {
    margin: 0;
    color: #ffffff;
  }

  .member-role {
    color: #9ca3af;
    font-size: 0.875rem;
  }

  .task-stats {
    text-align: right;
  }

  .stat-label {
    display: block;
    color: #9ca3af;
    font-size: 0.875rem;
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #ff3333;
  }

  .tasks-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .task-item {
    background: rgba(255, 0, 0, 0.05);
    border: 1px solid rgba(255, 0, 0, 0.2);
    border-radius: 0.75rem;
    padding: 1.5rem;
    transition: all 0.2s;
  }

  .task-item:hover {
    background: rgba(255, 0, 0, 0.1);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(255, 0, 0, 0.1);
  }

  .task-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .task-title-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .task-creation-date {
    font-size: 0.75rem;
    color: #9ca3af;
  }

  .task-badges {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }

  .task-priority {
    padding: 0.35rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }

  .task-priority.minor {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }

  .task-priority.mid {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }

  .task-priority.major {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }

  .task-description {
    margin: 1rem 0;
    color: #636363;
    line-height: 1.5;
  }

  .task-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
  }

  .task-dates {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .due-date {
    color: #9ca3af;
    font-size: 0.875rem;
  }

  .time-remaining {
    font-size: 0.875rem;
    font-weight: 500;
  }

  .time-remaining.overdue {
    color: #ef4444;
  }

  .time-remaining.urgent {
    color: #f59e0b;
  }

  .time-remaining.warning {
    color: #fbbf24;
  }

  .time-remaining.normal {
    color: #10b981;
  }

  .task-status {
    padding: 0.35rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .task-status.pending {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }

  .task-status.completed {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }

  .task-actions {
    display: flex;
    gap: 0.5rem;
  }

  .action-btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s;
  }

  .action-btn.complete {
    background: rgba(46, 204, 113, 0.2);
    color: #2ecc71;
  }

  .action-btn.postpone {
    background: rgba(241, 196, 15, 0.2);
    color: #f1c40f;
  }

  .action-btn.cancel {
    background: rgba(231, 76, 60, 0.2);
    color: #e74c3c;
  }

  .action-btn.delete {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }

  .action-btn.delete:hover {
    background: rgba(239, 68, 68, 0.3);
  }

  .action-btn:hover {
    filter: brightness(1.2);
  }

  /* Make team member rows clickable */
  .member-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .member-row {
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .member-row:hover {
    background: rgba(255, 0, 0, 0.1);
  }

  /* Remove these styles that were previously on .member-info */
  .member-info {
    cursor: default;
    padding: 0;
    border-radius: 0;
    transition: none;
  }

  .member-info:hover {
    background: none;
  }

  /* Add these new styles for activity status indicators */
  .activity-status {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 1rem;
  }

  .activity-status.pending {
    background: rgba(255, 193, 7, 0.2);
    color: #ffc107;
  }

  .activity-status.completed {
    background: rgba(46, 204, 113, 0.2);
    color: #2ecc71;
  }

  .activity-status.postponed {
    background: rgba(52, 152, 219, 0.2);
    color: #3498db;
  }

  .activity-status.cancelled {
    background: rgba(231, 76, 60, 0.2);
    color: #e74c3c;
  }

  .countdown {
    font-size: 0.875rem;
    font-weight: 600;
    padding: 0.35rem 0.75rem;
    border-radius: 1rem;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }

  .countdown.overdue {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }

  .countdown.urgent {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }

  .countdown.warning {
    background: rgba(251, 191, 36, 0.2);
    color: #fbbf24;
  }

  .countdown.normal {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }

  .task-stats-wrapper {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .task-stats {
    display: flex;
    gap: 0.5rem;
  }

  .task-stats .stat {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 1rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }

  .task-stats .stat.completed {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }

  .task-stats .stat.postponed {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }

  .task-stats .stat i {
    font-size: 0.75rem;
  }

  .stat {
    font-size: 0.75rem;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    white-space: nowrap;
  }

  .stat.completed {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }

  .stat.postponed {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }

  .stat i {
    font-size: 0.875rem;
  }

  .activity-card {
    height: fit-content;
    max-height: 500px; /* Ensure card doesn't grow too large */
  }

  .activity-card .card-content {
    height: calc(100% - 60px); /* Subtract header height */
    display: flex;
    flex-direction: column;
  }

  .activity-content {
    position: relative;
  }

  .activity-time {
    position: absolute;
    right: 0;
    bottom: -18px;
    font-size: 0.75rem;
    color: #9ca3af;
  }

  .activity-status.pending {
    background: rgba(255, 0, 0, 0.2);
    color: #ff0000;
    font-weight: 600;
    border: 1px solid rgba(255, 0, 0, 0.4);
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.05);
      opacity: 0.8;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  .activity-item:hover {
    background: rgba(255, 0, 0, 0.05);
    border-radius: 8px;
    padding: 8px;
    margin: -8px;
  }

  .activity-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 0.5rem;
  }

  .status-pending {
    background: rgba(255, 0, 0, 0.2);
    color: #ff0000;
    border: 1px solid rgba(255, 0, 0, 0.4);
  }

  .status-completed {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.4);
  }

  .status-postponed {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.4);
  }

  .status-deleted {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.4);
    animation: slideIn 0.3s ease;
  }

  @keyframes slideIn {
    from {
      transform: translateX(-10px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  .activity-timestamp {
    background: rgba(255, 0, 0, 0.1);
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    color: #ff0000;
    margin-left: 0.5rem;
  }
  .no-tasks {
    text-align: center;
    padding: 2rem;
    background: rgba(255, 0, 0, 0.05);
    border-radius: 0.75rem;
    margin: 1rem 0;
  }

  .no-tasks-icon {
    font-size: 3rem;
    color: #ff3333;
    margin-bottom: 1rem;
  }
  .title{
    font-size: 22px;
    color: rgb(215, 215, 215);
  }
  .no-tasks-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .no-tasks-message {
    color: #9ca3af;
    font-size: 0.875rem;
  }

  .stat.pending {
    background: rgba(7, 156, 255, 0.2);
    color: #078fff;
  }
  </style>
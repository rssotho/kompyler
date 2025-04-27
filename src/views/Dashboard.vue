<template>
  <div class="dashboard-container">
    <ResponsiveSidebar />
    <div class="main-content">
      <div class="dashboard-header">
        <div class="header-left">
          <h3 class="dashboard-title">Overview</h3>
          <p class="access-info">Effortlessly manage, track, and evaluate tasks with streamlined performance insights on a sleek, user-friendly dashboard.</p>
        </div>
        <div class="header-right">
          <div class="clock-wrapper">
            <div class="analog-clock">
              <div class="hand hour-hand" :style="hourHandStyle"></div>
              <div class="hand minute-hand" :style="minuteHandStyle"></div>
              <div class="hand second-hand" :style="secondHandStyle"></div>
              <div class="center-dot"></div>
            </div>
            <div class="date">{{ currentDate }}</div>
          </div>
        </div>
      </div>

      <div class="dashboard-grid">
        <!-- Overview Card -->
        <div class="card overview-card">
          <div class="card-header">
            <h2>Overview</h2>
            <div class="info-icon">
              <i class="fas fa-circle-info"></i>
            </div>
          </div>
          <div class="card-content">
            <div class="metrics">
              <div class="metric">
                <span class="metric-label">Max records</span>
                <span class="metric-value">2 times increase to the last month</span>
              </div>
              <div class="metric">
                <span class="metric-label">Comparative rates</span>
                <span class="metric-value">+ 12.83 %</span>
              </div>
            </div>
            
            <div class="time-filters">
              <button class="time-btn">24h</button>
              <button class="time-btn">Week</button>
              <button class="time-btn active">Month</button>
            </div>
            
            <div class="chart-container">
              <canvas ref="performanceChart"></canvas>
            </div>
            
            <div class="chart-footer">
              <div class="chart-dates">
                <span>Mar 8</span>
                <span>Mar 18</span>
                <span>Mar 28</span>
                <span>Apr 8</span>
              </div>
              <div class="growth-indicator">
                <span class="growth-value">+ 19.23 %</span>
                <div class="update-info">
                  <span>Last updated</span>
                  <span>Today, 06:49 AM</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Task Statistics Card -->
        <div class="card balance-card">
          <div class="card-header">
            <div>
              <h2>Task Statistics</h2>
              <p class="subtitle">Overall task and team performance metrics</p>
            </div>
            <div class="refresh-btn">
              <i class="fas fa-sync-alt"></i>
            </div>
          </div>
          
          <div class="card-content px-5">
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-icon total">
                  <i class="fas fa-tasks"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-label">Total Tasks</span>
                  <span class="stat-value">
                    <span ref="totalTasks">{{ stats.totalTasks }}</span>
                  </span>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon pending">
                  <i class="fas fa-clock"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-label">Pending</span>
                  <span class="stat-value">
                    <span ref="pendingTasks">{{ stats.pendingTasks }}</span>
                  </span>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon passed">
                  <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-label">Completed</span>
                  <span class="stat-value">
                    <span ref="passedTasks">{{ stats.passedTasks }}</span>
                  </span>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon failed">
                  <i class="fas fa-times-circle"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-label">Postponed</span>
                  <span class="stat-value">
                    <span ref="failedTasks">{{ stats.failedTasks }}</span>
                  </span>
                </div>
              </div>
              
              <div class="stat-item team">
                <div class="stat-icon team">
                  <i class="fas fa-users"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-label">Team Members</span>
                  <span class="stat-value">
                    <span ref="teamMembers">{{ stats.teamMembers }}</span>
                  </span>
                </div>
              </div>
            </div>

            <div class="member-performance">
              <div class="performance-header">
                <span>Team Performance</span>
                <div class="performance-stats">
                  <span class="performing">
                    <i class="fas fa-arrow-up"></i> {{ passedMembers }} 
                  </span>
                  <span class="struggling">
                    <i class="fas fa-arrow-down"></i> {{ failingMembers }}
                  </span>
                </div>
              </div>
              <div class="performance-bar">
                <div class="progress" :style="{ width: performanceRate + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- In Progress Tasks Card -->
        <div class="card in-progress-card">
          <div class="card-header">
            <h2>In Progress Tasks</h2>
            <div class="task-count" v-if="inProgressTasks.length > 0">{{ inProgressTasks.length }} Tasks</div>
          </div>
          
          <div class="card-content">
            <div v-if="inProgressTasks.length > 0" class="task-list">
              <div v-for="task in inProgressTasks" :key="task.id" class="task-item">
                <div class="task-header">
                  <div class="task-title-row">
                    <div class="task-title">{{ task.title }}</div>
                    <div class="task-priority" :class="task.priority.toLowerCase()">
                      {{ task.priority }}
                    </div>
                  </div>
                </div>
                <p class="task-description">{{ task.description }}</p>
                <div class="task-footer">
                  <div class="task-deadline">
                    <i class="fas fa-clock"></i>
                    <span>Due {{ formatDate(task.dueDate) }}</span>
                  </div>
                  <div class="task-assignee">
                    <div class="assignee-avatar">{{ getAssigneeInitials(task.assignedTo) }}</div>
                    <span>{{ getAssigneeName(task.assignedTo) }}</span>
                  </div>
                  <button @click="deleteTask(task.id)" class="delete-btn">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="no-tasks">
              <i class="fas fa-tasks no-tasks-icon"></i>
              <p>No tasks in progress</p>
              <p class="no-tasks-hint">Tasks will appear here when they are created</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Team Performance Section -->
      <div class="team-performance-section">
        <div class="section-header">
          <h2>Leading Team Members</h2>
          <div class="view-controls">
            <button class="period-btn active">This Month</button>
            <button class="period-btn">All Time</button>
          </div>
        </div>
        
        <div class="team-table">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Team Member</th>
                <th>Department</th>
                <th>Tasks Completed</th>
                <th>Success Rate</th>
                <th>On-Time Rate</th>
                <th>Performance</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="member in leadingMembers" :key="member.id">
                <td class="rank-cell">
                  <span class="rank" :class="{ 'top-three': member.rank <= 3 }">#{{ member.rank }}</span>
                </td>
                <td>
                  <div class="member-info">
                    <div class="member-avatar" :style="{ backgroundColor: member.avatarColor }">
                      {{ member.name.charAt(0) }}
                    </div>
                    <div class="member-details">
                      <span class="member-name">{{ member.name }}</span>
                      <span class="member-role">{{ member.role }}</span>
                    </div>
                  </div>
                </td>
                <td>{{ member.department }}</td>
                <td>
                  <div class="completion-info">
                    <span class="completion-count">{{ member.tasksCompleted }}</span>
                    <span class="total-tasks">/ {{ member.totalTasks }}</span>
                  </div>
                </td>
                <td>
                  <div class="rate-badge success">{{ member.successRate }}%</div>
                </td>
                <td>
                  <div class="rate-badge ontime">{{ member.onTimeRate }}%</div>
                </td>
                <td>
                  <div class="performance-indicator">
                    <div class="performance-bar">
                      <div class="performance-fill" :style="{ width: member.performance + '%', backgroundColor: getPerformanceColor(member.performance) }"></div>
                    </div>
                    <span class="performance-value">{{ member.performance }}%</span>
                  </div>
                </td>
                <td>
                  <span class="status-badge" :class="member.status.toLowerCase()">{{ member.status }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- My Top Campaigns Section -->
      
    </div>
  </div>
</template>

<script>
import ResponsiveSidebar from '@/components/ResponsiveSidebar.vue';
import eventBus from '@/utils/eventBus';

export default {
  name: 'Dashboard',
  components: {
    ResponsiveSidebar
  },
  data() {
    return {
      hourHandStyle: '',
      minuteHandStyle: '',
      secondHandStyle: '',
      currentDate: '',
      timer: null,
      stats: {
        totalTasks: 0,
        pendingTasks: 0,
        passedTasks: 0,
        failedTasks: 0,
        teamMembers: 0
      }
    }
  },
  computed: {
    inProgressTasks() {
      try {
        const tasks = JSON.parse(localStorage.getItem('allTasks')) || [];
        const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
        const teamMemberIds = teamMembers.map(m => m.id);
        
        // Filter tasks that are:
        // 1. In pending status
        // 2. Assigned to any team member
        const validTasks = tasks.filter(task => {
          const assigneeExists = teamMemberIds.includes(Number(task.assignedTo));
          return task.status === 'pending' && assigneeExists;
        });

        console.log('All team members pending tasks:', validTasks);
        
        // Sort by due date (most recent first)
        return validTasks.sort((a, b) => new Date(b.dueDate) - new Date(a.dueDate));
      } catch (error) {
        console.error('Error loading tasks:', error);
        return [];
      }
    },
    
    taskStats() {
      try {
        const tasks = JSON.parse(localStorage.getItem('allTasks')) || [];
        const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
        
        // Filter tasks that belong to team members only
        const memberTasks = tasks.filter(task => {
          const assigneeExists = teamMembers.map(m => m.id).includes(Number(task.assignedTo));
          return assigneeExists; // Include all tasks assigned to team members
        });

        console.log('Dashboard - Member tasks:', memberTasks);

        const stats = {
          totalTasks: memberTasks.length, // Total tasks assigned to members
          pendingTasks: memberTasks.filter(task => task.status === 'pending').length,
          passedTasks: memberTasks.filter(task => task.status === 'completed').length,
          failedTasks: memberTasks.filter(task => task.status === 'postponed').length,
          teamMembers: teamMembers.length
        };

        this.stats = stats;
        return stats;
      } catch (error) {
        console.error('Error calculating stats:', error);
        return {
          totalTasks: 0,
          pendingTasks: 0,
          passedTasks: 0,
          failedTasks: 0,
          teamMembers: 0
        };
      }
    },
    passedMembers() {
      return this.teamMembers.filter(member => {
        const stats = this.getTaskStats(member.id);
        return (stats.completed / (stats.total || 1)) > 0.5;
      }).length;
    },
    failingMembers() {
      return this.teamMembers.length - this.passedMembers;
    },
    performanceRate() {
      return (this.passedMembers / (this.teamMembers.length || 1)) * 100;
    }
  },
  methods: {
    updateClock() {
      const now = new Date();
      const hours = now.getHours() % 12;
      const minutes = now.getMinutes();
      const seconds = now.getSeconds();
      // Calculate hand rotations
      const hourDegrees = (hours * 30) + (minutes / 2); // 30 degrees per hour + adjustment for minutes
      const minuteDegrees = minutes * 6; // 6 degrees per minute
      const secondDegrees = seconds * 6; // 6 degrees per second
      this.hourHandStyle = `transform: rotate(${hourDegrees}deg)`;
      this.minuteHandStyle = `transform: rotate(${minuteDegrees}deg)`;
      this.secondHandStyle = `transform: rotate(${secondDegrees}deg)`;
      this.currentDate = now.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric'
      });
    },
    deleteTask(taskId) {
      try {
        // Get current tasks
        const tasks = JSON.parse(localStorage.getItem('allTasks')) || [];
        // Filter out the deleted task
        const updatedTasks = tasks.filter(task => task.id !== taskId);
        // Update localStorage
        localStorage.setItem('allTasks', JSON.stringify(updatedTasks));
        // Refresh data immediately
        this.refreshData();
        // Emit event for other components
        eventBus.emit('task-deleted', taskId);
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    },
    refreshData() {
      // Force recompute of taskStats
      this.$nextTick(() => {
        this.stats = this.taskStats;
        this.inProgressTasks = this.getInProgressTasks();
      });
    },
    getInProgressTasks() {
      try {
        const tasks = JSON.parse(localStorage.getItem('allTasks')) || [];
        return tasks.filter(task => task.status === 'pending')
          .sort((a, b) => new Date(b.dueDate) - new Date(a.dueDate));
      } catch (error) {
        console.error('Error loading tasks:', error);
        return [];
      }
    },
    handleTaskCreated() {
      console.log('New task created, refreshing dashboard stats');
      this.refreshData();
    },
    getAssigneeName(assignedTo) {
      if (!assignedTo) return 'Unassigned';
      const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
      const member = teamMembers.find(m => m.id === Number(assignedTo));
      return member ? member.name : 'Unknown';
    },
    getAssigneeInitials(assignedTo) {
      if (!assignedTo) return '?';
      const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
      const member = teamMembers.find(m => m.id === Number(assignedTo));
      return member ? member.name.charAt(0) : '?';
    },
    formatDate(date) {
      if (!date) return 'No date';
      const dueDate = new Date(date);
      const today = new Date();
      if (dueDate.toDateString() === today.toDateString()) return 'Today';
      return dueDate.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      });
    },
    handleTaskDelete(taskId) {
      console.log('Task deleted, refreshing dashboard:', taskId);
      this.refreshData();
    }
  },
  created() {
    this.refreshData();
    eventBus.on('task-created', this.handleTaskCreated);
    // Update event listeners to use refreshData directly
    eventBus.on('task-updated', this.refreshData);
    eventBus.on('task-created', this.refreshData);
    eventBus.on('task-deleted', this.refreshData);
    eventBus.on('member-deleted', this.refreshData);
  },
  mounted() {
    this.updateClock();
    this.timer = setInterval(this.updateClock, 1000);
  },
  beforeUnmount() {
    clearInterval(this.timer);
    eventBus.off('task-updated', this.refreshData);
    eventBus.off('task-created', this.refreshData);
    eventBus.off('task-deleted', this.handleTaskDelete);
    eventBus.off('member-deleted', this.refreshData);
    eventBus.off('task-created', this.handleTaskCreated);
  }
};
</script>

<style scoped>
.dashboard-container {
  position: relative; /* Add this */
  display: flex; /* Changed from min-height to fixed height */
  height: 100vh; /* Changed from min-height to fixed height */
  background-color: #000000;
  color: #e6eaef;
  overflow: hidden; /* Prevent container from scrolling */
}
.main-content {
  flex-grow: 1;
  padding: 1.5rem;
  overflow-y: auto; /* Make only main content scrollable */
  height: 100vh; /* Full height */
  padding-top: 0;
}

@media (max-width: 767px){
  .clock-wrapper{
    display: none !important;
  }

  .dashboard-header{
    top: -20px !important;
  }

  .stat-item{
    display: block !important;
  }
}

.dashboard-header {
  position: sticky;
  top: 0;
  z-index: 100; /* Lower than tooltip */
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding: 1rem 0;
  background: linear-gradient(180deg, #000000 95%, rgba(0, 0, 0, 0));
  backdrop-filter: blur(8px);
  isolation: isolate; /* Create new stacking context */
}
.dashboard-title {
  margin: 0;
  margin-bottom: 0.5rem;
  margin-top: 1rem;
  font-size: 22px;
  color: rgb(215, 215, 215);
}
.access-info {
  color: #9ca3af;
  font-size: 0.875rem;
  margin: 0;
}
.datetime-display {
  background-color: #1c2127;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  text-align: center;
  border: 1px solid rgba(255, 0, 0, 0.1);
}
.datetime-display .time {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ff3333;
  margin-bottom: 0.25rem;
}
.datetime-display .date {
  font-size: 0.875rem;
  color: #9ca3af;
}
.dashboard-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.card {
  position: relative;
  z-index: 1; /* Lower than header */
  background: linear-gradient(145deg, #1a1a1a 0%, #0a0a0a 100%);
  border: 1px solid rgba(255, 0, 0, 0.1);
  border-radius: 0.75rem;
  overflow: hidden;
  transition: all 0.3s ease;
}
.card:hover {
  border-color: rgba(255, 0, 0, 0.2);
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.05);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 0, 0, 0.1);
  background: linear-gradient(145deg, #1c1c1c 0%, #141414 100%);
}
.card-header h2 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}
.subtitle {
  color: #9ca3af;
  font-size: 0.875rem;
  margin: 0.25rem 0 0 0;
}
.card-content {
  padding: 1rem;
}
.metrics {
  margin-bottom: 1rem;
}
.metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}
.metric-label {
  color: #9ca3af;
  font-size: 0.875rem;
}
.metric-value {
  font-size: 0.875rem;
}
.time-filters {
  display: flex;
  margin-bottom: 1rem;
  background: linear-gradient(145deg, #1c1c1c 0%, #141414 100%);
  border: 1px solid rgba(255, 0, 0, 0.1);
  border-radius: 0.5rem;
  overflow: hidden;
}
.time-btn {
  flex: 1;
  background: none;
  border: none;
  color: #9ca3af;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}
.time-btn.active {
  background: linear-gradient(135deg, #ff0000 0%, #990000 100%);
  color: #e6eaef;
}
.chart-container {
  position: relative;
  height: 200px;
  margin-bottom: 1rem;
  z-index: 4; /* Higher than card */
  isolation: isolate; /* Create new stacking context */
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
.chart-placeholder {
  height: 100%;
  background: linear-gradient(180deg, rgba(255, 0, 0, 0.05) 0%, rgba(0, 0, 0, 0.02) 100%);
  border-radius: 0.5rem;
  position: relative;
  overflow: hidden;
}
.chart-placeholder::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at center, rgba(255, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0) 70%);
}
.chart-placeholder::after {
  content: '';
  position: absolute;
  height: 2px;
  bottom: 30%;
  left: 0;
  right: 0;
  background: linear-gradient(90deg, rgba(0, 0, 0, 0), rgba(255, 0, 0, 0.8), rgba(0, 0, 0, 0));
}
.chart-tooltip {
  position: fixed;
  top: var(--tooltip-y, 50%);
  left: var(--tooltip-x, 50%);
  transform: translate(-50%, -100%);
  background-color: #1c2127;
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.5rem;
  padding: 0.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  width: max-content;
  z-index: 99999 !important; /* Extreme high z-index */
  pointer-events: none;
}
/* Add this portal container at the root level */
.tooltip-portal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 0;
  z-index: 999999;
  pointer-events: none;
}
.tooltip-date {
  font-size: 0.75rem;
  color: #9ca3af;
}
.tooltip-value {
  font-weight: 600;
}
.tooltip-percentage {
  color: #10b981;
  font-size: 0.875rem;
}
.chart-footer {
  display: flex;
  justify-content: space-between;
}
.chart-dates {
  display: flex;
  justify-content: space-between;
  width: 70%;
  color: #9ca3af;
  font-size: 0.75rem;
}
.growth-indicator {
  text-align: right;
}
.growth-value {
  color: #ff3333;
  font-weight: 600;
  display: block;
}
.update-info {
  color: #9ca3af;
  font-size: 0.75rem;
}
.balance-amount h2 {
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
}
.balance-comparison {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.balance-comparison span:first-child {
  color: #9ca3af;
  font-size: 0.875rem;
}
.negative {
  color: #ef4444;
}
.yearly-average {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #9ca3af;
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}
.yearly-average i {
  color: #10b981;
}
.ai-assistant {
  background-color: #242a33;
  border-radius: 0.5rem;
  padding: 1rem;
}
.assistant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.assistant-header h3 {
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0;
}
.loading-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #9ca3af;
  font-size: 0.75rem;
}
.assistant-visual {
  height: 120px;
  background: linear-gradient(135deg, #ff0000 0%, #330000 100%);
  border-radius: 0.5rem;
}
.premium-offer {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.offer-header {
  margin-bottom: 1rem;
}
.offer-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.discount {
  background-color: #f59e0b;
  color: #000;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
}
.offer-details {
  flex-grow: 1;
  margin-bottom: 1rem;
}
.offer-details p {
  color: #9ca3af;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}
.offer-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e6eaef;
  font-weight: 500;
  cursor: pointer;
}
.offer-footer {
  display: flex;
  justify-content: space-between;
}
.dismiss-btn {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
}
.cta-btn {
  background: linear-gradient(135deg, #ff0000 0%, #990000 100%);
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}
.cta-btn:hover {
  background: linear-gradient(135deg, #cc0000 0%, #660000 100%);
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.section-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}
.view-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #242a33;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}
.campaigns-table {
  background: linear-gradient(145deg, #1a1a1a 0%, #0a0a0a 100%);
  border: 1px solid rgba(255, 0, 0, 0.1);
  border-radius: 0.75rem;
  overflow: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th {
  text-align: left;
  padding: 1rem;
  color: #9ca3af;
  font-weight: 500;
  font-size: 0.875rem;
  border-bottom: 1px solid rgba(255, 0, 0, 0.1);
}
td {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 0, 0, 0.1);
  font-size: 0.875rem;
}
.admin-avatar {
  width: 2rem;
  height: 2rem;
  background: linear-gradient(135deg, #ff0000 0%, #990000 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
}
.followers-avatars {
  display: flex;
  align-items: center;
}
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}
.status-badge.public {
  background: linear-gradient(145deg, rgba(255, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.1) 100%);
  border: 1px solid rgba(255, 0, 0, 0.2);
  color: #ff3333;
}
.status-badge.private {
  background: linear-gradient(145deg, rgba(128, 128, 128, 0.1) 0%, rgba(0, 0, 0, 0.1) 100%);
  border: 1px solid rgba(128, 128, 128, 0.2);
  color: #9ca3af;
}
.join-btn, .request-btn {
  background: linear-gradient(145deg, rgba(255, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.1) 100%);
  border: 1px solid rgba(255, 0, 0, 0.2);
  color: #ff3333;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.join-btn:hover, .request-btn:hover {
  background: linear-gradient(145deg, rgba(255, 0, 0, 0.2) 0%, rgba(0, 0, 0, 0.2) 100%);
  border-color: rgba(255, 0, 0, 0.3);
}
.campaign-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
.campaign-card {
  background-color: #1c2127;
  border-radius: 0.75rem;
  overflow: hidden;
}
.campaign-card .card-header {
  padding: 0.75rem;
}
.bullet {
  color: #ff0000;
  margin-right: 0.5rem;
  font-size: 1.25rem;
}
.campaign-name {
  flex-grow: 1;
  font-weight: 500;
}
.menu-btn {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
}
.campaign-metrics {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}
.followers-count {
  font-weight: 500;
}
.growth {
  color: #ff3333;
}
.pagination {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #9ca3af;
  font-size: 0.875rem;
}
.pagination-controls {
  display: flex;
  gap: 0.5rem;
}
.pagination-controls button {
  width: 1.5rem;
  height: 1.5rem;
  background-color: #242a33;
  border: none;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  cursor: pointer;
}
.clock-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.analog-clock {
  width: 60px;
  height: 60px;
  border: 2px solid rgba(255, 0, 0, 0.2);
  border-radius: 50%;
  position: relative;
  background: #1c2127;
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.1);
}
.hand {
  position: absolute;
  bottom: 50%;
  left: 50%;
  transform-origin: bottom;
  background: #ff3333;
  border-radius: 4px;
}
.hour-hand {
  width: 2px;
  height: 20px;
  background: #ff3333;
}
.minute-hand {
  width: 2px;
  height: 25px;
  background: #ff6666;
}
.second-hand {
  width: 1px;
  height: 28px;
  background: #ff0000;
}
.center-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #ff0000;
  transform: translate(-50%, -50%);
}
.date {
  font-size: 0.875rem;
  color: #9ca3af;
}
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .main-content {
    padding: 1rem;
  }
  .dashboard-header {
    flex-direction: column;
  }
  .finance-dropdown {
    margin-top: 1rem;
  }
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  .campaign-cards {
    grid-template-columns: 1fr;
  }
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(145deg, #1c1c1c 0%, #141414 100%);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 0, 0, 0.1);
}
.stat-item.team {
  grid-column: span 2;
}
.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  font-size: 1.5rem;
}
.stat-icon.total { background: linear-gradient(135deg, rgba(255, 0, 0, 0.2), rgba(0, 0, 0, 0.1)); }
.stat-icon.pending { background: linear-gradient(135deg, rgba(255, 166, 0, 0.2), rgba(0, 0, 0, 0.1)); }
.stat-icon.passed { background: linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 0, 0, 0.1)); }
.stat-icon.failed { background: linear-gradient(135deg, rgba(255, 0, 0, 0.2), rgba(0, 0, 0, 0.1)); }
.stat-icon.team { background: linear-gradient(135deg, rgba(0, 157, 255, 0.2), rgba(0, 0, 0, 0.1)); }
.stat-info {
  display: flex;
  flex-direction: column;
}
.stat-label {
  color: #9ca3af;
  font-size: 0.875rem;
}
.stat-value {
  font-size: 1rem;
  font-weight: 600;
  color: #ff3333;
}
.member-performance {
  background: linear-gradient(145deg, #1c1c1c 0%, #141414 100%);
  border-radius: 0.75rem;
  padding: 1rem;
  border: 1px solid rgba(255, 0, 0, 0.1);
}

.performance-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  color: #9ca3af;
}

.performance-stats {
  display: flex;
  gap: 1rem;
}

.performing {
  color: #10b981;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.struggling {
  color: #ef4444;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.performance-bar {
  height: 6px;
  background: rgba(255, 0, 0, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.performance-bar .progress {
  height: 100%;
  background: linear-gradient(90deg, #ef4444, #10b981);
  transition: width 1s ease-in-out;
}
.refresh-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  background: rgba(255, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}
.refresh-btn:hover {
  background: rgba(255, 0, 0, 0.2);
  transform: rotate(180deg);
}
/* Add these new styles */
.in-progress-card {
  min-height: 400px;
}
.task-count {
  background: rgba(255, 0, 0, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  color: #ff3333;
}
.task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}
.task-list::-webkit-scrollbar {
  width: 4px;
}
.task-list::-webkit-scrollbar-track {
  background: rgba(255, 0, 0, 0.1);
  border-radius: 2px;
}
.task-list::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #ff3333, #990000);
  border-radius: 2px;
}
.task-item {
  background: linear-gradient(145deg, #1c1c1c 0%, #141414 100%);
  border: 1px solid rgba(255, 0, 0, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  flex-shrink: 0;
}
.task-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.task-priority {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}
.task-priority.major {
  background: rgba(255, 59, 48, 0.1);
  color: #ff3b30;
  border: 1px solid rgba(255, 59, 48, 0.2);
}
.task-priority.mid {
  background: rgba(255, 149, 0, 0.1);
  color: #ff9500;
  border: 1px solid rgba(255, 149, 0, 0.2);
}
.task-priority.minor {
  background: rgba(52, 199, 89, 0.1);
  color: #34c759;
  border: 1px solid rgba(52, 199, 89, 0.2);
}
/* Remove task-progress related styles */
.task-progress,
.progress-bar,
.progress {
  display: none;
}
.task-description {
  color: #9ca3af;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}
.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}
.task-deadline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #9ca3af;
}
.task-assignee {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.assignee-avatar {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #ff3333, #990000);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: white;
}
.team-performance-section {
  margin-bottom: 2rem;
}
.period-btn {
  background: none;
  border: 1px solid rgba(255, 0, 0, 0.2);
  color: #9ca3af;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.period-btn.active {
  background: linear-gradient(135deg, #ff0000 0%, #990000 100%);
  color: #fff;
}
.team-table {
  background: linear-gradient(145deg, #1a1a1a 0%, #0a0a0a 100%);
  border: 1px solid rgba(255, 0, 0, 0.1);
  border-radius: 0.75rem;
  overflow: auto;
}
.rank-cell {
  width: 60px;
}
.rank {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  color: #9ca3af;
}
.rank.top-three {
  background: linear-gradient(135deg, #ff0000 0%, #990000 100%);
  color: #fff;
}
.member-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.member-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
}
.member-details {
  display: flex;
  flex-direction: column;
}
.member-name {
  font-weight: 500;
}
.member-role {
  font-size: 0.75rem;
  color: #9ca3af;
}
.completion-info {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.completion-count {
  font-weight: 600;
  color: #ff3333;
}
.total-tasks {
  color: #9ca3af;
  font-size: 0.875rem;
}
.rate-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}
.rate-badge.success {
  background: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.2);
}
.rate-badge.ontime {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.2);
}
.performance-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.performance-bar {
  flex-grow: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}
.performance-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}
.performance-value {
  font-size: 0.875rem;
  font-weight: 500;
  min-width: 3rem;
  text-align: right;
}
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}
.status-badge.active {
  background: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.2);
}
.status-badge.away {
  background: rgba(241, 196, 15, 0.1);
  color: #f1c40f;
  border: 1px solid rgba(241, 196, 15, 0.2);
}




.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); /* Adjust min-width as needed */
  gap: 1rem;
  margin-bottom: 1.5rem;
  width: 100%; /* Ensure full width */
  justify-content: center; /* Center grid items */
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(145deg, #1c1c1c 0%, #141414 100%);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 0, 0, 0.1);
  width: 100%; /* Ensure full width of grid cell */
  max-width: 300px; /* Optional: set a max-width */
  margin: 0 auto; /* Center within grid cell */
}

.stat-item.team {
  grid-column: span 2;
  max-width: 100%; /* Full width for team item */
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr; /* Single column on smaller screens */
  }

  .stat-item.team {
    grid-column: span 1; /* Reset team item to single column */
  }

  
}

</style>
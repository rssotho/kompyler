<template>
  <div class="wrapper">
    <ResponsiveSidebar/>
    <div class="content-wrapper">
      <div class="dashboard-container">
        <div class="dashboard-header sticky-header">
          <h3 class="title">Evaluation Results</h3>
          <p class="description">View all task evaluations and their outcomes.</p>
        </div>

        <div v-if="loading" class="loading">Loading evaluations...</div>
        <div v-else-if="evaluatedTasks.length === 0" class="no-evaluations">
          No evaluated tasks found
        </div>
        <div v-else class="evaluations-grid">
          <div v-for="task in evaluatedTasks" :key="task.id" class="evaluation-card">
            <div class="evaluation-header">
              <h3>{{ task.title }}</h3>
              <span :class="['status-badge', task.evaluation.passed ? 'pass' : 'fail']">
                {{ task.evaluation.passed ? 'Passed' : 'Needs Improvement' }}
              </span>
            </div>
            <div class="evaluation-details">
              <div class="detail-item">
                <span class="label">Score:</span>
                <span class="value">{{ task.evaluation.finalScore.toFixed(1) }}%</span>
              </div>
              <div class="detail-item">
                <span class="label">Evaluated by:</span>
                <span class="value">{{ task.evaluation.evaluatorName }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Date:</span>
                <span class="value">{{ formatDate(task.evaluation.date) }}</span>
              </div>
            </div>
            <div class="evaluation-footer">
              <button class="btn-primary" @click="viewDetails(task)">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Updated Evaluation Details Modal -->
    <div v-if="showDetailsModal" class="modal" @click.self="closeDetailsModal">
      <div class="modal-content popup-style">
        <div class="modal-header">
          <h2>{{ selectedTask?.title }}</h2>
          <button class="close-btn" @click="closeDetailsModal">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="categories-grid">
            <!-- Technical Skills -->
            <div class="category-box">
              <div class="category-title">
                <i class="fas fa-code"></i>
                <h3>Technical Skills</h3>
              </div>
              <div class="score-circle" :class="getCategoryClass(selectedTask?.evaluation?.categoryResults?.consistencyBranding?.percentage)">
                {{ selectedTask?.evaluation?.categoryResults?.consistencyBranding?.percentage.toFixed(1) }}%
              </div>
              <div class="criteria-list">
                <div v-for="(score, criterion) in selectedTask?.evaluation?.details?.consistencyBranding"
                     :key="criterion"
                     class="criterion-item">
                  <span class="criterion-name">{{ criterion }}</span>
                  <div class="score-pill" :class="getScoreClass(score)">
                    {{ score }}/5
                  </div>
                </div>
              </div>
            </div>

            <!-- Creative Quality -->
            <div class="category-box">
              <div class="category-title">
                <i class="fas fa-paint-brush"></i>
                <h3>Creative Quality</h3>
              </div>
              <div class="score-circle" :class="getCategoryClass(selectedTask?.evaluation?.categoryResults?.creativeQuality?.percentage)">
                {{ selectedTask?.evaluation?.categoryResults?.creativeQuality?.percentage.toFixed(1) }}%
              </div>
              <div class="criteria-list">
                <div v-for="(score, criterion) in selectedTask?.evaluation?.details?.creativeQuality"
                     :key="criterion"
                     class="criterion-item">
                  <span class="criterion-name">{{ criterion }}</span>
                  <div class="score-pill" :class="getScoreClass(score)">
                    {{ score }}/5
                  </div>
                </div>
              </div>
            </div>

            <!-- Time Management -->
            <div class="category-box">
              <div class="category-title">
                <i class="fas fa-clock"></i>
                <h3>Time Management</h3>
              </div>
              <div class="score-circle" :class="getCategoryClass(selectedTask?.evaluation?.categoryResults?.timeliness?.percentage)">
                {{ selectedTask?.evaluation?.categoryResults?.timeliness?.percentage.toFixed(1) }}%
              </div>
              <div class="criteria-list">
                <div v-for="(score, criterion) in selectedTask?.evaluation?.details?.timeliness"
                     :key="criterion"
                     class="criterion-item">
                  <span class="criterion-name">{{ criterion }}</span>
                  <div class="score-pill" :class="getScoreClass(score)">
                    {{ score }}/5
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Overall Score -->
          <div class="overall-score">
            <h3>Overall Performance</h3>
            <div class="final-score" :class="selectedTask?.evaluation?.passed ? 'pass' : 'fail'">
              {{ selectedTask?.evaluation?.finalScore.toFixed(1) }}%
            </div>
            <div class="evaluator-info">
              <span>Evaluated by: {{ selectedTask?.evaluation?.evaluatorName }}</span>
              <span>{{ formatDate(selectedTask?.evaluation?.date) }}</span>
            </div>
          </div>

          <!-- Improvement Areas -->
          <div v-if="selectedTask?.evaluation?.improvementAreas?.length" class="improvement-section">
            <h3>Areas for Improvement</h3>
            <div class="improvement-list">
              <div v-for="(area, index) in selectedTask.evaluation.improvementAreas" 
                   :key="index" 
                   class="improvement-card">
                <i class="fas fa-arrow-circle-up"></i>
                <div class="improvement-content">
                  <strong>{{ area.criterion }}</strong>
                  <p>{{ area.suggestion }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ResponsiveSidebar from '@/components/ResponsiveSidebar.vue';

export default {
  name: 'ViewEvaluations',
  components: {
    ResponsiveSidebar
  },
  data() {
    return {
      loading: true,
      evaluatedTasks: [],
      showDetailsModal: false,
      selectedTask: null
    }
  },
  mounted() {
    this.loadEvaluations();
  },
  methods: {
    loadEvaluations() {
      // Load tasks from localStorage
      const allTasks = JSON.parse(localStorage.getItem('allTasks')) || [];
      this.evaluatedTasks = allTasks.filter(task => task.evaluation);
      this.loading = false;
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
    viewDetails(task) {
      this.selectedTask = task;
      this.showDetailsModal = true;
    },
    closeDetailsModal() {
      this.showDetailsModal = false;
      this.selectedTask = null;
    },
    formatCategoryName(category) {
      const names = {
        consistencyBranding: 'Consistency & Branding',
        creativeQuality: 'Creative Quality',
        timeliness: 'Timeliness'
      };
      return names[category] || category;
    },
    getScoreClass(score) {
      if (score >= 80) return 'excellent';
      if (score >= 70) return 'good';
      if (score >= 60) return 'average';
      return 'poor';
    },
    getCategoryClass(percentage) {
      if (!percentage) return 'poor';
      if (percentage >= 80) return 'excellent';
      if (percentage >= 70) return 'good';
      if (percentage >= 60) return 'average';
      return 'poor';
    }
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  width: 100%;
  min-height: 100vh;
  background: #000000;
  color: #ffffff;
}

.content-wrapper {
  flex-grow: 1;
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.description {
  color: rgba(255, 255, 255, 0.7);
}

.evaluations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.evaluation-card {
  background: rgba(26, 26, 26, 0.6);
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: transform 0.2s;
}

.evaluation-card:hover {
  transform: translateY(-2px);
}

.evaluation-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.evaluation-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #ffffff;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.pass {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.status-badge.fail {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.evaluation-details {
  margin: 1rem 0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.label {
  color: rgba(255, 255, 255, 0.6);
}

.value {
  font-weight: 500;
}

.evaluation-footer {
  margin-top: 1rem;
  text-align: right;
}

.btn-primary {
  background: linear-gradient(to right, #ff0000, #990000);
  color: #ffffff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: linear-gradient(to right, #cc0000, #800000);
}

.loading, .no-evaluations {
  text-align: center;
  padding: 2rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.125rem;
}

@media (max-width: 768px) {
  .evaluations-grid {
    grid-template-columns: 1fr;
  }
  
  .content-wrapper {
    padding: 1rem;
  }
  
  .evaluation-card {
    padding: 1rem;
  }

}

.evaluation-details-modal .modal-content {
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 0, 0, 0.2);
}

.evaluator-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.score-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.final-score {
  font-size: 3rem;
  font-weight: bold;
}

.final-score.pass { color: #10b981; }
.final-score.fail { color: #ef4444; }

.category-scores {
  margin-bottom: 2rem;
}

.category-item {
  margin-bottom: 1rem;
}

.category-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.progress-bar {
  background: rgba(255, 255, 255, 0.1);
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  transition: width 0.3s ease;
}

.progress.excellent { background: #10b981; }
.progress.good { background: #3b82f6; }
.progress.average { background: #f59e0b; }
.progress.poor { background: #ef4444; }

.improvement-areas {
  margin-top: 2rem;
}

.improvement-item {
  background: rgba(255, 0, 0, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.improvement-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #ef4444;
}

.evaluation-comments {
  margin-top: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
}

.modal-body h3 {
  margin: 1.5rem 0 1rem;
  color: #ff3333;
  font-size: 1.1rem;
}

.popup-style {
  max-width: 1000px;
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 0, 0, 0.2);
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.1);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.category-box {
  background: rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.category-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.category-title i {
  font-size: 1.5rem;
  color: #ff3333;
}

.title{
  font-size: 22px;
  color: rgb(215, 215, 215);
}

.score-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 1rem 0;
}

.score-circle.excellent { background: rgba(16, 185, 129, 0.2); color: #10b981; }
.score-circle.good { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.score-circle.average { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.score-circle.poor { background: rgba(239, 68, 68, 0.2); color: #ef4444; }

.criteria-list {
  width: 100%;
}

.criterion-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.score-pill {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
}

.score-pill.excellent { background: rgba(16, 185, 129, 0.2); color: #10b981; }
.score-pill.good { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.score-pill.average { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.score-pill.poor { background: rgba(239, 68, 68, 0.2); color: #ef4444; }

.overall-score {
  text-align: center;
  margin: 2rem 0;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
}

.improvement-section {
  background: rgba(255, 0, 0, 0.1);
  padding: 1.5rem;
  border-radius: 1rem;
  margin-top: 2rem;
}

.improvement-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.improvement-card {
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.improvement-card i {
  color: #ff3333;
  font-size: 1.25rem;
}

@media (max-width: 768px) {
  .categories-grid {
    grid-template-columns: 1fr;
  }
  
  .popup-style {
    width: 95%;
    margin: 1rem;
  }
}
</style>
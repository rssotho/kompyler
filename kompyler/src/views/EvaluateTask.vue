<template>
  <div class="wrapper">
    <ResponsiveSidebar />
    <div class="content-wrapper">
      <div class="dashboard-container">
        <div class="dashboard-header sticky-header">
          <h3 class="title">Evaluate Tasks</h3>
          <p class="description">View and evaluate tasks assigned to team members.</p>
        </div>

        <div class="dashboard-grid">
          <!-- Evaluators Section -->
          <div class="card evaluators-card">
            <div class="card-header">
              <h3>Evaluators</h3>
              <button class="btn-primary" @click="showAddEvaluatorModal">
                <i class="fas fa-plus"></i> Add Evaluator
              </button>
            </div>
            <div class="card-content">
              <div class="evaluator-grid">
                <div v-for="evaluator in evaluators" :key="evaluator.id" class="evaluator-item">
                  <div class="evaluator-avatar" :style="{ background: getAvatarGradient() }">
                    {{ getInitials(evaluator.name) }}
                  </div>
                  <div class="evaluator-info">
                    <div class="evaluator-name">{{ evaluator.name }}</div>
                    <div class="evaluator-role">{{ evaluator.role }}</div>
                    <div class="evaluator-tasks">{{ evaluator.tasksEvaluated || 0 }} tasks evaluated</div>
                  </div>
                  <div class="evaluator-actions">
                    <button class="btn-icon" @click="viewEvaluatorTasks(evaluator.id)">
                      <i class="fas fa-eye"></i>
                    </button>
                    <!-- Only show delete button for non-team member evaluators -->
                    <button 
                      v-if="!isTeamMember(evaluator.id)" 
                      class="btn-icon btn-danger" 
                      @click="removeEvaluator(evaluator)"
                      :title="getEvaluatorActionTitle(evaluator)"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                    <div v-else class="evaluator-badge">
                      <i class="fas fa-user-shield" title="Team Member"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Add Evaluator Modal -->
          <div v-if="showModal" class="modal">
            <div class="modal-content">
              <span class="close" @click="closeModal">&times;</span>
              <h2>Add New Evaluator</h2>
              <form @submit.prevent="addEvaluator">
                <div class="form-group">
                  <label>Name</label>
                  <input v-model="newEvaluator.name" type="text" class="form-input" required>
                </div>
                <div class="form-group">
                  <label>Role</label>
                  <input v-model="newEvaluator.role" type="text" class="form-input" required>
                </div>
                <div class="form-actions">
                  <button type="submit" class="btn-primary">Add Evaluator</button>
                </div>
              </form>
            </div>
          </div>

          <!-- Tasks Section -->
          <div class="card tasks-card">
            <div class="card-header">
              <h3>Completed Tasks Pending Evaluation</h3>
            </div>
            <div class="card-content">
              <div v-if="pendingTasks.length > 0" class="task-list">
                <div v-for="task in pendingTasks" :key="task.id" class="task-item">
                  <div class="task-header">
                    <div class="task-title">{{ task.title }}</div>
                    <span :class="['status-badge', getPriorityClass(task.priority)]">
                      {{ task.priority }}
                      <i :class="getPriorityIcon(task.priority)"></i>
                    </span>
                  </div>
                  <div class="task-body">
                    <p class="task-description">{{ task.description }}</p>
                  </div>
                  <div class="task-footer">
                    <div class="task-meta">
                      <div class="task-assigned">
                        <span class="meta-label">Assigned to:</span>
                        <span class="meta-value">{{ getMemberName(task.assignedTo) }}</span>
                      </div>
                      <div class="task-due">
                        <span class="meta-label">Due:</span>
                        <span class="meta-value">{{ formatDate(task.dueDate) }}</span>
                      </div>
                      <div class="evaluation-status">
                        <span class="status-label">Evaluations:</span>
                        <span class="status-count">
                          {{ (task.evaluations?.length || 0) }} / {{ evaluators.length }}
                        </span>
                      </div>
                    </div>
                    <button 
                      class="btn-primary" 
                      @click="showEvaluatorSelection(task)"
                      :disabled="task.evaluations?.some(e => e.evaluatorId === currentEvaluator?.id)"
                    >
                      {{ task.evaluations?.some(e => e.evaluatorId === currentEvaluator?.id) 
                        ? 'Already Evaluated' 
                        : 'Evaluate' 
                      }}
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="no-tasks">
                <i class="fas fa-clipboard-check"></i>
                <p>No completed tasks pending evaluation</p>
                <p class="hint">Tasks will appear here after team members complete them</p>
              </div>
            </div>
          </div>

          <!-- Add new Evaluator Selection Modal -->
          <div v-if="showEvaluatorModal" class="modal evaluator-selection-modal">
            <div class="modal-content wide-modal">
              <span class="close" @click="closeEvaluatorModal">&times;</span>
              <h2>Who's evaluating?</h2>

              <div class="evaluator-profiles">
                <div 
                  v-for="evaluator in evaluators" 
                  :key="evaluator.id" 
                  class="evaluator-profile"
                  @click="selectEvaluator(selectedTask, evaluator)"
                  :class="{ 
                    'active': selectedEvaluator?.id === evaluator.id,
                    'disabled': isTaskAssignedToEvaluator(selectedTask, evaluator)
                  }"
                  :title="getEvaluatorDisabledMessage(selectedTask, evaluator)"
                >
                  <div class="evaluator-avatar large" :style="{ background: getAvatarGradient() }">
                    {{ getInitials(evaluator.name) }}
                  </div>
                  <div class="evaluator-name">{{ evaluator.name }}</div>
                  <div class="evaluator-stats">
                    {{ evaluator.tasksEvaluated || 0 }} evaluations
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Add this new Evaluation Modal -->
          <div v-if="showEvaluationModal" class="modal evaluation-modal">
            <div class="modal-content evaluation-content">
              <div class="modal-header">
                <h2>{{ `Evaluation by ${selectedEvaluator?.name}` }}</h2>
                <button class="close-btn" @click="closeEvaluationModal">&times;</button>
              </div>
              
              <div class="modal-body">
                <div class="rubric-container">
                  <div v-for="(category, categoryKey) in rubricData" :key="categoryKey" class="rubric-section">
                    <h3>{{ getCategoryTitle(categoryKey) }}</h3>
                    <table class="rubric-table">
                      <thead>
                        <tr>
                          <th>Criterion</th>
                          <th v-for="score in 5" :key="score">{{ score }} - {{ getScoreLabel(score) }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="criterion in category" :key="criterion.id">
                          <td class="criterion-name">{{ criterion.name }}</td>
                          <td 
                            v-for="score in 5" 
                            :key="score"
                            class="score-cell"
                            :class="{ selected: isScoreSelected(categoryKey, criterion.id, score) }"
                            @click="selectScore(categoryKey, criterion.id, score)"
                          >
                            <div class="score-content">
                              <div class="score-description">{{ criterion.descriptions[score-1] }}</div>
                              <div class="score-select"></div>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <div class="comments-section">
                    <label for="evaluation-comments">Additional Comments</label>
                    <textarea 
                      v-model="evaluationComments" 
                      id="evaluation-comments" 
                      class="evaluation-textarea"
                      placeholder="Add your comments here..."
                    ></textarea>
                  </div>
                </div>
              </div>

              <div class="modal-footer">
                <button class="btn-primary w-50" @click="submitEvaluation">Submit Evaluation</button>
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
  name: 'EvaluateTask',
  components: {
    ResponsiveSidebar
  },
  data() {
    return {
      evaluators: JSON.parse(localStorage.getItem('evaluators')) || [],
      showModal: false,
      newEvaluator: {
        name: '',
        role: ''
      },
      showEvaluatorModal: false,
      selectedTask: null,
      selectedEvaluator: null,
      rubric: {
        consistencyBranding: {
          weight: 0.35,
          criteria: {
            mobileResponsiveness: 0,
            contrastVisibility: 0,
            brandGuidelinesAdherence: 0
          }
        },
        creativeQuality: {
          weight: 0.45,
          criteria: {
            visualAppeal: 0,
            clarityComm: 0,
            innovationExecution: 0
          }
        },
        timeliness: {
          weight: 0.20,
          criteria: {
            deliveryTimeliness: 0,
            schedulingPlanning: 0,
            taskOrderAdherence: 0
          }
        }
      },
      rubricData: {
        consistencyBranding: [
          {
            id: 'mobileResponsiveness',
            name: 'Mobile Responsiveness',
            descriptions: [
              'Unresponsive design; mobile users struggle to navigate.',
              'Major usability issues; several elements break on mobile.',
              'Acceptable responsiveness; minor issues noted.',
              'Mostly responsive with only slight glitches.',
              'Fully responsive with a seamless mobile experience.'
            ]
          },
          {
            id: 'contrastVisibility',
            name: 'Contrast & Visibility',
            descriptions: [
              'Poor contrast making content unreadable.',
              'Several areas with low contrast; hard to read.',
              'Generally acceptable; minor adjustments needed.',
              'Clear, good contrast with minor imperfections.',
              'Outstanding clarity and accessibility.'
            ]
          },
          {
            id: 'brandGuidelinesAdherence',
            name: 'Brand Guidelines Adherence',
            descriptions: [
              'Colors, fonts, and layouts are inconsistent with the brand.',
              'Frequent deviations from the brand guidelines.',
              'Generally follows guidelines with some minor deviations.',
              'Largely consistent with established brand standards.',
              'Perfect alignment with all brand guidelines (incl. 60-30-10 rule).'
            ]
          }
        ],
        creativeQuality: [
          {
            id: 'visualAppeal',
            name: 'Visual Appeal & Engagement',
            descriptions: [
              'Unattractive, unengaging design.',
              'Lacks visual appeal; does little to engage the audience.',
              'Adequate design; meets basic expectations.',
              'Attractive and engaging with few minor issues.',
              'Exceptionally appealing, innovative, and highly engaging.'
            ]
          },
          {
            id: 'clarityComm',
            name: 'Clarity & Communication',
            descriptions: [
              'Message is very unclear or confusing.',
              'Several aspects are ambiguous; needs improvement.',
              'Conveys message adequately; some minor ambiguities.',
              'Clear and effective communication with only slight issues.',
              'Extremely clear, concise, and compelling messaging.'
            ]
          },
          {
            id: 'innovationExecution',
            name: 'Innovation & Execution',
            descriptions: [
              'Poor execution; no innovation observed.',
              'Minimal innovation with weak execution overall.',
              'Standard execution; meets requirements.',
              'Good execution with creative elements.',
              'Outstanding execution; highly innovative and polished.'
            ]
          }
        ],
        timeliness: [
          {
            id: 'deliveryTimeliness',
            name: 'Delivery Timeliness',
            descriptions: [
              'Extremely late; significant delay in delivery.',
              'Late delivery with notable impact on workflow.',
              'Delivered on time but with minor delays affecting quality.',
              'On time with only trivial issues in timing.',
              'Delivered promptly or even ahead of schedule as planned.'
            ]
          },
          {
            id: 'schedulingPlanning',
            name: 'Scheduling & Planning',
            descriptions: [
              'No planning evident; tasks appear randomly executed.',
              'Poor planning; misaligned with daily priorities.',
              'Average planning; some scheduling issues evident.',
              'Well-planned; mostly aligns with daily priorities.',
              'Exceptionally well-planned and integrated into the daily schedule.'
            ]
          },
          {
            id: 'taskOrderAdherence',
            name: 'Task Order Adherence',
            descriptions: [
              'Completely disregarded planned task order.',
              'Significant deviation from planned order, causing disruptions.',
              'Minor deviations from the planned order, but overall acceptable.',
              'Mostly adhered to planned order with slight exceptions.',
              'Fully followed the planned order; tasks executed in the intended sequence.'
            ]
          }
        ]
      },
      showEvaluationModal: false,
      evaluationComments: ''
    };
  },
  computed: {
    eligibleMembers() {
      const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
      return teamMembers.filter(member => 
        !this.evaluators.some(evaluator => evaluator.id === member.id)
      );
    },
    pendingTasks() {
      const allTasks = JSON.parse(localStorage.getItem('allTasks')) || [];
      const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
      const memberIds = teamMembers.map(m => m.id);

      // Filter tasks that:
      // 1. Are completed
      // 2. Have valid team members
      // 3. Have not been deleted
      // 4. Either have no evaluations or not all evaluators have evaluated
      return allTasks
        .filter(task => 
          task.status === 'completed' &&
          memberIds.includes(task.assignedTo) && 
          !task.deleted &&
          (!task.evaluations || task.evaluations.length < this.evaluators.length)
        )
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    },
    availableEvaluators() {
      const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
      return teamMembers.filter(member => 
        member.id !== this.selectedTask?.createdBy
      );
    },
    remainingEvaluators() {
      if (!this.selectedTask) return [];
      const evaluatedIds = this.selectedTask.evaluations?.map(e => e.evaluatorId) || [];
      return this.availableEvaluators.filter(member => 
        !evaluatedIds.includes(member.id)
      );
    },
    canSubmitEvaluation() {
      return this.selectedTask && 
             this.selectedEvaluator && 
             this.selectedEvaluator.id !== this.selectedTask.createdBy;
    }
  },
  created() {
    // Initialize evaluators from team members
    const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
    
    // Convert all team members to evaluators if none exist
    if (!this.evaluators.length) {
      this.evaluators = teamMembers.map(member => ({
        ...member,
        tasksEvaluated: 0
      }));
      this.saveEvaluators();
    } else {
      // Sync existing evaluators with team members
      this.syncEvaluatorsWithTeamMembers();
    }

    // Set up automatic sync when team members change
    window.addEventListener('storage', (e) => {
      if (e.key === 'teamMembers') {
        this.syncEvaluatorsWithTeamMembers();
      }
    });
  },
  methods: {
    viewEvaluatorTasks(evaluatorId) {
      // Implement logic to view tasks evaluated by the selected evaluator
      console.log('Viewing tasks for evaluator ID:', evaluatorId);
    },
    getPriorityClass(priority) {
      const classes = {
        major: 'priority-major',
        mid: 'priority-mid',
        minor: 'priority-minor'
      };
      return classes[priority.toLowerCase()] || 'priority-mid';
    },
    getPriorityIcon(priority) {
      const icons = {
        major: 'fas fa-exclamation-circle',
        mid: 'fas fa-arrow-circle-right',
        minor: 'fas fa-info-circle'
      };
      return icons[priority.toLowerCase()] || 'fas fa-circle';
    },
    showEvaluatorSelection(task) {
      this.selectedTask = task;
      this.selectedEvaluator = null;
      this.showEvaluatorModal = true;
    },
    closeEvaluatorModal() {
      this.showEvaluatorModal = false;
      this.selectedTask = null;
      this.selectedEvaluator = null;
    },
    hasEvaluatorReviewed(task, evaluatorId) {
      if (!task.evaluations) return false;
      return task.evaluations.some(evaluation => evaluation.evaluatorId === evaluatorId);
    },
    isTaskAssignedToEvaluator(task, evaluator) {
      return task.assignedTo === evaluator.id || this.hasEvaluatorReviewed(task, evaluator.id);
    },
    selectEvaluator(task, evaluator) {
      if (this.isTaskAssignedToEvaluator(task, evaluator)) {
        let message = task.assignedTo === evaluator.id 
          ? 'You cannot evaluate your own tasks.'
          : 'You have already evaluated this task.';

        window.Swal.fire({
          title: 'Not Allowed',
          text: message,
          icon: 'error',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
        return;
      }

      this.selectedEvaluator = evaluator;
      this.showEvaluatorModal = false;
      this.evaluateTask(task.id, evaluator);
    },
    getEvaluatorDisabledMessage(task, evaluator) {
      if (task.assignedTo === evaluator.id) {
        return 'Cannot evaluate own task';
      }
      if (this.hasEvaluatorReviewed(task, evaluator.id)) {
        return 'Already evaluated';
      }
      return '';
    },
    evaluateTask(taskId, evaluator) {
      const task = this.pendingTasks.find(t => t.id === taskId);
      if (!task) return;
      
      this.selectedTask = task;
      this.selectedEvaluator = evaluator;
      this.showEvaluationModal = true;
    },
    closeEvaluationModal() {
      this.showEvaluationModal = false;
      this.selectedTask = null;
      this.selectedEvaluator = null;
      this.evaluationComments = '';
      this.resetRubricScores();
    },
    getCategoryTitle(category) {
      const titles = {
        consistencyBranding: '1. Consistency & Branding (35%)',
        creativeQuality: '2. Creative Quality & Appeal (45%)',
        timeliness: '3. Timeliness & Execution (20%)'
      };
      return titles[category];
    },
    getScoreLabel(score) {
      const labels = {
        1: 'Poor',
        2: 'Below Average',
        3: 'Average',
        4: 'Above Average',
        5: 'Excellent'
      };
      return labels[score];
    },
    isScoreSelected(category, criterionId, score) {
      return this.rubric[category].criteria[criterionId] === score;
    },
    selectScore(category, criterionId, score) {
      this.rubric[category].criteria[criterionId] = score;
    },
    resetRubricScores() {
      Object.keys(this.rubric).forEach(category => {
        Object.keys(this.rubric[category].criteria).forEach(criterion => {
          this.rubric[category].criteria[criterion] = 0;
        });
      });
    },
    generateRubricHtml(task) {
      return `
        <div class="rubric-container">
          <div class="rubric-section">
            <h3>1. Consistency & Branding (35%)</h3>
            ${this.generateCriteriaTable('consistencyBranding')}
          </div>
          
          <div class="rubric-section">
            <h3>2. Creative Quality & Appeal (45%)</h3>
            ${this.generateCriteriaTable('creativeQuality')}
          </div>
          
          <div class="rubric-section">
            <h3>3. Timeliness & Execution (20%)</h3>
            ${this.generateCriteriaTable('timeliness')}
          </div>
          
          <div class="comments-section">
            <label for="evaluation-comments">Additional Comments</label>
            <textarea id="evaluation-comments" class="swal2-textarea"></textarea>
          </div>
        </div>
      `;
    },
    generateCriteriaTable(category) {
      const criteriaData = this.getRubricData(category);
      return `
        <table class="rubric-table">
          <thead>
            <tr>
              <th>Criterion</th>
              <th>1 - Poor</th>
              <th>2 - Below Average</th>
              <th>3 - Average</th>
              <th>4 - Above Average</th>
              <th>5 - Excellent</th>
            </tr>
          </thead>
          <tbody>
            ${criteriaData.map(criterion => `
              <tr>
                <td>${criterion.name}</td>
                ${[1,2,3,4,5].map(score => `
                  <td class="score-cell" data-category="${category}" data-criterion="${criterion.id}" data-score="${score}">
                    <div class="score-content">
                      <div class="score-description">${criterion.descriptions[score-1]}</div>
                      <div class="score-select"></div>
                    </div>
                  </td>
                `).join('')}
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    },
    initializeRubricHandlers() {
      document.querySelectorAll('.score-cell').forEach(cell => {
        cell.addEventListener('click', () => {
          const { category, criterion, score } = cell.dataset;
          
          // Clear previous selection in this row
          cell.closest('tr').querySelectorAll('.score-cell').forEach(c => {
            c.classList.remove('selected');
          });
          
          // Select this cell
          cell.classList.add('selected');
          
          // Update rubric data
          this.rubric[category].criteria[criterion] = parseInt(score);
        });
      });
    },
    collectRubricScores() {
      return {
        consistencyBranding: { ...this.rubric.consistencyBranding.criteria },
        creativeQuality: { ...this.rubric.creativeQuality.criteria },
        timeliness: { ...this.rubric.timeliness.criteria }
      };
    },
    calculateScores(scores) {
      const categoryScores = {
        consistencyBranding: this.calculateCategoryScore(scores.consistencyBranding),
        creativeQuality: this.calculateCategoryScore(scores.creativeQuality),
        timeliness: this.calculateCategoryScore(scores.timeliness)
      };

      const passesMinimums = Object.values(categoryScores).every(score => score >= 60);
      
      const finalScore = 
        (categoryScores.consistencyBranding * 0.35) +
        (categoryScores.creativeQuality * 0.45) +
        (categoryScores.timeliness * 0.20);

      return {
        passesMinimums,
        categoryScores,
        finalScore
      };
    },
    calculateCategoryScore(criteria) {
      const scores = Object.values(criteria);
      const average = scores.reduce((a, b) => a + b, 0) / scores.length;
      const percentage = (average / 5) * 100; // Convert to percentage
      return {
        average,
        percentage,
        passes: percentage >= 60 // Check minimum requirement
      };
    },

    calculateFinalScores() {
      // Calculate individual category scores
      const categoryResults = {
        consistencyBranding: this.calculateCategoryScore(this.rubric.consistencyBranding.criteria),
        creativeQuality: this.calculateCategoryScore(this.rubric.creativeQuality.criteria),
        timeliness: this.calculateCategoryScore(this.rubric.timeliness.criteria)
      };

      // Calculate weighted scores
      const weightedScores = {
        consistencyBranding: categoryResults.consistencyBranding.percentage * 0.35,
        creativeQuality: categoryResults.creativeQuality.percentage * 0.45,
        timeliness: categoryResults.timeliness.percentage * 0.20
      };

      // Calculate final score
      const finalScore = Object.values(weightedScores).reduce((a, b) => a + b, 0);

      // Check if all categories pass minimum requirement
      const allCategoriesPass = Object.values(categoryResults).every(score => score.passes);
      
      // Overall pass requires all categories to pass and final score >= 70%
      const passes = allCategoriesPass && finalScore >= 70;

      // Construct the final results object with all necessary details
      return {
        finalScore,
        passes,
        details: {
          consistencyBranding: {
            ...categoryResults.consistencyBranding,
            weight: '35%',
            weightedScore: weightedScores.consistencyBranding,
            passes: categoryResults.consistencyBranding.passes
          },
          creativeQuality: {
            ...categoryResults.creativeQuality,
            weight: '45%',
            weightedScore: weightedScores.creativeQuality,
            passes: categoryResults.creativeQuality.passes
          },
          timeliness: {
            ...categoryResults.timeliness,
            weight: '20%',
            weightedScore: weightedScores.timeliness,
            passes: categoryResults.timeliness.passes
          }
        }
      };
    },

    async submitEvaluation() {
      console.log('submitEvaluation called');

      if (!this.canSubmitEvaluation) {
        window.Swal.fire({
          title: 'Cannot Evaluate',
          text: 'Task creators cannot evaluate their own tasks',
          icon: 'warning',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
        return;
      }

      // Ask for confirmation first
      const confirmResult = await Swal.fire({
        title: 'Submit Evaluation?',
        text: 'Are you sure you want to submit this evaluation? This action cannot be undone.',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#ff0000',
        cancelButtonColor: '#1a1a1a',
        confirmButtonText: 'Yes, submit it!',
        background: '#1a1a1a',
        color: '#ffffff'
      });

      if (!confirmResult.isConfirmed) {
        return;
      }

      const evaluationResults = this.calculateFinalScores();
      
      // Show loading state
      Swal.fire({
        title: 'Submitting Evaluation...',
        text: 'Please wait while we process your submission.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        background: '#1a1a1a',
        color: '#ffffff',
        willOpen: () => {
          Swal.showLoading();
        }
      });

      try {
        // Create evaluation object with detailed scoring
        const evaluation = {
          evaluatorId: this.selectedEvaluator.id,
          evaluatorName: this.selectedEvaluator.name,
          date: new Date().toISOString(),
          scores: this.collectRubricScores(),
          results: evaluationResults,
          comments: this.evaluationComments
        };

        // Get current task and update its evaluations
        const allTasks = JSON.parse(localStorage.getItem('allTasks')) || [];
        const taskIndex = allTasks.findIndex(t => t.id === this.selectedTask.id);
        
        if (taskIndex === -1) {
          throw new Error('Task not found');
        }

        const task = allTasks[taskIndex];
        const evaluations = task.evaluations || [];

        evaluations.push(evaluation);
        task.evaluations = evaluations;

        const hasAllEvaluations = evaluations.length === this.availableEvaluators.length;
        
        if (hasAllEvaluations) {
          const overallResults = this.calculateOverallResults(evaluations);
          task.evaluation = {
            ...overallResults,
            completed: true,
            lastUpdated: new Date().toISOString()
          };
        }

        // Save updates
        allTasks[taskIndex] = task;
        localStorage.setItem('allTasks', JSON.stringify(allTasks));

        // Update evaluator stats
        const evaluatorIndex = this.evaluators.findIndex(e => e.id === this.selectedEvaluator.id);
        if (evaluatorIndex !== -1) {
          this.evaluators[evaluatorIndex].tasksEvaluated++;
          this.saveEvaluators();
        }

        // Show success message
        await Swal.fire({
          title: 'Evaluation Submitted!',
          text: 'Your evaluation has been successfully submitted.',
          icon: 'success',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#10b981'
        });

        // Then show the detailed results
        await this.showEvaluationResults(evaluationResults, hasAllEvaluations);
        this.closeEvaluationModal();

      } catch (error) {
        console.error('Error submitting evaluation:', error);
        await Swal.fire({
          title: 'Error!',
          text: 'Failed to submit evaluation. Please try again.',
          icon: 'error',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
      }
    },

    async showEvaluationResults(results, isFinal) {
      console.log('showEvaluationResults called'); // Debug log
      const resultHtml = `
        <div class="evaluation-results">
          <div class="eval-header">
            <h3 class="eval-title">Evaluation Summary</h3>
            <div class="eval-status ${results.passes ? 'pass' : 'fail'}">
              ${results.passes ? 'PASSED' : 'FAILED'}
            </div>
          </div>

          <div class="eval-score">
            <div class="score-ring ${results.passes ? 'pass' : 'fail'}">
              ${results.finalScore.toFixed(1)}%
            </div>
            <p class="score-message">${results.passes ? 
              'All requirements met' : 
              'Does not meet requirements'}</p>
          </div>

          <div class="eval-categories">
            ${Object.entries(results.details).map(([category, data]) => `
              <div class="eval-category ${data.passes ? 'pass' : 'fail'}">
                <div class="category-header">
                  <h4>${this.getCategoryTitle(category)}</h4>
                  <span class="category-value ${data.passes ? 'pass' : 'fail'}">
                    ${data.percentage.toFixed(1)}%
                  </span>
                </div>
                <div class="category-details">
                  <div class="detail-row">
                    <span>Raw Score:</span>
                    <span>${data.percentage.toFixed(1)}%</span>
                  </div>
                  <div class="detail-row">
                    <span>Weight:</span>
                    <span>${data.weight}</span>
                  </div>
                  <div class="detail-row">
                    <span>Weighted Score:</span>
                    <span>${data.weightedScore.toFixed(1)}%</span>
                  </div>
                  <div class="requirement-status ${data.passes ? 'pass' : 'fail'}">
                    ${data.passes ? '✓' : '✗'} Minimum Requirement (60%)
                  </div>
                </div>
              </div>
            `).join('')}
          </div>

          ${this.evaluationComments ? `
            <div class="eval-comments">
              <h4>Additional Comments</h4>
              <p>${this.evaluationComments}</p>
            </div>
          ` : ''}

          <div class="eval-footer">
            <div class="evaluator-info">
              <span>Evaluated by:</span>
              <strong>${this.selectedEvaluator.name}</strong>
            </div>
            <div class="eval-date">
              ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}
            </div>
          </div>
        </div>
      `;

      // Add a style tag to the SweetAlert modal
      const modalStyle = `
        <style>
          .evaluation-results {
            color: #fff;
          }
          .eval-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
          }
          .eval-title {
            font-size: 1.5rem;
            margin: 0;
          }
          .eval-status {
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
          }
          .eval-status.pass {
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
          }
          .eval-status.fail {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
          }
          .eval-score {
            text-align: center;
            margin-bottom: 2rem;
          }
          .score-ring {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: 700;
            margin: 0 auto 1rem;
            border: 4px solid;
          }
          .score-ring.pass {
            border-color: #10b981;
            color: #10b981;
            background: rgba(16, 185, 129, 0.1);
          }
          .score-ring.fail {
            border-color: #ef4444;
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
          }
          .score-message {
            color: #9ca3af;
            margin: 0;
          }
          .eval-categories {
            display: flex;
            flex-direction: column;
            gap: 1rem;
          }
          .eval-category {
            background: rgba(30, 30, 30, 0.4);
            border-radius: 0.75rem;
            padding: 1.25rem;
          }
          .category-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
          }
          .category-header h4 {
            margin: 0;
            font-size: 1.1rem;
          }
          .category-value {
            font-size: 1.25rem;
            font-weight: 600;
          }
          .category-value.pass { color: #10b981; }
          .category-value.fail { color: #ef4444; }
          .category-details {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
          }
          .detail-row {
            display: flex;
            justify-content: space-between;
            color: #9ca3af;
            font-size: 0.9rem;
          }
          .requirement-status {
            margin-top: 0.5rem;
            padding: 0.5rem;
            border-radius: 0.25rem;
            text-align: center;
            font-size: 0.875rem;
          }
          .requirement-status.pass {
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
          }
          .requirement-status.fail {
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
          }
          .eval-comments {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
          }
          .eval-comments h4 {
            margin: 0 0 0.5rem 0;
            color: #fff;
          }
          .eval-comments p {
            background: rgba(30, 30, 30, 0.4);
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0;
            color: #e5e7eb;
          }
          .eval-footer {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #9ca3af;
            font-size: 0.875rem;
          }
          .evaluator-info strong {
            color: #fff;
            margin-left: 0.5rem;
          }
        </style>
      `;

      console.log('Showing SweetAlert with results'); // Debug log
      await Swal.fire({
        title: isFinal ? 'Final Evaluation Complete' : 'Evaluation Submitted',
        html: modalStyle + resultHtml,
        icon: results.passes ? 'success' : 'error',
        background: '#1a1a1a',
        color: '#ffffff',
        confirmButtonColor: '#ff0000',
        width: '600px',
        showCloseButton: true,
        allowOutsideClick: false
      });
    },

    getRubricData(category) {
      return this.rubricData[category] || [];
    },
    getMemberName(memberId) {
      // First check team members
      const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
      const member = teamMembers.find(m => m.id === memberId);
      if (member) {
        return member.name;
      }
      
      // If not found in team members, check evaluators
      const evaluator = this.evaluators.find(e => e.id === memberId);
      return evaluator ? evaluator.name : 'Unknown';
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(date);
    },
    getTotalEvaluations() {
      return this.evaluators.reduce((total, evaluator) => total + evaluator.tasksEvaluated, 0);
    },
    getAverageEvaluations() {
      return this.getTotalEvaluations() / this.evaluators.length;
    },
    showAddEvaluatorModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.newEvaluator = {
        name: '',
        role: ''
      };
    },
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('');
    },
    getAvatarGradient() {
      const hue = Math.random() * 360;
      return `linear-gradient(135deg, hsl(${hue}, 70%, 50%), hsl(${hue + 60}, 70%, 30%))`;
    },
    isEvaluator(memberId) {
      return this.evaluators.some(e => e.id === memberId);
    },
    addEvaluator() {
      const evaluator = {
        id: Date.now(),
        name: this.newEvaluator.name,
        role: this.newEvaluator.role,
        tasksEvaluated: 0,
        dateAdded: new Date().toISOString() // Add timestamp for tracking
      };

      this.evaluators.push(evaluator);
      this.saveEvaluators();
      
      // Reset form and show success message
      this.newEvaluator = { name: '', role: '' };
      
      window.Swal.fire({
        title: 'Success!',
        text: 'Evaluator added successfully',
        icon: 'success',
        background: '#1a1a1a',
        color: '#ffffff',
        confirmButtonColor: '#ff0000'
      });

      // Add notification for new evaluator
      notificationStore.addNotification({
        id: Date.now(),
        type: 'info',
        title: 'New Evaluator Added',
        message: `${this.newEvaluator.name} has been added as an evaluator`
      });

      // Emit activity for new evaluator
      eventBus.emit('activity-created', {
        type: 'member',
        title: `New evaluator "${this.newEvaluator.name}" added`
      });

      this.closeModal();
    },
    isTeamMember(evaluatorId) {
      const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
      return teamMembers.some(member => member.id === evaluatorId);
    },

    getEvaluatorActionTitle(evaluator) {
      return this.isTeamMember(evaluator.id) 
        ? 'Team members cannot be removed from evaluators'
        : 'Remove additional evaluator';
    },

    async removeEvaluator(evaluator) {
      if (this.isTeamMember(evaluator.id)) {
        await Swal.fire({
          title: 'Cannot Remove Team Member',
          text: 'Team members are automatically evaluators and cannot be removed.',
          icon: 'warning',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
        return;
      }

      const result = await Swal.fire({
        title: 'Remove Additional Evaluator?',
        text: `Are you sure you want to remove ${evaluator.name} from evaluators?`,
        icon: 'warning',
        background: '#1a1a1a',
        color: '#ffffff',
        confirmButtonColor: '#ff0000',
        showCancelButton: true,
        confirmButtonText: 'Yes, remove',
        cancelButtonText: 'Cancel'
      });

      if (result.isConfirmed) {
        this.evaluators = this.evaluators.filter(e => e.id !== evaluator.id);
        this.saveEvaluators();
        
        await Swal.fire({
          title: 'Evaluator Removed',
          text: `${evaluator.name} has been removed from evaluators.`,
          icon: 'success',
          background: '#1a1a1a',
          color: '#ffffff',
          confirmButtonColor: '#ff0000'
        });
      }
    },

    // Update sync method to preserve additional evaluators
    syncEvaluatorsWithTeamMembers() {
      try {
        const teamMembers = JSON.parse(localStorage.getItem('teamMembers')) || [];
        const currentEvaluators = this.evaluators;
        
        // Split evaluators into team members and additional evaluators
        const additionalEvaluators = currentEvaluators.filter(
          evaluator => !teamMembers.some(member => member.id === evaluator.id)
        );
        
        // Create new evaluators array with team members
        this.evaluators = [
          ...teamMembers.map(member => ({
            ...member,
            tasksEvaluated: currentEvaluators.find(e => e.id === member.id)?.tasksEvaluated || 0
          })),
          ...additionalEvaluators // Keep additional evaluators
        ];
        
        this.saveEvaluators();
      } catch (error) {
        console.error('Error syncing evaluators:', error);
      }
    },
    saveEvaluators() {
      // Save full evaluator data including stats and timestamp
      localStorage.setItem('evaluators', JSON.stringify(this.evaluators));
    },

    getDetailedEvaluation() {
      const details = {};
      
      Object.keys(this.rubricData).forEach(category => {
        details[category] = this.rubricData[category].map(criterion => ({
          criterion: criterion.name,
          score: this.rubric[category].criteria[criterion.id],
          description: criterion.descriptions[this.rubric[category].criteria[criterion.id] - 1]
        }));
      });

      return details;
    },

    calculateOverallResults(evaluations) {
      // Calculate average scores for each category
      const categoryAverages = {
        consistencyBranding: { sum: 0, count: 0 },
        creativeQuality: { sum: 0, count: 0 },
        timeliness: { sum: 0, count: 0 }
      };

      evaluations.forEach(evaluation => {
        // Access the scores data from the correct path in the evaluation object
        const scores = evaluation.results.details;
        Object.entries(scores).forEach(([category, data]) => {
          if (categoryAverages[category]) {
            categoryAverages[category].sum += data.weightedScore;
            categoryAverages[category].count++;
          }
        });
      });

      // Calculate final category results
      const categoryResults = {};
      Object.entries(categoryAverages).forEach(([category, data]) => {
        const average = data.count > 0 ? data.sum / data.count : 0;
        categoryResults[category] = {
          percentage: average,
          passes: average >= 60
        };
      });

      // Calculate weighted scores
      const weightedScores = {
        consistencyBranding: categoryResults.consistencyBranding.percentage * 0.35,
        creativeQuality: categoryResults.creativeQuality.percentage * 0.45,
        timeliness: categoryResults.timeliness.percentage * 0.20
      };

      // Calculate final score and determine if it passes
      const finalScore = Object.values(weightedScores).reduce((a, b) => a + b, 0);
      const allCategoriesPass = Object.values(categoryResults).every(cat => cat.passes);
      const passes = finalScore >= 70 && allCategoriesPass;

      return {
        categoryResults,
        weightedScores,
        finalScore,
        passes,
        details: {
          consistencyBranding: {
            ...categoryResults.consistencyBranding,
            weight: '35%',
            weightedScore: weightedScores.consistencyBranding
          },
          creativeQuality: {
            ...categoryResults.creativeQuality,
            weight: '45%',
            weightedScore: weightedScores.creativeQuality
          },
          timeliness: {
            ...categoryResults.timeliness,
            weight: '20%',
            weightedScore: weightedScores.timeliness
          }
        }
      };
    }
  }
};
</script>

<style scoped>
.wrapper {
  display: flex;
  width: 100%;
  align-items: stretch;
  min-height: 100vh;
  background: #000000;
  color: #ffffff;
}

.content-wrapper {
    width: 100%;
    min-height: 100vh;
    transition: all 0.3s;
    background: #000000;
  }

 
.dashboard-container {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 2rem;
  padding: 1rem 0;
  background-color: #000000;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.sticky-header {
  position: sticky;
  top: 0;
}

.dashboard-header h1 {
  font-size: 2.25rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
  letter-spacing: -0.5px;
}

.dashboard-header .description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 0.5rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

/* Stats Card */
.stats-card {
  grid-column: 1 / -1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.stat-item {
  background: rgba(255, 0, 0, 0.1);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Evaluators Card */
.evaluator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.evaluator-item {
  display: flex;
  align-items: center;
  background: rgba(26, 26, 26, 0.6);
  padding: 1.25rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  transition: all 0.2s;
}

.evaluator-item:hover {
  background: rgba(26, 26, 26, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.evaluator-avatar {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(255, 0, 0, 0.7), rgba(153, 0, 0, 0.7));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  font-size: 1.25rem;
  margin-right: 1rem;
  flex-shrink: 0;
}

.evaluator-info {
  flex-grow: 1;
}

.evaluator-name {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.evaluator-role {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.25rem;
}

.evaluator-tasks {
  font-size: 0.8rem;
  color: rgba(255, 0, 0, 0.7);
}

.btn-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-icon:hover {
  background: rgba(255, 0, 0, 0.2);
  color: #ffffff;
}

/* Tasks Card */
.task-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.task-item {
  background: rgba(26, 26, 26, 0.6);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}

.task-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.task-header {
  padding: 1.25rem;
  border-bottom: 1px solid rgba(255, 0, 0, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(10, 10, 10, 0.5);
}

.task-title {
  font-weight: 600;
  font-size: 1.1rem;
}

.task-body {
  padding: 1.25rem;
  flex-grow: 1;
}

.task-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  margin: 0;
}

.task-footer {
  padding: 1.25rem;
  border-top: 1px solid rgba(255, 0, 0, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(10, 10, 10, 0.3);
}

.task-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.meta-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin-right: 0.5rem;
}

.meta-value {
  font-size: 0.9rem;
  color: #ffffff;
  font-weight: 500;
}

.priority-badge {
  padding: 0.3rem 0.7rem;
  border-radius: 0.4rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.priority-high {
  background-color: rgba(255, 59, 48, 0.2);
  color: rgb(255, 59, 48);
  border: 1px solid rgba(255, 59, 48, 0.3);
}

.priority-medium {
  background-color: rgba(255, 149, 0, 0.2);
  color: rgb(255, 149, 0);
  border: 1px solid rgba(255, 149, 0, 0.3);
}

.priority-low {
  background-color: rgba(52, 199, 89, 0.2);
  color: rgb(52, 199, 89);
  border: 1px solid rgba(52, 199, 89, 0.3);
}

.card {
  background-color: rgba(26, 26, 26, 0.4);
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(145deg, rgba(30, 30, 30, 0.4) 0%, rgba(20, 20, 20, 0.4) 100%);
  border-bottom: 1px solid rgba(255, 0, 0, 0.2);
}

.card-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.card-content {
  padding: 1.5rem;
}

.btn-primary {
  background: linear-gradient(to right, rgba(255, 0, 0, 0.8), rgba(153, 0, 0, 0.8));
  color: #ffffff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(255, 0, 0, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(to right, rgba(255, 0, 0, 1), rgba(153, 0, 0, 1));
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 0, 0, 0.4);
}

.evaluator-actions {
  display: flex;
  gap: 0.5rem;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.member-item:not(.already-evaluator):hover {
  background: rgba(255, 0, 0, 0.1);
}

.member-item.already-evaluator {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(0, 0, 0, 0.2);
}

.member-status {
  margin-left: auto;
  font-size: 0.875rem;
  color: #9ca3af;
}

.eligible-members {
  max-height: 400px;
  overflow-y: auto;
  margin-top: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.5rem;
  background: rgba(26, 26, 26, 0.6);
  color: #ffffff;
  margin-top: 0.5rem;
}

.form-input:focus {
  outline: none;
  border-color: rgba(255, 0, 0, 0.5);
  box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #1a1a1a;
  padding: 2rem;
  border-radius: 1rem;
  width: 100%;
  max-width: 500px;
  position: relative;
  border: 1px solid rgba(255, 0, 0, 0.2);
}

.close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  cursor: pointer;
  color: #ffffff;
}

.no-tasks {
  text-align: center;
  padding: 3rem 1rem;
  color: rgba(255, 255, 255, 0.6);
}

.no-tasks i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: rgba(255, 0, 0, 0.3);
}

.no-tasks .hint {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 0.5rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.priority-major {
  background: linear-gradient(135deg, rgba(255, 59, 48, 0.2), rgba(255, 0, 0, 0.1));
  color: #ff3b30;
  border: 1px solid rgba(255, 59, 48, 0.3);
}

.priority-mid {
  background: linear-gradient(135deg, rgba(255, 149, 0, 0.2), rgba(255, 100, 0, 0.1));
  color: #ff9500;
  border: 1px solid rgba(255, 149, 0, 0.3);
}

.priority-minor {
  background: linear-gradient(135deg, rgba(52, 199, 89, 0.2), rgba(0, 179, 89, 0.1));
  color: #34c759;
  border: 1px solid rgba(52, 199, 89, 0.3);
}

.card {
  background-color: rgba(26, 26, 26, 0.4);
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(145deg, rgba(30, 30, 30, 0.4) 0%, rgba(20, 20, 20, 0.4) 100%);
  border-bottom: 1px solid rgba(255, 0, 0, 0.2);
}

.card-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.card-content {
  padding: 1.5rem;
}

.btn-primary {
  background: linear-gradient(to right, rgba(255, 0, 0, 0.8), rgba(153, 0, 0, 0.8));
  color: #ffffff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(255, 0, 0, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(to right, rgba(255, 0, 0, 1), rgba(153, 0, 0, 1));
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 0, 0, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(255, 0, 0, 0.2);
}

.evaluator-actions {
  display: flex;
  gap: 0.5rem;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.member-item:not(.already-evaluator):hover {
  background: rgba(255, 0, 0, 0.1);
}

.member-item.already-evaluator {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(0, 0, 0, 0.2);
}

.member-status {
  margin-left: auto;
  font-size: 0.875rem;
  color: #9ca3af;
}

.eligible-members {
  max-height: 400px;
  overflow-y: auto;
  margin-top: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.5rem;
  background: rgba(26, 26, 26, 0.6);
  color: #ffffff;
  margin-top: 0.5rem;
}

.form-input:focus {
  outline: none;
  border-color: rgba(255, 0, 0, 0.5);
  box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #1a1a1a;
  padding: 2rem;
  border-radius: 1rem;
  width: 100%;
  max-width: 500px;
  position: relative;
  border: 1px solid rgba(255, 0, 0, 0.2);
}

.close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  cursor: pointer;
  color: #ffffff;
}

.no-tasks {
  text-align: center;
  padding: 3rem 1rem;
  color: rgba(255, 255, 255, 0.6);
}

.no-tasks i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: rgba(255, 0, 0, 0.3);
}

.no-tasks .hint {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 0.5rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.priority-major {
  background: linear-gradient(135deg, rgba(255, 59, 48, 0.2), rgba(255, 0, 0, 0.1));
  color: #ff3b30;
  border: 1px solid rgba(255, 59, 48, 0.3);
}

.priority-mid {
  background: linear-gradient(135deg, rgba(255, 149, 0, 0.2), rgba(255, 100, 0, 0.1));
  color: #ff9500;
  border: 1px solid rgba(255, 149, 0, 0.3);
}

.priority-minor {
  background: linear-gradient(135deg, rgba(52, 199, 89, 0.2), rgba(0, 179, 89, 0.1));
  color: #34c759;
  border: 1px solid rgba(52, 199, 89, 0.3);
}

.wide-modal {
  max-width: 800px;
}

.evaluator-profiles {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
  padding: 1rem;
}

.evaluator-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  border-radius: 0.75rem;
  background: rgba(26, 26, 26, 0.6);
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.evaluator-profile:hover {
  transform: translateY(-5px);
  background: rgba(26, 26, 26, 0.8);
  border-color: rgba(255, 0, 0, 0.3);
}

.evaluator-profile.active {
  border-color: #ff0000;
  background: rgba(255, 0, 0, 0.1);
}

.evaluator-avatar.large {
  width: 5rem;
  height: 5rem;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.evaluator-stats {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
}

.evaluator-selection-modal h2 {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.75rem;
  color: #ffffff;
}

.evaluator-profile.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(255, 0, 0, 0.1);
  border-color: rgba(255, 0, 0, 0.2);
}

.evaluator-profile.disabled:hover {
  transform: none;
  background: rgba(255, 0, 0, 0.1);
  border-color: rgba(255, 0, 0, 0.2);
}

.evaluator-profile.disabled::after {
  content: attr(title);
  position: absolute;
  bottom: -2rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.75rem;
  color: rgba(255, 0, 0, 0.8);
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s;
}

.title{
  font-size: 22px;
  color: rgb(215, 215, 215);
}

.evaluator-profile.disabled:hover::after {
  opacity: 1;
}

.rubric-table {
  width: 100%;
  margin-bottom: 2rem;
  border-collapse: separate;
  border-spacing: 2px;
  background: rgba(26, 26, 26, 0.6);
  border-radius: 0.75rem;
  overflow: hidden;
}

.rubric-table th,
.rubric-table td {
  padding: 1rem;
  background: rgba(20, 20, 20, 0.8);
  border: none;
  position: relative;
}

.rubric-table th {
  background: rgba(255, 0, 0, 0.1);
  color: #fff;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rubric-table td:first-child {
  background: rgba(255, 0, 0, 0.05);
  font-weight: 500;
  width: 200px;
}

.score-cell {
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
}

.score-cell:hover {
  background: rgba(255, 0, 0, 0.15);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 0, 0, 0.1);
}

.score-content {
  position: relative;
  padding: 0.5rem;
}

.score-description {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.4;
  margin-bottom: 1.5rem;
  min-height: 60px;
}

.score-select {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 0, 0, 0.3);
  border-radius: 50%;
  transition: all 0.2s ease;
}

.score-cell:hover .score-select {
  border-color: rgba(255, 0, 0, 0.6);
  transform: scale(1.1);
}

.score-cell.selected {
  background: rgba(255, 0, 0, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 0, 0, 0.15);
}

.selected .score-select {
  background: #ff0000;
  border-color: #ff0000;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
}

.selected .score-select::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 0.8rem;
}

.rubric-section h3 {
  color: #ff3333;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(255, 0, 0, 0.2);
}

/* Score hover effect */
.score-cell::before {
  content: attr(data-score);
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: rgba(255, 0, 0, 0.6);
  opacity: 0;
  transform: translateY(-5px);
  transition: all 0.2s ease;
}

.score-cell:hover::before {
  opacity: 1;
  transform: translateY(0);
}

/* Add responsive styles */
@media (max-width: 768px) {
  .rubric-table {
    font-size: 0.9rem;
  }

  .score-description {
    font-size: 0.8rem;
    min-height: 80px;
  }

  td:first-child {
    width: 150px;
  }

}

.comments-section {
  margin-top: 2rem;
}

.rubric-section {
  margin-bottom: 2rem;
}

.rubric-section h3 {
  margin-bottom: 1rem;
  color: #ff3333;
  font-size: 1.1rem;
}

/* Enhanced Rubric Modal Styles */
.rubric-container {
  padding: 1rem;
}

.rubric-table {
  width: 100%;
  margin-bottom: 2rem;
  border-collapse: separate;
  border-spacing: 2px;
  border: 1px solid rgba(255, 0, 0, 0.2);
}

.rubric-table th,
.rubric-table td {
  border: 1px solid rgba(255, 0, 0, 0.2);
  padding: 1rem;
  text-align: left;
  background: rgba(20, 20, 20, 0.8);
}

.rubric-table th {
  background: rgba(255, 0, 0, 0.1);
  font-weight: 600;
  color: #fff;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}

.rubric-table td:first-child {
  background: rgba(255, 0, 0, 0.05);
  font-weight: 500;
  width: 200px;
  position: sticky;
  left: 0;
}

.score-cell {
  cursor: pointer;
  transition: all 0.2s ease;
  vertical-align: top;
  min-width: 150px;
  border: 1px solid rgba(255, 0, 0, 0.2) !important;
}

.score-cell:hover {
  background: rgba(255, 0, 0, 0.1) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 0, 0, 0.1);
}

.score-content {
  position: relative;
  padding: 0.5rem;
  min-height: 120px;
  display: flex;
  flex-direction: column;
}

.score-description {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.4;
  margin-bottom: 1.5rem;
}

.score-select {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 0, 0, 0.3);
  border-radius: 50%;
  transition: all 0.2s ease;
}

.score-cell.selected {
  background: rgba(255, 0, 0, 0.15) !important;
  border-color: #ff0000 !important;
}

.selected .score-select {
  background: #ff0000;
  border-color: #ff0000;
}

.selected .score-select::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 0.8rem;
}

.comments-section {
  margin-top: 2rem;
  border-top: 1px solid rgba(255, 0, 0, 0.2);
  padding-top: 1rem;
}

.comments-section label {
  display: block;
  margin-bottom: 0.5rem;
  color: #fff;
  font-weight: 500;
}

.comments-section textarea {
  width: 100%;
  min-height: 100px;
  background: rgba(20, 20, 20, 0.8);
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.5rem;
  color: #fff;
  padding: 1rem;
  margin-top: 0.5rem;
}

/* Score level indicators */
.score-cell::before {
  content: attr(data-score);
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: #ff0000;
  opacity: 0.6;
}

/* Make the modal content scrollable */
.swal2-popup {
  max-height: 90vh !important;
  overflow-y: auto !important;
}

.swal2-html-container {
  max-height: none !important;
  overflow: visible !important;
}

/* Add responsive styles */
@media (max-width: 992px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .dashboard-container {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header h1 {
    font-size: 1.75rem;
  }
  
  .dashboard-header .description {
    font-size: 0.95rem;
  }
}

/* New Modal Styles */
.evaluation-modal {
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
  overflow: hidden; /* Prevent outer scrolling */
}

.evaluation-content {
  background: #1a1a1a;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  border-radius: 1rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Remove any scrolling here */
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 0, 0, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(145deg, rgba(30, 30, 30, 0.4) 0%, rgba(20, 20, 20, 0.4) 100%);
}

.modal-header h2 {
  color: #ffffff;
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: #ffffff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 0, 0, 0.1);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
  /* Consistent scrollbar styling */
  scrollbar-width: thin;
  scrollbar-color: #ff0000 #1a1a1a;
}

/* Webkit scrollbar styles */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #1a1a1a;
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #ff0000, #990000);
  border-radius: 4px;
  border: 2px solid #1a1a1a;
}

/* Remove individual section scrolling */
.rubric-container {
  padding: 1rem;
  /* remove max-height and overflow properties */
}

/* Remove table container scrolling */
.table-container {
  overflow: visible;
  /* remove max-height property */
}

/* Ensure tables don't create horizontal scroll */
.rubric-table {
  table-layout: fixed; /* Prevent table from expanding */
  width: 100%;
}

.score-cell {
  word-break: break-word; /* Handle long content */
}

/* Hide any other scrollbars */
.rubric-section,
.table-container,
.activity-timeline {
  overflow: visible;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 0, 0, 0.2);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: rgba(20, 20, 20, 0.8);
}

.evaluation-textarea {
  width: 100%;
  min-height: 100px;
  background: rgba(20, 20, 20, 0.8);
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-radius: 0.5rem;
  color: #ffffff;
  padding: 1rem;
  margin-top: 0.5rem;
  resize: vertical;
}

.evaluation-textarea:focus {
  outline: none;
  border-color: #ff0000;
  box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.1);
}

/* Additional table styles */
.criterion-name {
  font-weight: 500;
  color: #ffffff;
  background: rgba(255, 0, 0, 0.05);
  white-space: nowrap;
  min-width: 200px;
}

.rubric-table {
  margin: 1rem 0;
  border: 1px solid rgba(255, 0, 0, 0.2);
  border-collapse: collapse;
  width: 100%;
}

.rubric-table th,
.rubric-table td {
  border: 1px solid rgba(255, 0, 0, 0.2);
  padding: 1rem;
}
.evaluation-results {
  text-align: left;
  padding: 1rem;
}

.category-scores {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1rem 0;
}

.category {
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 0, 0, 0.2);
}

.category.passing {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.2);
}

.category.failing {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.2);
}

.score-details {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #9ca3af;
}

.final-score {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
}

.final-score.passing {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.final-score.failing {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.evaluation-results {
  text-align: left;
  padding: 1rem;
}

.evaluation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.overall-status {
  font-size: 1.25rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
}

.status-pass {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.status-fail {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.final-score-section {
  text-align: center;
  margin-bottom: 2rem;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  margin: 0 auto 1rem;
  border: 4px solid;
}

.score-circle.passing {
  border-color: #10b981;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.score-circle.failing {
  border-color: #ef4444;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.score-note {
  color: #9ca3af;
  font-size: 0.875rem;
}

.category {
  background: rgba(30, 30, 30, 0.4);
  border-radius: 0.75rem;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.category-score {
  font-size: 1.25rem;
  font-weight: 600;
}

.category-score.passing {
  color: #10b981;
}

.category-score.failing {
  color: #ef4444;
}

.score-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.score-label {
  color: #9ca3af;
}

.minimum-requirement {
  margin-top: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.25rem;
  text-align: center;
  font-size: 0.875rem;
}

.minimum-requirement.met {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.minimum-requirement.not-met {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.comments-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.comment-text {
  background: rgba(30, 30, 30, 0.4);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  color: #e5e7eb;
}

.evaluation-footer {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #9ca3af;
  font-size: 0.875rem;
}

.evaluator-name {
  color: #ffffff;
  font-weight: 500;
  margin-left: 0.5rem;
}

/* SweetAlert custom styles */
:deep(.evaluation-summary-popup) {
  max-width: 600px !important;
}

:deep(.evaluation-summary-container) {
  margin: 0;
  padding: 0;
}

.modal.evaluation-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  overflow: auto;
}

.modal-content.evaluation-content {
  border-radius: 8px;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 5px;
}

@media screen and (max-width: 768px) {
  .modal-content.evaluation-content {
    width: 100%;
    margin: 5px;
    padding: 5px;
  }

  .rubric-table {
    width: 100%;
    border-collapse: collapse;
  }

  .rubric-table thead {
    display: none; /* Hide original header */
  }

  .rubric-table tbody tr {
    display: block;
    margin-bottom: 10px;
    border-radius: 20px !important;
  }

  .rubric-table tbody td {
    display: block;
    text-align: left;
    padding: 8px;
  }

  .rubric-table tbody td:first-child {
    font-weight: bold;
  }

  .score-cell {
    position: relative;
    padding: 8px;
  }

  .score-cell .score-content {
    display: flex;
    flex-direction: column;
  }

  .score-cell .score-description {
    margin-bottom: 5px;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .comments-section {
    margin-top: 15px;
  }

  .modal-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
  }

  .modal-footer button {
    flex-grow: 1;
    margin: 0 5px;
  }
}

</style>
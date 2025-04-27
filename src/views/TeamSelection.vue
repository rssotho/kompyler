<template>
  <div class="selection-page">
    <div class="container team-selection-container">
      <div class="header">
        <h1>Welcome to Your Team Space</h1>
        <p>Select your team to continue to your personalized dashboard</p>
      </div>
      
      <div class="teams-grid">
        <div 
          v-for="team in teams" 
          :key="team.id" 
          class="team-card" 
          :class="{ 'selected': selectedTeam === team.id }"
          @click="selectTeam(team.id)"
        >
          <div class="selected-indicator">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="team-image">
            <img :src="team.imageUrl" :alt="team.name">
          </div>
          <div class="team-content">
            <h3 class="team-name">{{ team.name }}</h3>
            <p class="team-description">{{ team.description }}</p>
            <div class="team-stats">
              <span class="members">
                <i class="fas fa-users"></i> {{ team.members }} members
              </span>
              <span class="projects">
                <i class="fas fa-project-diagram"></i> {{ team.projects }} projects
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="selection-footer">
        <button 
          class="continue-btn" 
          :disabled="!selectedTeam"
          @click="continueToDashboard"
        >
          <span @click="$router.push('/dashboard')">Continue to Dashboard</span>
          <i class="fas fa-arrow-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedTeam: null,
      teams: [
        {
          id: 1,
          name: 'Development Team',
          description: 'Frontend and backend development, creating robust and scalable solutions.',
          members: 12,
          projects: 8,
          imageUrl: require('@/assets/login_1.png')  // Option 1: Use require for local images
          // Or use online images (Option 2):
          // imageUrl: 'https://images.unsplash.com/photo-1603201667141-5324c62746bc?q=80&w=2000&auto=format&fit=crop'
        },
        {
          id: 2,
          name: 'Design Team',
          description: 'UI/UX design, creating beautiful and intuitive user experiences.',
          members: 8,
          projects: 15,
          imageUrl: require('@/assets/login_2.png')
          // imageUrl: 'https://images.unsplash.com/photo-1587440871875-191322ee64b0?q=80&w=2000&auto=format&fit=crop'
        },
        {
          id: 3,
          name: 'Marketing Team',
          description: 'Digital marketing, brand strategy, and growth optimization.',
          members: 6,
          projects: 10,
          imageUrl: require('@/assets/login_3.png')
          // imageUrl: 'https://images.unsplash.com/photo-1552581234-26160f608093?q=80&w=2000&auto=format&fit=crop'
        }
      ]
    }
  },
  methods: {
    selectTeam(teamId) {
      this.selectedTeam = teamId;
    },
    continueToDashboard() {
      if (this.selectedTeam) {
        localStorage.setItem('selectedTeam', this.selectedTeam);
        this.$router.push('/dashboard');
      }
    }
  }
}
</script>

<style scoped>
.selection-page {
  min-height: 100vh;
  background-color: #121212;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.team-selection-container {
  max-width: 1200px;
  background-color: #1e1e1e;
  border-radius: 20px;
  padding: 3rem 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.header {
  text-align: center;
  margin-bottom: 4rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #ffffff;
  margin-bottom: 1rem;
  font-weight: 600;
}

.header p {
  color: #888;
  font-size: 1.1rem;
}

.teams-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 3rem;
}

.team-card {
  background-color: #252525;
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  border: 2px solid transparent;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(255, 0, 0, 0.1);
}

.team-card.selected {
  border-color: #ff3333;
  box-shadow: 0 0 30px rgba(255, 0, 0, 0.2);
}

.selected-indicator {
  position: absolute;
  top: 1rem;
  right: 1rem;
  color: #ff3333;
  font-size: 1.5rem;
  visibility: hidden;
  transform: scale(0.5);
  transition: all 0.2s ease;
  z-index: 10;
}

.team-card.selected .selected-indicator {
  visibility: visible;
  transform: scale(1);
}

.team-image {
  height: 160px;
  overflow: hidden;
}

.team-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.team-card:hover .team-image img {
  transform: scale(1.05);
}

.team-content {
  padding: 1.5rem;
}

.team-name {
  font-size: 1.4rem;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.team-description {
  color: #888;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.team-stats {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 0.9rem;
}

.team-stats i {
  color: #ff3333;
  margin-right: 0.5rem;
}

.continue-btn {
  background-color: #ff3333;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 10px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0 auto;
  cursor: pointer;
  transition: all 0.3s ease;
}

.continue-btn:hover:not(:disabled) {
  background-color: #ff4444;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 0, 0, 0.3);
}

.continue-btn:disabled {
  background-color: #444;
  cursor: not-allowed;
}

.continue-btn i {
  transition: transform 0.3s ease;
}

.continue-btn:hover:not(:disabled) i {
  transform: translateX(5px);
}

@media (max-width: 1024px) {
  .teams-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .team-selection-container {
    padding: 2rem 1rem;
  }

  .header h1 {
    font-size: 2rem;
  }

  .teams-grid {
    grid-template-columns: 1fr;
  }
}
</style>
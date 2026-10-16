pipeline {
  agent any

  options {
    timestamps()
  }

  stages {

    stage('Install') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install bandit==1.9.4
        '''
      }
    }

    stage('SAST - Bandit report') {
      steps {
        sh '''
          . .venv/bin/activate
          mkdir -p reports
          bandit -r app -f json -o reports/bandit.json || true
          bandit -r app -f txt  -o reports/bandit.txt  || true
        '''
        archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
      }
    }

    stage('Security gate') {
      steps {
        sh '''
          . .venv/bin/activate
          bandit -r app -lll
        '''
      }
    }

  }

  post {
    always {
      cleanWs()
    }
  }
}
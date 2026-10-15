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
          pip install -r requirements.txt
          pip install bandit==1.9.4
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
pipeline {
  agent any

  stages {
    stage('Build Docker Image') {
      steps {
        sh '''
          echo === BUILDING DOCKER IMAGE ===
          docker build -t parcial3_ocy1102-app -f app/Dockerfile .
        '''
      }
    }

    stage('Run Temporary App Container') {
      steps {
        sh '''
          echo === RUNNING TEMPORARY CONTAINER ===
          docker rm -f secure_app_temp || true
          docker run -d --name secure_app_temp --network parcial3_ocy1102_ci_network -p 5000:5000 parcial3_ocy1102-app
          sleep 5
        '''
      }
    }

    stage('Security Scan with OWASP ZAP') {
      steps {
        sh '''
          echo === RUNNING ZAP SCAN ===
          docker run --rm --network parcial3_ocy1102_ci_network \
            -v $WORKSPACE:/zap/wrk \
            ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
            -t http://secure_app_temp:5000 \
            -r zap_report.html
        '''
      }
    }

    stage('Archive Report') {
      steps {
        echo "=== ARCHIVING REPORT ==="
        archiveArtifacts artifacts: 'zap_report.html', fingerprint: true
      }
    }

    stage('Cleanup') {
      steps {
        sh '''
          echo === CLEANING UP ===
          docker rm -f secure_app_temp || true
        '''
      }
    }
  }
}

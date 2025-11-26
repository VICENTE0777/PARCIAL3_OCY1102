pipeline {
    agent any

    environment {
        APP_IMAGE = "parcial3_ocy1102-app"
        NETWORK = "parcial3_ocy1102_ci_network"
        TEMP_CONTAINER = "secure_app_temp"
        ZAP_CONTAINER = "zap"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "=== BUILDING DOCKER IMAGE ==="
                docker build -t $APP_IMAGE ./app
                '''
            }
        }

        stage('Run Temporary App Container') {
            steps {
                sh '''
                echo "=== RUNNING TEMPORARY CONTAINER ==="
                docker rm -f $TEMP_CONTAINER || true
                docker run -d --name $TEMP_CONTAINER --network $NETWORK -p 5000:5000 $APP_IMAGE
                sleep 5
                '''
            }
        }

        stage('Security Scan with OWASP ZAP') {
            steps {
                sh '''
                echo "=== STARTING ZAP SECURITY SCAN ==="

                docker exec $ZAP_CONTAINER zap-cli --api-key 12345 status -t 120
                docker exec $ZAP_CONTAINER zap-cli --api-key 12345 spider http://secure_app_temp:5000
                docker exec $ZAP_CONTAINER zap-cli --api-key 12345 active-scan http://secure_app_temp:5000

                docker exec $ZAP_CONTAINER zap-cli --api-key 12345 report -o /zap/reports/security_report.html -f html
                '''
            }
        }

        stage('Generate Report') {
            steps {
                sh '''
                echo "=== COPYING SECURITY REPORT ==="

                docker cp $ZAP_CONTAINER:/zap/reports/security_report.html ./security_report.html
                '''
            }
        }
    }

    post {
        always {
            sh '''
            echo "=== CLEANING UP ==="
            docker rm -f $TEMP_CONTAINER || true
            '''
        }
    }
}

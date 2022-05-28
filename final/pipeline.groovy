pipeline {
    agent any

    stages {
        stage('Clone repo') {
            steps {
                git branch: 'final', credentialsId: 'jenkins-key', url: 'https://github.com/geniyfolomeev/2022-1-QAPYTHON-VK-E-FOLOMEEV'
            }
        }
        stage("Run docker") {
            steps {
                bat """
                cd final
                docker-compose up -d
                """
            }
        }
        stage('Create venv') {
            steps {
                bat 'python -m virtualenv -p C:\\Users\\geniy\\AppData\\Local\\Programs\\Python\\Python39\\python.exe venv'
            }
        }
        stage('Run tests') {
            steps {
                bat """
                call ./venv/scripts/activate
                pip install --no-cache-dir -r requirements.txt
                cd final/tests
                python -m pytest -s -v -n 2 --alluredir=%WORKSPACE%/alluredir --selenoid
                """
            }
        }
    }
    post {
        always {
            bat """
            cd final
            docker-compose stop
            """
            allure([
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'alluredir']]
            ])
        }
    }
}

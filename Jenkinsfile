void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/my-org/my-repo"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

def  ubuntu18image = false
def  ubuntu20image = false
def  debianbusterimage = false

pipeline {
     agent any
     stages {

         stage("Build Test-Container"){
             steps {
                 sh "docker build -f aecid-testsuite/Dockerfile -t aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID ."
             }
         }
         
         stage("UnitTest"){
             steps {
       	         sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runUnittests"
       	         sh 'docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runSuspendModeTest'
       	         sh 'docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runRemoteControlTest'
             }
         }
         stage("Run Demo-Configs"){
             parallel {
                 stage("demo-config and jsonConverterHandler-demo-config") {
                     steps {
       	                 sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runAMinerDemo demo/AMiner/demo-config.py"
       	                 sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runAMinerDemo demo/AMiner/demo-config.yml"
                     }
                 }
                 stage("template_config") {
                     steps {
       	         	sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runAMinerDemo demo/AMiner/template_config.py"
       	         	sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runAMinerDemo demo/AMiner/template_config.yml"
                     }
                 }
                 stage("jsonConverterHandler") {
                     steps {
       	                 sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runAMinerDemo demo/AMiner/jsonConverterHandler-demo-config.py"
                     }
                 }


             }
         }

         stage("Integrations Test"){
             steps {
       	         sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runAMinerIntegrationTest aminerIntegrationTest.sh config.py"
       	         sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runAMinerIntegrationTest aminerIntegrationTest2.sh config21.py config22.py"
             }
         }


         stage("Wiki Tests"){
             //when {
             //    branch 'development'
             //}
             steps {
       	         sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runTryItOut"
       	         sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runGettingStarted"
             }
         }

         stage("Coverage Tests"){
             when {
                 branch 'development'
             }
             steps {
       	         sh "docker run -m=2G --rm aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID runCoverageTests"
             }
         }

                 stage("Test Debian Buster") {
                    when {
                       expression {
                            BRANCH_NAME == 'master' || BRANCH_NAME == 'development'
                       }
                    }
                    steps {
                    script {
                      debianbusterimage = true
                    }
                     sh "docker build -f aecid-testsuite/docker/Dockerfile_deb -t aecid/aminer-debian-buster:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID --build-arg=varbranch=development --build-arg=vardistri=debian:buster ."
                     sh "docker run --rm aecid/aminer-debian-buster:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID"
                   }
                 }

		stage("Test Ubuntu 18.04") {
                    when {
                       expression {
                            BRANCH_NAME == 'master' || BRANCH_NAME == 'development'
                       }
                    }
                    steps {
                     script{
                       ubuntu18image = true
                     }
                     sh "docker build -f aecid-testsuite/docker/Dockerfile_deb -t aecid/aminer-ubuntu-1804:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID --build-arg=varbranch=development --build-arg=vardistri=ubuntu:18.04 ."
                     sh "docker run --rm aecid/aminer-ubuntu-1804:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID"
                    }
                 }

		stage("Test Ubuntu 20.04") {
                    when {
                       expression {
                            BRANCH_NAME == 'master' || BRANCH_NAME == 'development'
                       }
                    }
                    steps {
                    script {
                      ubuntu20image = true
                    }
                     sh "docker build -f aecid-testsuite/docker/Dockerfile_deb -t aecid/aminer-ubuntu-2004:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID --build-arg=varbranch=development --build-arg=vardistri=ubuntu:20.04 ."
                     sh "docker run --rm aecid/aminer-ubuntu-1804:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID"
                   }
                 }
    }
    post {
        always {
           script {
           sh "docker rmi aecid/logdata-anomaly-miner-testing:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID"
           if( debianbusterimage == true ){
               sh "docker rmi aecid/aminer-debian-buster:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID"
           }
           if( ubuntu18image == true ){
               sh "docker rmi aecid/aminer-ubuntu-1804:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID"
           }
           if( ubuntu20image == true ){
               sh "docker rmi aecid/aminer-ubuntu-2004:$JOB_BASE_NAME-$EXECUTOR_NUMBER-$BUILD_ID"
           }
         }
        }
 
	success {
        setBuildStatus("Build succeeded", "SUCCESS");
    }
    failure {
        setBuildStatus("Build failed", "FAILURE");
    }
  }

} 
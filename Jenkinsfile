#!groovy
DEVELOPERS = ['tgal@km3net.de']

properties([gitLabConnection('KM3NeT GitLab')])


node('master') {

    // cleanWs()    // unocmment to start with a clean workspace
    checkout scm

    def docker_image = docker.build("orchestra-container:${env.BUILD_ID}")

    docker_image.inside {
        // Tell GitLab which stages exist, so it can display them in the Web 
        // GUI in advance.
        gitlabBuilds(builds: ["build", "test", "doc"]) {

            // Here are your stages...

            updateGitlabCommitStatus name: 'build', state: 'pending'
            stage("build") {
                try {
                    sh """
                        make install
                    """
                    updateGitlabCommitStatus name: 'build', state: 'success'
                } catch (e) {
                    sendMail("Build Failed")
                    updateGitlabCommitStatus name: 'build', state: 'failed'
                    throw e
                }
            }

            updateGitlabCommitStatus name: 'test', state: 'pending'
            stage("test") {
                try {
                    sh """
                        make test
                    """
                    updateGitlabCommitStatus name: 'test', state: 'success'
                } catch (e) {
                    sendMail("Tests Failed")
                    updateGitlabCommitStatus name: 'test', state: 'failed'
                    throw e
                }
                step([$class: 'XUnitBuilder',
                        thresholds: [
                            [$class: 'SkippedThreshold', failureThreshold: '5'],
                            [$class: 'FailedThreshold', failureThreshold: '0']
                        ],
                        tools: [
                            [$class: 'JUnitType', pattern: 'reports/junit.xml']
                        ]
                    ]
                )
            }
            updateGitlabCommitStatus name: 'doc', state: 'pending'
            stage("doc") {
              try { 
                sh """
                  cd doc
                  make html
                """
              } catch (e) { 
                sendChatMessage("Building Docs Failed")
                sendMail("Building Docs Failed")
                updateGitlabCommitStatus name: 'doc', state: 'failed'
                throw e
              }
              publishHTML target: [
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: "doc/_build/html",
                reportFiles: 'index.html',
                reportName: "Documentation"
              ]
              updateGitlabCommitStatus name: 'doc', state: 'success'
            }

        }
    }
}


// Sends a mail to all developers defined at the top of this script.
def sendMail(subject, message='', developers=DEVELOPERS) {
    for (int i = 0; i < developers.size(); i++) {
        def developer = DEVELOPERS[i]
        emailext (
            subject: "$subject - Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            body: """
                <p>$message</p>
                <p>Check console output at 
                <a href ='${env.BUILD_URL}'>${env.BUILD_URL}</a> 
                to view the results.</p>
            """,
            to: developer
        )
    }
}


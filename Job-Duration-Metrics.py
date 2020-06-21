import jenkins
import matplotlib.pyplot as plt
import matplotlib
import time
import sys, getopt
from datetime import datetime



class DurationMetrics:
    username = ''
    password = ''
    totalBuildDuration = 0.0
    numberOfBuilds = 0.0
    buildDurations = []
    buildTimestamps = []
    getAllBuildInfo = False
    server = None

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def calculateAverageDuration(self):
        #TODO: calculate average duration
        averageDuration = (self.totalBuildDuration / self.numberOfBuilds) / 1000
        return averageDuration

    def plotJobDuration(self):
        #TODO: plot job duration
        dateTimeObjs = self.convertTimestamps()
        dates = matplotlib.dates.date2num(dateTimeObjs)
        plt.plot_date(dates,self.buildDurations,'-')
        plt.xlabel('Time of Execution')
        plt.ylabel('Build Duration (seconds)')
        plt.title('Build Durations Over Time')
        plt.show()

    def getJobDuration(self):
        # TODO: get job duration
        jenkinsJobs = self.server.get_all_jobs()
        print(jenkinsJobs)
        myJob = self.server.get_job_info('python-test', 0, True)
        print(myJob)
        myJobBuilds = myJob.get('builds')
        for build in myJobBuilds:
            buildNumber = build.get('number')
            buildInfo = self.server.get_build_info('python-test', buildNumber)
            #print(buildInfo)
            buildDuration = buildInfo.get('duration')
            self.buildDurations.append((buildDuration / 1000))
            self.totalBuildDuration += buildDuration
            self.numberOfBuilds += 1.0
            buildTimestamp = buildInfo.get('timestamp')
            self.buildTimestamps.append(buildTimestamp)

    def connectToJenkins(self):

        # TODO: connect to Jenkins server
        self.server = jenkins.Jenkins('http://localhost:8080', username=self.username, password=self.password)
        user = self.server.get_whoami()
        version = self.server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))

    def convertTimestamps(self):
        dates = []
        for timestamp in self.buildTimestamps:
            dateTimeObj = datetime.fromtimestamp((timestamp / 1000))
            dates.append(dateTimeObj)
        return dates


def main(argv):

    username = ''
    password = ''

    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["username=", "password="])
    except getopt.GetoptError:
        print
        'python Job-Duration-Metrics.py -u <username> -p <password>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'python Job-Duration-Metrics.py -u <username> -p <password>'
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg

    durationMetrics = DurationMetrics(username,password)
    durationMetrics.connectToJenkins()
    durationMetrics.getJobDuration()
    print("Build Average Duration: %.2f seconds" % durationMetrics.calculateAverageDuration())
    durationMetrics.plotJobDuration()



if __name__ == "__main__":
   main(sys.argv[1:])


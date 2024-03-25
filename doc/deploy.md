# Deploying affils

The affils service is deployed to AWS's Elastic Beanstalk service. If
you use your Stanford credentials to log in to AWS, choose the
production profile, and set your region to Oregon (us-west-2), and then
you navigate to the Elastic Beanstalk console, you should see an Elastic
Beanstalk environment called `affils-env`. The `affils-env` environment
contains the `affils` application. If you click the `affils`
application, you should be able to view information about the affils
service.

To deploy the files from your computer, enter the following:

```
inv deploy
```

This command should upload the affils files from your computer to AWS's
Elastic Beanstalk service.

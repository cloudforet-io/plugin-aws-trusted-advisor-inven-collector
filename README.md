<h1 align="center">AWS Trusted Advisor Collector</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <img width="245" src="https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudservice.svg">
  <p> 
    <br>
    <img alt="Version"  src="https://img.shields.io/badge/version-1.4.2-blue.svg?cacheSeconds=2592000"  />    
    <a href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank"><img alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" /></a> 
  </p> 
</div>   

### Plugin to collect AWS Trust Advisor

> SpaceONE's [plugin-aws-trusted-advisor-inven-collector](https://github.com/spaceone-dev/plugin-aws-trusted-advisor-inven-collector) is a convenient tool to get Trusted Advisor from AWS.


Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/plugin-aws-trusted-advisor-inven-collector)
> Latest stable version : 1.4.2

Please contact us if you need any further information. (<support@spaceone.dev>)

---

## AWS Service Endpoint (in use)

There is an endpoints used to collect AWS Trusted advisor.

<pre>
https://support.us-east-1.amazonaws.com
</pre>

---

## Authentication Overview

Registered service account on SpaceONE must have certain permissions to collect cloud service data Please, set
authentication privilege for followings:

<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "support:DescribeTrustedAdvisorChecks",
                "support:DescribeTrustedAdvisorCheckResult",
                "support:RefreshTrustedAdvisorCheck",
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>


---
# Release Note

## Version 1.4.2
[fix: update cloud_service_type](https://github.com/spaceone-dev/plugin-aws-trusted-advisor-inven-collector/commit/9f29f245cf9e0cc769ebfad246d558a79174229d)

## Version 1.4.1

Add Error Resource

## Version 1.4

Add name field

## Version 1.0.3

Add Description tab
- Support HTML text

## Version 1.0.2

Change flagged_resource.
Add table data in Affected Resources

## Version 1.0.1

Support data.account_id




